#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NVODS="${1:-1}"
NLIVES="${2:-1}"
REGISTRY="$3"

HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

echo "Generating templates with NVODS=${NVODS}, NLIVES=${NLIVES}"

find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
find "${DIR}" -maxdepth 1 -name "*.cfg" -exec rm -rf "{}" \;
rm -rf "$DIR/../../volume/video/hls"
rm -rf "$DIR/../../volume/video/dash"
mkdir -p "$DIR/../../volume/video/hls"
mkdir -p "$DIR/../../volume/video/dash"

export CDN_CPU_REQUEST=2
export CDN_MEM_REQUEST=2000Mi
export REDIS_CPU_REQUEST=1
export REDIS_MEM_REQUEST=500Mi
export ZOOKEEPER_CPU_REQUEST=1
export ZOOKEEPER_MEM_REQUEST=500Mi
export KAFKA_CPU_REQUEST=1
export KAFKA_MEM_REQUEST=500Mi
export VOD_CPU_REQUEST=3
export VOD_MEM_REQUEST=3000Mi
export LIVE_CPU_REQUEST=4
export LIVE_MEM_REQUEST=3000Mi

export STREAM_NAME=bbb_sunflower_1080p_30fps_normal.mp4
export STREAM_WIDTH=856
export STREAM_HEIGHT=480
export STREAM_ENCODE_BITRATE=8M
export STREAM_ENCODE_FRAMERATE=30
export STREAM_ENCODE_GOP=100
export STREAM_ENCODE_MAXBFRAMES=2
export STREAM_ENCODE_REFSNUM=2
export STREAM_ENCODE_PRESET=veryfast
export STREAM_ENCODE_TYPE=AVC
export STREAM_ENCODE_HWACCEL=false
export STREAM_ENCODE_PROTOCOL=HLS
export STREAM_ENCODE_DENSITY=2

hosts=($(kubectl get node -l xeone3-zone!=yes -o jsonpath='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}:{range @.spec.taints[*]}{@.key}={@.effect};{end}{end}' | grep Ready=True | grep -v NoSchedule | cut -f1 -d':'))

echo $hosts

if test ${#hosts[@]} -eq 0; then
    printf "\nFailed to locate worker node(s) for shared storage\n\n"
    exit -1
elif test ${#hosts[@]} -lt 2; then
    hosts=(${hosts[0]} ${hosts[0]})
fi

export VIDEO_ARCHIVE_VOLUME_PATH=/tmp/archive/video
export VIDEO_ARCHIVE_VOLUME_SIZE=2
export VIDEO_ARCHIVE_VOLUME_HOST=${hosts[1]}

export VIDEO_CACHE_VOLUME_PATH=/tmp/cache/video
export VIDEO_CACHE_VOLUME_SIZE=2
export VIDEO_CACHE_VOLUME_HOST=${hosts[1]}

for template in $(find "${DIR}" -maxdepth 1 -name "*yaml.m4" -print); do
    if [[ -n $(grep LIVEIDX "$template") ]]; then
        for ((LIVEIDX=0;LIVEIDX<${NLIVES};LIVEIDX++)); do
            yaml=${template/-deploy.yaml.m4/-${LIVEIDX}-deploy.yaml}
            m4 -DLIVEIDX=${LIVEIDX} -DREGISTRY_PREFIX=${REGISTRY} -I "${DIR}" "${template}" > "${yaml}"
        done
    elif [[ -n $(grep NVODS "$template") ]] && [[ ${NVODS} -eq 0 ]]; then
        continue
    else
        yaml=${template/.m4/}
        m4 -DNVODS=${NVODS} -DHOSTIP=${HOSTIP} -DREGISTRY_PREFIX=${REGISTRY} $(env | grep _VOLUME_ | sed 's/^/-D/') -I "${DIR}" "${template}" > "${yaml}"        
    fi
done

for template in $(find "${DIR}" -maxdepth 1 -name "*cfg.m4" -print); do
    cfg=${template/.m4/}
    m4 $(env | grep _REQUEST | sed 's/^/-D/') -I "${DIR}" "${template}" > "${cfg}"
done

for ((LIVEIDX=0;LIVEIDX<${NLIVES};LIVEIDX++)); do
    cat <<EOF >> ${DIR}/cpu_mem_management.cfg

[live-${LIVEIDX}]
cpu = ${LIVE_CPU_REQUEST}
mem = ${LIVE_MEM_REQUEST}
EOF
    cat <<EOF >> ${DIR}/live-transcode.cfg
[live-${LIVEIDX}]
url = ${STREAM_NAME}
width = ${STREAM_WIDTH}
height = ${STREAM_HEIGHT}
bitrate = ${STREAM_ENCODE_BITRATE}
framerate = ${STREAM_ENCODE_FRAMERATE}
gop = ${STREAM_ENCODE_GOP}
maxbFrames = ${STREAM_ENCODE_MAXBFRAMES}
refsNum = ${STREAM_ENCODE_REFSNUM}
preset = ${STREAM_ENCODE_PRESET}
encodeType = ${STREAM_ENCODE_TYPE}
hwaccel = ${STREAM_ENCODE_HWACCEL}
protocol = ${STREAM_ENCODE_PROTOCOL}
density = ${STREAM_ENCODE_DENSITY}
EOF
done
