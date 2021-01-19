#!/usr/bin/python3

from messaging import Producer, Consumer
from os import listdir, walk
from os.path import getsize
import time
import json
import psutil
import re

KAFKA_TOPIC = "content_provider_sched"
KAFKA_WORKLOAD_TOPIC = "transcoding"

ARCHIVE_ROOT = "/var/www/archive"
TARGET_ROOT = "/var/www/video"
log_file = TARGET_ROOT+"/log.txt"

config_file="/home/transcoding.json"

streams = [s for s in listdir(ARCHIVE_ROOT) if s.endswith((".mp4", ".avi"))]

jobs=[]
with open(config_file,"rt") as fd:
    jobs=json.load(fd)

print("Submit jobs:", flush=True)
# ingest jobs to start transcoding
producer = Producer()
idx=0
for idx1,msg in enumerate(jobs):
    # schedule producing the stream
    name_pattern=msg["name"]
    for stream1 in streams:
        print("name_pattern={}".format(name_pattern), flush=True)
        print("stream1={}".format(stream1), flush=True)
        if re.match(name_pattern, stream1):
            msg.update({"idx": idx, "name": stream1})
            print(msg,flush=True)
            idx=idx+1

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

c = Consumer(None)

info={"summary":{"cpu": round(psutil.cpu_percent(),2), "mem": round(int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total), 2), "active": 0, "completed":0}}

def process_message(msg,sinfo):
    msg=json.loads(message)
    sinfo.update({msg["id"]:msg})
    active=[ item["id"] for k,item in sinfo.items() if "status" in item.keys() and item["status"] == "active"]
    complete=[ item["id"] for k,item in sinfo.items() if "status" in item.keys() and item["status"] == "completed"]
    sinfo.update({"summary":{"cpu": round(psutil.cpu_percent(),2), "mem": round(int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total), 2), "active": len(active), "completed":len(complete)}})

def format_info(sinfo):
    print("\n", flush=True)
    with open(log_file, "w") as f:
        for k,v in sinfo.items():
            print(k,v, flush=True)
            f.write(str(k)+": "+json.dumps(v))
            f.write("\n")

while True:
    try:
        for message in c.messages(KAFKA_WORKLOAD_TOPIC):
            process_message(message,info)
            format_info(info)
    except Exception as e:
        print("Exception: {}".format(e))
        time.sleep(2)
