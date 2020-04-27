apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    app: live-service
  name: live-service
spec:
  replicas: 1
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: live-service
    spec:
      containers:
      - image: ovc_software_transcode_service:latest
        imagePullPolicy: IfNotPresent
        name: live-service
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
