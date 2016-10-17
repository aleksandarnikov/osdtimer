from PyQt4.QtGui import QDialog, QVBoxLayout

from vtxtimer.rssiscanwidget import RSSIScanWidget


class RSSIScanWindow(QDialog):
    def __init__(self, controller, parent = None):
        super(RSSIScanWindow, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.controller = controller
        self.rssiscanwidget = RSSIScanWidget(self.controller)
        layout.addWidget(self.rssiscanwidget)
        
    
    
    