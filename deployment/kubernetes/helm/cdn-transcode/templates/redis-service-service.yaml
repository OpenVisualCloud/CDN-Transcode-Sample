apiVersion: v1
kind: Service
metadata:
  labels:
    app: redis-service
  name: redis-service
spec:
  ports:
  - name: "6379"
    port: 6379
    targetPort: 6379
  selector:
    app: redis-service
