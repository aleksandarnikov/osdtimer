from osdlaptimer.controller import Controller


print "hello"

hostip = "192.168.42.1"
#hostip = "192.168.1.110"

controller = Controller(hostip);
controller.start();
