#!/bin/bash -e

IMAGE="tc_content_provider_archive"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=("--volume=$DIR/../volume/video:/mnt:rw" "--volume=$DIR:/home:ro")

. "$DIR/../script/shell.sh"
