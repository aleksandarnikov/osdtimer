import threading
import time
from Queue import Queue

class TestQueue1(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue;
    
    def run(self):
        while True:
            self.queue.put("hello");
            print("sent " + "hello")
            time.sleep(2);
        
        
        

class TestQueue2(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue;
        
    def run(self):
        while True:
            s = self.queue.get();
            print("received " + s)
        

queue = Queue();
test1 = TestQueue1(queue);
test2 = TestQueue2(queue);

test1.start();
time.sleep(10)
test2.start();
