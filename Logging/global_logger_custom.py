import logging.config

''' 
Here we are declaring the logger directly
'''

logger_path = "new_log.txt"
logging.config.fileConfig('logging_config_3.ini',
                               defaults={'logfilename': logger_path},
                               disable_existing_loggers=False)
logger = logging.getLogger()

class TestGlobalLogger:
    def filter_test(self):
        logger.info("In Class : TestGlobalLogger")
        logger.info("An INFO message from " + __name__)
        logger.error("An ERROR message from " + __name__)
        logger.debug("An DEBUG message from " + __name__)


class TestGlobalLogger1:
    def filter_test(self):
        logger.info("In Class : TestGlobalLogger")
        logger.info("An INFO message from " + __name__)
        logger.error("An ERROR message from " + __name__)
        logger.warning("An WARNING message from " + __name__)


if __name__ == '__main__':
    test1 = TestGlobalLogger()
    test2 = TestGlobalLogger1()
    logger.info("Checking the object of the TestGlobalLogger")
    test1.filter_test()
    logger.info("Checking the object of the TestGlobalLogger1")
    test2.filter_test()