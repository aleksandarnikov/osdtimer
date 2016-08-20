
import threading
import requests
import time

class LapTimerInfo(threading.Thread):

    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.controller = controller

    def run(self): 
        while True:
            response = requests.get('http://192.168.1.110/api/v1/monitor')
            data = response.json()
            
            for x in data['data']:
                if x['pilot']['transponder_token'] == '16':
                    self.controller.sendToSerialPort("1" + x['pilot']['name'])
                    self.controller.sendToSerialPort("3" + self.controller.timeFromMillis(x['fastest_lap']['lap_time']))
                   
            
            time.sleep(30)