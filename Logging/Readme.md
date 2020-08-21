File: logging_config_2.ini
The file specifies the config for the logger which is being used in the file 
logging_with_streaming_console.py to output the logs to both the console and the file stream
We have here used the FileHandler so the File is getting appended everytime.
NOTE:
1. We can use TimeRotatingFileHandler(supports rotation of disk log files at certain timed intervals.)
 or RotatingFileHandler(supports rotation of disk log files based on size) as per our requirement.
2. We can also delete the existing file during the setup phase of the test suite run.