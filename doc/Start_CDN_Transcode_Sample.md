# Start CDN Transcode Sample
user@server:/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes# ./start.sh
service "kafka-service" deleted
service "zookeeper-service" deleted
service "cdn-service" deleted
service "redis-service" deleted
deployment.extensions "redis-service" deleted
deployment.extensions "zookeeper-service" deleted
deployment.extensions "cdn-service" deleted
deployment.extensions "kafka-service" deleted
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/cdn-service-service.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/kafka-service-service.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/redis-service-service.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/zookeeper-service-service.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/cdn-service-deployment.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/kafka-service-deployment.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/live-service-deployment.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/redis-service-deployment.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/vod-service-deployment.yaml" created
INFO Kubernetes file "/home/media/workroom/CDN-Transcode-Sample/deployment/kubernetes/zookeeper-service-deployment.yaml" created
There are 2 kubernetes nodes on your host server!!!
Please input where the video clips server is ([NFS server IP address]): 10.67.119.111
There are 2 kubernetes nodes on your host server!!!
Please input where the video clips server is ([NFS server IP address]): 10.67.119.111
Please input CDN-Transcode-Sample volume directory path on NFS server: /home/media/workroom/CDN-Transcode-Sample/
Please input NFS server username: media
[10.67.119.111] Login password for 'media':
Do you need to deploy the vod transcode service? ([y] or [n]): n
Do you need to deploy the live transcode service? ([y] or [n]): y
Please choose the transcode mode of the 0thlive ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5): sw
Do you need to deploy live-transcode-service by customizing parameters([y] or [n]): y
Please choose the output channel (1, 2 ,3, 4): 1
Please choose the 1th output encoder ('AVC', 'HEVC', 'AV1'): avc
Please choose the 1th output resolution (a: hd480, b: hd720, c: hd1080, d: 2kqhd): d
Please enter the 1th output bitrate([1-20]Mbps): 5
Please choose the 1th output streaming media communication protocol(a: HLS, b: DASH): a
Please enter the 1th output video clip name: meida
Do you still need to deploy the 2th live? ([y] or [n]): n
Please input run cdn node name ('media-server-e5-maowenquan-1', 'media-server-zhangchuang-2'): media-server-e5-maowenquan-1
Please input run cdn request cpu core number: 0.2
Please input run cdn request memory quota(MiB): 500
Please input run redis node name ('media-server-e5-maowenquan-1', 'media-server-zhangchuang-2'): media-server-e5-maowenquan-1
Please input run redis request cpu core number: 0.2
Please input run redis request memory quota(MiB): 500
Please input run zookeeper node name ('media-server-e5-maowenquan-1', 'media-server-zhangchuang-2'): media-server-e5-maowenquan-1
Please input run zookeeper request cpu core number: 0.2
Please input run zookeeper request memory quota(MiB): 500
Please input run kafka node name ('media-server-e5-maowenquan-1', 'media-server-zhangchuang-2'): media-server-e5-maowenquan-1
Please input run kafka request cpu core number: 0.2
Please input run kafka request memory quota(MiB): 500
Please input run live0 node name ('media-server-e5-maowenquan-1', 'media-server-zhangchuang-2'): media-server-zhangchuang-2
Please input run live0 request cpu core number: 4
Please input run live0 request memory quota(MiB): 2000

The live video playlist URL are below:
https://10.67.119.111/hls/meida_0_0/index.m3u8
secret/ovc-ssl-certificates configured
deployment.extensions/redis-service created
service/kafka-service created
deployment.extensions/live0-service configured
secret/ovc-ssl-certificates configured
service/zookeeper-service created
service/cdn-service created
service/redis-service created
deployment.extensions/zookeeper-service created
deployment.extensions/cdn-service created
deployment.extensions/kafka-service created

