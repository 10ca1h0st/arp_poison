import threading

class Poison_Thread(threading.thread):
    def __init__(self):
        super(Poison_Thread,self).__init__()
        self.stopped=False
    def run(self):
        def poison():
            pass
        sub=threading.Thread(target=poison,args=())
        sub.setDaemon(True)
        sub.start()

        while not self.stopped:
            sub.join(1)
    def stop(self):
        self.stopped=True
