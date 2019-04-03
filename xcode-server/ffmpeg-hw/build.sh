#!/bin/bash -e

IMAGE="ovc_transcode_hw"
DIR=$(dirname $(readlink -f "$0"))

clips=('http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_30fps_normal.mp4')

mkdir -p "$DIR/../../volume/video/archive"
mkdir -p "$DIR/../../volume/video/dash"
mkdir -p "$DIR/../../volume/video/hls"
. "${DIR}/../../script/build.sh"
for clip in "${clips[@]}"; do
    clip_name="${clip##*/}"
    if test ! -f "${DIR}/../../volume/video/archive/${clip_name}"; then
        wget -O "${DIR}/../../volume/video/archive/${clip_name}" "$clip"
    fi
    if test ! -f "${DIR}/../../volume/video/archive/${clip_name}.png"; then
        ffmpeg -i "${DIR}/../../volume/video/archive/${clip_name}" -vf "thumbnail,scale=640:360" -frames:v 1 -y "${DIR}/../../volume/video/archive/${clip_name}.png" || rm -rf "${DIR}/../../volume/video/archive/${clip_name}"
    fi
    sudo chown "$(id -un).$(id -gn)" "${DIR}/../../volume/video/archive/${clip_name}" "${DIR}/../../volume/video/archive/${clip_name}.png"
    sudo chmod 644 "${DIR}/../../volume/video/archive/${clip_name}" "${DIR}/../../volume/video/archive/${clip_name}.png"
done
wait
