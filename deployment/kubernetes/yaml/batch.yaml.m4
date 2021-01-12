include(platform.m4)

apiVersion: batch/v1
kind: Job
metadata:
  name: batch
spec:
  template:
    spec:
      enableServiceLinks: false
      containers:
        - name: batch
          image: defn(`REGISTRY_PREFIX')tc_batch_service:latest
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
      volumes:
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
      restartPolicy: Never
PLATFORM_NODE_SELECTOR(`Xeon')dnl
