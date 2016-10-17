import pyttsx
engine = pyttsx.init()

print engine.getProperty('rate')
print engine.getProperty('voice')
print engine.getProperty('volume')

engine.setProperty('rate', 150)

engine.say('New Lap 1 minute 23.2 seconds')
engine.say('Best lap 1 minute 21.3 seconds')
engine.runAndWait()


