apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: zookeeper-service
  name: zookeeper-service
spec:
  selector:
    matchLabels:
      app: zookeeper-service
  replicas: 1
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: zookeeper-service
    spec:
      containers:
      - env:
        - name: ZOOKEEPER_CLIENT_PORT
          value: "2181"
        - name: ZOOKEEPER_HEAP_OPTS
          value: -Xmx2048m -Xms2048m
        - name: ZOOKEEPER_LOG4J_LOGGERS
          value: zookeepr=ERROR
        - name: ZOOKEEPER_LOG4J_ROOT_LOGLEVEL
          value: ERROR
        - name: ZOOKEEPER_MAX_CLIENT_CNXNS
          value: "20000"
        - name: ZOOKEEPER_SERVER_ID
          value: "1"
        - name: ZOOKEEPER_TICK_TIME
          value: "2000"
        image: zookeeper:latest
        name: zookeeper-service
        ports:
        - containerPort: 2181
        resources:
          limits:
            cpu: "2"
            memory: 1048576e3
          requests:
            cpu: "1"
            memory: 524288e3
      nodeSelector:
        kubernetes.io/hostname: master.machine
      restartPolicy: Always
