
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  labels:
    app: redis
spec:
  ports:
  - port: 6379
    protocol: TCP
  selector:
    app: redis
