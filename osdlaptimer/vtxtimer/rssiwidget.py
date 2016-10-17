from PyQt4 import QtCore
from PyQt4.QtCore import QLineF, QRectF
from PyQt4.QtGui import QWidget, QHBoxLayout, QPainter, QBrush, \
    QPen, QColor


class RSSIWidget(QWidget):
    def __init__(self, controller):
        self.controller = controller
        QWidget.__init__(self)
        QHBoxLayout(self)
        self.W = 800
        self.HChart = 400
        self.H = 500
        self.sizeHint = lambda: QtCore.QSize (self.W, self.H)
        self.values = []
        i = 0;
        while i < self.W:
            self.values.append(0)
            i = i + 1
        self.states = []
        i = 0;
        while i < self.W:
            self.states.append(0)
            i = i + 1
        self.thr_min = 0
        self.thr_max = 0

#         self.pixmap = QPixmap(QSize(400,400))
#         self.child = QLabel()
#         self.child.setPixmap(self.pixmap)
#         self.layout().addWidget(self.child)
        
    def updateValue(self, y, state):
        self.values = self.values[1:]
        self.values.append(y)
        self.states = self.states[1:]
        self.states.append(state)
        self.update()
        #print "updatevalue"

        
    def paintEvent(self, *args, **kwargs):
        #QGraphicsView.paintEvent(self, *args, **kwargs)
        painter = QPainter()   
        painter.begin(self) 
        
        painter.fillRect(QRectF(0, 0, self.W, self.HChart), QtCore.Qt.white)
        
        painter.setPen(QPen(QBrush(QColor('#900090')), 1.0))
        painter.drawLine(QLineF(0, self.HChart - self.thr_min * 4, self.W, self.HChart - self.thr_min * 4))
        painter.drawLine(QLineF(0, self.HChart - self.thr_max * 4, self.W, self.HChart - self.thr_max * 4))
        
        i = 1;
        while i < self.W:
            if self.states[i] == 0:
                painter.setPen(QPen(QBrush(QColor('#309030')), 2.0))
            if self.states[i] == 1:
                painter.setPen(QPen(QBrush(QColor('#903030')), 2.0))    
            if self.states[i] == 2:
                painter.setPen(QPen(QBrush(QColor('#303090')), 2.0))                 
            painter.drawLine(QLineF(i - 1, self.HChart - self.values[i - 1] * 4, i, self.HChart - self.values[i] * 4))
            i = i + 1
        
        painter.end()
        #print "paint"
