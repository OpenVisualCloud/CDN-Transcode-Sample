#!/usr/bin/python3

from tornado.options import define, options, parse_command_line

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.autoreload

import os,setting
import configparser


from views.schedule import ScheduleHandler
from views.user import UploadHandler
from views.comment import CommentHandler
from views.user import AuthcodeHandler,  UserInfoHandler
from views.video import PlaylistHandler, VideoHandler

config = configparser.ConfigParser()
config.read('config.ini')
tempPath = config.get('path', 'tempPath')
srcPath = config.get('path', 'srcPath')


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/video/list/(?P<num>\d*)",PlaylistHandler),
        (r"/video/play/",VideoHandler),
        (r"/comment/",CommentHandler),
        (r"/user/sign_up/auth_code/",AuthcodeHandler),
        (r"/user/upload/",UploadHandler),
        (r"/user/info/",UserInfoHandler),
        (r'/schedule/.*', ScheduleHandler),
        ],
        **setting.set,
    )

    os.popen('celery multi start w1 -A tasks -l info --logfile=/var/www/log/celery.log --pidfile=/var/www/log/celery.pid')
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(2222)
    tornado.ioloop.IOLoop.current().start()
