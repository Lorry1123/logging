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
    def __init__(self, name, propagate=True):
        self.name = name
        self.handlers = []
        self.level = NOTSET
        self.parent = None
        self.propagate = propagate

    def _log(self, level, msg, args):
        record = LogRecord(self.name, level, msg, args)
        self.callHandlers(record)

    def callHandlers(self, record):
        c = self
        found = 0
        while c:
            for handler in c.handlers:
                found += 1
                if record.levelno >= handler.level:
                    handler.emit(record)
            if not c.propagate:
                c = None
            else:
                c = c.parent

        if found == 0:
            raise Exception('No handlers could be found for logger "%s"' % self.name)

    def addHandler(self, handler):
        if not isinstance(handler, BaseHandler):
            raise Exception('addHandler only receive a instance of BaseHandler')

        self.handlers.append(handler)

    def setLevel(self, level):
        self.level = level

    def isEnabledFor(self, level):
        return level >= self.level

    def debug(self, msg, *args):
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, args)

    def info(self, msg, *args):
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, args)

    def warning(self, msg, *args):
        if self.isEnabledFor(WARN):
            self._log(WARN, msg, args)

    warn = warning

    def error(self, msg, *args):
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, args)



class BaseHandler():
    def __init__(self):
        self.formatter = Formatter('%(message)s')
        self.level = NOTSET

    def emit(self, record):
        pass

    def setFormatter(self, formatter):
        self.formatter = formatter

    def setLevel(self, level):
        self.level = level


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
        self.levelno = level
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
# logger.addHandler(MyStreamHandler())


# logger.setLevel(WARN)
# logger.info('hello world')
# logger.warn('hello %s', 'lorry')

# sh.setLevel(ERROR)
# logger.info('hello info')
# logger.warn('hello warning')

parent = Logger('parent logger')
parent_hdl = MyStreamHandler()
parent_hdl.setFormatter(Formatter('[PARENT][%(level)s][%(message)s]'))
parent.addHandler(parent_hdl)
# 父节点

logger.parent = parent

logger.info('hello parent')

logger.propagate = False
logger.info('hello parent 2')
