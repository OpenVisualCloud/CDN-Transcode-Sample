# Kubernetes common setup
## On ubuntu
Scripts can refer to [Kubeadm script](scripts/)

### Master
```shell
$ ./Kubernetes_setup_ubuntu_master.sh
```

#### Start Dashboard
Dashboard scripts can refer to [Dashboard script](deployment/kubernetes/dashboard/)
```shell
$ cd dashboard
$ ./start_dashboard.sh
$ kubectl proxy
```
####  Visit Dashboard by Web browser
- Open with Firefox like
http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/

#### Sign in with token then display the Dashboard
```shell
$ kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}') | grep token: | awk '{print $2}'
```
the token is like:
```shell
eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWxuc2p6Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJmNzJjMDNkNS01ZjVhLTExZTktYTI2MC0wMGEwYTU5M2IyYTciLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.sHN_V_fZm8fj3OuwzMqAD1GJnffbNbE6SIsBHeFEZmDu9irsF3vnCWQeHFDHNQg66YbpK_j6iLts42GXrJ6QvpAahM-Lqt862PhR06UXJhVROgG-KAQ2qpOxj9f5VKOKfWHG8OOMknRu871Zgc1PQMpYYefpLvFHcP6eQIbDFWq-JwVQTQS3Jjn_cNbamxkU01JY9JLS9AmfuQUfErmzAmWCqC9fWAXH-5A4EV9L2hDPFIvh1cLX-XURTMFeNbHBqv5n2n31rkzWKCP0C3aduAfzRp3UV2-Tt6b1aGgplaEWE0WgG4Q4j_WWD8Mq1W7CoUhTuFlLjfucTv4Q9U44gQScreenshort
```
### Optional: Node
```shell
$ ./Kubernetes_setup_ubuntu_node.sh
```
#### Please replace follow with correct command which is outputted by Master output
```shell
$ kubeadm join Master_IP:6443 --token 2ua9p6.wzwpqhff5a3xupu6 \
--discovery-token-ca-cert-hash sha256:de7bfedccdf99e9aed0af2197d82aa890d20af6e70fe315339c05560cf200a60
```
Notice: 
- If occured error about hostname, Please according to the Err Message to modify the hostname.
- Set correct DNS at /etc/resolv.conf

### Check k8s on master
```shell
$ kubectl get nodes
NAME             STATUS   ROLES    AGE     VERSION
master-hostname  Ready    master   6d21h   v1.14.1
node-hostname    Ready    <none>   6d21h   v1.14.1
```
### Install NFS on all machine(Make sure have CDN-Transcode-Sample source code)
```shell
$ ./nfs_setup_ubuntu.sh
```
### Remove the k8s env on Master and Node
```shell
$ ./Kubernetes_remove_ubuntu.sh
```
