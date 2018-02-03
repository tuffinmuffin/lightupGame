# -*- coding: utf-8 -*-

import logger
log = logger.getLogger()



import threading

import socket




class DashListener:
    
    def __init__(self, port, callback,interface = "", validSeq =['add', 'old']):
        self.port = port
        self.interface = interface
        self.callback = callback
        self.spawnListener()


    def spawnListener(self):
        self.dashSockThread = threading.Thread(target = self.socketListener, name = "dashSocketThread")
        self.dashSockThread.start()
        
    def socketListener(self):
        try:
            self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.socket.bind(('',self.port))
            
            while(threading.get_ident() == self.dashSockThread.ident):
                msg = self.socket.recvfrom(1024)
                message = str(msg[0], 'ascii')
                #print(dir(message))
                source = str(msg[1])
                log.info("Recieved '%s' from %s",message,source)
                #print(msg)
                self.callback(message)
        except Exception as err:
            log.exception("Socket error")
            return
            






def sampleCallback(msg):
    log.info("callback msg %s"%(msg))
    


if __name__ == '__main__':
    dashButton = DashListener(2000,sampleCallback)
