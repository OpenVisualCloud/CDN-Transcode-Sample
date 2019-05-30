#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
EXT=*.yaml

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

rm -rf $DIR/$EXT

yml="$DIR/docker-compose-template.yml"
test -f "$yml"

dcv="$(kompose version | cut -f1 -d' ')"
mdcv="$(printf '%s\n' $dcv 1.16 | sort -r -V | head -n 1)"
if test "$mdcv" = "1.16"; then
    echo ""
    echo "kompose >=1.16 is required."
    echo "Please upgrade kompose at https://docs.docker.com/compose/install."
    echo ""
    exit 0
fi

kompose convert -f "$yml" -o "$DIR"

"$DIR/update_yaml.py" "$DIR"

for i in $(find "$DIR" -name "*service.yaml"); do
    kubectl apply -f "$i"
done

for i in $(find "$DIR" -name "*deployment.yaml" | grep -v 'live-transcode*'); do
    kubectl apply -f "$i"
done

sleep 2s

for i in $(find "$DIR" -name "*deployment.yaml" | grep -v 'live-transcode*'); do
    len=$(echo $DIR | wc -m)
    i1=$(echo ${i:${len}} | sed 's/-deployment.yaml//')

    while true; do
        if (kubectl get pod | awk '{print $1,$3}' | grep -q "${i1}.*Running"); then
            break
        else
            sleep 2s
        fi
    done
done

kubectl apply -f "$(find "$DIR" -name "live-transcode*.yaml")"

