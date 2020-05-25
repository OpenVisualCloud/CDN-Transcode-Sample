apiVersion: v1
kind: Service
metadata:
  name: kafka-service
  labels:
    app: kafka
spec:
  ports:
  - port: 9092
    protocol: TCP
  selector:
    app: kafka
