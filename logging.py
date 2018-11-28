# coding: utf8

import sys
from exceptions import Exception

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

_levelNames = {
    CRITICAL : 'CRITICAL',
    ERROR : 'ERROR',
    WARNING : 'WARNING',
    INFO : 'INFO',
    DEBUG : 'DEBUG',
    NOTSET : 'NOTSET',
    'CRITICAL' : CRITICAL,
    'ERROR' : ERROR,
    'WARN' : WARNING,
    'WARNING' : WARNING,
    'INFO' : INFO,
    'DEBUG' : DEBUG,
    'NOTSET' : NOTSET,
}

class Logger():
    def __init__(self, name):
        self.name = name
        self.handlers = []

    def _log(self, level, msg, args):
        if not len(self.handlers):
            raise Exception('No handlers could be found for logger "%s"' % self.name)

        for handler in self.handlers:
            record = LogRecord(self.name, level, msg, args)
            handler.emit(record)

    def addHandler(self, handler):
        if not isinstance(handler, BaseHandler):
            raise Exception('addHandler only receive a instance of BaseHandler')

        self.handlers.append(handler)

    def debug(self, msg, *args):
        self._log(DEBUG, msg, args)

    def info(self, msg, *args):
        self._log(INFO, msg, args)

    def warning(self, msg, *args):
        self._log(WARN, msg, args)

    warn = warning

    def error(self, msg, *args):
        self._log(ERROR, msg, args)



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
        self.level = _levelNames[level]
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
logger.info('hello world')
logger.warn('hello %s', 'lorry')
