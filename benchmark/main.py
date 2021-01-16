#!/usr/bin/python3

from messaging import Producer
from os import listdir, walk
from os.path import getsize
import time
import json

KAFKA_TOPIC = "content_provider_sched"
ARCHIVE_ROOT = "/var/www/archive"
TARGET_ROOT = "/var/www/video"

config_file="/home/transcoding.json"

streams = [s for s in listdir(ARCHIVE_ROOT) if s.endswith((".mp4", ".avi"))]

jobs=[]
with open(config_file,"rt") as fd:
    jobs=json.load(fd)

print("Submit jobs:", flush=True)
# ingest jobs to start transcoding
producer = Producer()
for idx,msg in enumerate(jobs):
    # schedule producing the stream
    if msg["target"] == "file":
        if msg["name"] not in streams:
            continue
    msg.update({"idx": idx})
    print(msg,flush=True)

    while True:
        try:
            producer.send(KAFKA_TOPIC, json.dumps(msg))
            break
        except Exception as e:
            print("Exception: {}".format(e))
            time.sleep(5)

# show transcoding statistics

def stats_fileinfo(root):
    nfiles=0
    size=0
    for path, dirs, files in walk(root):
        for stream1 in files:
            if stream1.endswith((".mp4", ".avi", ".ts")):
                nfiles=nfiles+1
                size=size+getsize(path+"/"+stream1)
    return (nfiles, size)

srcinfo=stats_fileinfo(ARCHIVE_ROOT) 
print(srcinfo)
dstinfo=(0,0)
start=time.time()
while True:
    dstinfo1=stats_fileinfo(TARGET_ROOT)
    if dstinfo1[0]==dstinfo[0] and dstinfo1[1]==dstinfo[1]:
        time.sleep(1) 
        continue

    now=time.time()
    delta=now-start

    print("src: {} media files, size {} bytes".format(srcinfo[0], srcinfo[1]), flush=True)
    if delta>0:
        print("dst: {} media files, size {} bytes, throughput {:.2f} MB/s".format(dstinfo1[0], dstinfo1[1], dstinfo1[1]/delta/1024/1024), flush=True)

    dstinfo=dstinfo1
    time.sleep(1) 
