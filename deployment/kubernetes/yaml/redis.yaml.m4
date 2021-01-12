include(platform.m4)
include(configure.m4)

apiVersion: v1
kind: Service
metadata:
  name: redis-service
  labels:
    app: redis
spec:
  ports:
  - port: 6379
    protocol: TCP
  selector:
    app: redis

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  labels:
     app: redis
spec:
  replicas: ifelse(defn(`SCENARIO'),`cdn',1,0)
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:latest
          imagePullPolicy: IfNotPresent
          command:
            - redis-server 
          ports:
            - containerPort: 6379
          securityContext:
            runAsUser: 999
          resources:
              requests:
                  cpu: defn(`REDIS_CPU')
                  memory: defn(`REDIS_MEMORY')Mi
              limits:
                  cpu: eval(defn(`REDIS_CPU')*2)
                  memory: eval(defn(`REDIS_MEMORY')*2)Mi
PLATFORM_NODE_SELECTOR(`Xeon')dnl
