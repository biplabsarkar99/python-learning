File: logging_config_2.ini
The file specifies the config for the logger which is being used in the file 
logging_with_streaming_console.py to output the logs to both the console and the file stream
We have here used the FileHandler so the File is getting appended everytime.
NOTE:
1. We can use TimeRotatingFileHandler(supports rotation of disk log files at certain timed intervals.)
 or RotatingFileHandler(supports rotation of disk log files based on size) as per our requirement.
2. We can also delete the existing file during the setup phase of the test suite run.

File: logging_config_3.ini
The file specifies the config for the logger which is being used in the file 
logging_module_inherited.py to output the logs to both the console and the file stream
We have here used the FileHandler so the File is getting appended everytime.
NOTE:
1. We can use TimeRotatingFileHandler(supports rotation of disk log files at certain timed intervals.)
 or RotatingFileHandler(supports rotation of disk log files based on size) as per our requirement.
2. We can also delete the existing file during the setup phase of the test suite run.

The file format is based on configparser functionality which can be directly
decoded by the fileConfig function.

Description: 
loggers : Defines the identity of the different types of loggers. 
For each type, there is a separate section which identifies how that logger is configured. So, for the 
logger root, the conf details will be defined under logger_root or for the logger log1 the details will be 
logger_log1.
eg logger_root : Sets the config details for the root logger eg level, name of the different handlers
which are used in the root logger.
formatter : They are used to set the format of the various handlers and the configuration of the same can be
defined under the subsections like for the formatter simple, the config details can be checked under
formatter_simple.
handlers: Handler are the different ways in which the logs will be streams like in file, on console , how 
the file needs to be stored. All the conf details are stored in the handler subsection ex the for the handler
file, the conf details are mentioned in handler_file
keys=file,screen
