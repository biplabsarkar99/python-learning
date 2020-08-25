"""
The python file is using an ini file to define the logger properties.
We are creating a class TestLogger whose object can be used to log .We can keep the TestLogger in
central repo and import it wherever it is required or we can add the code to setup master class.
The config file specifies two handlers- File handler and one is log handler. (logging_config_3.ini)
We have been defining the log file name in the script instead of the config file using the defaults functionality
Refer Readme.md to understand more about the logging_config_3.ini

"""
import logging.config

class TestLogger:
    """
    master test class of the framework where we define the setup and tear down activities
    Here, sets the config variables for the logging
    """
    def __init__(self):
        # Setting the logger and its path to save
        self.logger_path = "my_logger_new.log"
        logging.config.fileConfig('logging_config_3.ini',
                                  defaults={'logfilename': self.logger_path},
                                  disable_existing_loggers=False)
        self.test_logger = logging.getLogger("Tests")

    def get_logger(self):
        return self.test_logger

class TestLoggingModule:
    """
    We have inherited the testlogger here to use the logger initiated there
    """

    def __init__(self):
        """
        setup class
        """
        self.test_logger = TestLogger().get_logger()
        print(self.test_logger)
        self.test_logger.info("Test setup class")

    def test_logging_function(self):
        self.test_logger.info("This message should go to both the log file and console")
        self.test_logger.debug('This message should go only to the log file')
        self.test_logger.info('This message should go to both the log file and console')
        self.test_logger.warning('This message should go to both the log file and console')


if __name__ == '__main__':
    new_test = TestLoggingModule()
    new_test.test_logging_function()