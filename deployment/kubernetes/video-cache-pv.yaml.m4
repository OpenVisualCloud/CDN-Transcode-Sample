
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: video-cache
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: video-cache
spec:
  capacity:
    storage: defn(`VIDEO_CACHE_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: video-cache
  local:
    path: defn(`VIDEO_CACHE_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`VIDEO_CACHE_VOLUME_HOST')"

