
FROM openvisualcloud/xeon-ubuntu1804-media-nginx:20.3.1

Run DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-setuptools python3-redis python-celery-common python3-tornado python3-kafka python3-kazoo vim openssh-server && rm -rf /var/lib/apt/lists/*

COPY *.xsl  /etc/nginx/
COPY *.conf /etc/nginx/
COPY *.py   /home/
CMD  ["/bin/bash","-c","/home/main.py&/usr/local/sbin/nginx"]
WORKDIR /home
EXPOSE 8080
