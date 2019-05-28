#!/bin/bash -e

IMAGE="ovc_content_provider_archive"
DIR=$(dirname $(readlink -f "$0"))
sample_video="http://distribution.bbb3d.renderfarming.net/video/mp4"
clips=("$sample_video/bbb_sunflower_1080p_30fps_normal.mp4")

case "$(cat /proc/1/sched | head -n 1)" in
*build.sh*)
    cd /mnt
    mkdir -p archive dash hls
    for clip in "${clips[@]}"; do
        clip_name="${clip/*\//}"
        clip_name="${clip_name/*=/}"
        clip_name="${clip_name/.mp4/}.mp4"
        if test ! -f "archive/$clip_name"; then
            wget -O "archive/$clip_name" "$clip"
        fi
    done
    for clip in `find archive -name "*.mp4" -print`; do
        clip_name="${clip/*\//}"
        if test ! -f "archive/$clip_name".png; then
            ffmpeg -i "archive/$clip_name" -vf "thumbnail,scale=640:360" -frames:v 1 -y "archive/$clip_name".png
        fi
    done
    wait
    ;;
*) 
    mkdir -p "$DIR/../volume/video/archive"
    mkdir -p "$DIR/../volume/video/dash"
    mkdir -p "$DIR/../volume/video/hls"
    . "$DIR/../script/build.sh"
    . "$DIR/shell.sh" /home/build.sh $@
    ;;
esac
