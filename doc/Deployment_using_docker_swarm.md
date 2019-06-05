# Docker swarm/compose Deployment on E5
## Start CDN transcode service
Run below steps on CDN-Transcode server to start/stop docker swarm service.

- Initialize docker swarm if you have not
```bash
sudo docker swarm init
```
- start/stop docker swarm services
```bash
make start_docker_swarm
make stop_docker_swarm
```

Run below steps on CDN-Transcode server to start/stop docker compose service.
- start/stop docker compose services
```bash
make start_docker_compose
make stop_docker_compose
```
## Playback
### Web browser playback
Visit https://\<CDN-Transcode Server IP address\>/ using any web browser, you will see the playlist and then click any of the streams in the playlist to playback.
### VLC playback
You can also use Windows VLC player to playback the HTTPs streams provided by the sample service. A sample [VLC playback script](client/vlc_playback.bat) is provided for this purpose. You may need to change this script to set the IP address and the VLC path in this script.
