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


#detect system arch.
ULONG_MASK=`getconf ULONG_MAX`
if [ $ULONG_MASK == 18446744073709551615 ]; then
    SYSARCH=64
else
    echo -e $ECHO_PREFIX_ERROR "This package does not support 32-bit system.\n"
    exit 1
fi

# Build gpu plugin
if [ -f go1.11.2.linux-amd64.tar.gz ]; then
    try_command rm go1.11.2.linux-amd64.tar.gz
fi
try_command wget https://dl.google.com/go/go1.11.2.linux-amd64.tar.gz
try_command tar -C /usr/local -xzf go1.11.2.linux-amd64.tar.gz
try_command rm go1.11.2.linux-amd64.tar.gz
try_command export PATH=$PATH:/usr/local/go/bin
try_command go version
try_command mkdir -p /usr/local/go/src/github.com/intel
try_command cd /usr/local/go/src/github.com/intel
if [ -d intel-device-plugins-for-kubernetes ]; then
    try_command rm -rf intel-device-plugins-for-kubernetes
fi
try_command git clone https://github.com/intel/intel-device-plugins-for-kubernetes.git
try_command cd intel-device-plugins-for-kubernetes
try_command make
