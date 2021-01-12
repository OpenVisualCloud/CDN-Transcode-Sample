# tc_transcode_xeone3

FROM openvisualcloud/xeone3-ubuntu1804-media-ffmpeg:20.7

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-tornado python3-kafka python3-kazoo && rm -rf /var/lib/apt/lists/*

COPY --from=tc_common /home/ /home/
COPY *.py  /home/
CMD    ["/home/main.py"]
WORKDIR /home

####
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} docker; \
     [ ${UID} -gt 0 ] && useradd -d /home/docker -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} docker; \
     chown -R ${UID}:${GID} /home
USER ${UID}
####