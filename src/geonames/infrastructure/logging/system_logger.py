import logging
import os
from src.geonames.application.contracts.abstract_logger import AbstractLogger

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

class SystemLogger(AbstractLogger):
    
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def error(self, message: str) -> None:
        self._logger.error(message)