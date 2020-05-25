include(platform.m4)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zookeeper
  labels:
     app: zookeeper
spec:
  replicas: 1
  selector:
    matchLabels:
      app: zookeeper
  template:
    metadata:
      labels:
        app: zookeeper
    spec:
      enableServiceLinks: false
      containers:
        - name: zookeeper
          image: zookeeper:3.5.6
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 2181
          env:
            - name: "ZOO_TICK_TIME"
              value: "10000"
            - name: "ZOO_MAX_CLIENT_CNXNS"
              value: "160000"
            - name: "ZOO_AUTOPURGE_PURGEINTERVAL"
              value: "1"
            - name: "ZOO_LOG4J_PROP"
              value: "ERROR"
          resources:
              requests:
                  cpu: 1
                  memory: 500Mi
              limits:
                  cpu: 2
                  memory: 1000Mi
PLATFORM_NODE_SELECTOR(`Xeon')dnl
