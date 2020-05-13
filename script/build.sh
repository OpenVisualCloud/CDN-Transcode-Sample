#!/bin/bash -e

if test -z "${DIR}"; then
    echo "This script should not be called directly."
    exit -1
fi

# build image(s) in order (to satisfy dependencies)
for dep in .8 .7 .6 .5 .4 .3 .2 .1 ''; do
    if test -f "${DIR}/Dockerfile$dep"; then
        image=$(grep -m1 '#' "$DIR/Dockerfile$dep" | cut -d' ' -f2)
        if test -z "$dep"; then image="$IMAGE"; fi

        if grep -q 'AS build' "${DIR}/Dockerfile$dep"; then
            docker build --network=host --file="${DIR}/Dockerfile$dep" --target build -t "$image:build" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /')
        fi

        docker build --network=host --file="${DIR}/Dockerfile$dep" -t "$image:latest" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /')
    fi
done
