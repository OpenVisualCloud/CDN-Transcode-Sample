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

# Install packages
# Set Proxy if need
try_command apt-get update && apt-get install -y apt-transport-https curl
try_command curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
try_command cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
try_command apt-get update
try_command apt-get install -y kubelet kubeadm kubectl
try_command apt-mark hold kubelet kubeadm kubectl
try_command systemctl enable --now kubelet
try_command systemctl start kubelet

try_command swapoff -a
try_command modprobe br_netfilter
try_command cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
try_command sysctl --system

# Docker cgroupdriver
try_command cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

# Kubelet Proxy
try_command mkdir -p /etc/systemd/system/kubelet.service.d/
try_command cat <<EOF > /etc/systemd/system/kubelet.service.d/proxy.conf
[Service]
Environment="HTTP_PROXY=${http_proxy}"
Environment="HTTPS_PROXY=${https_proxy}"
Environment="NO_PROXY=${no_proxy}"
EOF
try_command systemctl daemon-reload
try_command systemctl restart docker
try_command systemctl restart kubelet
unset http_proxy
unset https_proxy

# Kubeadm init
try_command kubeadm init --pod-network-cidr=10.244.0.0/16
try_command mkdir -p $HOME/.kube
try_command cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
try_command chown $(id -u):$(id -g) $HOME/.kube/config
try_command export KUBECONFIG=$HOME/.kube/config
try_command kubectl taint nodes --all node-role.kubernetes.io/master-

# Set Proxy if need
try_command kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml
