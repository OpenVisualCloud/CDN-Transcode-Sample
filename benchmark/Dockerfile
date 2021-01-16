
FROM tc_common

Run apt-get update -q && apt-get install -y -q python3-kafka python3-kazoo && rm -rf /var/lib/apt/lists/*

COPY *.py   /home/
COPY *.json   /home/
CMD  ["/bin/bash","-c","/home/main.py"]
WORKDIR /home

####
ARG  UID
RUN  mkdir -p /var/www/archive
USER ${UID}
####
