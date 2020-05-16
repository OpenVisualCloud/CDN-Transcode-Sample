
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: html
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: html
spec:
  capacity:
    storage: defn(`HTML_VOLUME_SIZE')
  accessModes:
  - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: html
  local:
    path: defn(`HTML_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`HTML_VOLUME_HOST')"
