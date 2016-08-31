
import threading
import requests
import time

class LapTimerInfo(threading.Thread):

    def __init__(self, controller, hostip):
        threading.Thread.__init__(self)
        self.controller = controller
        self.hostip = hostip

    def run(self): 
        while True:
            response = requests.get('http://' + self.hostip + '/api/v1/monitor')
            data = response.json()
            
            for x in data['data']:
                if x['pilot']['transponder_token'] == '12':
                    self.controller.sendToSerialPort("1" + x['pilot']['name'])
                    self.controller.sendToSerialPort("3" + self.controller.timeFromMillis(x['fastest_lap']['lap_time']))
                   
            
            time.sleep(30)