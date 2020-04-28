apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: cdn-service
  name: cdn-service
spec:
  selector:
    matchLabels:
      app: cdn-service
  replicas: 1
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: cdn-service
    spec:
      containers:
      - args:
        - bash
        - -c
        - /home/main.py&/usr/local/sbin/nginx
        image: ovc_cdn_service:latest
        imagePullPolicy: IfNotPresent
        name: cdn-service
        ports:
        - containerPort: 8080
        - containerPort: 1935
        resources:
          limits:
            cpu: "3"
            memory: 3145728e3
          requests:
            cpu: 1500m
            memory: 1572864e3
      nodeSelector:
        kubernetes.io/hostname: master.machine
      restartPolicy: Always
