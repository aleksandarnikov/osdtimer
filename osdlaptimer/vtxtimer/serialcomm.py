import threading
import serial
import time

class SerialComm(threading.Thread):

    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.controller = controller
        self.port = "COM28"

    def run(self): 
        #ser = serial.Serial("COM12")  # open first serial port
        ser = serial.Serial(self.port, baudrate=9600, timeout = 2)  # open first serial port
        print ser.portstr       # check which port was really used
        time.sleep(3)
        while True:
            x = ser.readline()
            if x:
                self.controller.sendToController(x)
            y = self.controller.getFromController()
            if y != "":
                #print "Write serial " + y
                ser.write(y + "\n\r")
#             if s != "":
#                 ser.write(s.encode('ascii','ignore') + "\n\r")      # write a string
        ser.close() 