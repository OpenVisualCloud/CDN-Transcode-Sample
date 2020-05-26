#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

rm -rf "$DIR/../../volume/video/cache"
mkdir -p "$DIR/../../volume/video/cache/hls" "$DIR/../../volume/video/cache/dash"

# make sure kubectl is functional
kubectl get node >/dev/null 2>/dev/null || exit 0

hosts=($(kubectl get node -l xeone3-zone!=yes -o jsonpath='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}:{range @.spec.taints[*]}{@.key}={@.effect};{end}{end}' | grep Ready=True | grep -v NoSchedule | cut -f1 -d':'))

if test ${#hosts[@]} -eq 0; then
    printf "\nFailed to locate worker node(s) for shared storage\n\n"
    exit -1
elif test ${#hosts[@]} -lt 2; then
    hosts=(${hosts[0]} ${hosts[0]})
fi

. "$DIR/volume-info.sh" "${hosts[@]}"
for pv in $(find "${DIR}" -maxdepth 1 -name "*-pv.yaml.m4" -print); do
    m4 $(env | grep _VOLUME_ | sed 's/^/-D/') -I "${DIR}" "${pv}" > "${pv/.m4/}"
done
