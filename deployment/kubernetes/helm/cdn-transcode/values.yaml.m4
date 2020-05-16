
zookeeper:
  heapSize: 1024m

kafka:
  heapSize: 1024m

liveTranscode:
  replicas: defn(`NLIVES')

vodTranscode:
  replicas: defn(`NVODS')

cdn:
  hostIP: defn(`HOSTIP')

volume:
  html: 
    size: defn(`HTML_VOLUME_SIZE')
  video:
    archive:
      size: defn(`ARCHIVE_VOLUME_SIZE')
    dash:
      size: defn(`DASH_VOLUME_SIZE')
    hls:
      size: defn(`HLS_VOLUME_SIZE')
