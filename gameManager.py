# -*- coding: utf-8 -*-
import logger
log = logger.getLogger()

import ledDriver

import configReader

import time
import sys
import APA102_Pi

import threading

class GameManager:
    
    def __init__(self, ledManager, config):
        self.ledManager = ledManager
        self.config = config
        

        self.buttonLockoutCurrent = self.buttonLockoutDefault = config.getValue(config.app,'btTimeout',0.0)
            
        self.lightTimerCurrent = self.lightTimerDefault = config.getValue(config.app,'lightTimer',10.0)
                     
        self.fadeTimerCurrent = self.fadeTimerDefault = config.getValue(config.app,'fadeTimer',0.25)
        
        self.buttonGpio = config.getValue(config.app,'buttonGpio',4)

        
        self.buttonThread = threading.Thread(target = self.buttonMonitor, name = "buttonMonitor", daemon=True)
        self.buttonThread.start()
        
    '''
    cycles to the next element without changing timers
    '''
    def cycle(self):
        pass
    
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
        pass
    
    
    def buttonMonitor(self):
        while(threading.get_ident() == self.buttonThread.ident):
            #print(dir(threading.current_thread()))
            #add code here to check the button
            state = getButtonStatus(self.buttonGpio)
            
            #if button is pressed
            if state:
                #reload default timeout incase it was updated
                
                self.buttonLockoutCurrent = self.buttonLockoutDefault
                
                #call cycle. This may update the current button timeout
                self.cycle()
                log.info("Button was pressed. sleeping for %f seconds"%(self.buttonLockoutCurrent))
                #if the button is pressed, we will lockout the button for
                #specifed timeout. We do this by just sleeping before checking the button again
                time.sleep(self.buttonLockoutCurrent)
                log.info("Button lockout expired")
            else:
                #sleep for 10 ms
                time.sleep(0.01)
                
        log.info("Button Monitor Done")
        



test1 = False

def getButtonStatus(gpio):
    global test1
    if test1:
        test1 = False
        return True
    return False



def main():
    global game
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
        

    if 'updateRateHz' in config.app:
        updateRateHz = config.app['updateRateHz']
    else:
        print(config.app)
        log.info("unable to find updateRateHz in config. Using default")
        #default
        updateRateHz = 100
    
    ledManager = ledDriver.LedManager(updateRateHz,led)
    
    game = GameManager(ledManager,config)


if __name__ == "__main__":
    main()
