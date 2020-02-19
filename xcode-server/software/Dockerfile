FROM openvisualcloud/xeon-ubuntu1804-media-ffmpeg:20.2

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-tornado python3-bs4 python3-pip && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'

# Install
COPY *.ini /home/
COPY *.py  /home/

CMD    ["/bin/bash","-c","/home/main.py"]
WORKDIR /home
