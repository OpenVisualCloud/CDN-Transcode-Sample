# OVC CDN Transcode E2E Sample Reference Architecture
[TOC]
# Introduction
## Purpose
This document describes the reference architecture (RA) design of the OVC CDN Transcode E2E Sample (abbr as CTES in this document) which can demostrate the media delivery over CDN network capability using Open Visual Cloud software stack.

## Overview
The CTES is not a single sample application, but a reference solution which contains multiple software ingredients, configurations and documentations. The software ingredients includes Intel HW/SW video codec drivers & libraries, industry encoder, somedia framework like FFmpeg, nginx web server, and a setup dockerfile/scripts.

The CTES is part of the Intel OVC project, which has two key characters:
- All the ingredients are open sourced.
- The key components are packed into dockers to provide out-of-box service.

# Architecture
The CTES will mainly two kinds of use cases: live broadcasting (short for live in this document) and VOD (video on demand). The architecture for these two user cases shares some same design and key ingredients, with workflow and and protocals varies. Below section describes the architectures for these two user cases.
                                   
## Live Use Case
For live use case, there are mainly five logic nodes in the solution - the **Streaming Server**, **Transcode Server**, **CDN Edge Server**, **Client System**, and the **CDN Manager**.  The Streaming Server broadcast the encoded source video into the Transcode Server. The Transcode Server receives the video streams, transcode to video streams with different codec/resolution/bitrate, and streams distribute to CDN Edge server by command from CDN manager with different protocols. The CDN Edge server receives streams from Transcode server, and send streams to Client System.

There are 4 typical protocols widely used for stream from Transcode Server to CDN Edge Server, below table briefs the key differences:

| Live Protocol | Streaming Server | Transcode Server | CDN Edge Server | Client |
|:------------- | :--------------- | ---------------- | --------------- | ------ |
| RTMP          | out: rtmp        | in:rtmp out: rtmp| in:rtmp out:rtmp| rtmp   |
| HLS           | out: rtmp        | in:rtmp out: http| in:http out:http| http   |
| DASH          | out: rtmp        | in:rtmp out: http| in:http out:http| http   |
| HTTP-FLV      | out: rtmp        | TBD              | TBD             | http   |

### Live user scenario 1 - RTMP Live
Below is the simple workflow of the RTMP live user scenario:
```
                                                                         
                            +----------------+                           
                            |  CDN Manager   |                           
                            +----------------+                           
                              /           \                              
+------------+      +------------+      +------------+      +----------+ 
|  Streaming | rtmp | Transcode  | rtmp |  CDN Edge  | rtmp |  Client  | 
|  Server    |----->|  Server    |----->|   Server   |----->|  System  | 
+------------+      +------------+      +------------+      +----------+ 
                                                                         
```
In the **Streaming Server** side, a live video stream, either from a camera or HD video file, is pushed into **Transcode Server** over rtmp protocol in flv format. In CTES, FFmpeg is used to provide the RTMP streaming service, which is built into a docker image.

The **Transcode Server** receives the video stream over rtmp, decapsulate and demux the flv video, transcode to other codecs/bitrate/resolution, in 1:N manner, which means one input and N output. E.g.: one channel HEVC 4k@60fps, transcoded into one channle AVC 720p@30fps, one channel HEVC 1080p@30fps and one channel HEVC 4k@60fps. The transcoded video streams are then be encapsulated in flv over rtmp, be distributed to the **CDN Edge Server** over CDN network, accordingly to the decision from **CDN Manager**. FFmpeg is used here as the transcode framework, with plugins to support various decoders and encoders, like SVT, QSV or VAAPI. The **Transcode Server** needs to provide rtmp service as well, in CTES Ngnix and nginx-rtmp module is used for this purpose. To provide out-of-box service, the transcode software ingredients and Nginx as well as configurations are bundled into a docker image as well.

The **CDN Edge** server receives the video streams from **Transcode Server**, cache the streams and push the steams into various clients over rtmp. In real production it may require transcode in edge as well. In CTES, only cache and relay is supported to simply the typical workflow logically. Same as **Transcode** server, Nginux and nginx-rtmp module is needed and built into docker image as well.

The **Client System** supports rtmp playback and AVC/HEVC decode, in CTES FFplay is used.

### Live user scenario 2 - HLS Live
Below is the simple workflow of the HLS live user scenario:
```
                                                                         
                            +----------------+                           
                            |  CDN Manager   |                           
                            +----------------+                           
                              /           \                              
+------------+      +------------+      +------------+      +----------+ 
|  Streaming | rtmp | Transcode  | rtmp |  CDN Edge  | http |  Client  | 
|  Server    |----->|  Server    |----->|   Server   |<-----|  System  | 
+------------+      +------------+      +------------+      +----------+ 
                                                                         
```
For the workflow for HLS Live, the **Streaming Server** and **Transcode Server** is the same as the RTMP Live. The diference is the **CDN Edge Server** side and **Client System** side.

The **CDN Edge Server** receives video streams via rtmp, and will translate the video streams into HLS TS format, split into .ts segmentation, and generate HLS .m3u8 index file. The Nginx is used to provide the http service while nginx-rtmp module is also used, to provide rtmp service and also rtmp->hls translation. Same as above, all of them provided in terms of docker.

The **Client System** supports HLS playback and AVC/HEVC decode, in CTES hls.js is used.

### Live user scenario 3 - DASH Live
Below is the simple workflow of the DASH (short for MPEG-DASH) live user scenario:
```
                                                                         
                            +----------------+                           
                            |  CDN Manager   |                           
                            +----------------+                           
                              /           \                              
+------------+      +------------+      +------------+      +----------+ 
|  Streaming | rtmp | Transcode  | rtmp |  CDN Edge  | http |  Client  | 
|  Server    |----->|  Server    |----->|   Server   |<-----|  System  | 
+------------+      +------------+      +------------+      +----------+ 
                                                                         
```
The workflow for **DASH Live** is very similiar with **HLS Live**, both DASH and HLS are over HTTP, with video stream segmented and playlist index file provided. The key differences is that segmentation and index methodlogy, that means that the configuration in CDN Edge server and the **Client System** play differs.

The **CDN Edge Server** receives video streams via rtmp, and will translate the video streams into mp4 format, split into .mp4 segmentation, and generate DASH .mpd index file. 

The **Client System** supports DASH playback and AVC/HEVC decode, in dash.js is used.

### Live user scenario 4 - HTTP-FLV Live
TODO

## VOD Use Case

For VOD use case, there are mainly five logic nodes in the solution - the **Video Publisher**, **Transcode Server**, **OSS Server**, **CDN Edge Server**, **Client System**, and the **CDN Manager**.  The **Video Publisher** publish the encoded source video into the Transcode Server over http, by web browser or mobile app. The Transcode Server receives the video streams, transcode to video streams with different codec/resolution/bitrate, generate HLS or DASH video segmentation and index file, and save to **OSS Server**. The transcode output video files will then be distributed to **CDN Edge Server** by decision from **CDN manager**. The **CDN Edge Server** receives streams from **Transcode Server**, and send streams to **Client System** per request.

There are 2 typical protocols used for VOD, below table briefs the key differences:

| VOD Protocol  | Video Publisher  | Transcode Server | CDN Edge Server | Client |
|:------------- | :--------------- | ---------------- | --------------- | ------ |
| HLS           | segment: ts      | in:file out: hls | in:hls  out:hls | hls    |
| DASH          | segment: mp4     | in:file out: dash| in:dash out:dash| dash   |

### VOD user scenario 1 - HLS VOD
Below is the simple workflow of the HLS VOD user scenario:
```
                                                                         
                            +----------------+                           
                            |  CDN Manager   |                           
                            +----------------+                           
                              /           \                              
+------------+      +------------+      +------------+      +----------+ 
|  Video     | http | Transcode  | http |  CDN Edge  | http |  Client  | 
|  Publisher |----->|  Server    |<---->|   Server   |<-----|  System  | 
+------------+      +------------+      +------------+      +----------+ 
                          |                                              
                          V                                              
                    +------------+                                       
                    |    OSS     |                                       
                    |   Server   |                                       
                    +------------+                                       
                                                                         
```
In the **Video Publisher** side, the user uploads a HD video file to the **Transcode Server**. In CTES, no special client software but just web browser is used.

The **Transcode Server** receives the video stream over http, transcode to other codecs/bitrate/resolution, in 1:N manner, do segmentation and create index file as playlist. The results will be stored in **OSS Server**, which means Open Storage System, and then be distributed to the **CDN Edge Server** over CDN network, accordingly to the decision from **CDN Manager**. Again, FFmpeg is used here as the transcode framework. The **Transcode Server** needs to provide http service as well, in CTES Ngnix is used for this purpose. Same as above, the transcode software ingredients and Nginx as well as configurations are bundled into a docker image as well.

The **CDN Edge** server receives the video streams from **Transcode Server**, cache the streams and push the steams into various clients over http. In real production it may require transcode in edge as well. In CTES, **CDN Edge** node can also be ommitted so **Client System** requests are sent to **Transcode Server** directly.

The **Client System** supports HLS playback and AVC/HEVC decode, in CTES HLS.js or VLC is used.

### VOD user scenario 2 - DASH VOD
Below is the simple workflow of the DASH VOD user scenario:
```
                                                                         
                            +----------------+                           
                            |  CDN Manager   |                           
                            +----------------+                           
                              /           \                              
+------------+      +------------+      +------------+      +----------+ 
|  Video     | http | Transcode  | http |  CDN Edge  | http |  Client  | 
|  Publisher |----->|  Server    |<---->|   Server   |<-----|  System  | 
+------------+      +------------+      +------------+      +----------+ 
                          |                                              
                          V                                              
                    +------------+                                       
                    |    OSS     |                                       
                    |   Server   |                                       
                    +------------+                                       
                                                                         
```
It's almost the same as HLS VOD scenario with some minor difference: FFmpeg should generate DASH .mp4 segmentations and index file, and the **Client System** supports DASH playback and AVC/HEVC decode, DASH.js will be used.

# Reference Demo
## Hardware Requirement
## Software Ingredients
## Network Configuration
## Video Clips
