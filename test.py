import threading
import time

class Poison_Thread(threading.Thread):
    def __init__(self,num):
        super(Poison_Thread,self).__init__()
        self.stopped=False
        self.num=num
    def run(self):
        def poison():
            while not self.stopped:
                print self.num
        sub=threading.Thread(target=poison,args=())
        sub.setDaemon(True)
        sub.start()
        '''

        while not self.stopped:
            sub.join(1)
        '''
    def stop(self):
        self.stopped=True


if __name__=="__main__":
    pt1=Poison_Thread(1)
    pt2=Poison_Thread(2)
    pt1.start()
    pt2.start()
    time.sleep(0.5)
    pt1.stop()
    pt2.stop()
