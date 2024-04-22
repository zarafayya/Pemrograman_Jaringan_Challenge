import threading

def worker(num):
    print('Worker: ' + str(num))

threads = []

# worker diberi parameter
for i in range(5):
    t = threading.Thread(target=worker, args=(i, ))
    threads.append(t)
    t.start