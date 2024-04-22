import threading
import datetime

class ThreadClass(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print(self.getName() + ' says Hello World at time: ' + str(now) + '\n')
    
for i in range(5):
    t = ThreadClass()
    t.start