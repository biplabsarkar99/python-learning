"""
The python file is using an ini file to define the logger properties
The config file specifies two handlers- File handler and one is log handler.
"""

import logging

from logging.config import fileConfig

# importing a logging file which defines two handlers - File and console for the logger
# The console has the DEBUG
fileConfig('logging_config_2.ini')
logger = logging.getLogger(__name__)

logger.info("This message should go to both the log file and console")
logger.debug('This message should go only to the log file')
logger.info('This message should go to both the log file and console')
logger.warning('This message should go to both the log file and console')