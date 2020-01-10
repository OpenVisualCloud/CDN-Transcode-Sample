# Open Visual Cloud CDN Transcode Sample

[TOC]

[![Travis Build Status](https://travis-ci.com/OpenVisualCloud/CDN-Transcode-Sample.svg?branch=master)](https://travis-ci.com/OpenVisualCloud/CDN-Transcode-Sample)

[![Stable release](https://img.shields.io/badge/latest_release-v1.0-green.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/releases/tag/v1.0)
[![License](https://img.shields.io/badge/license-BSD_3_Clause-green.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/blob/master/LICENSE)
[![Contributions](https://img.shields.io/badge/contributions-welcome-blue.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki)

The CDN Transcode Sample is an Open Visual Cloud software stack with all required open source ingredients well integrated to provide out-of-box CDN media transcode service, including live streaming and video on demand. It also provides Docker-based media delivery software development environment upon which developer can easily build their specific applications.

# Architecture

The sample implements a reference server-side transcode system over CDN infrastructure, which features `live streaming` and `VOD`.

<IMG src="https://github.com/OpenVisualCloud/CDN-Transcode-Sample/blob/master/volume/html/image/CDN-Transcode-Sample-Arch.png" height="450">


# What's in this project
The CDN Transcode Sample contains below components:
-  Dockerfiles
-  Python web services source code
-  BASH glue scripts
-  HTML web pages
-  CMakefiles
-  Configuration files
-  Documents

# System requirements
## Operating system
The CDN Transcode Sample may run on Linux* 64 bit operating systems. The list below represents the operating systems that the transcode application and library were tested and validated on:
- Ubuntu* 18.04 Server LTS
- CentOS* 7.6

# How to setup The CDN Transcode Sample
## Setup the CDN Transcode Sample OS environment(Both of master and slave nodes)
Install Ubuntu 18.04/CentOS 7.6 on CDN-Transcode Server, and configure the IP address & proxy properly.
### Install ubuntu18.04.2/CentOS 7.6
-  [Download ubuntu OS](https://ubuntu.com/download)
-  [Download CentOS](https://www.centos.org/download/)


## Setup CDN environment(Both of master and slave nodes)
### Install the third-party dependency Libraries and tools
	sudo -E ./script/install_dependency.sh
### Setup docker proxy as follows if you are behind a firewall
-   sudo mkdir -p /etc/systemd/system/docker.service.d
-   printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf
-   sudo systemctl daemon-reload
-   sudo systemctl restart docker

## Build(Both of master and slave nodes)
Run below command to build docker images
	

```
    cd CDN-Transcode-Sample
	mkdir build
	cd build
	cmake ..
	make
```




## Deploy
### Auto deployment using Kubernetes

It divides into two parts: master node or slave node

-  [Setup Kubernetes master node environment ubuntu](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-master-node-environment-ubuntu)
-  [Setup Kubernetes master node environment CentOS](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-master-node-environment-CentOS)
-  [Setup Kubernetes slave node environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-slave-node-environment)
-  [Setup NFS environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-NFS-environment)
-  [Remove the Kubernetes environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Remove-the-Kubernetes-environment)

Run the following script to start/stop services
-  [Start CDN Transcode Sample](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Start-CDN-Transcode-Sample)
	
	```
	sudo ./deployment/kubernetes/start.sh
	sudo ./deployment/kubernetes/stop.sh
	```
	
	
	

____
### See Also

-  [Deploy E3](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-Xeon-E3-with-Gen-GFX-using-Kubernetes)
-  [Deploy VAC2](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-VCA2-using-Kubernetes)
-  [Set proxy server](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Set-proxy-server)
-  [CDN Transcode Sample Reference Architecture](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/OVC-CDN-Transcode-E2E-Sample-Reference-Architecture)
-  [Setup Kubernetes slave environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-slave-environment)
-  [Setup NFS environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-NFS-environment)
-  [Remove the Kubernetes environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Remove-the-Kubernetes-environment)
-  [Start CDN Transcode Sample](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Start-CDN-Transcode-Sample)
-  [Setup Kubernetes master environment ubuntu](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-master-environment-ubuntu)
-  [Setup Kubernetes master environment CentOS](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-master-environment-CentOS)
