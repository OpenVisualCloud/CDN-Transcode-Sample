#!/usr/bin/python3

from os import listdir
import json
from tornado import web, gen

ARCHIVE_ROOT = "/var/www/archive"

class PlayListHandler(web.RequestHandler):
    def __init__(self, app, request, **kwargs):
        super(PlayListHandler, self).__init__(app, request, **kwargs)
        self._cache = {}

    @gen.coroutine
    def get(self):
        try:
            streams = [s for s in listdir(ARCHIVE_ROOT) if s.endswith((".mp4", ".avi"))]
        except:
            self.set_status(404, "VIDEO NOT FOUND")
            return

        self.set_status(200, "OK")
        self.set_header("Content-Type", "application/json")
        types = [("hls", ".m3u8"), ("dash", ".mpd")]
        self.write(json.dumps([{"name":t[0]+"-"+s, "url":t[0]+"/"+s+"/index"+t[1],
                                "img":"thumbnail/"+s+".png"} for t in types for s in streams]))
