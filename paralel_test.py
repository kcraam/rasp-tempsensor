#!/usr/bin/python
#-*- coding: utf-8 -*-
import paho.mqtt.publish as publish
from multiprocessing import Process
import time
import os
import logging
import random

# create logger
logger = logging.getLogger('PSENSv0.1')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def info(title):
    logger.debug(title)
    logger.debug('debug message')

    if hasattr(os, 'getppid'):  # only available on Unix
        logger.debug( 'parent process : %i', os.getppid())
    logger.debug( 'process id: %i', os.getpid())


def logon(org,place,brokerIP,clientId):
    logger.debug(logon)
    info('logon')
    while True:
        publish.single(org + "/" + place + "/" + "internal/status/logon" , "0", hostname = brokerIP, client_id= clientId, will=None, auth=None,tls=None)
        logger.debug('Sleeping 6 sec')
        time.sleep(1) #seconds
        if random.randint(0,5) == 1:
            break


def broker(org,place,brokerIP,clientId):
    logger.debug(broker)
    info('broker')
    while True:
        publish.single(org + "/" + place + "/" + "internal/status/publish" , "0", hostname = brokerIP, client_id= clientId, will=None, auth=None,tls=None)
        logger.debug('Sleeping 12 sec')
        time.sleep(1.5) #seconds

if __name__ == '__main__':
    info('main line')
    p = Process(target=logon, args=('sens.solutions','pool','84.88.95.122','Raspi1'))
    p.start()


    o = Process(target=broker, args=('sens.solutions','pool','84.88.95.122','Raspi2'))
    o.start()

    while True:
        if not p.is_alive():
           logger.warning('logon is DEAD - Restarting-it')
           p.terminate()
           p.run()
           time.sleep(0.5)
           logger.warning( "New PID: " + str(p.pid))

        if o.is_alive():
           pass
           #logger.debug('broker is alive? %s',str(o.is_alive()))
        else:
           logger.warning('broker is DEAD - Restarting-it')
           o.start()

    p.join()
    o.join()
