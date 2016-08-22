from osdlaptimer.irlap import IrLap
from osdlaptimer.laptimerinfo import LapTimerInfo
from osdlaptimer.serialcomm import SerialComm
from Queue import Queue

class Controller(object):
    def __init__(self, hostip):   
        self.squeue = Queue()
        self.irlap = IrLap(self, hostip)
        self.laptimerinfo = LapTimerInfo(self, hostip)
        self.serialcomm = SerialComm(self)

    def start(self):
        self.irlap.start()
        self.laptimerinfo.start()    
        self.serialcomm.start()
                
    def sendToSerialPort(self, s):
        print "To queue " + s
        self.squeue.put(s)
        
    def getSerialComm(self):
        s = self.squeue.get()
        print "From queue " + s
        return s
    
    def timeFromMillis(self, s):
        x1 = int(s) / 1000
        mmin = x1 / 60
        sec = x1 % 60
        hun = (int(s) % 1000) / 10
        ss = ""
        if mmin < 10:
            ss += "0"
        ss += str(mmin)
        ss += ":"
        if sec < 10:
            ss += "0"
        ss += str(sec)
        ss += ":"
        if hun < 10:
            ss += "0"
        ss += str(hun)
        return ss