'''
The python file is using the properties define in the config
'''

import logging
import os

# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=os.getcwd() + '\\test_log.log',
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

# tell the handler to use this format
console.setFormatter(formatter)

# add the handler to the root logger(which used the file handler)
logging.getLogger().addHandler(console)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('THIS IS the fisrt INFO ')

# Now, define loggers which will be used in the application

logger1 = logging.getLogger('mylogs1')
logger2 = logging.getLogger('mylogs2')

logger1.debug('This is a debug statement.')
logger1.info('This is an info statement.')

logger2.warning('This is a warning for the user.')
logger2.error('This the error occured in the application.')