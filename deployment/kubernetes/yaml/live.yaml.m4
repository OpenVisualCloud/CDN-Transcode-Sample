include(../../../script/loop.m4)
include(configure.m4)
include(platform.m4)

loopifdef(LIDX,0,``LIVE_'defn(`LIDX')_CPU',`

apiVersion: apps/v1
kind: Deployment
metadata:
  name: live-defn(`LIDX')
  labels:
    app: live-defn(`LIDX')
spec:
  replicas: ifelse(defn(`SCENARIO'),`cdn',eval(defn(`LIDX')<defn(`NLIVES')),0)
  selector:
    matchLabels:
      app: live-defn(`LIDX')
  template:
    metadata:
      labels:
        app: live-defn(`LIDX')
    spec:
      enableServiceLinks: false
      containers:
        - name: live-defn(`LIDX')
          image: defn(`REGISTRY_PREFIX')tc_transcode_xeon:latest
          imagePullPolicy: IfNotPresent
          resources:
            limits:
              cpu: eval(defn(`LIVE_'defn(`LIDX')_CPU)*2)
              memory: eval(defn(`LIVE_'defn(`LIDX')_MEMORY)*2)Mi
            requests:
              cpu: defn(`LIVE_'defn(`LIDX')_CPU)
              memory: defn(`LIVE_'defn(`LIDX')_MEMORY)Mi
          env:
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /var/www/archive
              name: video-archive
              readOnly: true
          command: [
            "/usr/local/bin/ffmpeg","-re","-stream_loop","-1",
            "-i","/var/www/archive/defn(`LIVE_'defn(`LIDX')_URL)",
loopifdef(KIDX,0,``LIVE_'defn(`LIDX')`_'defn(`KIDX')_PROTOCOL',`dnl
            "-vf", "scale=defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_WIDTH):defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_HEIGHT)",
            "-c:v", "defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_ENCODETYPE)",
            "-b:v", "defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_BITRATE)",
            "-r", "defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_FRAMERATE)",
            "-g", "defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_GOP)",
            "-bf", "defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_MAXBFRAMES)",
            "-refs", "defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_REFSNUM)",
            "-preset", "defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_PRESET)",
            "-forced-idr", "1",
            "-an", 
            "-f", "flv", "`rtmp://cdn-service/'defn(`LIVE_'defn(`LIDX')`_'defn(`KIDX')_PROTOCOL)`/media_'defn(`LIDX')`_'defn(`KIDX')",
')dnl
            ]
      volumes:
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---
')
