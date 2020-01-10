# Setup Kubernetes master environment on CentOS

[TOC]



## Setup kubelet proxy use the host proxy
        * sudo mkdir -p /etc/systemd/system/kubelet.service.d/
        * printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/kubelet.service.d/proxy.conf
## Run below command to setup Kubernetes master node
        * sudo -E ./script/Kubernetes_setup_master.sh
_Save the output command line for slave node to join in the master: _
kubeadm join 10.67.116.165:6443 --token iwnkiw.1w29nkpsngdsx4x7  --discovery-token-ca-cert-hash sha256:e1a46195c5fcc59855adcd25b2cca5e58dd330a3ac7d8e133c6dcbfaaf272c3d
	

```
	*  mkdir -p $HOME/.kube
	*  sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
	*  sudo chown $(id -u):$(id -g) $HOME/.kube/config
	*  export KUBECONFIG=$HOME/.kube/config
	*  kubectl taint nodes --all node-role.kubernetes.io/master-
	*  sudo sed -i '/- kube-apiserver/a\\    - --service-node-port-range=1-65535' /etc/kubernetes/manifests/kube-apiserver.yaml
```




## Get admin-user's token and launch the CDN Sample UI
On Kubernetes master node, run below command to get the dashboard token
        

```
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}') | grep token: | awk '{print $2}'
```

_Save the output to launch the CDN Sample UI_
Launch Firefox browser to Visit https://<CDN-Transcode Server IP address>:8080, you will see the login page and then input the gotten token to login