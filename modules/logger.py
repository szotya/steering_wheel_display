"""
Saját logger modul ami kezeli a következő üzeneteket:
- INFO
- DEBUG
- WARNING
- ERROR

Az üzenet formátuma a következő: "2024-10-14 00:01:13,135 - <logger_neve> - INFO - <üzenet_helye>."
"""
import logging
import os
import sys
from datetime import datetime
import pytz

class Logger:
    """
    Saját logger osztály és definíciók.
    Beállítja a logok formátumát illetve az időzónát (CET)
    """
    def __init__(self, name, timezone='CET'):
        """
        Logger osztály inicializálás
        name: Logger neve
        timezone: időzóna, alapbeállításban CET
        """
        self.logger = logging.getLogger(name)
        self.timezone = timezone

        debug_mode = os.getenv('DEBUG', 'False').lower() in {'true', '1'}

        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

            cet = pytz.timezone(self.timezone)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            formatter.converter = lambda *args: datetime.now(tz=cet).timetuple()

            ch_info = logging.StreamHandler(sys.stdout)
            ch_info.setLevel(logging.INFO)
            ch_info.setFormatter(formatter)
            ch_info.addFilter(lambda record: record.levelno == logging.INFO)
            
            ch_warning = logging.StreamHandler(sys.stdout)
            ch_warning.setLevel(logging.WARNING)
            ch_warning.setFormatter(formatter)
            ch_warning.addFilter(lambda record: record.levelno == logging.WARNING)

            ch_error = logging.StreamHandler(sys.stderr)
            ch_error.setLevel(logging.ERROR)
            ch_error.setFormatter(formatter)

            self.logger.addHandler(ch_info)
            self.logger.addHandler(ch_warning)
            self.logger.addHandler(ch_error)

            if debug_mode:
                ch_debug = logging.StreamHandler(sys.stdout)
                ch_debug.setLevel(logging.DEBUG)
                ch_debug.setFormatter(formatter)
                self.logger.addHandler(ch_debug)
                ch_debug.addFilter(lambda record: record.levelno == logging.DEBUG)

    def debug(self, message):
        """
        DEBUG üzenet
        message: az üzenet string
        """
        self.logger.debug(message)

    def info(self, message):
        """
        INFO üzenet
        message: az üzenet string
        """
        self.logger.info(message)

    def warning(self, message):
        """
        WARNING üzenet
        message: az üzenet string
        """
        self.logger.warning(message)

    def error(self, message):
        """
        ERROR üzenet
        message: az üzenet string
        """
        self.logger.error(message)


class LogCaptureHandler(logging.Handler):
    """
    Üzenet begyűjtő segítő osztály
    """
    def __init__(self):
        """
        Osztály inicializálás
        """
        super().__init__()
        self.records = []

    def emit(self, record):
        """
        Üzenet kiküldés
        record: az üzenet maga
        """
        self.records.append(self.format(record))
