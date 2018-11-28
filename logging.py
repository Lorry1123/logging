# coding: utf8

import sys
from exceptions import Exception

class Logger():
    def __init__(self, name):
        self.name = name
        self.handlers = []

    def log(self, msg, *args):
        if not len(self.handlers):
            raise Exception('No handlers could be found for logger "%s"' % self.name)

        for handler in self.handlers:
            record = LogRecord(self.name, 'warning', msg, args)
            handler.emit(record)

    def addHandler(self, handler):
        if not isinstance(handler, BaseHandler):
            raise Exception('addHandler only receive a instance of BaseHandler')

        self.handlers.append(handler)


class BaseHandler():
    def __init__(self):
        self.formatter = Formatter('%(message)s')

    def emit(self, record):
        pass

    def setFormatter(self, formatter):
        self.formatter = formatter


class MyStreamHandler(BaseHandler):
    def __init__(self):
        BaseHandler.__init__(self)
        self.stream = sys.stdout

    def emit(self, record):
        msg = self.formatter.format(record)
        self.stream.write('%s\n' % msg)


class LogRecord():
    def __init__(self, name, level, msg, args):
        self.name = name
        self.level = level
        self.msg = msg
        self.args = args

    def getMessage(self):
        return self.msg % self.args



class Formatter():
    def __init__(self, fmt):
        self.fmt = fmt

    def format(self, record):
        record.message = record.getMessage()
        ret = self.fmt % record.__dict__
        return ret


# test code

logger = Logger('my_logger')
sh = MyStreamHandler()
sh.setFormatter(Formatter('[%(level)s][%(message)s]'))
logger.addHandler(sh)
logger.addHandler(MyStreamHandler())
logger.log('hello world')
logger.log('hello %s', 'lorry')
