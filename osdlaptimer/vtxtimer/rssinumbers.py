import threading
import winsound
from PyQt4.QtCore import QObject

class RSSINumbers(threading.Thread, QObject):
    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.controller = controller
        self.c = 0
        self.thr_min = 75
        self.thr_max = 85
        self.consecutive_count = 20
        self.state = 0
        self.last_thr = 0
        self.last_count = 0
        self.chans =   [5865, 5845, 5825, 5805, 5785, 5765, 5745, 5725, # Band A
                            5733, 5752, 5771, 5790, 5809, 5828, 5847, 5866, # Band B
                            5705, 5685, 5665, 5645, 5885, 5905, 5925, 5945, # Band E
                            5740, 5760, 5780, 5800, 5820, 5840, 5860, 5880,  # Band F / Airwave
                            5658, 5695, 5732, 5769, 5806, 5843, 5880, 5917]  # Band C / Immersion Raceband
        self.channames = [0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, # Band A
                                0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, # Band B
                                0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, # Band E
                                0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, # Band F / Airwave
                                0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8]  # Band C / Immersion Raceband)
        self.chanorder = [19, 18, 32, 17, 33, 16, 7, 34, 8, 24, 6, 9, 25, 5, 35, 10, 26, 4, 11, 27, 3, 36, 12, 28, 2, 13, 29, 37, 1, 14, 30, 0, 15, 31, 38, 20, 21, 39, 22, 23]
        
    def run(self): 
        while True:
            x = self.controller.getFromSerialPort()
            z = x.strip().split(" ")
            if len(z) > 1:
                if z[0] == 'RSSI':
                    self.rssi(z)
                if z[0] == 'SCAN':
                    self.scan2(z)
                    self.controller.publishRSSIScan(x)  
                   
                    
    def rssi(self, z):
        y = int(z[1])
        if y < self.thr_min:
            if self.state == 0 or self.state == 2:
                if self.last_thr == 1:
                    self.last_count = self.last_count + 1
                    if self.last_count >= self.consecutive_count:
                        self.state = 1
                        self.last_count = 0
                        #winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
                else:
                    self.last_thr = 1
                    self.last_count = 0
        if y > self.thr_max:
            if self.state == 0 or self.state == 1:
                if self.last_thr == 2:
                    self.last_count = self.last_count + 1
                    if self.last_count >= self.consecutive_count:
                        self.state = 2
                        self.last_count = 0
                        # beeeeeep
                        #winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                else:
                    self.last_thr = 2
                    self.last_count = 0
        if y > self.thr_min and y < self.thr_max:
            self.last_thr = 0
            self.last_count = 0
        print y,
        self.c = self.c + 1
        if self.c == 40:
            self.c = 0
            print ""    
        self.controller.publishRSSINumber(y, self.state)    

    def scan(self, z):
        i = 1
        while i <= 40:
            rssi = z[i]
            chan = self.chans[i - 1];
            name = self.channames[i - 1];
            print chan,
            print hex(name)[2:],
            print rssi,
            print " - ",
            if i % 8 == 0:
                print ""
            i = i + 1
        print ""
        print ""
        
    def scan2(self, z):
        i = 1;
        while i <= 40:
            chanIndex = self.chanorder[i - 1]
            rssi = z[chanIndex + 1];
            chan = self.chans[chanIndex];
            name = self.channames[chanIndex];
            print "", hex(name)[2:], "",
            i = i + 1
        print ""
        i = 1
        while i <= 40:
            chanIndex = self.chanorder[i - 1]
            rssi = z[chanIndex + 1];
            chan = self.chans[chanIndex];
            name = self.channames[chanIndex];
            print chan,
            i = i + 1
        print ""
        i = 1
        while i <= 40:
            chanIndex = self.chanorder[i - 1]
            rssi = z[chanIndex + 1];
            chan = self.chans[chanIndex];
            name = self.channames[chanIndex];
            print "", rssi, "",
            i = i + 1
        print ""
        print ""
        