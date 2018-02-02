# -*- coding: utf-8 -*-

import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
#print(fh)
#print(ch)
log.addHandler(fh)
log.addHandler(ch)


def getLogger():
    return log

#log.info("test")