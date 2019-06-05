# CDN Transcode Sample Getting Started Guide

   * [CDN Transcode Sample Getting Started Guide](#cdn-transcode-sample-getting-started-guide)
   * [Prerequisites](#prerequisites)
      * [Setup CDN-Transcode Server](#setup-cdn-transcode-server)
      * [Setup Streaming Server](#setup-streaming-server)
      * [Setup Client](#setup-client)
   * [Build](#build)
   * [Deploy](#deploy)
      * [Auto deployment](#auto-deployment)  
            * [Auto deployment by docker swarm/compose](#auto-deployment-by-docker-swarm/compose)  
            * [Auto deployment by kubernetes](#auto-deployment-by-kubernetes)
      * [Manual deployment](#manual-deployment)


This document describes how to run the CDN Transcode Sample step by step. Please refer to [reference architecture](CDN_Transcode_Sample_RA.md) to understand the sample reference architecture design and how the sample works.

The sample provides two kinds of services - `live streaming` and `VOD`, and this guide just shows how to use the services in a simplest and typical way which can be scaled out to more complex environment. E.g.: in this guide, the docker images for transcoder server and cdn edge server are hosted on the same physical server. In real case, they can be hosted on different servers located in different places in the CDN network.

# Prerequisites
In this document, we'll use the simplest example to show how to build up the pipeline for different user scenarios. To simply the setup, we'll host docker nodes on the same physical server (named as "CDN-Transcode Server" in this document). One Streaming Server will be used as well to RTMP stream the source video content to CDN-Transcode Server, however you can omit Streaming Server if you want to just use local video content on CDN-Transcode Server. A client system is also needed to playback the transcoded video streams.

Below is the basic block diagram for the sample setup:
```
 +------------------+   +----------------------+   +------------+  
 |                  |   |                      |   |            |  
 | Streaming Server +---+ CDN-Transcode Server +---+   Client   |  
 |                  |   |                      |   |            |  
 +------------------+   +----------------------+   +------------+  
                                                                   
````
**Note**: for `live streaming` and `VOD` in this document, it refers the interaction between `CDN-Transcode Server` and `Client`, not refers interaction between `Streaming Server` and `CDN-Transcode Server`.
## Setup CDN-Transcode Server
- Install Ubuntu 18.04/CentOS 7.6 on CDN-Transcode Server, and configure the IP address & proxy properlly.
- Install Third-party dependency Libraries
```
script/install_dependency.sh
```

- Setup docker network proxy
You may need to setup the docker proxy on CDN-Transcode Server. Below is an example to directly use the host proxy as the docker proxy.
```
sudo mkdir -p /etc/systemd/system/docker.service.d
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## Optional: Setup Streaming Server
As mentioned above, Streaing Server is not a must, you can skip this section if you do not want to stream the source via RTMP.
- Install Ubuntu 18.04 on Streaming Server, and configure the IP address & proxy properlly.
- Install FFmpeg
```sh
sudo apt-get install -y ffmpeg
```
- Install Nginx
```
sudo apt-get install -y nginx
```

## Setup Client
In this document, we can use both VLC and web browser as the playback tool. To use VLC, it's recommended to use Windows VLC client. For web brower, in theory any web browser could be OK, like Chrome, Firefox, Microsoft Edge, IOS Safari, however HEVC playback is not well supported by web browsers, so if you want to playback HEVC stream, use VLC. Also AV1 playback is only supported by Firefox.

# Build
On CDN-Transcode Server, run below command to build docker images:
``` sh
mkdir build
cd build
cmake ..
make
```

# Deploy
The sample supports both auto deployment and manual deployment. The auto deployment will help users to have quick try to use this sample while the manual deployment give more flexibility for customerization.
## Auto deployment
The auto deploy supports both docker swarm, docker compose and kubernetes. The auto deploy will deploy the live streaming and VOD services automatically using a default video stream "big buck bunny" as an example. To simply the setup, the original source video content are local content but not streamed from the RTMP streaming server.

**Note**: If you want to use other video clips to try the auto deployment, you can simply copy the clips into <CDN-Transcode-Sample>/volume/video/archive folder, then run below command to generate video clip thumbnails. The transcode service will perform 1:N transcoding for these video clips. It's recommended to use .mp4 video clip files.
```
ffmpeg -i <CDN-Transcode-Sample>/volume/video/archive/<clip_name> -vf "thumbnail,scale=640:360" -frames:v 1 -y <CDN-Transcode-Sample>/volume/video/archive/<clip_name>.png
```
### Auto deployment using docker swarm/compose
Please refer to [How to deploy CDN Transcode Sample using docker swarm on E5](doc/Deployment_using_docker_swarm.md)
### Auto deployment using kubernetes
#### Setup kubernetes environment
Please refer to [How to setup Kubernetes environment](doc/K8s_Common_Setup.md)
#### Auto deployment using kubernetes on E3
Please refer to [How to deploy CDN Transcode Sample using Kubernetes on E3](doc/Deployment_using_k8s_on_E3.md)
#### Auto deployment using kubernetes on E5
Please refer to [How to deploy CDN Transcode Sample using Kubernetes on E5](doc/Deployment_using_k8s_on_E5.md)
#### Auto deployment using kubernetes on VCA2
Please refer to [How to deploy CDN Transcode Sample using Kubernetes on VCA2](doc/Deployment_using_k8s_on_VCA2.md)

## Manual deployment
The manual deployment give an example to users who want to use this sample as a base to build up more complicated CDN transcode solution. please refer to [How to deploy CDN Transcode Sample by manual](doc/Deployment_by manual.md)
