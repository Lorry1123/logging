# coding: utf8

import logging

request_id = '假装是个 request_id'


class SmsLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, level)

    def _log(self, level, msg, args, exc_info=None, extra=None):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        if True:
            #IronPython doesn't track Python frames, so findCaller raises an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func = self.findCaller()
                # 可能需要针对需求做一些hack，比如翻 traceback 的时候不仅跳过 logging.py 还要跳过这个文件
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        # ----- 添加部分 ------
        if extra is None:
            extra = dict()

        extra['request_id'] = request_id

        # --------------------

        record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra)
        self.handle(record)

logging.rootLogger = SmsLogger('')

if __name__ == '__main__':
    logging.setLoggerClass(SmsLogger)
    logging.Logger.manager.setLoggerClass(SmsLogger)
    logger  = logging.getLogger('123')

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("[SMS LOGGING][%(levelname)s][%(request_id)s][%(msg)s]"))
    logger.addHandler(sh)

    logger.warning('test')
