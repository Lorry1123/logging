# coding: utf8

import sys
from exceptions import Exception

class Logger():
    def __init__(self, name):
        self.name = name
        self.handlers = []

    def log(self, msg):
        if not len(self.handlers):
            raise Exception('No handlers could be found for logger "%s"' % self.name)

        for handler in self.handlers:
            handler.emit(msg)

    def addHandler(self, handler):
        if not isinstance(handler, BaseHandler):
            raise Exception('addHandler only receive a instance of BaseHandler')

        self.handlers.append(handler)


class BaseHandler():
    def __init__(self):
        pass

    def emit(msg):
        pass


class MyStreamHandler(BaseHandler):
    def __init__(self):
        BaseHandler.__init__(self)
        self.stream = sys.stdout

    def emit(self, msg):
        self.stream.write('%s\n' % msg)


# test code

logger = Logger('my_logger')
logger.addHandler(MyStreamHandler())
logger.log('hello world')

