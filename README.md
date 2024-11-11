# PROJECT NOT UNDER ACTIVE MANAGEMENT #  
This project will no longer be maintained by Intel.  
Intel has ceased development and contributions including, but not limited to, maintenance, bug fixes, new releases, or updates, to this project.  
Intel no longer accepts patches to this project.  
 If you have an ongoing need to use this project, are interested in independently developing it, or would like to maintain patches for the open source software community, please create your own fork of this project.  
  


### Open Visual Cloud CDN Transcode Sample

[![Travis Build Status](https://travis-ci.com/OpenVisualCloud/CDN-Transcode-Sample.svg?branch=master)](https://travis-ci.com/OpenVisualCloud/CDN-Transcode-Sample)
[![Stable release](https://img.shields.io/badge/latest_release-v1.0-green.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/releases/tag/v1.0)
[![License](https://img.shields.io/badge/license-BSD_3_Clause-green.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/blob/master/LICENSE)
[![Contributions](https://img.shields.io/badge/contributions-welcome-blue.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki)

The CDN Transcode Sample is an Open Visual Cloud software stack with all required open source ingredients well integrated to provide out-of-box simple transcode or transcode+CDN service, including live streaming and video on demand. It also provides Docker-based media delivery software development environment upon which developer can easily build their specific applications. 

### Architecture

The sample implements a reference server-side transcode system over CDN infrastructure, which features `live streaming` and `VOD`. Among them, the `VOD` service can run independently to provide a simple transcode service.  

<IMG src="doc/CDN-Transcode-Sample-Arch.png" height="450">

### Software Stacks

The sample is powered by the following Open Visual Cloud software stacks:

- Media transcoding software stack:  

The FFmpeg-based media transcoding stack is used to transcode media content from a higher resolution/quality to a lower resolution/quality. The software stack is optimized for Intel Xeon Scalable Processors and Intel XeonE3 Scalable Processors. 

- Media streaming and Web Hosting software stack:  

The NGINX-based software stack is used to host web services, video content and provide video streaming services. The software stack is optimized for Intel Xeon Scalable Processors.  

### Install Prerequisites:

- **Time Zone**: Check that the timezone setting of your host machine is correctly configured. Timezone is used during build. If you plan to run the sample on a cluster of machines, please make sure to synchronize time among the controller node and worker nodes.

- **Build Tools**: Install `cmake`, `make`, `m4`, `wget` and `gawk` if they are not available on your system.

- **Docker Engine**: 

    - Install [docker engine](https://docs.docker.com/get-docker). Minimum version required: `17.05`. Make sure you setup docker to run as a regular user.
    - Setup `Kubernetes`. See [Kubernetes Setup](deployment/kubernetes/README.md) for additional setup details.
    - Setup docker proxy as follows if you are behind a firewall:   

```
sudo mkdir -p /etc/systemd/system/docker.service.d       
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf       
sudo systemctl daemon-reload          
sudo systemctl restart docker     
```

### Build the Sample  

Run the following command to run the sample as a simple transcoder:  
```
mkdir build
cd build
cmake ..
make
```

Run the following command to run the sample as transcode+CDN:  
```
mkdir build
cd build
cmake -DSCENARIO=cdn ..
make
```

---

If you deploy the sample to a cluster, please configure the sample, as `cmake -DREGISTRY=<registry-url> ..`, to push the sample images to the private docker registry after each build.   

To deploy without a private registry, run `make update` after each build to push the sample images to the cluster nodes (which requires passwordless access from the master node to the worker nodes.)   

---

### Deploy the Sample

Start/stop the sample with Kubernetes [yaml configurations](deployment/kubernetes/yaml):  

```
make volume
make start_kubernetes
...
make stop_kubernetes
```

Start/stop the sample with Kubernetes [Helm charts](deployment/kubernetes/helm):  

```
make volume
make start_helm
...
make stop_helm
```

For the `transcode` scenario, look at the logs of the `benchmark` pod for the batch transcoding summary. For the `cdn` scenario, point your browser to `https://<your-host>` to watch the list of video clips via `DASH` or `HLS`.   

# See Also

- [Kubernetes Setup](deployment/kubernetes/README.md)   
- [Build Options](doc/cmake.md)   
- [Reference Architecture](https://networkbuilders.intel.com/solutionslibrary/container-bare-metal-for-2nd-generation-intel-xeon-scalable-processor)   

