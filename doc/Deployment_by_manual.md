# Manual deployment
## Setup network topology
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

## Config CDN-Transcode Server
Run below command on CDN-Transcode Server to create docker network:
```
docker network create -d bridge --subnet 192.168.31.0/24 --gateway 192.168.31.1 my_bridge
```

## Optional: Config Streaming Server
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

## Start CDN transcode service
### Start zookeeper service
Run below command on CDN-Transcode Server to create zookeeper docker instance:
```
docker pull zookeeper
docker run -d --name zookeeper-service --env ZOOKEEPER_SERVER_ID=1 --env ZOOKEEPER_CLIENT_PORT=2181 --env ZOOKEEPER_TICK_TIME=2000 --env ZOOKEEPER_MAX_CLIENT_CNXNS=20000 --env ZOOKEEPER_HEAP_OPTS="-Xmx2048m -Xms2048m" --restart=always --network=my_bridge --ip 192.168.31.29 -it zookeeper
```

### Start kafka service
Run below command on CDN-Transcode Server to create kafka docker instance:
```
docker pull wurstmeister/kafka
docker run -d --name kafka-service --link zookeeper-service --env KAFKA_BROKER_ID=1 --env KAFKA_ADVERTISED_HOST_NAME=kafka-service --env KAFKA_ADVERTISED_PORT=9092 --env KAFKA_ZOOKEEPER_CONNECT=zookeeper-service:2181 --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka-service:9092 --env KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT --env KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT --env KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1  --env KAFKA_DEFAULT_REPLICATION_FACTOR=1 --env KAFKA_AUTO_CREATE_TOPICS_ENABLE=true --env KAFKA_NUM_PARTITIONS=16 --env KAFKA_CREATE_TOPICS="content_provider_sched:16:1" --env KAFKA_HEAP_OPTS="-Xmx1024m -Xms1024m" --restart=always --network=my_bridge --ip 192.168.31.30 -it wurstmeister/kafka
```

### Start live transcode docker
Run below command on CDN-Transcode Server to create live transcode docker instance:
```
docker run -it --network=my_bridge --ip 192.168.31.32 --name live-transcode-service -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls ovc_transcode_sw /bin/bash
```

### Start VOD transcode service
Run below commands on CDN-Transcode Server to create two vod transcode docker instances:
```
docker run -it --network=my_bridge --ip 192.168.31.33 --name vod-transcode-service-1 -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample>/volume/video/archive:/var/www/archive ovc_transcode_sw /bin/bash -c '/home/main.py'
docker run -it --network=my_bridge --ip 192.168.31.34 --name vod-transcode-service-2 -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample>/volume/video/archive:/var/www/archive ovc_transcode_sw /bin/bash -c '/home/main.py'
```

### Start nginx web service
Run below command on CDN-Transcode Server to create cdn docker instance:
```
docker run -it -p 443:8080 --network=my_bridge --ip 192.168.31.35 --name cdn-service -v /var/www/dash:/var/www/dash -v /var/www/hls:/var/www/hls -v <CDN-Transcode-Sample>/volume/video/archive:/var/www/archive -v <CDN-Transcode-Sample>/volume/html:/var/www/html ovc_cdn_service /bin/bash -c '/home/main.py&/home/self-sign.sh&&/usr/sbin/nginx'
```

### Start live transcode service
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

## Playback
### Web browser playback
Visit https://\<CDN-Transcode Server IP address\>/ using any web browser, you will see the playlist and then click any of the streams in the playlist to playback.

### VLC playback
Same as auto deployment, you can use VLC client as well following instructions in the above section.
**Note**: for adaptative streaming, please run below commands.
```
vlc https://<CDN-Transcode Server IP address>/dash/big_buck_bunny.mpd
```
