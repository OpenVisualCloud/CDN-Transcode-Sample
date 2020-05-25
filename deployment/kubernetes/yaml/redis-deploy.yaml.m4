include(platform.m4)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  labels:
     app: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:latest
          imagePullPolicy: IfNotPresent
          command:
            - redis-server 
          ports:
            - containerPort: 6379
          resources:
              requests:
                  cpu: 1
                  memory: 500Mi  
              limits:
                  cpu: 2
                  memory: 1000Mi
PLATFORM_NODE_SELECTOR(`Xeon')dnl
