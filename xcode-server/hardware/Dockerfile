
FROM openvisualcloud/xeone3-ubuntu1804-media-ffmpeg:20.3.1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-tornado python3-kafka python3-kazoo vim && rm -rf /var/lib/apt/lists/*

COPY *.py  /home/

CMD    ["/bin/bash","-c","/home/main.py"]
WORKDIR /home
