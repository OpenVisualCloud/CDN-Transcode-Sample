
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: video-archive
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: video-archive
spec:
  capacity:
    storage: defn(`VIDEO_ARCHIVE_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: video-archive
  local:
    path: defn(`VIDEO_ARCHIVE_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`VIDEO_ARCHIVE_VOLUME_HOST')"

