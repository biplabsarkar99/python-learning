'''
Exhibiting the example of non daemon thread
Here, both the threads executed and then main thread exits and terminates the program
NOTE : non-daemon thread blocks the main program to exit if they are not dead
'''

import threading
import time


def print_work_a():
    print('Starting of thread :', threading.currentThread().name)
    time.sleep(2)
    print('Finishing of thread :', threading.currentThread().name)


def print_work_b():
    print('Starting of thread :', threading.currentThread().name)
    print('Finishing of thread :', threading.currentThread().name)


a = threading.Thread(target=print_work_a, name='Thread-a')
b = threading.Thread(target=print_work_b, name='Thread-b')

a.start()
b.start()