# CDN Transcode Sample Getting Started Guide

   * [CDN Transcode Sample Getting Started Guide](#cdn-transcode-sample-getting-started-guide)
   * [Prerequisites](#prerequisites)
      * [Setup CDN-Transcode Server](#setup-cdn-transcode-server)
      * [Setup Streaming Server](#setup-streaming-server)
      * [Setup Client](#setup-client)
   * [Build](#build)
   * [Deploy](#deploy)
      * [Auto deployment](#auto-deployment)
         * [Start CDN transcode service](#start-cdn-transcode-service)
         * [Playback](#playback)
            * [Web browser playback](#web-browser-playback)
            * [VLC playback](#vlc-playback)
      * [Manual deployment](#manual-deployment)
         * [Setup network topology](#setup-network-topology)
         * [Config CDN-Transcode Server](#config-cdn-transcode-server)
         * [Config Streaming Server](#config-streaming-server)
         * [Start CDN transcode service](#start-cdn-transcode-service-1)
            * [Start zookeeper service](#start-zookeeper-service)
            * [Start kafka service](#start-kafka-service)
            * [Start live transcode docker](#start-live-transcode-docker)
            * [Start VOD transcode service](#start-vod-transcode-service)
            * [Start nginx web service](#start-nginx-web-service)
            * [Start live transcode service](#start-live-transcode-service)
         * [Playback](#playback-1)
            * [Web browser playback](#web-browser-playback-1)
            * [VLC playback](#vlc-playback-1)


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
- Install [docker.ce](https://docs.docker.com/install).
- Install [docker compose](https://docs.docker.com/compose/install) by referencing docker composer setup guide. Version 1.20+ is required.
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- Install [kompose](https://github.com/kubernetes/kompose/blob/master/docs/installation.md) by referencing kubernetes kompose setup guide. Version 1.16+ is required.
```
sudo curl -L https://github.com/kubernetes/kompose/releases/download/v1.18.0/kompose-linux-amd64 -o /usr/local/bin/kompose
```
- Install python3, pip3 and ruamel.yaml

|  Ubuntu 18.04 | CentOS 7.6 |
|:--------------|:-----------|
|(1) sudo apt-get install -y python3-pip |(1) sudo yum install -y python36 python36-pip |
|(2) pip3 install ruamel.yaml            |(2) pip3 install ruamel.yaml                  |

- Setup docker network proxy
You may need to setup the docker proxy on CDN-Transcode Server. Below is an example to directly use the host proxy as the docker proxy.
```
sudo mkdir -p /etc/systemd/system/docker.service.d
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## Setup Streaming Server
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
The auto deploy supports both docker swarm and docker compose. You're recommended to use docker compose in this sample. The auto deploy will deploy the live streaming and VOD services automatically using a default video stream "big buck bunny" as an example. To simply the setup, the original source video content are local content but not streamed from the RTMP streaming server.

**Note**: If you want to use other video clips to try the auto deployment, you can simply copy the clips into <CDN-Transcode-Sample>/volume/video/archive folder, then run below command to generate video clip thumbnails. The transcode service will perform 1:N transcoding for these video clips. It's recommended to use .mp4 video clip files.
```
ffmpeg -i <CDN-Transcode-Sample>/volume/video/archive/<clip_name> -vf "thumbnail,scale=640:360" -frames:v 1 -y <CDN-Transcode-Sample>/volume/video/archive/<clip_name>.png
```
### Start CDN transcode service
Run below steps on CDN-Transcode server to stop/start docker swarm service.

- Initialize docker swarm if you have not
```bash
sudo docker swarm init
```
- Restart docker swarm services
```bash
make stop_docker_swarm
make start_docker_swarm
```
- Restart docker-compose service
```bash
make stop_docker_compose
make start_docker_compose
```
### Playback
#### Web browser playback
Visit https://\<CDN-Transcode Server IP address\>/ using any web browser, you will see the playlist and then click any of the streams in the playlist to playback.
#### VLC playback
You can also use Windows VLC player to playback the HTTPs streams provided by the sample service. A sample [VLC playback script](client/vlc_playback.bat) is provided for this purpose. You may need to change this script to set the IP address and the VLC path in this script.

## Manual deployment
The manual deployment give an example to users who want to use this sample as a base to build up more complicated CDN transcode solution. 

### Setup network topology
In this guide we use a very simple topology diagram to showcase the interconnection between each nodes. Below is an example:
```
                        +-----------------+-----------------+-----------------+
                        |  Live transcode | VOD transcode 1 | VOD transcode 2 |
                        | [Ubuntu docker] | [Ubuntu docker] | [Ubuntu docker] |
                        |  192.168.31.32  |  192.168.31.33  |  192.168.31.34  |
                        +-----------------+-----------------+-----------------+
                        |    Zookeeper    |      Kafka      |      Nginx      |
+----------------+      | [Ubuntu docker] | [Ubuntu docker] | [Ubuntu docker] |      +-------------+
|Streaming Server|      |  192.168.31.29  |  192.168.31.30  |  192.168.31.35  |      |   Client    |
| 10.67.117.70   |----->|-----------------+-----------------+-----------------+----->|10.67.117.80 |
| FFmpeg Nginx   |      |     CDN-Transcode Server: Linux OS 10.67.116.179    |      | VLC/browser |
+----------------+      +-----------------------------------------------------+      +-------------+

```

### Config CDN-Transcode Server
Run below command on CDN-Transcode Server to create docker network:
```
docker network create -d bridge --subnet 192.168.31.0/24 --gateway 192.168.31.1 my_bridge
```

### Config Streaming Server
Add below Nginx configuration section into nginx.conf (may be /etc/nginx/nginx.conf) on streaming server, then copy video clips to the path defined in the configuration. E.g: /var/www/clips is used in this sample.
```
rtmp {
    server {
        application live {
            live on;
            exec_options on;
            exec_pull ffmpeg -re -i http://localhost/$name.mp4 -c:v copy -an -f flv rtmp://localhost/$app/$name;
        }
    }
}
......
http {
    server {
        location / {
            root /var/www/clips;
            autoindex on;
            autoindex_exact_size off;
            autoindex_localtime on;
        }
    }
}
```

### Start CDN transcode service
#### Start zookeeper service
Run below command on CDN-Transcode Server to create zookeeper docker instance:
```
docker pull zookeeper
docker run -d --name zookeeper-service --env ZOOKEEPER_SERVER_ID=1 --env ZOOKEEPER_CLIENT_PORT=2181 --env ZOOKEEPER_TICK_TIME=2000 --env ZOOKEEPER_MAX_CLIENT_CNXNS=20000 --env ZOOKEEPER_HEAP_OPTS="-Xmx2048m -Xms2048m" --restart=always --network=my_bridge --ip 192.168.31.29 -it zookeeper
```

#### Start kafka service
Run below command on CDN-Transcode Server to create kafka docker instance:
```
docker pull wurstmeister/kafka
docker run -d --name kafka-service --link zookeeper-service --env KAFKA_BROKER_ID=1 --env KAFKA_ADVERTISED_HOST_NAME=kafka-service --env KAFKA_ADVERTISED_PORT=9092 --env KAFKA_ZOOKEEPER_CONNECT=zookeeper-service:2181 --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka-service:9092 --env KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT --env KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT --env KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1  --env KAFKA_DEFAULT_REPLICATION_FACTOR=1 --env KAFKA_AUTO_CREATE_TOPICS_ENABLE=true --env KAFKA_NUM_PARTITIONS=16 --env KAFKA_CREATE_TOPICS="content_provider_sched:16:1" --env KAFKA_HEAP_OPTS="-Xmx1024m -Xms1024m" --restart=always --network=my_bridge --ip 192.168.31.30 -it wurstmeister/kafka
```

#### Start live transcode docker
Run below command on CDN-Transcode Server to create live transcode docker instance:
```
docker run -it --network=my_bridge --ip 192.168.31.32 --name live-transcode-service -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls ovc_transcode_sw /bin/bash
```

#### Start VOD transcode service
Run below commands on CDN-Transcode Server to create two vod transcode docker instances:
```
docker run -it --network=my_bridge --ip 192.168.31.33 --name vod-transcode-service-1 -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample>/volume/video/archive:/var/www/archive ovc_transcode_sw /bin/bash -c '/home/main.py'
docker run -it --network=my_bridge --ip 192.168.31.34 --name vod-transcode-service-2 -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample>/volume/video/archive:/var/www/archive ovc_transcode_sw /bin/bash -c '/home/main.py'
```

#### Start nginx web service
Run below command on CDN-Transcode Server to create cdn docker instance:
```
docker run -it -p 443:8080 --network=my_bridge --ip 192.168.31.35 --name cdn-service -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample>/volume/video/archive:/var/www/archive -v <CDN-Transcode-Sample>/volume/html:/var/www/html ovc_cdn_service /bin/bash -c '/home/main.py&/home/self-sign.sh&&/usr/sbin/nginx'
```

#### Start live transcode service
Run below commands on live transcode docker instance to show one 1:4 channels of live transcode. It supports 1 channel of H264 decode, 2 channels of SVT-HEVC encode and 2 channels of x264 encode. **Note**: you need to replace the IP address below with the actual Streaming Server IP address in your setup.
```
ffmpeg -i rtmp://10.67.117.70/live/bbb_sunflower_1080p_30fps_normal \
 -vf scale=2560:1440 -c:v libsvt_hevc -b:v 15M -f flv \
 rtmp://cdn-service/hls/big_buck_bunny_2560x1440 -vf scale=1920:1080 -c:v libsvt_hevc -b:v 10M -f flv \
 rtmp://cdn-service/hls/big_buck_bunny_1920x1080 -vf scale=1280:720 -c:v libx264 -b:v 8M -f flv \
 rtmp://cdn-service/hls/big_buck_bunny_1280x720 -vf scale=854:480 -c:v libx264 -b:v 6M -f flv \
 rtmp://cdn-service/hls/big_buck_bunny_854x480 -abr_pipeline
```

**Note**: for live ABR (using ffmpeg to trancode in 3 variants, and nginx produce one manifest, there are only 3 different resolutions and bit rates supported in live ABR).
Run below commands on live transcode docker instance, the suffix "hi" corresponds to the maximum resolution or bit rate, the suffix "mid" corresponds to the medium resolution or bit rate and the suffix "low" corresponds to the minimum resolution or bit rate.
For DASH
```
ffmpeg -i rtmp://10.67.117.70/live/bbb_sunflower_1080p_30fps_normal -vf scale=1920:1080 -c:v libsvt_hevc -b:v 8M -f flv \
 rtmp://cdn-service/dash/big_buck_bunny_hi -vf scale=1280:720 -c:v libsvt_hevc -b:v 4M -f flv \
 rtmp://cdn-service/dash/big_buck_bunny_mid -vf scale=854:480 -c:v libsvt_hevc -b:v 2M -f flv \
 rtmp://cdn-service/dash/big_buck_bunny_low -abr_pipeline
```
For HLS
```
ffmpeg -i rtmp://10.67.117.70/live/bbb_sunflower_1080p_30fps_normal -vf scale=1920:1080 -c:v libsvt_hevc -b:v 8M -f flv \
 rtmp://cdn-service/hls/big_buck_bunny_hi -vf scale=1280:720 -c:v libsvt_hevc -b:v 4M -f flv \
 rtmp://cdn-service/hls/big_buck_bunny_mid -vf scale=854:480 -c:v libsvt_hevc -b:v 2M -f flv \
 rtmp://cdn-service/hls/big_buck_bunny_low -abr_pipeline
```

Configure below parameters on cdn docker instance, the "max" flag which indicate which representation should have max witdh and height and so use it to create the variant manifest on DASH.
```
rtmp {
  server {
    ......
    application hls {
      ......
      hls_variant _low BANDWIDTH=2048000 RESOLUTION=854x480;
      hls_variant _mid BANDWIDTH=4096000 RESOLUTION=1280x720;
      hls_variant _hi  BANDWIDTH=8192000 RESOLUTION=1920x1080;
    }
    application dash {
      ......
      dash_variant _low bandwidth="2048000" width="854" height="480";
      dash_variant _med bandwidth="4096000" width="1280" height="720";
      dash_variant _hi bandwidth="8192000" width="1920" height="1080" max;
    }
  }
}
```

### Playback
#### Web browser playback
Visit https://\<CDN-Transcode Server IP address\>/ using any web browser, you will see the playlist and then click any of the streams in the playlist to playback.

#### VLC playback
Same as auto deployment, you can use VLC client as well following instructions in the above section.
**Note**: for adaptative streaming, please run below commands.
```
vlc https://\<CDN-Transcode Server IP address\>/dash/big_buck_bunny.mpd
```
