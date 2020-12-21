version: '3.1'

include(platform.m4)
services:

    redis-service:
        image: redis:latest
        restart: always
        deploy:
            replicas: 1
        user: redis
        command:
            redis-server

    zookeeper-service:
        image: zookeeper:latest
        environment:
            ZOOKEEPER_SERVER_ID: 1
            ZOOKEEPER_CLIENT_PORT: '2181'
            ZOOKEEPER_TICK_TIME: '2000'
            ZOOKEEPER_HEAP_OPTS: '-Xmx2048m -Xms2048m'
            ZOOKEEPER_MAX_CLIENT_CNXNS: '20000'
            ZOOKEEPER_LOG4J_LOGGERS: 'zookeepr=ERROR'
            ZOOKEEPER_LOG4J_ROOT_LOGLEVEL: 'ERROR'
        user: zookeeper
        restart: always
        deploy:
            replicas: 1

    kafka-service:
        image: defn(`REGISTRY_PREFIX')ovc_kafka_service:latest
        depends_on:
            - zookeeper-service
        environment:
            KAFKA_BROKER_ID: 1
            KAFKA_ADVERTISED_HOST_NAME: 'kafka-service'
            KAFKA_ADVERTISED_PORT: '9092'
            KAFKA_ZOOKEEPER_CONNECT: 'zookeeper-service:2181'
            KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka-service:9092'
            KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'PLAINTEXT:PLAINTEXT'
            KAFKA_INTER_BROKER_LISTENER_NAME: 'PLAINTEXT'
            KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
            KAFKA_DEFAULT_REPLICATION_FACTOR: 1
            KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
            KAFKA_NUM_PARTITIONS: 16
            KAFKA_CREATE_TOPICS: 'content_provider_sched:16:1'
            KAFKA_LOG_RETENTION_HOURS: 8
            KAFKA_HEAP_OPTS: '-Xmx1024m -Xms1024m'
            KAFKA_LOG4J_LOGGERS: 'kafka=ERROR,kafka.controller=ERROR,state.change.logger=ERROR,org.apache.kafka=ERROR'
            KAFKA_LOG4J_ROOT_LOGLEVEL: 'ERROR'
        user: kafka
        restart: always
        deploy:
            replicas: 1

    cdn-service:
        image: defn(`REGISTRY_PREFIX')`ovc_'defn(`SCENARIO')_service:latest
        ports:
ifelse(defn(`SCENARIO'),`cdn',`dnl
            - "443:8443"
')dnl
            - "1935:1935"
        volumes:
            - ${VIDEO_ARCHIVE_VOLUME}:/var/www/archive:rw
            - ${VIDEO_CACHE_VOLUME}:/var/www/video:rw
        depends_on:
            - kafka-service
        deploy:
            replicas: 1
        secrets:
            - source: self_crt
              target: /var/run/secrets/self.crt
              uid: ${USER_ID}
              gid: ${GROUP_ID}
              mode: 0444
            - source: self_key
              target: /var/run/secrets/self.key
              uid: ${USER_ID}
              gid: ${GROUP_ID}
              mode: 0440

    vod-transcode-service:
        image: defn(`REGISTRY_PREFIX')`ovc_transcode_'defn(`PLATFORM_SUFFIX'):latest
        volumes:
            - ${VIDEO_ARCHIVE_VOLUME}:/var/www/archive:ro
            - ${VIDEO_CACHE_VOLUME}:/var/www/video:rw
        deploy:
            replicas: defn(`NVODS')
        depends_on:
            - kafka-service
            - zookeeper-service

ifelse(defn(`SCENARIO'),`cdn',`dnl
    live-transcode-service:
        image: defn(`REGISTRY_PREFIX')`ovc_transcode_'defn(`PLATFORM_SUFFIX'):latest
        volumes:
            - ${VIDEO_ARCHIVE_VOLUME}:/var/www/archive:ro
        depends_on:
            - cdn-service
        environment:
            no_proxy: "cdn-service"
            NO_PROXY: "cdn-service"
        command: ["ffmpeg","-re","-stream_loop","-1","-i","/var/www/archive/bbb_sunflower_1080p_30fps_normal.mp4","-vf","scale=856:480","-c:v","libx264","-b:v","8000000","-forced-idr","1","-preset","veryfast","-an","-f","flv","rtmp://cdn-service/dash/media_0_0","-vf","scale=856:480","-c:v","libsvt_hevc","-b:v","8000000","-forced-idr","1","-preset","9","-an","-f","flv","rtmp://cdn-service/hls/media_0_0","-abr_pipeline"]
')dnl

secrets:
    self_key:
        file: ${SECRETS_VOLUME}/self.key
    self_crt:
        file: ${SECRETS_VOLUME}/self.crt
