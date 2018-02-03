# -*- coding: utf-8 -*-

import sys

sys.path.append("./APA102_Pi/Adafruit_Python_GPIO")

import logger
log = logger.getLogger()

from Adafruit_GPIO import GPIO



class buttonGpio:
    def __init__(self, gpio, pullState):
        self.gpio = GPIO.get_platform_gpio()
        self.gpio.setup(gpio,GPIO.IN,pullState)
        self.gpio = gpio
  
    def getButtonState(self):
        state = self.gpio.input(self.gpio)
        print(state)
        return state
        


if __name__ == "__main__":
    testButton = buttonGpio(8, GPIO.PUD_UP)
    
    testButton.getButtonState()
    import time
    time.sleep(5)
    testButton.getButtonState()