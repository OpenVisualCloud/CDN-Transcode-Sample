# Kubernetes Deployment on E5
## Start CDN transcode service
```shell
$ cd build
$ make start_kubernetes
```
## Playback
### Web browser playback
Visit https://<CDN-Transcode Server IP address>:30443/ using any web browser, you will see the playlist and then click any of the streams in the playlist to playback.

### VLC playback
You can also use Windows VLC player to playback the HTTPs streams provided by the sample service. please run below commands.
vlc https://<CDN-Transcode Server IP address>:30443/hls/big_buck_bunny_1280x720/index.m3u8
