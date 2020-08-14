'''
When Debug level set to
1. INFO : Only info messages are printed
2. DEBUG: All the messages are printed including info, warning, error
3. WARNING: The messages for the error and warning are displayed
4. ERROR: Only error messages are displayed
'''

import logging
from logging.config import fileConfig


fileConfig('logging_config.ini')
logger = logging.getLogger()
logger.info("Checking the print tof the messages based on the loggin level set in logging_config.ini")
logger.debug('often makes a very good meal of %s', 'visiting tourists')
logger.error('Check if the error occured')
logger.warning('We have a warning here')

