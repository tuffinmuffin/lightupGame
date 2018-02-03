# -*- coding: utf-8 -*-
import logger
log = logger.getLogger()

import ledDriver

import configReader

import time
import sys
import APA102_Pi

import button
import threading

class GameManager:
    
    def __init__(self, ledManager, button, config):
        self.ledManager = ledManager
        self.config = config
        self.button = button
        

        self.buttonLockoutCurrent = self.buttonLockoutDefault = config.getValue(config.app,'btTimeout',0.0)
            
        self.lightTimerCurrent = self.lightTimerDefault = config.getValue(config.app,'lightTimer',10.0)
                     
        self.fadeTimerCurrent = self.fadeTimerDefault = config.getValue(config.app,'fadeTimer',0.25)
        
        
        self.colors = config.colors
        
        self.patterns = config.patterns

        self.reset()
        
    '''
    cycles to the next element without changing timers
    '''
    def cycle(self):
        #reset defaults
        self.buttonLockoutCurrent = self.buttonLockoutDefault
        self.fadeTimerCurrent = self.fadeTimerDefault
        self.lightTimerCurrent = self.lightTimerDefault
        
        return self.setNextState()
        
    
    '''
    advance the button to the next state due to 
    state timeout
    '''
    def advance(self):
        pass
    
    '''
    reset the counter and resets sequence to init
    '''
    def reset(self):
        
        self.buttonThread = threading.Thread(target = self.buttonMonitor, name = "buttonMonitor", daemon=True)
        self.buttonThread.start()
        
        self.currentPatternName = 'init'
        #get a copy of the pattern so we can pop from it.
        self.currentPattern = self.patterns['init'][:]    
        
        
        self.colorThread = threading.Thread(target = self.colorCycler, name = "Color Cycler", daemon=True)
        self.colorThread.start()
    
    def shutdown(self):
        pass
    
    
    def buttonMonitor(self):
        while(threading.get_ident() == self.buttonThread.ident):
            #print(dir(threading.current_thread()))
            #add code here to check the button
            state = self.button.getButtonState()
            
            #if button is pressed
            if state:                
                #call cycle. This may update the current button timeout
                data = self.cycle()
                log.info("Button was pressed. sleeping for %f seconds. cycle %d"%(self.buttonLockoutCurrent, data))
                #if the button is pressed, we will lockout the button for
                #specifed timeout. We do this by just sleeping before checking the button again
                time.sleep(self.buttonLockoutCurrent)
                log.info("Button lockout expired")
            else:
                #sleep for 10 ms
                time.sleep(0.01)
                
        log.info("Button Monitor Done")
        
        
    def colorCycler(self):
        while(threading.get_ident() == self.colorThread.ident):
            #print(dir(threading.current_thread()))
            #add code here to check the button
            try:
                data = self.cycle()
            
                time.sleep(self.lightTimerCurrent)
                log.debug("Color Cycle data %s"%(data))
            except:
                self.playError()
                
        log.info("Color cycler Done")        

    '''
    When an error occures this resets the output to the error pattern
    and kicks off the playback
    '''
    def playError(self):
        pass

    def setNextState(self):
        
        #iterate over the list until we find a color to set
        while(True):
            nextValue = self.currentPattern.pop(0)
            
            #if we are a color, set the new color and return. 
            if nextValue in self.colors:
                color = self.colors[nextValue]
                red, green, blue = ledDriver.splitColor(color)
                
                self.currentColor = color
                ledManager.update(red,green,blue,self.fadeTimerCurrent)
                return color
            


def main():
    global game
    global ledManager
    global gpioButton
    log.info("Game Started")
    print(sys.argv)
    if len(sys.argv) < 2:
        log.error("Config file not given")
        return
        
    config = configReader.Configuration(sys.argv[1])

    #create led manager
    try:
        #led = APA102_Pi.apa102.APA102(**config.apa102)
        led = ledDriver.ledManagerTest()
    except:
        log.exception("Failed to create leds")
        return
        

    
    updateRateHz = config.getValue(config.app, 'updateRateHz', 100)
    
    
    ledManager = ledDriver.LedManager(updateRateHz,led)


    buttonGpio = int(config.getValue(config.app,'buttonGpio',9))
    #gpioButton = button.buttonGpio(buttonGpio)
    gpioButton = button.sampleButton()
    game = GameManager(ledManager, gpioButton, config)


if __name__ == "__main__":
    main()

    #time.sleep(120)
