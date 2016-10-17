import sys

from PyQt4.QtGui import QApplication

from vtxtimer.controller import Controller
from vtxtimer.mainwindow import MainWindow



print "hello"

#hostip = "192.168.42.1"
#hostip = "192.168.1.110"

app = QApplication(sys.argv)

controller = Controller(); # 0 means always take the last token

w = MainWindow(controller)

#w.addComponent(controller.rssiwidget)

controller.start();
w.show()
sys.exit(app.exec_())
