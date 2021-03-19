
FROM openvisualcloud/xeon-ubuntu1804-media-nginx:21.3
COPY *.conf /etc/nginx/
CMD  ["/usr/sbin/nginx"]
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
