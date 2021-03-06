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
import socketListener


class GameManager:
    
    def __init__(self, ledManager, button, config):
        self.ledManager = ledManager
        self.config = config
        self.button = button
        
        self.syncLockout = 10
	#wait 10 seconds for boot
        self.syncLast = time.time()
        
        self.running = False

        self.buttonLockoutCurrent = self.buttonLockoutDefault = config.getValue(config.app,'btTimeout',0.0)
            
        self.lightTimerCurrent = self.lightTimerDefault = config.getValue(config.app,'lightTimer',10.0)
                     
        self.fadeTimerCurrent = self.fadeTimerDefault = config.getValue(config.app,'fadeTimer',0.25)
        
        
        self.colors = config.colors
        
        self.patterns = config.patterns

        #self.reset()
        self.ledManager.update(255,255,255,0.0)
        time.sleep(2)
        self.ledManager.update(0,0,255,0)
        time.sleep(2)
        self.ledManager.update(0,0,0,1.0)
        
        
        
        
    '''
    creates tasks for timer and buttons
    this can be used to create new tasks or mark
    the current ones to go away
    '''
    def _createTasks(self):
        self.buttonThread = threading.Thread(target = self.buttonMonitor, name = "buttonMonitor", daemon=True)
        self.colorThread = threading.Thread(target = self.colorCycler, name = "Color Cycler", daemon=False)
        
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
    reset the counter and resets sequence to init
    '''
    def reset(self):
        self._createTasks()
        
        
        
        #reset data
        self.currentPatternName = 'init'
        #get a copy of the pattern so we can pop from it.
        self.currentPattern = self.patterns['init'].copy()  
        
        
        self.buttonThread.start()
        self.colorThread.start()
        self.running = True
    
    def shutdown(self):
        self._createTasks()

        self.ledManager.update(0,0,0,1.0)
        self.running = False
    
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
                log.debug("Color Cycle data %s sleep %f"%(data, self.lightTimerCurrent))
                time.sleep(self.lightTimerCurrent)
            except:
                log.exception("Color cycle error")
                self.playError()
                return
                
        log.info("Color cycler Done")        

    '''
    When an error occures this resets the output to the error pattern
    and kicks off the playback
    '''
    def playError(self):
        #disable the button
        if(self.buttonThread):
            self.buttonThread._delete()
        #brute force the error message
        self.currentPatternName = "error"
        self.currentPattern = self.patterns['error'].copy()
        print(self.currentPattern)
        
        while(len(self.currentPattern) != 0):
            self.setNextState();
            time.sleep(self.lightTimerCurrent);
            self.lightTimerCurrent = self.lightTimerDefault

    def setNextState(self):
        
        #iterate over the list until we find a color to set
        while(True):
            nextValue = self.currentPattern.pop(0)
            log.debug("Popped %s"%(nextValue))
            
            #if we are a color, set the new color and return. 
            if nextValue in self.colors:
                color = self.colors[nextValue]
                red, green, blue = ledDriver.splitColor(color)
                
                self.currentColor = color
                ledManager.update(red,green,blue,self.fadeTimerCurrent)
                return color
            
            if nextValue == 'repeat':
                log.info("%s pattern: repeating"%(self.currentPatternName))
                self.currentPattern = self.patterns[self.currentPatternName].copy()
                continue
                
            if "=" in nextValue:
                splits = nextValue.split("=")
                name = splits[0]
                value = splits[1]
                
                if name == "goto":
                    log.info("goto:%s"%(nextValue))
                    self.currentPatternName = value
                    self.currentPattern = self.patterns[value].copy()
                    continue
                if name == 'timer':
                    log.info('timer:%s'%(nextValue))
                    self.lightTimerCurrent = float(value)
                    continue
                if name == 'setTimer':
                    log.info("setTimer:%s"%(nextValue))
                    self.lightTimerCurrent = self.lightTimerDefault = float(value)
                    continue
                if name == 'fade':
                    log.info('fade:%s'%(nextValue))
                    self.fadeTimerCurrent = float(value)
                    continue
                if name == 'fadeTimer':
                    log.info("fadeTimer:%s"%(nextValue))
                    self.fadeTimerCurrent = self.fadeTimerDefault = float(value)
                    continue
            log.warning("Unknown command %s"%(nextValue))
            
            
    def syncListener(self, msg, source):
        currentTime = time.time()

        log.info("sync recieved at %s. msg %s.", currentTime, msg)
        
        if (self.syncLockout + self.syncLast) < currentTime:
            if(self.running):
                log.info("Stopping patterns and entering standby")
                self.shutdown()
            else:
                log.info("starting patterns and timers")
                self.reset()
            self.syncLast = currentTime            
        else:
            log.info("sync lockout not met ignoring message %f + %f < %f", self.syncLockout, self.syncLast, currentTime)
        


def main():
    global game
    global ledManager
    global gpioButton
    log.info("Game Started")
    sim = False
    print(sys.argv)
    if len(sys.argv) < 2:
        log.error("Config file not given")
        return
        
    for i in sys.argv:
        if i == "sim":
            sim = True
            log.info("Enabling SIM")
    config = configReader.Configuration(sys.argv[1])    
    
    updateRateHz = config.getValue(config.app, 'updateRateHz', 100)

    buttonGpio = int(config.getValue(config.app,'buttonGpio',9))


    dashName = config.getValue(config.network,'dashName', '')
    socketForNotification = int(config.getValue(config.network, 'socketForNotification', 2000))
    
    if not sim:
        gpioButton = button.buttonGpio(buttonGpio)
        #create led manager
        try:
            led = APA102_Pi.apa102.APA102(**config.apa102)
        except:
            log.exception("Failed to create leds")
            return        
    else:
        gpioButton = button.sampleButton()
        led = ledDriver.ledManagerTest()
        
        
        
    ledManager = ledDriver.LedManager(updateRateHz,led)
    

    game = GameManager(ledManager, gpioButton, config)

    dashListener = socketListener.DashListener(socketForNotification, game.syncListener, dashName)

if __name__ == "__main__":
    main()

    #time.sleep(120)
