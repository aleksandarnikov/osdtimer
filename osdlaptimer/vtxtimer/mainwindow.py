from PyQt4 import QtGui
from PyQt4.QtGui import QWidget, QMainWindow

from vtxtimer import rssiwindow, rssiscanwindow
import serial


class MainWindow(QMainWindow):
    def __init__(self, controller):
        self.controller = controller
        QWidget.__init__(self)
        self.setWindowTitle("RSSI Lap Timer") 
        self.statusBar().showMessage('Ready')
        self.initUI()
        
    def initUI(self):               
        self.statusBar().showMessage('Ready')
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Statusbar')    
        
        btn = QtGui.QPushButton("RSSI", self)
        btn.clicked.connect(self.startRSSI)
        btn.resize(btn.minimumSizeHint())
        btn.move(20,20)
        btn.setEnabled(False)
        self.btnRSSI = btn
        
        btn = QtGui.QPushButton("SCAN", self)
        btn.clicked.connect(self.startScan)
        btn.resize(btn.minimumSizeHint())
        btn.move(120,20)
        btn.setEnabled(False)
        self.btnScan = btn
        
        btn = QtGui.QPushButton("Connect", self)
        btn.clicked.connect(self.connect)
        btn.resize(btn.minimumSizeHint())
        btn.move(360,20)
        btn.setEnabled(True)
        
        
        
        self.items = []
        self.items.append("COM28")
        comboBox = QtGui.QComboBox(self)
        comboBox.setEditable(False)
        comboBox.addItems(self.items)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Preferred)
        comboBox.move(260, 20)
        
        self.comboBox = comboBox
        self.show()    
        
    def addComponent(self, widget):
        print ""
        #
        
    def connect(self):
        self.controller.startSerialComm(self.items[self.comboBox.currentIndex()])
        self.btnRSSI.setEnabled(True)
        self.btnScan.setEnabled(True)
        
    def startRSSI(self):
        self.controller.startRSSI()
        w = rssiwindow.RSSIWindow(self.controller, self)
        self.controller.rssiwidget = w.rssiwidget
        self.controller.hasRssiWidget = 1
        w.exec_()
        self.controller.hasRssiWidget = 0
        self.controller.stopRSSI()
        
    def startScan(self):
        self.controller.startScan()
        w = rssiscanwindow.RSSIScanWindow(self.controller, self)
        self.controller.rssiscanwidget = w.rssiscanwidget
        self.controller.hasRssiScanWidget = 1
        w.exec_()
        self.controller.hasRssiScanWidget = 0
        self.controller.stopScan()
        
        
        
