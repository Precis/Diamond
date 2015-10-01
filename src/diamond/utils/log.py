# coding=utf-8


import logging
import logging.config
import sys
import os


class DebugFormatter(logging.Formatter):

    def __init__(self, fmt=None):
        if fmt is None:
            fmt = ('%(created)s\t' +
                   '[%(processName)s:%(process)d:%(levelname)s]\t' +
                   '%(message)s')
        self.fmt_default = fmt
        self.fmt_prefix = fmt.replace('%(message)s', '')
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        self._fmt = self.fmt_default

        if record.levelno in [logging.ERROR, logging.CRITICAL]:
            self._fmt = ''
            self._fmt += self.fmt_prefix
            self._fmt += '%(message)s'
            self._fmt += '\n'
            self._fmt += self.fmt_prefix
            self._fmt += '%(pathname)s:%(lineno)d'

        return logging.Formatter.format(self, record)


def setup_logging(configfile, stdout=None):
    log = logging.getLogger('diamond')

    if stdout:
        if stdout is True:
            log_level = logging.DEBUG
        else:
            log_level = logging.getLevelName(stdout)
            if not isinstance(log_level, int):
                log_level = logging.DEBUG
        log.setLevel(log_level)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(DebugFormatter())
        stream_handler.setLevel(log_level)
        log.addHandler(stream_handler)
    else:
        try:
            if sys.version_info >= (2, 6):
                logging.config.fileConfig(configfile,
                                          disable_existing_loggers=False)
            else:
                # python <= 2.5 does not have disable_existing_loggers
                # default was to always disable them, in our case we want to
                # keep any logger created by handlers
                logging.config.fileConfig(configfile)
                for logger in logging.root.manager.loggerDict.values():
                    logger.disabled = 0
        except Exception, e:
            sys.stderr.write("Error occurs when initialize logging: ")
            sys.stderr.write(str(e))
            sys.stderr.write(os.linesep)

    return log
