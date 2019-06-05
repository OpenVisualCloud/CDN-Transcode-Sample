# Kubernetes Deployment on VCA2
## Enable VCA2 (Card0 CPU0 for Example)
```shell
$ vcactl blockio open 0 0 vcablk0 RW vca_disk30_reference_k4.19_ubuntu18.04_5.7.1-0.vcad
$ vcactl boot 0 0 vcablk0
$ vcactl status
Card: 0 Cpu: 0 STATE: net_device_ready
```
### Check the list for image
```shell
$ vcactl blockio list
 Card   Cpu      Name     State     Mode  Size(MB) FilePath
------------------------------------------------------------
    0     0   vcablk0    active       RW     30720 vca_disk30_reference_k4.19_ubuntu18.04_5.7.1-0.vcad
$ vcactl network ip
Card 0 Cpu 0:
172.31.1.1
```
### Set up Network
Scripts can refer to [Kubeadm script](scripts/) 
```shell
$ ./enable_nat.sh
```
### Modify node name
```shell
$ vcactl config 0 0 node-name vca-node00-k8s
```
### Reboot node
```shell
$ vcactl boot 0 0 vcablk0
$ vcactl status
Card: 0 Cpu: 0 STATE: net_device_ready
```

## Enable Intel GPU plugin on VCA2
### Verify kubelet socket exists in /var/lib/kubelet/device-plugins/ directory
```shell
$ ls /var/lib/kubelet/device-plugins/kubelet.sock
/var/lib/kubelet/device-plugins/kubelet.sock
```
### Set up Go environment
```shell
$ wget https://dl.google.com/go/go1.11.2.linux-amd64.tar.gz
$ tar -C /usr/local -xzf go1.11.2.linux-amd64.tar.gz
$ export PATH=$PATH:/usr/local/go/bin
$ go version
go version go1.11.2 linux/amd64
```
### Get source code
```shell
$ mkdir -p /usr/local/go/src/github.com/intel
$ cd /usr/local/go/src/github.com/intel
$ git clone https://github.com/intel/intel-device-plugins-for-kubernetes.git
```
### Build and run intel gpu plugin
```shell
$ cd intel-device-plugins-for-kubernetes
$ make
$./cmd/gpu_plugin/gpu_plugin
GPU device plugin started
Start server for i915 at: /var/lib/kubelet/device-plugins/gpu.intel.com-i915.sock
Device plugin for i915 registered
```
### Verify GPU device plugin is registered( Execute on Master)
```shell
$ kubectl describe node | grep gpu.intel.com
gpu.intel.com/i915:  1
gpu.intel.com/i915:  1
```
## Start CDN transcode service(run on master)
```shell
cd build
make start_kubernetes
```
## Playback
### Web browser playback
Visit https://<CDN-Transcode Server IP address>:30443/ using any web browser, you will see the playlist and then click any of the streams in the playlist to playback.

### VLC playback
You can also use Windows VLC player to playback the HTTPs streams provided by the sample service. please run below commands.
vlc https://<CDN-Transcode Server IP address>:30443/hls/big_buck_bunny_1280x720/index.m3u8
