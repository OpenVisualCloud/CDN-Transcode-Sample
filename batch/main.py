#!/usr/bin/python3

from os.path import isfile
from messaging import Producer
import time
from os import listdir
import json

KAFKA_TOPIC_VODS = "content_provider_sched_vods"
KAFKA_TOPIC_LIVES = "content_provider_sched_lives"
DASHLS_ROOT = "/var/www"
ARCHIVE_ROOT = "/var/www/archive"

config_file="/home/transcoding.json"

streams = [s for s in listdir(ARCHIVE_ROOT) if s.endswith((".mp4", ".avi"))]

info={}
with open(config_file,"rt") as fd:
    info=json.load(fd)

print(info,flush=True)

producer = Producer()
for stream in info[0]["vods"]:
    # schedule producing the stream
    if stream["name"] in streams:
        msg=stream
        print("start VOD transccoding on {} with {}: ".format(stream["name"],stream["type"]), flush=True)
        print(msg,flush=True)
        producer.send(KAFKA_TOPIC_VODS, json.dumps(msg))
        # wait until file is available, return it
        start_time = time.time()
        while time.time() - start_time < 60:
            if isfile(DASHLS_ROOT+"/"+stream["name"]): break 
            time.sleep(1)

producer.close()

while True:
    print("Running...",flush=True)
    time.sleep(30)

