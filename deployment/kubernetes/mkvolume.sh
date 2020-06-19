#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

echo "Making volumes..."
HOSTS=$(kubectl get node -o 'custom-columns=NAME:.status.addresses[?(@.type=="Hostname")].address,IP:.status.addresses[?(@.type=="InternalIP")].address' | awk '!/NAME/{print $1":"$2}')
awk -v DIR="$DIR" -v HOSTS="$HOSTS" '
BEGIN{
    split(HOSTS,tmp1," ");
    for (i in tmp1) {
        split(tmp1[i],tmp2,":");
        host2ip[tmp2[1]]=tmp2[2];
    }
}
/name:/ {
    gsub("-","/",$2)
    content="\""DIR"/../../volume/"$2"\""
}
/path:/ {
    path=$2
}
/- ".*"/ {
    host=host2ip[substr($2,2,length($2)-2)];
    paths[host,path]=1;
    contents[host,path]=content
}
END {
    for (item in paths) {
        split(item,tmp,SUBSEP);
        host=tmp[1]
        path=tmp[2];
        print host, path;
        system("ssh "host" \"mkdir -p "path";find "path" -mindepth 1 -maxdepth 1 -exec rm -rf {} \\\\;\"");
        system("scp -r "contents[host,path]"/* "host":"path);
    }
}
' "$DIR"/*-pv.yaml
