
FROM openvisualcloud/xeon-ubuntu1804-media-nginx:21.3

Run DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-setuptools python3-redis python-celery-common python3-tornado python3-kafka python3-kazoo openssh-server && rm -rf /var/lib/apt/lists/*

COPY *.xsl  /etc/nginx/
COPY *.conf /etc/nginx/
COPY html /var/www/html
COPY *.py   /home/
CMD  ["/bin/bash","-c","/home/main.py&/usr/local/sbin/nginx"]
WORKDIR /home

####
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} docker; \
     [ ${UID} -gt 0 ] && useradd -d /home/docker -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} docker; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/video /var/www/archive && \
     chown -R ${UID}:${GID} /var/run/nginx.pid /var/www /var/log/nginx /var/lib/nginx
USER ${UID}
####
