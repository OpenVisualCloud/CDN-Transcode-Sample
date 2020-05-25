#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

yml="$DIR/docker-compose.$(hostname).yml"
test -f "$yml" || yml="$DIR/docker-compose.yml"

docker stack rm cdnt
