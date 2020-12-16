#!/usr/bin/python3

from os.path import isfile
from tornado import web, gen
from messaging import Producer
import time
import json

KAFKA_TOPIC_VODS = "content_provider_sched_vods"
DASHLS_ROOT = "/var/www"

class ScheduleHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        stream = self.requeist.uri.replace("/schedule/", "")

        # schedule producing the stream
        print("request received to process stream: "+stream, flush=True)
        producer = Producer()
        msg.update({
            "name":stream.split("/")[1],
            "type":stream.split("/")[0],
            "parameters": [ ],
            "codec": "AVC",
            "loop": 0,
            "target": "file",
            "platform": "software"
            })
        producer.send(KAFKA_TOPIC_VODS, msg)
        producer.close()

        # wait until file is available, return it
        start_time = time.time()
        while time.time() - start_time < 60:
            if isfile(DASHLS_ROOT+"/"+stream):
                self.set_header('X-Accel-Redirect', '/'+stream)
                self.set_status(200, "OK")
                return
            yield gen.sleep(0.5)

        # wait too long, skip this REST API
        self.set_status(503, "Request scheduled")
