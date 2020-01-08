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

# Kubeadm reset
if [ -f /usr/bin/kubeadm ]; then
    try_command kubeadm reset
    try_command iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
fi

# Install packages
# Set Proxy if need
proxy_http=$http_proxy
proxy_https=$https_proxy
export http_proxy=$proxy_http
export https_proxy=$proxy_https

if [[ -z `grep "swapoff -a" "${HOME}/.bashrc"` ]]; then
    echo "swapoff -a" >> "${HOME}/.bashrc"
fi

try_command swapoff -a

try_command lsb_release -si > /dev/null

LINUX_DISTRO=`lsb_release -si`

if [ "$LINUX_DISTRO" == "Ubuntu" ]; then
    try_command apt-get update && apt-get install -y apt-transport-https curl
    try_command curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo  apt-key add -
    try_command cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
    try_command apt-get update
    try_command apt-get install -y kubelet=1.15.3-00 kubeadm=1.15.3-00 kubectl=1.15.3-00 openssh-client fabric
    try_command apt-mark hold kubelet kubeadm kubectl
elif [ "$LINUX_DISTRO" == "CentOS" ]; then
    cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kube*
EOF
yum install -y kubelet-1.15.3 kubeadm-1.15.3 kubectl-1.15.3 openssh-clients fabric --disableexcludes=kubernetes
else
    echo -e $ECHO_PREFIX_INFO "The installation will be cancelled."
    echo -e $ECHO_PREFIX_INFO "The CDN-Transcode-Sample does not support this OS, please use Ubuntu 18.04 or CentOS 7.6.\n"
    exit 1
fi

try_command systemctl enable --now kubelet
try_command systemctl start kubelet

try_command modprobe br_netfilter

try_command cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
try_command sysctl --system

# Docker cgroupdriver
try_command mkdir -p /etc/docker
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
try_command systemctl daemon-reload
try_command systemctl restart docker
try_command systemctl restart kubelet

# Kubeadm init
unset http_proxy
unset https_proxy
try_command kubeadm init --kubernetes-version=v1.15.3 --pod-network-cidr=10.244.0.0/16
try_command mkdir -p $HOME/.kube
try_command cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
try_command chown $(id -u):$(id -g) $HOME/.kube/config
try_command export KUBECONFIG=$HOME/.kube/config
try_command kubectl taint nodes --all node-role.kubernetes.io/master-

# Set Proxy if need
export http_proxy=$proxy_http
export https_proxy=$proxy_https
try_command kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml
try_command sed -i '/- kube-apiserver/a\\    - --service-node-port-range=1-65535' /etc/kubernetes/manifests/kube-apiserver.yaml

echo -e $ECHO_PREFIX_INFO "Installation completed."
