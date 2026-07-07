from threading import Semaphore, Thread
import time

sem: Semaphore = Semaphore()


def fun1():
    while True:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while True:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1, daemon=True)
t2: Thread = Thread(target=fun2, daemon=True)

t1.start()
t2.start()

try:
    while t1.is_alive() and t2.is_alive():
        t1.join(timeout=0.5)
        t2.join(timeout=0.5)
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    exit(1)