#!/usr/bin/python3

from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from playlist import PlayListHandler
from schedule import ScheduleHandler

APP = web.Application([
    (r'/playlist', PlayListHandler),
    (r'/schedule/.*', ScheduleHandler),
])

if __name__ == "__main__":
    define("port", default=2222, help="the binding port", type=int)
    define("ip", default="127.0.0.1", help="the binding ip")
    parse_command_line()
    print("Listening to " + options.ip + ":" + str(options.port))
    APP.listen(options.port, address=options.ip)
    ioloop.IOLoop.instance().start()
