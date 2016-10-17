from PyQt4 import QtCore
from PyQt4.QtCore import QLineF, QRectF, QPointF
from PyQt4.QtGui import QWidget, QHBoxLayout, QPainter, QBrush, \
    QPen, QColor, QFont

class RSSIScanWidget(QWidget):
    def __init__(self, controller):
        self.controller = controller
        QWidget.__init__(self)
        QHBoxLayout(self)
        self.W = 800
        self.H = 500
        self.HChart = 400
        self.sizeHint = lambda: QtCore.QSize (self.W, self.H)
        self.values = []
        i = 0
        while i < 40:
            self.values.append(0)
            i = i + 1
        
    def updateValue(self, data):
        z = data.split(" ")
        self.values = []
        i = 1
        while i <= 40:
            self.values.append(int(z[self.controller.rssinumbers.chanorder[i - 1] + 1]))
            i = i + 1
        self.update()
         
    def paintEvent(self, *args, **kwargs):
        painter = QPainter()   
        painter.begin(self) 
        painter.fillRect(QRectF(0, 0, self.W, self.HChart), QtCore.Qt.white)
        i = 0;
        painter.setFont(QFont(painter.font().family(), 6))  
        while i < 40:
            painter.fillRect(QRectF(i * 20 + 2, self.HChart - self.values[i] * 4, 16, self.values[i] * 4), QBrush(QColor('#309090')))
            painter.setPen(QPen(QBrush(QColor(QtCore.Qt.white)), 1.0))
            z = self.values[i]
            painter.drawText(QPointF(i * 20 + 7, self.HChart - 6), str(z % 10) )
            z = z / 10
            painter.drawText(QPointF(i * 20 + 7, self.HChart - 16), str(z % 10))
            z = z / 10
            if z > 0:
                painter.drawText(QPointF(i * 20 + 7, self.HChart - 26), str(z % 10) )
            i = i + 1

        painter.setPen(QPen(QBrush(QColor('#900090')), 1.0))
        painter.drawLine(QLineF(0, self.HChart - self.controller.rssinumbers.thr_min * 4 + 10, self.W, self.HChart - self.controller.rssinumbers.thr_min * 4 + 10))
        painter.drawLine(QLineF(0, self.HChart - self.controller.rssinumbers.thr_max * 4 + 10, self.W, self.HChart - self.controller.rssinumbers.thr_max * 4 + 10))

        painter.setFont(QFont(painter.font().family(), 8))       

        painter.setPen(QPen(QBrush(QColor(QtCore.Qt.black)), 1.0))
        i = 0;
        while i < 40:
            channame = hex(self.controller.rssinumbers.channames[self.controller.rssinumbers.chanorder[i]])[2:]

            painter.drawText(QPointF(i * 20 + 2, self.HChart + 16), channame)
            x = self.controller.rssinumbers.chans[self.controller.rssinumbers.chanorder[i]]
            j = 0
            painter.setFont(QFont(painter.font().family(), 6))     
            while j < 4:
                y = x % 10
                x = x / 10
                painter.drawText(QPointF(i * 20 + 6, self.HChart + 16 + (4 - j) * 10), str(y))
                j = j + 1
            i = i + 1
            painter.setFont(QFont(painter.font().family(), 8))     
        
        