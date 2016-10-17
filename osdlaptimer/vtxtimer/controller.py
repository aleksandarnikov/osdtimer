from Queue import Queue
import time

from PyQt4.QtCore import QObject, pyqtSignal

from vtxtimer.rssinumbers import RSSINumbers
from vtxtimer.serialcomm import SerialComm


class Controller(QObject):
    
    rssiNumberSignalObject = pyqtSignal(object)
    rssiScanSignalObject = pyqtSignal(object)
    
    def __init__(self):   
        QObject.__init__(self)
        self.squeue = Queue()
        self.fqueue = Queue()
        self.serialcomm = SerialComm(self)
        self.rssinumbers = RSSINumbers(self)
        self.hasRssiWidget = 0
        self.hasRssiScanWidget = 0

    def start(self):
        self.rssiNumberSignalObject.connect(self.rssiDataReady)
        self.rssiScanSignalObject.connect(self.rssiScanDataReady)
        self.rssinumbers.start()

    def startSerialComm(self, port):
        self.serialcomm.port = port
        self.serialcomm.start()
        
    def startRSSI(self):
        self.sendToSerialPort("C38")
        self.sendToSerialPort("R")
        
    def stopRSSI(self):
        self.sendToSerialPort("S")
                
    def startScan(self):
        self.sendToSerialPort("X")            
    
    def stopScan(self):
        self.sendToSerialPort("S")
    
    def sendToSerialPort(self, s):
        #print "To queue " + s
        self.squeue.put(s)
        
    def getFromSerialPort(self):
        s = self.fqueue.get()
        #print "From queue " + s
        return s
    
    def sendToController(self, s):
        #print "To queue " + s
        self.fqueue.put(s)
        
    def getFromController(self):
        if not self.squeue.empty():
            s = self.squeue.get()
            #print "From queue " + s
            return s
        else:
            return ""
        
    def publishRSSINumber(self, y, state):
        self.rssiNumberSignalObject.emit('%s %s' % (y, state))
    
    def publishRSSIScan(self, data):
        self.rssiScanSignalObject.emit(data)
    
    def rssiDataReady(self, data):
        z = data.split(" ")
        if self.hasRssiWidget == 1:
            self.rssiwidget.updateValue(int(z[0]), int(z[1]))
            
    def rssiScanDataReady(self, data):
        if self.hasRssiScanWidget == 1:
            self.rssiscanwidget.updateValue(data)
        
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