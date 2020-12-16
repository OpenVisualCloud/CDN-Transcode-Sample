
apiVersion: v1
kind: Service
metadata:
  name: cdn-service
  labels:
    app: cdn
spec:
  ports:
ifelse(defn(`SCENARIO'),`cdn',`dnl
  - port: 443
    targetPort: 8443
    name: https
')dnl
  - port: 1935
    targetPort: 1935
    name: rtmp
  externalIPs:
    - defn(`HOSTIP')
  selector:
    app: cdn

