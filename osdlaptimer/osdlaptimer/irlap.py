
import threading
import socket
import sys

class IrLap(threading.Thread):

    def __init__(self, controller, hostip):
        threading.Thread.__init__(self)
        self.controller = controller
        self.hostip = hostip

    def run(self): 
        # Bind the socket to the port
        server_address = (self.hostip, 3007)
        print >>sys.stderr, 'starting up on %s port %s' % server_address
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        s = ''
        while True:
            ata = sock.recv(1)

            if ata == '#':
                print s
                s = s.strip();
                if s.startswith("NEW_LAP_TIME"):
                    ss = s.split(" ")
                    token = ss[1]
                    time = ss[2]
                    print token + "/" + time
                    if token == '16':
                        self.controller.sendToSerialPort("-")
                        self.controller.sendToSerialPort("4" + self.controller.timeFromMillis(time))
                s = ''
            else:
                s = s + ata
        