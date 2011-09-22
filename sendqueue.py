# This took me way too long to write...
from collections import deque
import time, sys, thread
import botCore

queue = deque([])

def queueloop():
    while True:
       time.sleep(0.5)
       sendNext()

def sendNext():
    try:
        print '>>> {0}'.format(queue[0].rstrip())
        botCore.s.send(queue[0])
        queue.popleft()
    except IndexError:
        pass
    
def initQueue():
    thread.start_new_thread(queueloop, ())
