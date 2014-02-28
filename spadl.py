
import logging

from dbglog import dbg


DEBUG = 'DBG'
INFO = 'INFO'
WARNING = 'WARN'
ERROR = 'ERR'
FATAL = 'FATAL'

DBG_LOG_LEVELS = {
    logging.DEBUG: DEBUG,
    logging.INFO: INFO,
    logging.WARNING: WARNING,
    logging.ERROR: ERROR,
    logging.FATAL: FATAL,
}


class DbgLogHandler(logging.Handler):
    """
    A handler class which writes logging records to DbgLog.
    """

    def __init__(self, severity):
        logging.Handler.__init__(self)
        if isinstance(severity, (int, long)):
            self.severities = {'': severity}
        else:
            self.severities = severity

    def emit(self, record):
        """
        Emits a record.

        Logs the record using the DbgLog library.

        """
        try:
            level = self.getDbgLogLevel(record)
            severity = self.getDbgLogSeverity(record)
            if level > 0 and severity > 0:
                msg = self.format(record)
                location = (record.filename, record.funcName, record.lineno)
                dbg.log(msg, location=location, **{level: severity})
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def getDbgLogLevel(self, record):
        """
        Returns name of DbgLog level.

        Maps a standard logging level set to a `logging.LogRecord`
        instance to one of 'FATAL', 'ERR', 'WARN', 'INFO' and 'DBG'.

        """
        level = record.levelno
        try:
            return DBG_LOG_LEVELS[level // 10 * 10]
        except KeyError:
            return FATAL if level > logging.FATAL else 0

    def getDbgLogSeverity(self, record):
        """
        Returns severity for DbgLog.

        Maps a logger name set to a `logging.LogRecord` instance
        to a severity number from 1 to 4 (inclusive).

        """
        severities = self.severities
        name = record.name or 'root'
        while True:
            try:
                return severities[name]
            except KeyError:
                pass
            try:
                name = name[:name.rindex('.')]
            except ValueError:
                if not name:
                    return 0
                name = ''
