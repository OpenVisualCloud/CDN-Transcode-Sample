#!/usr/bin/python3


from os import listdir
from urllib.request import urlopen
import configparser
import json
from bs4 import BeautifulSoup
from tornado import web, gen

class PlayListHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(PlayListHandler, self).__init__(app, request, **kwargs)
        self._cache = {}

    @gen.coroutine
    def get(self):
        try:
            streams = []
            config = configparser.ConfigParser()
            config.read('config.ini')
            src_mode = config.get('mode', 'srcMode')
            src_path = config.get('path', 'srcPath')
            if src_mode == "local":
                streams = [s for s in listdir(src_path) if s.endswith((".mp4", ".avi"))]
            else:
                html = urlopen("http://"+src_path)
                soup = BeautifulSoup(html, 'html.parser')
                for item in soup.findAll('a')[1:]:
                    if item.get('href').endswith((".mp4", ".avi")):
                        streams.append(item.get('href'))
        except:
            self.set_status(404, "VIDEO NOT FOUND")
            return

        self.set_status(200, "OK")
        self.set_header("Content-Type", "application/json")
        types = [("hls", ".m3u8"), ("dash", ".mpd")]
        self.write(json.dumps([{"name":t[0]+"-"+s, "url":t[0]+"/"+s+"/index"+t[1],
                                "img":"thumbnail/"+s+".png"} for t in types for s in streams]))
