# -*- coding: utf-8 -*-

import sys

sys.path.append("./APA102_Pi/Adafruit_Python_GPIO")

import logger
log = logger.getLogger()

from Adafruit_GPIO import GPIO



class buttonGpio:
    def __init__(self, pin, pullState):
        self.gpio = GPIO.get_platform_gpio()
        self.gpio.setup(pin,GPIO.IN,pullState)
        self.pin = pin
  
    def getButtonState(self):
        state = self.gpio.input(self.pin)
        print(state)
        return state
        


if __name__ == "__main__":
    testButton = buttonGpio(9, GPIO.PUD_UP)
    
    testButton.getButtonState()
    import time
    time.sleep(5)
    testButton.getButtonState()
