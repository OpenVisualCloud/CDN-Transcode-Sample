
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
    storage: defn(`ARCHIVE_VOLUME_SIZE')
  accessModes:
  - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: video-archive
  local:
    path: defn(`ARCHIVE_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`ARCHIVE_VOLUME_HOST')"
