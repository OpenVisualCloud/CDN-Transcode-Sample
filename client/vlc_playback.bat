rem
rem This is an example to playback 4 channels of video streams with 2x2 layout on Windows using VLC. 
rem It will launch 4 VLC process with each process playing back 1 channel of video stream, while keep 
rem in a well designed layout. The VLC player will have no border, menu bar and tool bar, and also with
rem proper Windows position. In this example it works for 1920x1080 resolution. You can reference this
rem example to design other layout and also for other resolution.
rem 
rem Below is how the windows will look like:
rem
rem   +---------+---------+                                                     
rem   |         |         |                                                     
rem   |         |         |                                                     
rem   +---------+---------+                                                     
rem   |         |         |                                                     
rem   |         |         |                                                     
rem   +---------+---------+                                                     
rem                                                                             

C:
cd "C:\Program Files (x86)\VideoLAN\VLC"

set VM1=192.168.1.107

start vlc http://%VM1%:80/hls/big_buck_bunny_2560x1440/index.m3u8  --no-video-deco --no-embedded-video --video-x=1 --video-y=1    --qt-start-minimized --zoom=0.375 -L
timeout /t 3 /NOBREAK

start vlc http://%VM1%:80/hls/big_buck_bunny_1920x1080/index.m3u8  --no-video-deco --no-embedded-video --video-x=960 --video-y=1    --qt-start-minimized --zoom=0.5 -L
timeout /t 3 /NOBREAK

start vlc http://%VM1%:80/hls/big_buck_bunny_1280x720/index.m3u8  --no-video-deco --no-embedded-video --video-x=1 --video-y=540    --qt-start-minimized --zoom=0.75 -L
timeout /t 3 /NOBREAK

start vlc http://%VM1%:80/hls/big_buck_bunny_854x480/index.m3u8  --no-video-deco --no-embedded-video --video-x=960 --video-y=540    --qt-start-minimized --zoom=1.12 -L
timeout /t 3 /NOBREAK

