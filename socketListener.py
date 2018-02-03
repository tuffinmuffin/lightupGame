# -*- coding: utf-8 -*-

import logger
log = logger.getLogger()



import threading

import socket




class DashListener:
    
    def __init__(self, port, callback, hostname, validSeq =['add', 'old'], interface = ""):
        self.port = port
        self.interface = interface
        self.callback = callback
        self.spawnListener()
        self.hostname = hostname
        self.validSeq = validSeq


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
                
                if(self.hostname in message):
                    #print("host found")
                    for name in self.validSeq:
                        #print("checking %s"%(name))
                        #goldfish has "old" so only look at first few chars
                        if name in message[:10]:
                            #print("Found Name in message")
                            self.callback(message, source)
                            break
                else:
                    log.info("host not found %s",self.hostname)    
        except Exception as err:
            log.exception("Socket error")
            self.socket.close()
            return
            






def sampleCallback(msg, source):
    log.info("callback msg %s"%(msg))
    


if __name__ == '__main__':
    dashButton = DashListener(2000,sampleCallback)
