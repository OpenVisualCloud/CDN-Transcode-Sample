#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
export VIDEO_ARCHIVE_VOLUME=$(readlink -f "$DIR/../../volume/video/archive")
export VIDEO_CACHE_VOLUME=$(readlink -f "$DIR/../../volume/video/cache")
export SECRETS_VOLUME=$(readlink -f "$DIR/../certificate")

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
"$DIR/../certificate/self-sign.sh"
docker stack deploy -c "$DIR/docker-compose.yml" cdnt
