#!/usr/bin/python3

from os.path import isfile
from subprocess import call
import subprocess
from os import mkdir
from zkstate import ZKState
from messaging import Consumer
from abr_hls_dash import GetABRCommand,GetLiveCommand
import traceback
import time
import json
import re
from datetime import datetime, timedelta
import random

KAFKA_TOPIC = "content_provider_sched"
KAFKA_GROUP = "content_provider_dash_hls_creator"

ARCHIVE_ROOT = "/var/www/archive"
DASH_ROOT = "/var/www/video/dash"
HLS_ROOT = "/var/www/video/hls"

fps_regex = re.compile(
            r"\s*frame=\s*(?P<frame_count>\d+)\s*fps=\s*(?P<fps>\d+\.?\d*).*"
            r"time=(?P<duration>\d+:\d+:\d+\.\d+).*speed=\s*(?P<speed>\d+\.\d+)x")

def get_fps(next_line,start_time):
    matched = fps_regex.match(next_line)
    if (matched):
        fps = float(matched.group('fps'))
        speed = float(matched.group("speed"))
        frame_count = int(matched.group("frame_count"))
        time_value = datetime.strptime(
            matched.group("duration"), "%H:%M:%S.%f")
        duration = timedelta(
            hours=time_value.hour,
            minutes=time_value.minute,
            seconds=time_value.second,
            microseconds=time_value.microsecond)
        if fps < 0:
            fps = (frame_count / (duration.total_seconds())) * speed
        now=time.time()
        return {"fps":fps, "speed":speed, "frames":frame_count, "start":start_time, "duration":now-start_time,"end":now}
    return {}

def execute(name, cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    p.poll()
    start_time=time.time()
    sinfo={"id": int(random.random()*10000), "stream":name}
    while p.returncode is None:
        next_line = p.stderr.readline()
        r=get_fps(next_line,start_time)
        if r:
            sinfo.update(r)
            print(sinfo, flush=True)
        p.poll()
    return p.returncode

def process_stream_vods(msg):
    stream_name=msg["name"]
    stream_type=msg["type"]
    stream_parameters=msg["parameters"]
    loop= msg["loop"]
    stream=stream_type+"/"+stream_name

    print("VOD transcode:",stream , flush=True)
    if not isfile(ARCHIVE_ROOT+"/"+stream_name):
        return

    zk = ZKState("/content_provider_transcoder/"+ARCHIVE_ROOT+"/vods/"+stream)
    if zk.processed():
        zk.close()
        return

    target_root=HLS_ROOT
    if stream_type=="dash":
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
            r = execute(stream_name, cmd)
            if r:
                raise Exception("status code: "+str(r))
            zk.process_end()
        except:
            print(traceback.format_exc(), flush=True)
            zk.process_abort()

    zk.close()

def process_stream_lives(msg):
    stream_name=msg["name"]
    stream_type=msg["type"]
    codec_type=msg["codec"]
    stream_parameters=msg["parameters"]
    target=msg["target"]
    loop= msg["loop"]
    idx=msg["idx"]
    stream=stream_type+"/"+stream_name

    if not isfile(ARCHIVE_ROOT+"/"+stream_name):
        return

    target_rtmp=target+stream_type +"/media_" + str(idx)+"_"
    print("LIVE transcode:",target_rtmp , flush=True)
    zk = ZKState("/content_provider_transcoder/"+ARCHIVE_ROOT+"/lives/"+stream)
    if zk.processed():
        zk.close()
        return

    if zk.process_start():
        try:
            if stream_parameters:
                cmd = GetLiveCommand(ARCHIVE_ROOT+"/"+stream_name, target_rtmp, codec_type,renditions=stream_parameters,loop=loop)
            else:
                cmd = GetLiveCommand(ARCHIVE_ROOT+"/"+stream_name, target_rtmp, codec_type,loop=loop)
            print(cmd, flush=True)
            r = execute(stream_name, cmd)
            if r:
                raise Exception("status code: "+str(r))
            zk.process_end()
        except:
            print(traceback.format_exc(), flush=True)
            zk.process_abort()

    zk.close()

def process_stream(msg):
    if msg["target"] == "file":
        process_stream_vods(msg)
    else:
        process_stream_lives(msg)

if __name__ == "__main__":
    c = Consumer(KAFKA_GROUP)
    while True:
        try:
            for message in c.messages(KAFKA_TOPIC):
                process_stream(json.loads(message))
        except:
            print(traceback.format_exc(), flush=True)
            time.sleep(2)
    c.close()
