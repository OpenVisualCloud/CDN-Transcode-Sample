apiVersion: v1
kind: Service
metadata:
  labels:
    app: zookeeper-service
  name: zookeeper-service
spec:
  ports:
  - name: "2181"
    port: 2181
    targetPort: 2181
  selector:
    app: zookeeper-service
  type: NodePort
