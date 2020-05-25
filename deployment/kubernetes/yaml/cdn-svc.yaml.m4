apiVersion: v1
kind: Service
metadata:
  name: cdn-service
  labels:
    app: cdn
spec:
  ports:
  - port: 443
    targetPort: 8443
    name: https
  - port: 1935
    protocol: TCP
    name: tcp
  externalIPs:
    - defn(`HOSTIP')
  selector:
    app: cdn
