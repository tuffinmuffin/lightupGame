# -*- coding: utf-8 -*-

import sys

sys.path.append("./APA102_Pi/Adafruit_Python_GPIO")

import logger
log = logger.getLogger()

from Adafruit_GPIO import GPIO



class buttonGpio:
    def __init__(self, pin, invert = True, pullState = GPIO.PUD_UP):
        self.gpio = GPIO.get_platform_gpio()
        self.gpio.setup(pin,GPIO.IN,pullState)
        self.pin = pin
        self.invert = invert
  
    def getButtonState(self):
        state = self.gpio.input(self.pin)
        if(self.invert):
             state = not state 
        #print(state)
        return state
        


class sampleButton:
    
    def __init__(self,*args):
        self.state = False
        
    def getButtonState(self):
        return self.state

if __name__ == "__main__":
    testButton = buttonGpio(9, GPIO.PUD_UP)
    
    testButton.getButtonState()
    import time
    time.sleep(5)
    testButton.getButtonState()
