#!/usr/bin/python3

from os.path import isfile
from messaging import Producer
import time
from os import listdir
import json

KAFKA_TOPIC = "content_provider_sched"
DASHLS_ROOT = "/var/www"
ARCHIVE_ROOT = "/var/www/archive"

config_file="/home/transcoding.json"

streams = [s for s in listdir(ARCHIVE_ROOT) if s.endswith((".mp4", ".avi"))]

info={}
with open(config_file,"rt") as fd:
    info=json.load(fd)

producer = Producer()
for idx,stream in enumerate(info[0]["vods"]):
    # schedule producing the stream
    if stream["name"] in streams:
        msg=stream
        msg.update({"idx": idx})
        print("start VOD transccoding on {} with {}: ".format(stream["name"],stream["type"]), flush=True)
        print(msg,flush=True)
        producer.send(KAFKA_TOPIC, json.dumps(msg))

for idx,stream in enumerate(info[0]["lives"]):
    # schedule producing the stream
    if stream["name"] in streams:
        msg=stream
        msg.update({"idx": idx})
        print("start LIVE transccoding on {} with {}: ".format(stream["name"],stream["type"]), flush=True)
        print(msg,flush=True)
        producer.send(KAFKA_TOPIC, json.dumps(msg))

producer.close()

while True:
    print("Running...",flush=True)
    time.sleep(30)

