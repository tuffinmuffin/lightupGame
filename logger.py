# -*- coding: utf-8 -*-

import logging



log = logging.getLogger()
if not log.hasHandlers():
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler('log.txt')
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
