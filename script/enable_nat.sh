#!/bin/bash
sysctl -w net.ipv4.ip_forward=1
[ ${UID} -ne 0 ] && echo "Please run as root!!" && exit 1
for (( i=1; i<=6; i++))
do
    iptables -t nat -A POSTROUTING -s 172.31.$i.0/24 -d 0/0 -j MASQUERADE
    iptables -I FORWARD -j ACCEPT -i eth$(($i - 1))
    iptables -I FORWARD -j ACCEPT -o eth$(($i - 1))
done
echo "Done"
