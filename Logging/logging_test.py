"""
Logging serves two purposes:
1. Diagnostic logging records events related to the application’s operation.
eg. If a user calls in to report an error, for example, the logs can be searched for context.
2. Audit logging records events for business analysis. A user’s transactions can be extracted and
combined with other user details for reports or to optimize a business goal.
"""

# importing the logging module
import logging

# Best Practice :
# Instantiate loggers in a library using the __name__ global variable as
# the logging module creates a hierarchy of loggers using dot notation, so using __name__ ensures no name collisions.
print(logging.getLogger(__name__).addHandler(logging.NullHandler()))

