#!/bin/bash -e

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


# Detect system arch.
ULONG_MASK=`getconf ULONG_MAX`
if [ $ULONG_MASK == 18446744073709551615 ]; then
    SYSARCH=64
else
    echo -e $ECHO_PREFIX_ERROR "This package does not support 32-bit system.\n"
    exit 1
fi


if [ `cat /etc/os-release | grep -E "CentOS" | wc -l` -ne 0 ]; then
    try_command yum -y install redhat-lsb-core
elif [ `cat /etc/os-release | grep -E "Ubuntu" | wc -l` -ne 0 ]; then
    try_command apt-get update
    try_command apt-get install -y lsb-release
fi

try_command lsb_release -si > /dev/null

LINUX_DISTRO=`lsb_release -si`

if [ "$LINUX_DISTRO" == "Ubuntu" ]; then
    try_command apt-get install -y curl gnupg software-properties-common cmake
    apt-get remove -y docker docker-engine docker.io containerd runc
    try_command curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    try_command apt-key fingerprint 0EBFCD88
    try_command add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"
    try_command apt-get update
    try_command apt-get install -y docker-ce docker-ce-cli containerd.io
    try_command curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    try_command curl -L https://github.com/kubernetes/kompose/releases/download/v1.18.0/kompose-linux-amd64 -o /usr/local/bin/kompose
    try_command chmod +x /usr/local/bin/kompose
    try_command apt-get install -y python3-pip libgtk-3-dev
    try_command pip3 install ruamel.yaml fabric3 wxpython
elif [ "$LINUX_DISTRO" == "CentOS" ]; then
    try_command yum install -y curl cmake
    yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
    try_command yum install -y yum-utils device-mapper-persistent-data lvm2
    try_command yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    try_command yum install -y docker-ce docker-ce-cli containerd.io
    try_command curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    try_command curl -L https://github.com/kubernetes/kompose/releases/download/v1.18.0/kompose-linux-amd64 -o /usr/bin/kompose
    try_command chmod +x /usr/bin/kompose
    try_command yum install -y epel-release 
    try_command yum install -y python36 python36-pip python3-devel gtk3-devel
    try_command pip3 install ruamel.yaml fabric3
    try_command yum -y install wxPython
else
    echo -e $ECHO_PREFIX_INFO "The installation will be cancelled."
    echo -e $ECHO_PREFIX_INFO "The CDN-Transcode-Sample does not support this OS, please use Ubuntu 18.04 or CentOS 7.6.\n"
    exit 1
fi

echo -e $ECHO_PREFIX_INFO "Installation completed."
