# -*- coding: utf-8 -*-

import logging
import logging.handlers


log = logging.getLogger()
if not log.hasHandlers():
    log.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler("/var/log/gameLog.log", mode='a', maxBytes=1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
    #fh = logging.FileHandler('log.txt')
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    
    formatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    #print(fh)
    #print(ch)
    log.addHandler(fh)
    log.addHandler(ch)
else:
    log.info("Logging already inited")

def getLogger():
    return log

#log.info("test")
