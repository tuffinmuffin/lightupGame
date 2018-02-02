# -*- coding: utf-8 -*-

import queue

import threading

import time

from APA102_Pi import apa102 

import logger
log = logger.getLogger()

class Queue(queue.Queue):
  '''
  A custom queue subclass that provides a :meth:`clear` method.
  '''

  def clear(self):
    '''
    Clears all items from the queue.
    '''

    with self.mutex:
      unfinished = self.unfinished_tasks - len(self.queue)
      if unfinished <= 0:
        if unfinished < 0:
          raise ValueError('task_done() called too many times')
        self.all_tasks_done.notify_all()
      self.unfinished_tasks = unfinished
      self.queue.clear()
      self.not_full.notify_all()
      
      





class ledManagerTest:
    num_led = 5;
    
    def set_pixel(self, led_num, red, green, blue, bright_percent=100):
        #print("setting pixels led %d: %d %d %d"%(led_num,red,green,blue))
        pass
    def show(self):
        pass



class LedManager:
    
    def __init__(self, updateFreq, ledController):
        self.updateFreq = updateFreq
        self.updatePeriod = 1 / self.updateFreq
        self.leds = ledController
        self.queue = Queue()
        self.currentColor = buildColorDict(0,0,0)
        
        self.ledWriterThread = threading.Thread(target = self.ledWriter, name = "ledThreadWriter")
        self.ledWriterThread.setDaemon(True)
        self.ledWriterThread.start()
        


    def ledWriter(self):
        sleepTime = self.updatePeriod
        while(True):
            startTime = time.clock()
            
            for led in range(self.leds.num_led):
                self.leds.set_pixel(led, **self.currentColor)
            self.leds.show()
            endTime = time.clock()
            
            delay = sleepTime - (endTime - startTime)
            if delay < 0:
                log.debug("Timer slipped by %f s"%(delay))
                delay = 0
                
            try:
                #sleep to sync times
                time.sleep(delay)
                #get next color, if there isn't one ready then we go ahead and write last color
                self.currentColor = self.queue.get(False)
                print("new color %s"%(str(self.currentColor)))
            except:
                pass
            #loop back to top and write the current Color
            
            
            
    def update(self, red, green, blue, transTime, bright_percent = 100.0):
        #stop animation
        self.queue.clear()
        
        colorList = buildColorDict(red,green,blue, bright_percent)
        for key in self.currentColor:
            colorList[key] = generateSteps(self.currentColor[key], colorList[key], self.updateFreq,transTime)
        
        for i in range(len(colorList['green'])):
            colorStep = {}
            for key in colorList:
                colorStep[key] = colorList[key][i]
            self.queue.put(colorStep)
        
        
    



def buildColorDict(red,green,blue, bright_percent = 100):
    return {'red':red,'green':green,'blue':blue,'bright_percent':bright_percent}


def generateSteps(start, stop, freq, duration):
    samples = int(freq * duration)
    step = (stop - start) / samples
    output = []
    for i in range(samples):
        output.append(int(start + step * (1+i) + 0.5))
        
    return output

if __name__ == "__main__":
    ledTest = ledManagerTest()
    ledManager = LedManager(200,ledTest)
    ledManager.update(100,100,102,.1)
    time.sleep(.05)
    ledManager.update(0,0,0,.1)