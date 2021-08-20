#!/usr/bin/python3

from os.path import isfile
from subprocess import call
import subprocess
from os import makedirs 
from zkstate import ZKState
from messaging import Consumer, Producer
from ffmpegcmd import FFMpegCmd
import traceback
import time
import json
import re
from datetime import datetime, timedelta
import random
import psutil
import os

KAFKA_TOPIC = "content_provider_sched"
KAFKA_GROUP = "content_provider_dash_hls_creator"
KAFKA_WORKLOAD_TOPIC = "transcoding"

ARCHIVE_ROOT = "/var/www/archive"
VIDEO_ROOT = "/var/www/video/"
DASH_ROOT = "/var/www/video/dash"
HLS_ROOT = "/var/www/video/hls"
MP4_ROOT = "/var/www/video/mp4"
CACHE_RAW_YUV_ROOT = "/var/www/video/rawyuv"
CACHE_DECODED_YUV_ROOT = "/var/www/video/decodedyuv"

HW_ACC_TYPE=os.getenv("HW_ACC_TYPE","sw")
HW_DEVICE=os.getenv("HW_DEVICE",None)
SCENARIO=os.getenv("SCENARIO","transcode")

fps_regex = re.compile(
            r"\s*frame=\s*(?P<frame_count>\d+)\s*fps=\s*(?P<fps>\d+\.?\d*).*"
            r"time=(?P<duration>\d+:\d+:\d+\.\d+).*speed=\s*(?P<speed>\d+\.\d+)x")

producer = Producer()

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
        return {"fps":round(fps,1), "speed":round(speed,3), "frames":frame_count, "start":round(start_time,3), "duration":round(now-start_time,3), "end":round(now,3), "status": "active"}
    return {}

def execute(idx, name, cmd,kafka=True):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    p.poll()
    start_time=time.time()
    sinfo={"id": str(idx), "stream":name}
    p1=psutil.Process(p.pid)
    while p.returncode is None:
        next_line = p.stderr.readline()
        r=get_fps(next_line,start_time)
        if r:
            sinfo.update({"cpu": round(p1.cpu_percent(),2), "mem": round(p1.memory_percent(),2)})
            sinfo.update(r)
            print(sinfo, flush=True)
            try:
                if kafka: producer.send(KAFKA_WORKLOAD_TOPIC, json.dumps(sinfo))
            except Exception as e:
                print("Exception: {}".format(e))
                continue
        p.poll()
    try:
        if p.returncode:
            sinfo.update({"status": "aborted"})
        else:
            sinfo.update({"status": "completed"})
        print(sinfo, flush=True)
        producer.send(KAFKA_WORKLOAD_TOPIC, json.dumps(sinfo))
    except Exception as e:
        print("Exception: {}".format(e))
    return p.returncode

def decode_yuv(yuv_path,in_stream_name,nframes=None):
    try:
        yuv_name=yuv_path+"/"+in_stream_name.split("/")[-1].replace(".mp4",".yuv")
        if not os.path.exists(path): makedirs(yuv_path)
        if os.path.exists(yuv_name): return
        if nframes:
            cmd = ["ffmpeg", "-hide_banner", "-i",in_stream_name, "-vcodec rawvideo", "-an","-frames:v", str(nframes),"-y",yuv_name]
        else:
            cmd = ["ffmpeg", "-hide_banner", "-i",in_stream_name, "-vcodec rawvideo", "-an","-y",yuv_name]
        print(cmd, flush=True)
        execute(5001,"decoded",cmd,kafka=False)
    except Exception as e:
        print("Exception: {}".format(e))
        pass
    return yuv_name

def measure_quality_vmaf(idx,name, raw_mp4_path, target_mp4_path,width,height, nframes=100):
    vmaf_score=None
    model_path="/home/models/"
    try:
        if width >=1920 and height >=1080:
            model_name=model_path+"vmaf_4k_v0.6.1.json"
        else:
            model_name=model_path+"vmaf_v0.6.1.json"
        log_path=target_mp4_path+".json"
        framerate=24
        cmd = ["ffmpeg", "-r", str(framerate), "-i",raw_mp4_path, "-r", str(framerate), "-i", target_mp4_path, "-lavfi", "[0:v]trim=end_frame={},scale={}:{}:flags=bicubic,setpts=PTS-STARTPTS[reference];[1:v]trim=end_frame={},setpts=PTS-STARTPTS[distorted];[distorted][reference]libvmaf=log_fmt=json:log_path={}:model_path={}".format(nframes,width,height,nframes,log_path,model_name),"-f", "null", "-"]
        print(cmd,flush=True)
        execute(str(idx+1000),name,cmd,kafka=False)
        with open(log_path) as f:
            obj = json.load(f)
            sinfo={"id": str(idx+1000), "stream":name}
            vmaf_score=float(obj["pooled_metrics"]["vmaf"]["mean"])
            sinfo.update({"vmaf":vmaf_score})
            producer.send(KAFKA_WORKLOAD_TOPIC, json.dumps(sinfo))

    except Exception as e:
        print("Exception: {}".format(e))
    return vmaf_score

def process_stream_vods(msg):
    stream_name=msg["name"]
    stream_type=msg["output"]["type"]
    stream_parameters=msg["parameters"]
    loop= msg["loop"]
    idx=msg["idx"] if "idx" in msg.keys() else int(random.random()*10000)
    stream=stream_type+"/"+stream_name

    print("VOD transcode:",stream , flush=True)
    if not isfile(ARCHIVE_ROOT+"/"+stream_name):
        return

    zk = ZKState("/content_provider_transcoder/"+ARCHIVE_ROOT+"/vods/"+stream)
    if zk.processed():
        zk.close()
        return

    target_root=VIDEO_ROOT+stream_type

    try:
        makedirs(target_root+"/"+stream_name)
    except:
        pass

    if zk.process_start():
        try:
            input_stream=ARCHIVE_ROOT+"/"+stream_name
            cmd = FFMpegCmd(input_stream, target_root+"/"+stream_name, stream_type, params=stream_parameters, acc_type=HW_ACC_TYPE, loop=loop, device=HW_DEVICE).cmd()
            if cmd:
                print(cmd, flush=True)
                r = execute(idx, stream_name, cmd)
                if r:
                    raise Exception("status code: "+str(r))
                zk.process_end()
        except:
            print(traceback.format_exc(), flush=True)
            zk.process_abort()

    zk.close()

def process_stream_lives(msg):
    stream_name=msg["name"]
    stream_parameters=msg["parameters"]
    codec=stream_parameters["codec_type"]
    stream_type=msg["output"]["type"]
    target=msg["output"]["target"]
    loop= msg["loop"]
    idx=int(msg["idx"]) if "idx" in msg.keys() else int(random.random()*10000)
    stream=stream_type+"/"+stream_name

    if not isfile(ARCHIVE_ROOT+"/"+stream_name):
        return

    target_root=VIDEO_ROOT+stream_type

    try:
        makedirs(target_root+"/"+stream_name)
    except:
        pass

    if target != "file":
        target_name=target+stream_type +"/media_" + str(idx)+"_"
    else:
        target_name=target_root+"/"+stream_name

    print("LIVE transcode:",target_name , stream_type, flush=True)
    zk = ZKState("/content_provider_transcoder/"+ARCHIVE_ROOT+"/lives/"+str(idx)+"/"+stream)
    if zk.processed():
        zk.close()
        return

    if zk.process_start():
        try:
            input_stream = ARCHIVE_ROOT+"/"+stream_name
            cmd = FFMpegCmd(input_stream, target_name, stream_type, params=stream_parameters, acc_type=HW_ACC_TYPE, loop=loop, device=HW_DEVICE).cmd()

            if cmd:
                print(cmd, flush=True)
                r = execute(idx, stream_name, cmd)
                if r:
                    raise Exception("status code: "+str(r))
                if SCENARIO == "transcode-quality":
                    width=stream_parameters["renditions"][0][0]
                    height=stream_parameters["renditions"][0][1]
                    mp4_file=cmd[-1]
                    measure_quality_vmaf(idx,stream_name,raw_mp4_path=input_stream,target_mp4_path=mp4_file,width=width,height=height)
                zk.process_end()
        except:
            print(traceback.format_exc(), flush=True)
            zk.process_abort()

    zk.close()

def process_stream(msg):
    if msg["live_vod"] == "vod":
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
