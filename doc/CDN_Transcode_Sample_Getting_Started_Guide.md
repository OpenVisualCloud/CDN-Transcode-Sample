# CDN Transcode Sample Getting Started Guide

   * [CDN Transcode Sample Getting Started Guide](#cdn-transcode-sample-getting-started-guide)
   * [Architecture](#architecture)
   * [Prerequisites](#prerequisites)
      * [Setup CDN-Transcode Server](#setup-cdn-transcode-server)
      * [Setup Streaming Server \(Optional\)](#setup-streaming-server-optional)
      * [Setup Client](#setup-client)
   * [Build](#build)
   * [Deploy](#deploy)
      * [Auto deployment](#auto-deployment)  
            * [Auto deployment using docker swarm](#auto-deployment-using-docker-swarm)  
            * [Auto deployment using Kubernetes](#auto-deployment-using-Kubernetes)
      * [Manual deployment](#manual-deployment)


This document describes how to run the CDN Transcode Sample step by step.

The sample provides two kinds of services - `live streaming` and `VOD`, and this guide shows how to use the services in a simplest and typical way which can be scaled out to more complex environment. E.g.: in this guide, the docker images for transcoder server and cdn edge server are hosted on the same physical server. In real case, they can be hosted on different servers located in different places in the CDN network.

# Architecture
The sample implements a reference server-side transcode system over CDN infrastructure, which features `live streaming` and `VOD`.

<IMG src="https://github.com/OpenVisualCloud/CDN-Transcode-Sample/blob/master/volume/html/image/CDN-Transcode-Sample-Arch.png" height="450">


The workflow of live streaming is as follows:
- The live transcode service receives the video stream locally or over rtmp, decapsulate and demux the flv video, transcode to other codecs/bitrate/resolution, in 1:N manner, which means one input and N output. E.g.: one channel HEVC 4k@60fps, transcoded into one channle AVC 720p@30fps, one channel HEVC 1080p@30fps and one channel HEVC 4k@60fps. The transcoded video streams are then be encapsulated in flv over rtmp, be distributed to the CDN service.
- The CDN service receives the video streams from the Live transcode Service, and will translate the video streams into HLS/DASH format.
- The client starts playback the video.

The workflow of VOD is as follows:
- The client starts playback of a video by requesting the video manifest file.
- The CDN service checks if the video has been transcoded. If the DASH/HLS segments exist, the CDN service simply returns the manifest (and any subsequent video segments.) Otherwise, the CDN service schedules transcoding of the video in Kafka, a message system shared between the CDN service and the VOD trancode service.
- The VOD trancode service receives the request and starts transcoding of the video clip.
- The CDN service returns the resulting DASH/HLS manifest and segments to the client.


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
- Install the third-party dependency Libraries and tools.
```
script/install_dependency.sh
```
**Note**: This script must be run as root.

- Setup docker network proxy
You may need to setup the docker proxy on CDN-Transcode Server. Below is an example to directly use the host proxy as the docker proxy.
```
sudo mkdir -p /etc/systemd/system/docker.service.d
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## Setup Streaming Server (Optional)
As mentioned above, Streaing Server is not a must, you can skip this section if you do not want to stream the source via RTMP.
- Install Ubuntu 18.04 on Streaming Server, and configure the IP address & proxy properlly.
- Install FFmpeg
```sh
sudo apt-get install -y ffmpeg
```
- Install Nginx and Nginx RTMP Module
```
git clone https://github.com/arut/nginx-rtmp-module.git

wget http://nginx.org/download/nginx-1.14.2.tar.gz
tar -xvzf nginx-1.14.2.tar.gz
cd nginx-1.14.2
./configure --prefix=/usr/local/nginx --conf-path=/etc/nginx/nginx.conf --add-module=/path/to/nginx-rtmp-module
make && sudo make install
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
The auto deploy supports both docker swarm and kubernetes. The auto deploy will deploy the live streaming and VOD services automatically using a default video stream "big buck bunny" as an example. To simply the setup, the original source video content are local content but not streamed from the RTMP streaming server.

**Note**: If you want to use other video clips to try the auto deployment, you can simply visit https://\<CDN-Transcode Server IP address\>/ using web browser, click the guest button at the top right-hand corner and then choose upload option. It's recommended to use .mp4 video clip files.

### Auto deployment using docker swarm
  For details, please refer to [Deploy on Xeon E5 using docker swarm](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-Xeon-E5-using-docker-swarm).
### Auto deployment using Kubernetes
1. Setup kubernetes environment  
   For details, please refer to [Setup Kubernetes environment](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Setup-Kubernetes-environment).  
**Note**: If you have setup kubernetes environment, please skip this step.
2. Auto deployment on your own platform
   * Auto deployment using kubernetes on E3  
   For details, please refer to [Deploy on Xeon E3 with Gen GFX server using Kubernetes](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-Xeon-E3-with-Gen-GFX-using-Kubernetes).
   * Auto deployment using kubernetes on E5  
   For details, please refer to [Deploy on Xeon E5 server using Kubernetes](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-Xeon-E5-server-using-Kubernetes).
   * Auto deployment using kubernetes on VCA2  
   For details, please refer to [Deploy on VCA2 using Kubernetes](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Deploy-on-VCA2-using-Kubernetes).

## Manual deployment
The manual deployment give an example to users who want to use this sample as a base to build up more complicated CDN transcode solution. For details, please refer to [Manual Deploy](https://github.com/OpenVisualCloud/CDN-Transcode-Sample/wiki/Manual-Deploy).
