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
        

        if 'btTimeout' in config.app:
            self.buttonLockoutDefault = config.app['btTimeout']
        else:
            log.info("No button timeout using default of 0")
            self.buttonLockoutDefault = 0.0
        self.buttonLockoutCurrent = self.buttonLockoutDefault
            

        if 'lightTimer' in config.app:
            self.lightTimerDefault = config.app['lightTimer']
        else:
            log.info("No light timer using default of 10.0")
            self.lightTimerDefault = 10.0
            
        self.lightTimerCurrent = self.lightTimerDefault;
            
        
        if 'fadeTimer' in config.app:
            self.fadeTimerDefault = config.app['fadeTimer']
        else:
            log.info("No fade timeout using default of 0.25")
            self.fadeTimerDefault = 0.25
            
        self.fadeTimerCurrent = self.fadeTimerDefault; 
        
        
        
        if 'buttonGpio' in config.app:
            self.buttonGpio = config.app['buttonGpio']
        else:
            log.info("Default button GPIO being used (4)")
            self.buttonGpio = 4

        
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
