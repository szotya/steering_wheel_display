"""
Saját logger modul
"""
import unittest
from unittest.mock import patch
import os
import logging
import sys
from io import StringIO
from modules.logger import Logger, LogCaptureHandler

class TestLogger(unittest.TestCase):
    """
    Saját logger osztály tesztelése. A következő funkciókat teszteli ez a unit teszt: INFO, DEBUG, WARNING, ERROR.
    Mindemellett nem csak az üzenet típusát hanem magát az üzenet str elemét is vizsgálja.
    """

    def setUp(self):
        """
        Teszt beállítása történik itt. A DEBUG változót alapból bekapcsolja, behívja a LogCaptureHandler és
        a sys.stdout illetve sys.stderr-t egy üres StringIO() objektumba teszi.
        """
        # Patch the environment variable to ensure consistent test results
        self.debug_env_var_patch = patch.dict(os.environ, {'DEBUG': 'true'})
        self.debug_env_var_patch.start()

        # Set up a log capture handler
        self.log_capture_handler = LogCaptureHandler()
        self.log_capture_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # Redirect stdout and stderr
        self.stdout_orig = sys.stdout
        self.stderr_orig = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        """
        Lebontja a tesztet és visszaállítja a sys.stdout és sys.stderr üzeneteket.
        """
        self.debug_env_var_patch.stop()
        logging.getLogger('TestLogger').removeHandler(self.log_capture_handler)

        # Restore original stdout and stderr
        sys.stdout = self.stdout_orig
        sys.stderr = self.stderr_orig

    def add_log_capture_handler(self, logger):
        """
        Handler működés.
        logger: Logger osztály
        """
        logger.logger.addHandler(self.log_capture_handler)
        logger.logger.setLevel(logging.DEBUG)

    def test_info_message(self):
        """
        Teszteli az INFO logger üzenetet.
        """
        logger = Logger('TestLogger')
        self.add_log_capture_handler(logger)
        logger.info("This is an info message")
        self.assertTrue(any("INFO" in record and "This is an info message" in record
                            for record in self.log_capture_handler.records))

    def test_debug_message(self):
        """
        Teszteli a DEBUG logger üzenetet.
        """
        logger = Logger('TestLogger')
        self.add_log_capture_handler(logger)
        logger.debug("This is a debug message")
        self.assertTrue(any("DEBUG" in record and "This is a debug message" in record
                            for record in self.log_capture_handler.records))

    def test_warning_message(self):
        """
        Teszteli a WARNING logger üzenetet.
        """
        logger = Logger('TestLogger')
        self.add_log_capture_handler(logger)
        logger.warning("This is a warning message")
        self.assertTrue(any("WARNING" in record and "This is a warning message" in record
                            for record in self.log_capture_handler.records))

    def test_error_message(self):
        """
        Teszteli az ERROR logger üzenetet.
        """
        logger = Logger('TestLogger')
        self.add_log_capture_handler(logger)
        logger.error("This is an error message")
        self.assertTrue(any("ERROR" in record and "This is an error message" in record
                            for record in self.log_capture_handler.records))

if __name__ == "__main__":
    unittest.main()
