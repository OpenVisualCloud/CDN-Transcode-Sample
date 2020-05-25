# Minimum resource requirements on container runtime, the maximum resource requirements is 2x minimum.
[cdn]
cpu = defn(`CDN_CPU_REQUEST')
mem = defn(`CDN_MEM_REQUEST')

[redis]
cpu = defn(`REDIS_CPU_REQUEST')
mem = defn(`REDIS_MEM_REQUEST')

[zookeeper]
cpu = defn(`ZOOKEEPER_CPU_REQUEST')
mem = defn(`ZOOKEEPER_MEM_REQUEST')

[kafka]
cpu = defn(`KAFKA_CPU_REQUEST')
mem = defn(`KAFKA_MEM_REQUEST')

[vod]
cpu = defn(`VOD_CPU_REQUEST')
mem = defn(`VOD_MEM_REQUEST')
