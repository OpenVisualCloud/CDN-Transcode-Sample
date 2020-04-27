apiVersion: v1
kind: Service
metadata:
  labels:
    app: cdn-service
  name: cdn-service
spec:
  ports:
  - name: "8080"
    port: 8080
    targetPort: 8080
  - name: "1935"
    port: 1935
    targetPort: 1935
  selector:
    app: cdn-service
  type: NodePort
