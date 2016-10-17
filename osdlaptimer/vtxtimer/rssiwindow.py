from PyQt4.QtGui import QDialog, QVBoxLayout

from vtxtimer.rssiwidget import RSSIWidget


class RSSIWindow(QDialog):
    def __init__(self, controller, parent = None):
        super(RSSIWindow, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.controller = controller
        self.rssiwidget = RSSIWidget(self.controller)
        layout.addWidget(self.rssiwidget)
        self.rssiwidget.thr_min = self.controller.rssinumbers.thr_min 
        self.rssiwidget.thr_max = self.controller.rssinumbers.thr_max 
        
    
    
    