#!/bin/bash -x

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

# Kubeadm reset
try_command kubeadm reset
try_command iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X

# Remove Package
try_command apt-get remove kubelet kubeadm kubectl
try_command apt -y autoremove
