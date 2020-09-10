import logging.config
import sys
from configparser import RawConfigParser

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

    def print_logger_conf(self):
        config = RawConfigParser()
        print("###################################################")
        print("Before the config file is read")
        print(list(config.sections()))
        print("###################################################")
        config.read('logging_config_3.ini')
        print("After the config file is read")
        for element in config.sections():
            print("{}:".format(element))
            print(config[element])
            for element_child in config[element]:
                print("\t{} : {}".format(element_child, config.get(element, element_child)))
        print("###################################################")

    def update_logger_conf(self, level= None):
        file_handler = logger.handlers[1]
        file_handler.setLevel(level)
        print("###################################################")
        print(file_handler)
        print("###################################################")


if __name__ == '__main__':
    test1 = TestGlobalLogger()
    if len(sys.argv) > 1:
        if sys.argv[1] in ["INFO", "DEBUG", "ERROR","WARNING"]:
            test1.update_logger_conf(sys.argv[1])
        else:
            print("Invalid Log type. We will use a default logger. ")
    print("Printing the test config")
    test1.print_logger_conf()
    logger.info("Checking the object of the TestGlobalLogger")
    test1.filter_test()
