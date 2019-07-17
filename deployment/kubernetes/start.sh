#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
EXT=*.yaml

# Set Bash color
ECHO_PREFIX_INFO="\033[1;32;40mINFO...\033[0;0m"
ECHO_PREFIX_ERROR="\033[1;31;40mError...\033[0;0m"

# Try command  for test command result.
function try_command {
    "$@"
    status=$?
    if [ $status -ne 0 ]; then
        echo -e $ECHO_PREFIX_ERROR "ERROR with \"$@\", Return status $status."
        exit $status
    fi
    return $status
}

# This script must be run as root
if [[ $EUID -ne 0 ]]; then
    echo -e $ECHO_PREFIX_ERROR "This script must be run as root!" 1>&2
    exit 1
fi

try_command hash kubectl > /dev/null

for i in $(find "$DIR" -path "$DIR/dashboard" -prune -o -type f -name "*service.yaml" -print); do
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
    for j in $(kubectl get pod | awk '{print $1}' | sed -n '2, $p' | awk -F '-' '{$NF=""; $(NF-1)=""; gsub("  ", "");gsub(" ", "-"); print}'); do
        if [ ${i1} == ${j} ]; then
            kubectl delete -f "${i}"
        fi
    done
done

for i in $(find "$DIR" -name "*certificates.yaml"); do
    len=$(echo $DIR | wc -m)
    i1=$(echo ${i:${len}} | sed 's/.yaml//')
    for j in $(kubectl get secret | awk '{print $1}' | sed -n '2, $p' | grep -v 'default-token'); do
        if [ ${i1} == ${j} ] && [ -f "${i}" ]; then
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

try_command kompose convert -f "$yml" -o "$DIR"

try_command "$DIR/update_yaml.py" "$DIR"

try_command kubectl create secret generic ovc-ssl-certificates --from-file=self.key="$DIR/../../self-certificates/self.key" --from-file=self.crt="$DIR/../../self-certificates/self.crt" --from-file=dhparam.pem="$DIR/../../self-certificates/dhparam.pem" --dry-run -o yaml > "$DIR/ovc-ssl-certificates.yaml"

try_command kubectl apply -f "$DIR/ovc-ssl-certificates.yaml"

for i in $(find "$DIR" -path "$DIR/dashboard" -prune -o -type f -name "*service.yaml" -print); do
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

sleep 2s

for i in $(find "$DIR" -name "live-transcode*.yaml"); do
    kubectl apply -f "$i"
done

