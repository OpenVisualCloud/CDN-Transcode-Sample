#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NVODS="${1:-1}"
NLIVES="${2:-1}"

echo "Generating templates with NVODS=${NVODS}, NLIVES=${NLIVES}"

find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
find "${DIR}" -maxdepth 1 -name "*.cfg" -exec rm -rf "{}" \;

for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    yaml=${template/.m4/}
    m4 -DNVODS=${NVODS} -I "${DIR}" "${template}" > "${yaml}"
done

cat <<EOF >> ${DIR}/cpu_mem_managerment.cfg
[cdn]
cpu = 2
mem = 2000
[redis]
cpu = 1
mem = 500
[zookeeper]
cpu = 1
mem = 500
[kafka]
cpu = 1
mem = 500
EOF

for ((VODIDX=0;VODIDX<${NVODS};VODIDX++)); do
    cat <<EOF >> ${DIR}/cpu_mem_managerment.cfg
[vod${VODIDX}]
cpu = 3
mem = 3000
EOF
    cat <<EOF >> ${DIR}/transcode.cfg
[vod${VODIDX}]
hwaccel = false
EOF
done

for ((LIVEIDX=0;LIVEIDX<${NLIVES};LIVEIDX++)); do
    cat <<EOF >> ${DIR}/cpu_mem_managerment.cfg
[live${LIVEIDX}]
cpu = 4
mem = 3000
EOF
    cat <<EOF >> ${DIR}/transcode.cfg
[live${LIVEIDX}]
url = bbb_sunflower_1080p_30fps_normal.mp4
width_height = 856x480
bitrate = 8000000
framerate = 25
gop = 100
maxbFrames = 2
refsNum = 2
rcMode = 0
preset = veryfast
encoder_type = AVC
protocol = HLS
hwaccel = false
density = 2
EOF
done
