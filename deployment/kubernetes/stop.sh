#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

for i in $(find "$DIR/" -name "*service.yaml"); do
    len=$(echo $DIR | wc -m)
    i1=$(echo ${i:${len}} | sed 's/-service.yaml//')
    for j in $(kubectl get svc | awk '{print $1}' | sed -n '2, $p' | grep -v 'kubernetes'); do
        if [ "$i1" == "$j" ]; then
            kubectl delete -f "$i"
        fi
    done
done

for i in $(find "$DIR" -name "*deployment.yaml"); do
    len=$(echo $DIR | wc -m)
    i1=$(echo ${i:${len}} | sed 's/-deployment.yaml//')

    for j in $(kubectl get pod | awk '{print $1}' | sed -n '2, $p' | sed 's/service-.*$//' | sort | uniq); do
        #j1=$(echo $j | sed 's/service-.*$//')service
        j1=${j}service
        if [ ${i1} == ${j1} ]; then
            kubectl delete -f "${i}"
        fi
    done
done

rm -rf "$DIR/*.yaml"
