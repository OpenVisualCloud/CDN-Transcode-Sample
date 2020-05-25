include(platform.m4)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: live-defn(`LIVEIDX')
  labels:
    app: live-defn(`LIVEIDX')
spec:
  replicas: 1
  selector:
    matchLabels:
      app: live-defn(`LIVEIDX')
  template:
    metadata:
      labels:
        app: live-defn(`LIVEIDX')
    spec:
      enableServiceLinks: false
      containers:
        - name: live-defn(`LIVEIDX')
          image: defn(`REGISTRY_PREFIX')ovc_software_transcode_service:latest
          imagePullPolicy: IfNotPresent
          resources:
            limits:
              cpu: 8
              memory: 6000Mi
            requests:
              cpu: 4
              memory: 3000Mi
          env:
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
      volumes:
          - name: video-cache
            persistentVolumeClaim:
               claimName: video-cache
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
PLATFORM_NODE_SELECTOR(`Xeon')dnl
