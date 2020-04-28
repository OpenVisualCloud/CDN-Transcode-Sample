apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: vod-service
  name: vod-service
spec:
  selector:
    matchLabels:
      app: vod-service
  replicas: 1
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: vod-service
    spec:
      containers:
      - args:
        - bash
        - -c
        - /home/main.py
        image: ovc_software_transcode_service:latest
        imagePullPolicy: IfNotPresent
        name: vod-service
        resources:
          limits:
            cpu: "6"
            memory: 6291456e3
          requests:
            cpu: "3"
            memory: 3145728e3
      nodeSelector:
        kubernetes.io/hostname: master.machine
      restartPolicy: Always
