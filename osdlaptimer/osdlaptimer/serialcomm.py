
import threading
import serial
import time

class SerialComm(threading.Thread):

    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.controller = controller

    def run(self): 
        #ser = serial.Serial("COM12")  # open first serial port
        ser = serial.Serial("COM24")  # open first serial port
        print ser.portstr       # check which port was really used
        time.sleep(3)
        while True:
            s = self.controller.getSerialComm()
            if s != "":
                ser.write(s.encode('ascii','ignore') + "\n\r")      # write a string
        ser.close() 