#!/usr/bin/python3

from os.path import isfile
from subprocess import call
from os import mkdir
from zkstate import ZKState
from messaging import Consumer
from abr_hls_dash import GetABRCommand
import traceback
import time
import json

KAFKA_TOPIC_VODS = "content_provider_sched_vods"
KAFKA_GROUP = "content_provider_dash_hls_creator"

ARCHIVE_ROOT = "/var/www/archive"
DASH_ROOT = "/var/www/video/dash"
HLS_ROOT = "/var/www/video/hls"

def process_stream(msg):
    stream_name=msg["name"]
    stream_type=msg["type"]
    stream_parameters=msg["parameters"]
    loop= msg["loop"]
    stream=stream_type+"/"+stream_name

    if not isfile(ARCHIVE_ROOT+"/"+stream_name):
        return

    zk = ZKState("/content_provider_transcoder/"+ARCHIVE_ROOT+"/"+stream)
    if zk.processed():
        zk.close()
        return

    target_root=HLS_ROOT
    if stream_type=="DASH":
        target_root=DASH_ROOT

    try:
        mkdir(target_root+"/"+stream_name)
    except:
        pass

    if zk.process_start():
        try:
            if stream_parameters:
                cmd = GetABRCommand(ARCHIVE_ROOT+"/"+stream_name, target_root+"/"+stream_name, stream_type,renditions=stream_parameters,loop=loop)
            else:
                cmd = GetABRCommand(ARCHIVE_ROOT+"/"+stream_name, target_root+"/"+stream_name, stream_type,loop=loop)
            print(cmd, flush=True)
            r = call(cmd)
            if r:
                raise Exception("status code: "+str(r))
            zk.process_end()
        except:
            print(traceback.format_exc(), flush=True)
            zk.process_abort()

    zk.close()

if __name__ == "__main__":
    c = Consumer(KAFKA_GROUP)
    while True:
        try:
            for message in c.messages(KAFKA_TOPIC_VODS):
                process_stream(json.loads(message))
        except:
            print(traceback.format_exc(), flush=True)
            time.sleep(2)
    c.close()
