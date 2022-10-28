import threading
import time
from server_multiple import MyTCPHandler
import socketserver
exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        server = socketserver.TCPServer(('', self.counter), MyTCPHandler)
        server.serve_forever()


def print_time(threadName, counter, delay):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print(threadName, time.ctime(time.time()))
        counter -= 1



