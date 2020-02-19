#!/usr/bin/python3

from subprocess import call
from os import mkdir
from os import listdir
from urllib.request import urlopen
import configparser
import time
from bs4 import BeautifulSoup
from zkstate import ZKState
from messaging import Consumer
from abr_hls_dash import GetABRCommand

KAFKA_TOPIC = "content_provider_sched"
KAFKA_GROUP = "content_provider_dash_hls_creator"

DASH_ROOT = "/var/www/dash"
HLS_ROOT = "/var/www/hls"

def process_stream(stream):
    streams = []
    stream_name = stream.split("/")[1]
    config = configparser.ConfigParser()
    config.read('config.ini')
    src_mode = config.get('mode', 'srcMode')
    src_path = config.get('path', 'srcPath')
    src_protocol = ""
    src_api = ""
    if src_mode == "local":
        streams = listdir(src_path)
    elif src_mode == "live":
        html = urlopen("http://"+src_path)
        soup = BeautifulSoup(html, 'html.parser')
        src_protocol = "rtmp://"
        src_api = src_mode
        for item in soup.findAll('a')[1:]:
            streams.append(item.get('href'))
    else:
        return

    if stream_name not in streams:
        return

    if src_mode == "live":
        stream_name = stream_name[:stream_name.index('.')]

    zk = ZKState(src_protocol+src_path+"/"+src_api+"/"+stream.replace("/", "_"))
    if zk.processed():
        zk.close()
        return

    if stream.endswith(".mpd"):
        try:
            mkdir(DASH_ROOT+"/"+stream_name)
        except Exception as e:
            print(str(e))

        if zk.process_start():
            try:
                cmd = GetABRCommand(src_protocol+src_path+"/"+src_api+"/"+stream_name,
                                    DASH_ROOT+"/"+stream_name, "dash")
                r = call(cmd)
                if r:
                    raise Exception("status code: "+str(r))
                zk.process_end()
            except Exception as e:
                print(str(e))
                zk.process_abort()
    if stream.endswith(".m3u8"):
        try:
            mkdir(HLS_ROOT+"/"+stream_name)
        except Exception as e:
            print(str(e))

        if zk.process_start():
            try:
                cmd = GetABRCommand(src_protocol+src_path+"/"+src_api+"/"+stream_name,
                                    HLS_ROOT+"/"+stream_name, "hls")
                r = call(cmd)
                if r:
                    raise Exception("status code: "+str(r))
                zk.process_end()
            except Exception as e:
                print(str(e))
                zk.process_abort()

    zk.close()

if __name__ == "__main__":
    c = Consumer(KAFKA_GROUP)
    while True:
        try:
            for message in c.messages(KAFKA_TOPIC):
                process_stream(message)
        except Exception as e:
            print(str(e))
        time.sleep(2)
