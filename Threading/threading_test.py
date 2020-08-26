# importing threading module
import threading

# importing time module
import time


# defining a function with parameters - thread_name and delay time
def thread_delay(thread_name, delay):
    print("In Thread Delay function")
    count = 0
    while count < 3:
        time.sleep(delay)
        count += 1
        print(thread_name, '-------->', time.time())

def volume_cube(thread_name, a):
    print(thread_name, '-------->', time.time())
    print("Volume of Cube:", a*a*a)

def volume_square(thread_name, a):
    print(thread_name, '-------->', time.time())
    print("Volume of Square:", a*a)


if __name__ == '__main__':
    print("Starting the threads")
    t1 = threading.Thread(target=thread_delay, args=('t1', 1))
    t2 = threading.Thread(target=thread_delay, args=('t2', 3))

    t3 = threading.Thread(target=volume_cube, args=('t3', 3))
    t4 = threading.Thread(target=volume_square, args=('t4', 4))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
