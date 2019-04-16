# CDN Transcode Sample Getting Started Guide
This document describes how to run the CDN Transcode Sample (abbr as CTS) step by step. Please refer to [reference architecture](CDN_Transcode_Sample_RA.md) to understand the CTS reference architecture design and how CTS works.

The CTS provides CDN transcode services, and this guide just shows how to use the services in a simplest and typical way which can be scaled out to more complex environment. E.g.: in this guide, the docker images for transcoder server and cdn edge server are hosted on the same physical server. In real case, they can be hosted on differented servers located in different places in the CDN network.

In this document, we'll use the simplest example to show how to build up the pipeline for different user scenarios. To simply the setup, we'll host some docker nodes in the same physical machine.

# Prerequisites
In this document, Ubuntu 18.04 is taken as the host OS.
## Install docker on E3/VCA2/E5 host
- Install [docker.ce](https://docs.docker.com/install).
- Install [docker compose](https://docs.docker.com/compose/install) by referencing docker composer setup guide. Version 1.20+ is required.
- Install [docker swarm](https://docs.docker.com/engine/swarm) by referencing docker swarm setup guide.
- Install FFmpeg.
```sh
sudo apt-get install ffmpeg
```

## Setup docker proxy on E3/VCA2/E5 host
```
sudo mkdir -p /etc/systemd/system/docker.service.d
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
```

# How to build
## Build docker images
On E5 Server, run below command to build docker images:
``` sh
mkdir build
cd build
cmake ..
cd xcode-server/ffmpeg-sw
make
cd cdn-server
make
cd deployment/docker-swarm
make
```

On E3/VCA2 Server, run below command to build docker images:
``` sh
mkdir build
cd build
cmake ..
cd xcode-server/ffmpeg-hw
make
cd cdn-server
make
cd deployment/docker-swarm
make
```

# Auto deploy
The sample supports both auto deployment and manual deployment. There are two ways for auto deployment. For hardware acceleration transcode, docker compose is recommended.

## Stop/start service
Use the following commands to stop/start docker swarm service
```bash
make stop_docker_swarm
make start_docker_swarm
```

Use the following commands to stop/start via docker-compose service
```bash
make stop_docker_compose
make start_docker_compose
```
## Sample execution
### Playback on Web browser
Access URL:https://10.67.116.179/ with any browser, you will see the playlist and then click to play.
### Playback using VLC
Modify the IP address setting in client/vlc_playback.bat, then run the script on Windows client.

# Manual deploy
## Live Streaming
### Environment setup
Below diagram shows how the CTS nodes interconnect with each other and the network topology used in this guide.
```

                          +------------------+-----------------+-----+
                          | Transcode Server | CDN Edge Server |     |
+------------------+      | [Ubuntu docker]  | [Ubuntu docker] |     |     +------------------+
| Streaming Server |      | 192.168.31.31    | 192.168.31.32   | ... |     | Client           |
| PC1 10.67.117.70 |----->|------------------+-----------------+-----|---->| PC2 10.67.117.80 |
| FFmpeg Nginx     |      | E3/VCA2/E5: Ubuntu l8.04 10.67.116.179   |     | VLC              |
+------------------+      +------------------------------------------+     +------------------+

```

### Install FFmpeg on Streaming Server
Run below command on streaming server:
```
sudo apt-get install -y ffmpeg nginx
```

Modify as follows elements at nginx.conf, then copy streams to the path you defined, such as /data/www/file.
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
            root /data/www/file;
            autoindex on;
            autoindex_exact_size off;
            autoindex_localtime on;
        }
    }
}
```

### Create docker network
Run below command on E3/VCA2/E5 server:
```
docker network create -d bridge --subnet 192.168.31.0/24 --gateway 192.168.31.1 my_bridge
```

### Create transcoder server docker instance
Run below command on E5 server:
```
docker run -it --network=my_bridge --ip 192.168.31.31 --name xcoder ovc_transcode_sw /bin/bash
```

Run below command on E3/VCA2 server:
```
docker run -it --device=/dev/dri:/dev/dri --network=my_bridge --ip 192.168.31.31 --name xcoder ovc_transcode_hw /bin/bash
```

### Create CDN server docker instance
Run below command on E3/VCA2/E5 server:
```
docker run -it -p 443:8080 --network=my_bridge --ip 192.168.31.32 --name nginx ovc_cdn_service /bin/bash
```

### Install VLC on client
Run below command on client:
```
sudo apt-get install -y vlc
```

### Sample Execution
#### CDN server
Run below command on CDN server:
```
nginx &
```

#### Transcoder server
Run below command on transcoder server:
```
ffmpeg -i rtmp://10.67.117.70/live/bbb_sunflower_1080p_30fps_normal -vf scale=2560:1440 -c:v libsvt_hevc -b:v 15M -f flv rtmp://192.168.31.32/hls/big_buck_bunny_2560x1440 -vf scale=1920:1080 -c:v libsvt_hevc -b:v 10M -f flv rtmp://192.168.31.32/hls/big_buck_bunny_1920x1080 -vf scale=1280:720 -c:v libx264 -b:v 8M -f flv rtmp://192.168.31.32/hls/big_buck_bunny_1280x720 -vf scale=854:480 -c:v libx264 -b:v 6M -f flv rtmp://192.168.31.32/hls/big_buck_bunny_854x480 -abr_pipeline
```
Alternatively, you can choose to use intel GPU hardware acceleration on E3/VCA2 server, please run below command on transcoder server:
```
ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 -hwaccel_output_format vaapi -i rtmp://10.67.117.70/live/bbb_sunflower_1080p_30fps_normal -vf 'scale_vaapi=w=2560:h=1440' -c:v h264_vaapi -b:v 15M -f flv rtmp://192.168.31.32/hls/big_buck_bunny_2560x1440 -vf 'scale_vaapi=w=1920:h=1080' -c:v h264_vaapi -b:v 10M -f flv rtmp://192.168.31.32/hls/big_buck_bunny_1920x1080 -vf 'scale_vaapi=w=1280:h=720' -c:v h264_vaapi -b:v 8M -f flv rtmp://192.168.31.32/hls/big_buck_bunny_1280x720 -vf 'scale_vaapi=w=854:h=480' -c:v h264_vaapi -b:v 6M -f flv rtmp://192.168.31.32/hls/big_buck_bunny_854x480 -abr_pipeline

```

#### Live play
Run below command on client:
```
vlc https://10.67.116.179:443/hls/big_buck_bunny_2560x1440/index.m3u8
```

## Video on Demand
### Environment setup
Below diagram shows how the CTS nodes interconnect with each other and the network topology used in this guide.
```

                          +------------------+-----+-----------------+
                          | Transcode Server | ... | CDN Edge Server |
                          | [Ubuntu docker]  | ... | [Ubuntu docker] |
                          | 192.168.31.31    | ... | 192.168.31.32   |
                          +------------------+-----+-----------------+
                          | Zookeeper        | Kafka Server          |
+------------------+      | [Ubuntu docker]  | [Ubuntu docker]       |     +------------------+
| Streaming Server |      | 192.168.31.29    | 192.168.31.30         |     | Client           |
| PC1 10.67.117.70 |----->|------------------+-----------------------|---->| PC2 10.67.117.80 |
| FFmpeg Nginx     |      | E3/VCA2/E5: Ubuntu l8.04 10.67.116.179   |     | Browser          |
+------------------+      +------------------------------------------+     +------------------+

```

### Create docker network
Run below command on E3/VCA2/E5 server:
```
docker network create -d bridge --subnet 192.168.31.0/24 --gateway 192.168.31.1 my_bridge
```

### Run zookeeper server docker instance
Run below command on E3/VCA2/E5 server:
```
docker pull confluentinc/cp-zookeeper
docker run -d --name zookeeper --env ZOOKEEPER_SERVER_ID=1 --env ZOOKEEPER_CLIENT_PORT=2181 --env ZOOKEEPER_TICK_TIME=2000 --env ZOOKEEPER_MAX_CLIENT_CNXNS=20000 --env ZOOKEEPER_HEAP_OPTS="-Xmx2048m -Xms2048m" --restart=always --network=my_bridge --ip 192.168.31.29 -it confluentinc/cp-zookeeper
```

### Run kafka server docker instance
Run below command on E3/VCA2/E5 server:
```
docker pull confluentinc/cp-kafka
docker run -d --name kafka --link zookeeper --env KAFKA_BROKER_ID=1 --env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092 --env KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT --env KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT --env KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1  --env KAFKA_DEFAULT_REPLICATION_FACTOR=1 --env KAFKA_AUTO_CREATE_TOPICS_ENABLE=true --env CONFLUENT_SUPPORT_METRICS_ENABLE=0 --env KAFKA_NUM_PARTITIONS=16 --env KAFKA_HEAP_OPTS="-Xmx1024m -Xms1024m" --restart=always --network=my_bridge --ip 192.168.31.30 -it confluentinc/cp-kafka
```

### Run kafka-init server docker instance
Run below command on E3/VCA2/E5 server:
```
docker run -d --name kafka-init --link kafka --env KAFKA_BROKER_ID=ignored --env KAFKA_ZOOKEEPER_CONNECT=ignored --network=my_bridge --ip 192.168.31.31 -it confluentinc/cp-kafka bash -c 'cub kafka-ready -b kafka:9092 1 20 && kafka-topics --create --topic content_provider_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 && sleep infinity'
```

### Run transcoder server docker instance
Run below command on E5 server:
```
docker run -it --network=my_bridge --ip 192.168.31.32 --name xcoder -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <<vcse-cdn project path>>/volume/video/archive:/var/www/archive ovc_transcode_sw /bin/bash
Run:
python3 main.py
```

Run below command on E3/VCA2 server:
```
docker run -it --device=/dev/dri:/dev/dri --network=my_bridge --ip 192.168.31.32 --name xcoder -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <<vcse-cdn project path>>/volume/video/archive:/var/www/archive ovc_transcode_hw /bin/bash
Run:
python3 main.py
```

### Run CDN server docker instance
Run below command on E3/VCA2/E5 server:
```
docker run -it -p 443:8080 --network=my_bridge --ip 192.168.31.33 --name nginx -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <<vcse-cdn project path>>/volume/video/archive/:/var/www/archive ovc_cdn_service /bin/bash
Run:
nginx &
python3 main.py
```

### Configure input streaming parameter on transcoder server docker instance and CDN server docker instance
Modify below parameter in config.ini:
```
[mode]                         # input streaming mode
srcMode=local                  # live - the input is remote rtmp streaming, local - the input is a local stream
[path]                         # local stream path or remote desktop IP.
srcPath=/var/www/archive
```

### Install FFmpeg and Nginx on Streaming Server
Install FFmpeg and Nginx on Streaming Server for live use case:
```
sudo apt-get install -y ffmpeg nginx
```
Add below configuration elements in nginx.conf, then copy video clips to the path defined in the config. E.g: /data/www/file in below config:
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
            root /data/www/file;
            autoindex on;
            autoindex_exact_size off;
            autoindex_localtime on;
        }
    }
}
```

### Playback on Web browser
Access URL:https://10.67.116.179/ with your web browser, you will see the playlist and then click to play.
