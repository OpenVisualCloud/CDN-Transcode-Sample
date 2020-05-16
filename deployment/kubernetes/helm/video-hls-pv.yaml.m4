
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: video-hls
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: video-hls
spec:
  capacity:
    storage: defn(`HLS_VOLUME_SIZE')
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: video-hls
  local:
    path: defn(`HLS_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`HLS_VOLUME_HOST')"
