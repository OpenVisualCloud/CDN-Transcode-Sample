# CDN Transcode Sample Getting Started Guide
This document describes how to run the CDN Transcode Sample (abbr as CTS) step by step. Please refer to [reference architecture](CDN_Transcode_Sample_RA.md) to understand the CTS reference architecture design and how CTS works.

The CTS provides two kinds of services - live streaming and VOD, and this guide just shows how to use the services in a simplest and typical way which can be scaled out to more complex environment. E.g.: in this guide, the docker images for transcoder server and cdn edge server are hosted on the same physical server. In real case, they can be hosted on differented servers located in different places in the CDN network.

In this document, we'll use the simplest example to show how to build up the pipeline for different user scenarios. To simply the setup, we'll host some docker nodes in the same physical server (we call it as CDN-Transcode server in this document).

# Prerequisites
In this document, Ubuntu 18.04 is taken as the CDN-Transcode server OS.
## Install Docker
- Install [docker.ce](https://docs.docker.com/install).
- Install [docker compose](https://docs.docker.com/compose/install) by referencing docker composer setup guide. Version 1.20+ is required.
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
## Install FFmpeg
```sh
sudo apt-get install ffmpeg
```

## Setup docker proxy on CDN-Transcode server
```
sudo mkdir -p /etc/systemd/system/docker.service.d
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
```

# Build docker images
On CDN-Transcode Server, run below command to build docker images:
``` sh
mkdir build
cd build
cmake ..
cd xcode-server/ffmpeg-sw
make
cd ../../cdn-server
make
cd ../deployment/docker-swarm
make
```

# Deploy
The sample supports both auto deployment and manual deployment. The auto deployment will help users to have quick try to use this sample while the manual deployment give more flexibility for customerization.

**Note: If you want to add your own video clips, please copy them to <CDN-Transcode-Sample folder path>/volume/video/archive folder, then run below command to generate video clip preview pictures. For video clips suffix name, .mp4 is recommended.**
```
ffmpeg -i <CDN-Transcode-Sample folder path>/volume/video/archive/<clip_name> -vf "thumbnail,scale=640:360" -frames:v 1 -y <CDN-Transcode-Sample folder path>/volume/video/archive/<clip_name>.png
```

## Auto deploy
The auto deploy supports both docker swarm and docker compose. You're recommend to use docker compose in this sample. The auto deploy will deploy the VOD and live streaming sample service automatically using a video stream big buck bunny as one example. For auto deployment, the original source video content are local content but not streamed from a streaming server, to simply the setup.
### Stop/start service
Use the following commands to stop/start docker swarm service
```bash
make stop_docker_swarm
make start_docker_swarm
```

Use the following commands to stop/start docker-compose service
```bash
make stop_docker_compose
make start_docker_compose
```
### Playback on web browser
Access URL:https://\<CDN-Transcode Server IP address\>/ with any browser, you will see the playlist and then click any of the streams in the playlist to playback.
### Playback on VLC client
You can also modify client/vlc_playback.bat to use Windows VLC player to playback the HTTPs streams provided by the sample service. E.g: the IP address and the VLC path may need to be changed.

## Manual deploy
The manual deployment give an example to users who want to use this sample as a base to build up more complicated CDN transcode solution. 
### Environment setup
#### Network topology
In this guide we use a very simple topology diagram to showcase the interconnection between each nodes. Below is the diagram: 
```
                     +-----------------+-----------------+-----------------+-----------------+                  
                     |  Live transcode | VOD transcode 1 | VOD transcode 2 |                 |                  
                     | [Ubuntu docker] | [Ubuntu docker] | [Ubuntu docker] |      ...        |                  
                     | 192.168.31.32   | 192.168.31.33   | 192.168.31.34   |                 |                  
                     +-----------------+-----------------+-----------------+-----------------+                  
                     |    Zookeeper    |      Kafka      |   kafka-init    |     Nginx       |                  
+----------------+   | [Ubuntu docker] | [Ubuntu docker] | [Ubuntu docker] | [Ubuntu docker] |   +-------------+
|Streaming Server|   | 192.168.31.29   | 192.168.31.30   | 192.168.31.31   | 192.168.31.35   |   |   Client    |
| 10.67.117.70   |-->|-----------------+-----------------+-----------------+-----------------+-->|10.67.117.80 |
|FFmpeg Nginx    |   |           CDN-Transcode Server:  Ubuntu l8.04 10.67.116.179           |   |VLC/browser  |
+----------------+   +-----------------------------------------------------------------------+   +-------------+

```
#### Install FFmpeg on Streaming Server
Run below command on streaming server. If you deploy streaming server on the same physical CDN-Transcode server, you can skip this step. Note that in this guide Ubuntu 18.04 is taken as the Streaming Server Operating System.
```
sudo apt-get install -y ffmpeg nginx
```

#### Adjust Nginx in config
Add below Nginx configuration section into nginx.conf (may be /etc/nginx/nginx.conf) on streaming server, then copy streams to the path defined in the configuration. E.g: /var/www/clips is used in this sample.
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
#### Create docker network
Run below command on CDN-Transcode server to create docker network:
```
docker network create -d bridge --subnet 192.168.31.0/24 --gateway 192.168.31.1 my_bridge
```
### Launch CDN transcode service
#### Create zookeeper docker instance
Run below command on CDN-Transcode server to create zookeeper docker instance:
```
docker pull confluentinc/cp-zookeeper
docker run -d --name zookeeper --env ZOOKEEPER_SERVER_ID=1 --env ZOOKEEPER_CLIENT_PORT=2181 --env ZOOKEEPER_TICK_TIME=2000 --env ZOOKEEPER_MAX_CLIENT_CNXNS=20000 --env ZOOKEEPER_HEAP_OPTS="-Xmx2048m -Xms2048m" --restart=always --network=my_bridge --ip 192.168.31.29 -it confluentinc/cp-zookeeper
```

#### Create kafka docker instance
Run below command on CDN-Transcode server to create kafka docker instance:
```
docker pull confluentinc/cp-kafka
docker run -d --name kafka --link zookeeper --env KAFKA_BROKER_ID=1 --env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092 --env KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT --env KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT --env KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1  --env KAFKA_DEFAULT_REPLICATION_FACTOR=1 --env KAFKA_AUTO_CREATE_TOPICS_ENABLE=true --env CONFLUENT_SUPPORT_METRICS_ENABLE=0 --env KAFKA_NUM_PARTITIONS=16 --env KAFKA_HEAP_OPTS="-Xmx1024m -Xms1024m" --restart=always --network=my_bridge --ip 192.168.31.30 -it confluentinc/cp-kafka
```

#### Create kafka-init docker instance
Run below command on CDN-Transcode server to create kafka-init docker instance:
```
docker run -d --name kafka-init --link kafka --env KAFKA_BROKER_ID=ignored --env KAFKA_ZOOKEEPER_CONNECT=ignored --network=my_bridge --ip 192.168.31.31 -it confluentinc/cp-kafka bash -c 'cub kafka-ready -b kafka:9092 1 20 && kafka-topics --create --topic content_provider_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 && sleep infinity'
```

#### Create live transcode docker instance
Run below command on CDN-Transcode server to create live transcode docker instance:
```
docker run -it --network=my_bridge --ip 192.168.31.32 --name live_transcode -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls ovc_transcode_sw /bin/bash
```

#### Create two VOD transcode docker instances
Run below commands on CDN-Transcode server to create two vod transcode docker instances:
```
docker run -it --network=my_bridge --ip 192.168.31.33 --name vod_transcode_1 -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample folder path>/volume/video/archive:/var/www/archive ovc_transcode_sw /bin/bash -c '/home/main.py'
docker run -it --network=my_bridge --ip 192.168.31.34 --name vod_transcode_2 -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample folder path>/volume/video/archive:/var/www/archive ovc_transcode_sw /bin/bash -c '/home/main.py'
```

#### Create nginx web service docker instance
Run below command on CDN-Transcode server to create nginx docker instance:
```
docker run -it -p 443:8080 --network=my_bridge --ip 192.168.31.35 --name nginx -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample folder path>/volume/video/archive:/var/www/archive -v <CDN-Transcode-Sample folder path>/volume/html:/var/www/html ovc_cdn_service /bin/bash -c '/home/main.py&/home/self-sign.sh&&/usr/sbin/nginx'
```

#### Launch live transcoder service
Run below commands on live transcode docker instance to show one 1:4 channels of live transcode. It supports 1 channel of H264 decode, 2 channels of SVT-HEVC encode and 2 channels of x264 encode.
```
ffmpeg -i rtmp://10.67.117.70/live/bbb_sunflower_1080p_30fps_normal -vf scale=2560:1440 -c:v libsvt_hevc -b:v 15M -f flv \
 rtmp://nginx/hls/big_buck_bunny_2560x1440 -vf scale=1920:1080 -c:v libsvt_hevc -b:v 10M -f flv \
 rtmp://nginx/hls/big_buck_bunny_1920x1080 -vf scale=1280:720 -c:v libx264 -b:v 8M -f flv \
 rtmp://nginx/hls/big_buck_bunny_1280x720 -vf scale=854:480 -c:v libx264 -b:v 6M -f flv \
 rtmp://nginx/hls/big_buck_bunny_854x480 -abr_pipeline
```
#### Playback video streams on the clients
##### Playback on web browser

Access https://\<CDN-Transcode Server IP address\>/ with any browser, you will see the playlist and then click any of the streams in the playlist to playback.

##### Playback on VLC client

You can also modify client/vlc_playback.bat to use Windows VLC player to playback the HTTPs streams provided by the sample service. E.g: the IP address and the VLC path may need to be changed.

