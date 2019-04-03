#!/bin/bash -e

IMAGE="ovc_self_certificate"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
