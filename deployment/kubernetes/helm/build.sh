#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NVODS="${1:-1}"
NLIVES="${2:-1}"
REGISTRY="$3"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

if [ ! -x /usr/bin/helm ] && [ ! -x /usr/local/bin/helm ]; then
    exit 0
fi 

echo "Generating persistent volume yaml(s)"
# list all workers
hosts=($(kubectl get node -l vcac-zone!=yes -o custom-columns=NAME:metadata.name,STATUS:status.conditions[-1].type,TAINT:spec.taints | grep " Ready " | grep -v "NoSchedule" | cut -f1 -d' '))
if test ${#hosts[@]} -eq 0; then
    printf "\nFailed to locate worker node(s) for shared storage\n\n"
    exit 1
elif test ${#hosts[@]} -lt 2; then
    hosts=(${hosts[0]} ${hosts[0]})
fi

export HTML_VOLUME_PATH=/tmp/volume/html
export HTML_VOLUME_SIZE=1Gi
export HTML_VOLUME_HOST=${hosts[0]}

export ARCHIVE_VOLUME_PATH=/tmp/volume/video/archive
export ARCHIVE_VOLUME_SIZE=1Gi
export ARCHIVE_VOLUME_HOST=${hosts[0]}

export DASH_VOLUME_PATH=/tmp/volume/video/dash
export DASH_VOLUME_SIZE=1Gi
export DASH_VOLUME_HOST=${hosts[1]}

export HLS_VOLUME_PATH=/tmp/volume/video/hls
export HLS_VOLUME_SIZE=1Gi
export HLS_VOLUME_HOST=${hosts[1]}

for pv in "$DIR"/*-pv.yaml.m4; do
    m4 $(env | grep _VOLUME_ | sed 's/^/-D/') "$pv" > "${pv/.m4/}"
done

echo "Generating helm chart"
m4 -DREGISTRY_PREFIX=${REGISTRY} -DNVODS=${NVODS} -DNLIVES=${NLIVES} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} $(env | grep _VOLUME_ | sed 's/^/-D/') -I "${DIR}/cdn-transcode" "$DIR/cdn-transcode/values.yaml.m4" > "$DIR/cdn-transcode/values.yaml"

