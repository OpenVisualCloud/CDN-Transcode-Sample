
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-cache
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: video-cache
  resources:
    requests:
      storage: defn(`VIDEO_CACHE_VOLUME_SIZE')Gi
