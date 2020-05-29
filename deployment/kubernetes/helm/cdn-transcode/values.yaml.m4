
registryPrefix: "defn(`REGISTRY_PREFIX')"

zookeeper:
  heapSize: 1024m

kafka:
  heapSize: 1024m

liveTranscode:
  replicas: defn(`NLIVES')
  streams:
    - name: "/var/www/archive/bbb_sunflower_1080p_30fps_normal.mp4"
      transcode:
        - protocol: dash
          scale: "856:480"
          bitrate: "8000000"
          framerate: 25
          gop: 100
          maxbframes: 2
          refsNum: 2
          preset: veryfast
          encoderType: libx264
    - name: "/var/www/archive/bbb_sunflower_1080p_30fps_normal.mp4"
      transcode:
        - protocol: hls
          scale: "856:480"
          bitrate: "8000000"
          framerate: 25
          gop: 100
          maxbframes: 2
          refsNum: 2
          preset: 9
          encoderType: libsvt_hevc

vodTranscode:
  replicas: defn(`NVODS')

cdn:
  hostIP: defn(`HOSTIP')

volume:
  video:
    archive:
      size: defn(`VIDEO_ARCHIVE_VOLUME_SIZE')
    cache:
      size: defn(`VIDEO_CACHE_VOLUME_SIZE')

