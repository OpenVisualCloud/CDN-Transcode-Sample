
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: video-dash
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: video-dash
spec:
  capacity:
    storage: defn(`DASH_VOLUME_SIZE')
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: video-dash
  local:
    path: defn(`DASH_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`DASH_VOLUME_HOST')"
