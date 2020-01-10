# Setup Kubernetes slaver node environment

[TOC]



## Setup kubelet proxy use the host proxy
        * sudo mkdir -p /etc/systemd/system/kubelet.service.d/
        * printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/kubelet.service.d/proxy.conf
        * sudo systemctl daemon-reload
## Run below command to setup Kubernetes slave node
        * sudo -E ./script/Kubernetes_setup_node.sh
        * sudo systemctl restart docker
        * sudo systemctl restart kubelet
## Run kubeadm join command which come from master node, after run the command "./script/Kubernetes_setup_master.sh" in the step "Setup Kubernetes master environment"
        * sudo kubeadm join 10.67.116.165:6443 --token iwnkiw.1w29nkpsngdsx4x7  --discovery-token-ca-cert-hash sha256:e1a46195c5fcc59855adcd25b2cca5e58dd330a3ac7d8e133c6dcbfaaf272c3d
## Install the NFS Kernel Server and restart
### Install the NFS Kernel Server on Ubuntu
        * sudo apt-get install nfs-kernel-server
        * sudo /etc/init.d/nfs-kernel-server restart
### Install the NFS Kernel Server on CentOS
	* sudo yum install -y rpcbind nfs-utils openssh-server 
	* sudo systemctl start rpcbind nfs-server sshd 

