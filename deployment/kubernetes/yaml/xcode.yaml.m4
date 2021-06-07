include(../../../script/loop.m4)
include(configure.m4)
include(platform.m4)

loop(DEVICEIDX,0,eval(defn(`HW_DEVICE_NUM')-1),`

apiVersion: apps/v1
kind: Deployment
metadata:
  name: xcode-defn(`DEVICEIDX')
  labels:
    app: xcode-defn(`DEVICEIDX')
spec:
  replicas: defn(`NVODS')
  selector:
    matchLabels:
      app: xcode-defn(`DEVICEIDX')
  template:
    metadata:
      labels:
        app: xcode-defn(`DEVICEIDX')
    spec:
      enableServiceLinks: false
      containers:
        - name: xcode-defn(`DEVICEIDX')
          image: defn(`REGISTRY_PREFIX')`tc_xcode_'defn(`PLATFORM_SUFFIX'):latest
          imagePullPolicy: IfNotPresent
ifelse(defn(`SCENARIO'),`cdn',,`dnl
          resources:
            limits:
              cpu: eval(defn(`VOD_CPU')*4)
              memory: eval(defn(`VOD_MEMORY')*4)Mi
            requests:
              cpu: eval(defn(`VOD_CPU')*2)
              memory: eval(defn(`VOD_MEMORY')*2)Mi
')dnl
          env:
            - name: HW_ACC_TYPE
              value: ifelse(defn(`PLATFORM'),`Xeon',"sw","defn(`HW_ACC_PLUGIN_TYPE')")
ifelse(defn(`PLATFORM'),`Xeon',,`dnl
            - name: HW_DEVICE
              value: "`/dev/dri/renderD'eval(defn(`DEVICEIDX')+128)"
')dnl
            - name: `SCENARIO'
              value: "defn(`SCENARIO')"
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
      initContainers:
        - image: busybox:latest
          imagePullPolicy: IfNotPresent
          name: init
          command: ["sh", "-c", "chown -R 1000:1000 /var/www/video"]
          volumeMounts:
            - mountPath: /var/www/video
              name: video-cache
      volumes:
          - name: video-cache
            persistentVolumeClaim:
               claimName: video-cache
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---
')

ifelse(defn(`SCENARIO'),`cdn',,`
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
