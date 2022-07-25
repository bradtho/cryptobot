#!/usr/bin/env python3

import logging
import os

class Logs:
    def setupLogging(name="cryptobot"):
        logger = logging.getLogger(__name__)

        if logger.hasHandlers():
            return logger

        logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))

        s_handler = logging.StreamHandler()
        s_formatter = logging.Formatter("%(asctime)s %(message)s")
        s_handler.setFormatter(s_formatter)

        logger.addHandler(s_handler)
        return logger
