
FROM openvisualcloud/xeon-ubuntu1804-media-nginx:20.3.1

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends vim && \
    rm -rf /var/lib/apt/lists/*

COPY *.conf /etc/nginx/
CMD  ["/bin/bash","-c","/usr/sbin/nginx"]
WORKDIR /home
EXPOSE 80 1935
