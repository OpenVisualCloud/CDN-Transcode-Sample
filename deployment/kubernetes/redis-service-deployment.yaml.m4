apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    app: redis-service
  name: redis-service
spec:
  replicas: 1
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: redis-service
    spec:
      containers:
      - args:
        - redis-server
        image: redis:latest
        name: redis-service
        ports:
        - containerPort: 6379
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
