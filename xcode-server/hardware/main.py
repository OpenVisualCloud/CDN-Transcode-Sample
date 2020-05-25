#!/usr/bin/python3

from os.path import isfile
from subprocess import call
from os import mkdir
from zkstate import ZKState
from messaging import Consumer
from abr_hls_dash import GetABRCommand
import traceback
import time

KAFKA_TOPIC = "content_provider_sched"
KAFKA_GROUP = "content_provider_dash_hls_creator"

ARCHIVE_ROOT = "/var/www/archive"
DASH_ROOT = "/var/www/video/dash"
HLS_ROOT = "/var/www/video/hls"

def process_stream(stream):
    stream_name = stream.split("/")[1]

    if not isfile(ARCHIVE_ROOT+"/"+stream_name):
        return

    zk = ZKState("/content_provider_transcoder/"+ARCHIVE_ROOT+"/"+stream)
    if zk.processed():
        zk.close()
        return

    if stream.endswith(".mpd"):
        try:
            mkdir(DASH_ROOT+"/"+stream_name)
        except:
            pass

        if zk.process_start():
            try:
                cmd = GetABRCommand(ARCHIVE_ROOT+"/"+stream_name, DASH_ROOT+"/"+stream_name, "dash")
                r = call(cmd)
                if r:
                    raise Exception("status code: "+str(r))
                zk.process_end()
            except:
                print(traceback.format_exc(), flush=True)
                zk.process_abort()

    if stream.endswith(".m3u8"):
        try:
            mkdir(HLS_ROOT+"/"+stream_name)
        except:
            pass

        if zk.process_start():
            try:
                cmd = GetABRCommand(ARCHIVE_ROOT+"/"+stream_name, HLS_ROOT+"/"+stream_name, "hls")
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
            for message in c.messages(KAFKA_TOPIC):
                process_stream(message)
        except:
            print(traceback.format_exc(), flush=True)
            time.sleep(2)
    c.close()
