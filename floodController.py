import thread
import time
from botparse import Utils

Utils = Utils() 

def loop():
    while True:
        time.sleep(5)
        Utils.resetFloodCount()
 
thread.start_new_thread(loop, ())
