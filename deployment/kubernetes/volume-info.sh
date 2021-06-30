#!/bin/bash -e

export VIDEO_ARCHIVE_VOLUME_PATH=/home/${USER}/sdp/archive/video
export VIDEO_ARCHIVE_VOLUME_SIZE=2
export VIDEO_ARCHIVE_VOLUME_HOST=$1

export VIDEO_CACHE_VOLUME_PATH=/home/${USER}/sdp/cache/video
export VIDEO_CACHE_VOLUME_SIZE=2
export VIDEO_CACHE_VOLUME_HOST=$2
