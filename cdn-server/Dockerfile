
FROM openvisualcloud/xeon-ubuntu1804-media-nginx:20.2

Run DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-setuptools python3-redis python-celery-common python3-tornado python3-pip python3-bs4 vim openssh-server && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'

COPY *.xsl  /etc/nginx/
COPY *.conf /etc/nginx/
COPY *.ini  /home/
COPY *.py   /home/
CMD  ["/bin/bash","-c","/home/main.py&/usr/local/sbin/nginx"]
WORKDIR /home
EXPOSE 8080
