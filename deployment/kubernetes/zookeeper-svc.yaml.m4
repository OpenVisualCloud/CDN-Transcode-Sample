apiVersion: v1
kind: Service
metadata:
  name: zookeeper-service
  labels:
    app: zookeeper
spec:
  ports:
  - port: 2181
    protocol: TCP
  selector:
    app: zookeeper
