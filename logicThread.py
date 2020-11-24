import threading
import time


class Work:
    def doWork(self):
        return

class WorkItem(Work):
    def doWork(self):
        print ("I am doing something in my work item")

class WorkItem2(Work):

    def __init__(self, var):
        self.var = var

    def doWork(self):
        print (self.var)

class Worker:
    cond = None
    def __init__(self):
        print ("do init")
        self.cond = threading.Condition()
        print ("starting thread")
        self.thread = threading.Thread(name = 'worker', target=self.run)
        self.work = []
        self.thread.start()
        print ("finished startup")
    def run(self):
        
        print ("entering run")
        while True:
            print ("acquire mutex")
            self.cond.acquire()
            
            print ("Waiting for work")
            self.cond.wait()
            
            print ("doing something")
            print ("items in queue " + str( len(self.work) ))
            for w in self.work:
                w.doWork()
            self.work = []
            print ("going to wait")
           
    def addWork(self, work):
        try:
            print ("> waiting for mutex")
            self.cond.acquire()
            
            print ("> adding work")
            self.work.append(work)
            
            print ("> releasing mutex")
            self.cond.notify()
        finally:
            print ("> items in queue " + str( len(self.work) ))
            self.cond.release()
def main(*args, **kwargs):
    print ("Starting")
    
    t = Worker()
    t.addWork ( WorkItem() )
    t.addWork ( WorkItem() )
    t.addWork ( WorkItem2( "Mario kann Multithreading "))

if __name__ == "__main__":
    main()