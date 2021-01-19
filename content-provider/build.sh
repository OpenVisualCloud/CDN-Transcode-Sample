#!/bin/bash -e

IMAGE="tc_content_provider_archive"
DIR=$(dirname $(readlink -f "$0"))
LICENSE="https://www.pexels.com/photo-license"
clips=(
    https://www.pexels.com/video/3115738/download
    https://www.pexels.com/video/2274223/download
    https://www.pexels.com/video/3061912/download
    https://www.pexels.com/video/1110140/download
    https://www.pexels.com/video/2644023/download
    https://www.pexels.com/video/2257025/download
    https://www.pexels.com/video/3743056/download
    https://www.pexels.com/video/5419496/download
    https://www.pexels.com/video/2249449/download
    https://www.pexels.com/video/3121138/download
    https://www.pexels.com/video/2324293/download
    https://www.pexels.com/video/5413799/download
    https://www.pexels.com/video/3063911/download
    https://www.pexels.com/video/852435/download
)
   
case "$(cat /proc/1/sched | head -n 1)" in
*build.sh*)
    cd /mnt
    for clip in "${clips[@]}"; do
        clip_name="$(echo $clip | cut -f5 -d/).mp4"
        if test ! -f "archive/$clip_name"; then
            if test "$reply" == ""; then
                printf "\n\n\nThe sample requires you to have a set of video clips as the transcoding and streaming source. Please accept the license terms from $LICENSE to start downloading the video clips.\n\nThe terms and conditions of the license apply. Intel does not grant any rights to the video files.\n\n\nPlease type \"accept\" or anything else to skip the download.\n"
                read reply
            fi
            if test "$reply" == "accept"; then
                echo "Downloading $clip..."
                wget -q -U "XXX YYY" -O "archive/$clip_name" "$clip"
            fi
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
    . "$DIR/../script/build.sh"
    . "$DIR/shell.sh" /home/build.sh $@
    ;;
esac
