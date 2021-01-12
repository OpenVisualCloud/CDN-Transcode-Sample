#!/usr/bin/python3

from messaging import Producer
from os import listdir
import time
import json

KAFKA_TOPIC = "content_provider_sched"
ARCHIVE_ROOT = "/var/www/archive"

config_file="/home/transcoding.json"

streams = [s for s in listdir(ARCHIVE_ROOT) if s.endswith((".mp4", ".avi"))]

info={}
with open(config_file,"rt") as fd:
    info=json.load(fd)

producer = Producer()
for idx,stream in enumerate(info["vods"]):
    # schedule producing the stream
    if stream["name"] in streams:
        msg=stream
        msg.update({"idx": idx})
        print("start VOD transccoding on {} with {}: ".format(stream["name"],stream["type"]), flush=True)
        print(msg,flush=True)

        while True:
            try:
                producer.send(KAFKA_TOPIC, json.dumps(msg))
                break
            except Exception as e:
                print("Exception: {}".format(e))
                time.sleep(5)
