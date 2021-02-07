include(platform.m4)
include(configure.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: vod
  labels:
    app: vod
spec:
  replicas: defn(`NVODS')
  selector:
    matchLabels:
      app: vod
  template:
    metadata:
      labels:
        app: vod
    spec:
      enableServiceLinks: false
      containers:
        - name: vod
          image: defn(`REGISTRY_PREFIX')`tc_transcode_'defn(`PLATFORM_SUFFIX'):latest
          imagePullPolicy: IfNotPresent
ifelse(defn(`SCENARIO'),`transcode',`dnl
          resources:
            limits:
              cpu: eval(defn(`VOD_CPU')*4)
              memory: eval(defn(`VOD_MEMORY')*4)Mi
            requests:
              cpu: eval(defn(`VOD_CPU')*2)
              memory: eval(defn(`VOD_MEMORY')*2)Mi
')dnl
          env:
            - name: HW_ACCELERATOR
              value: ifelse(defn(`PLATFORM'),`Xeon',"false","true")
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /var/www/video
              name: video-cache
            - mountPath: /var/www/archive
              name: video-archive
              readOnly: true
defn(`PLATFORM_RESOURCES')dnl
      volumes:
          - name: video-cache
            persistentVolumeClaim:
               claimName: video-cache
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
PLATFORM_NODE_SELECTOR(`Xeon')dnl

ifelse(defn(`SCENARIO'),`transcode',`
---

apiVersion: batch/v1
kind: Job
metadata:
  name: benchmark
spec:
  template:
    spec:
      enableServiceLinks: false
      containers:
        - name: benchmark
          image: defn(`REGISTRY_PREFIX')tc_benchmark_service:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: HW_ACCELERATOR
              value: ifelse(defn(`PLATFORM'),`Xeon',"false","true")
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /var/www/archive
              name: video-archive
              readOnly: true
            - mountPath: /var/www/video
              name: video-cache
defn(`PLATFORM_RESOURCES')dnl
      volumes:
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
          - name: video-cache
            persistentVolumeClaim:
               claimName: video-cache
      restartPolicy: Never
PLATFORM_NODE_SELECTOR(`Xeon')dnl
')
