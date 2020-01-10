# Open Visual Cloud CDN Transcode Sample

[![Travis Build Status](https://travis-ci.com/OpenVisualCloud/CDN-Transcode-Sample.svg?branch=master)](https://travis-ci.com/OpenVisualCloud/CDN-Transcode-Sample)
[![Stable release](https://img.shields.io/badge/latest_release-v1.0-green.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/releases/tag/v1.0)
[![License](https://img.shields.io/badge/license-BSD_3_Clause-green.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/blob/master/LICENSE)
[![Contributions](https://img.shields.io/badge/contributions-welcome-blue.svg)](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki)

Table of Contents
=================
 * [Open Visual Cloud CDN Transcode Sample](#open-visual-cloud-cdn-transcode-sample)
   * [Architecture](#architecture)
   * [What's in this project](#whats-in-this-project)
   * [System requirements](#system-requirements)
      * [Operating system](#operating-system)
   * [How to setup The CDN Transcode Sample](#how-to-setup-the-cdn-transcode-sample)
      * [Setup the CDN Transcode Sample OS environment(Both of master and slave nodes)](#setup-the-cdn-transcode-sample-os-environmentboth-of-master-and-slave-nodes)
         * [Install ubuntu18.04.2/CentOS 7.6](#install-ubuntu18042centos-76)
      * [Setup CDN environment(Both of master and slave nodes)](#setup-cdn-environmentboth-of-master-and-slave-nodes)
         * [Install the third-party dependency Libraries and tools](#install-the-third-party-dependency-libraries-and-tools)
         * [Setup docker proxy as follows if you are behind a firewall](#setup-docker-proxy-as-follows-if-you-are-behind-a-firewall)
      * [Build(Both of master and slave nodes)](#buildboth-of-master-and-slave-nodes)
      * [Deploy](#deploy)
         * [Auto deployment using Kubernetes](#auto-deployment-using-kubernetes)
         * [See Also](#see-also)

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
- Ubuntu* 18.04.2 Server LTS
- CentOS* 7.6

# How to setup The CDN Transcode Sample
## Setup the CDN Transcode Sample OS environment(Both of master and slave nodes)
Install Ubuntu 18.04.2/CentOS 7.6 on CDN-Transcode Server, and configure the IP address & proxy properly.
### Install ubuntu18.04.2/CentOS 7.6
-  [Download Ubuntu and Install](https://ubuntu.com/download)
-  [Download CentOS and install](https://www.centos.org/download/)

## Setup CDN environment(Both of master and slave nodes)
### Install the third-party dependency Libraries and tools
```
sudo -E ./script/install_dependency.sh
```
### Setup docker proxy as follows if you are behind a firewall
```
sudo mkdir -p /etc/systemd/system/docker.service.d
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
```
## Build(Both of master and slave nodes)
Run below commands to build docker images
```
cd CDN-Transcode-Sample
mkdir build
cd build
cmake ..
make
```

## Deploy
### Auto deployment using Kubernetes

**Tips:** It divides into two parts: master or slave ones
- [Setup Kubernetes master environment for CentOS](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-master-environment-for-CentOS)
- [Setup Kubernetes master environment for Ubuntu](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-master-environment-for-Ubuntu)
- [Setup Kubernetes slave environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-slave-environment)
- [Setup NFS environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-NFS-environment)
- [Remove Kubernetes environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Remove-Kubernetes-environment)

Run the following commands to start/stop services

**Tips:** [Configuration example for Kubernetes deploy](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Configuration-example-for-Kubernetes-deploy)
```
make start_kubernetes
make stop_kubernetes
```

____
### See Also
- [Deploy on Xeon E5 using docker swarm](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-Xeon-E5-using-docker-swarm)
- [Deploy on Xeon E5 using Kubernetes](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-Xeon-E5-using-Kubernetes)
- [Deploy on Xeon E3 with Gen GFX using Kubernetes](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-Xeon-E3-with-Gen-GFX-using-Kubernetes)
- [Deploy on VCA2 with Gen GFX using Kubernetes](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-VCA2-with-Gen-GFX-using-Kubernetes)
- [Setup proxy server](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-proxy-server)
- [Setup Kubernetes Logging](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-logging-environment)
- [Setup Kubernetes Monitoring](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-monitoring-environment)
