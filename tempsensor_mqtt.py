#!/usr/bin/python
#-*- coding: utf-8 -*-
import Adafruit_DHT
import datetime
import random
import ConfigParser
from ConfigParser import SafeConfigParser
import sys
import paho.mqtt.publish as publish
from multiprocessing import Process
import time
import os
import logging

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

if len(sys.argv) > 2:
    print "Too much arguments"
    print "Usage " + str(sys.argv[0]) + "configuration.conf"
else:
    cfgfile= str(sys.argv[1])

Config = SafeConfigParser()
Config.read("tempsensor.cfg")


sensorType = Config.getint('Sensor', 'sensor')
sensorName = Config.get('Sensor', 'sensor_name')
pin        = Config.getint('Sensor', 'pin')

brokerIP   = Config.get('Broker', 'broker_ip')
clientId   = Config.get('Broker', 'client_id') + "/" +  str(random.randint(1000,9999))
topic      = Config.get('Broker', 'topic')
sensorTemp = Config.get('Broker', 'sensor_temp')
sensorHum  = Config.get('Broker', 'sensor_hum')
sleepTime  = Config.getfloat('Broker', 'sleep_time')

writeLog   = Config.getboolean('Log','write_log')
#logName    = ConfigSectionMap("Log")['logname']
logName    = Config.get('Log', 'logname')

try:
    #sens.solutions/pool/sensors/air/humidity
    parts = topic.split('/')
    org = parts[0]
    place = parts[1]
    what = parts[2]
except:
    org = 'unknown'
    place = 'unknown'
    what = 'unknow'
# IMplementing connexion debugging



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
        try:
            login = publish.single(org + "/" + place + "/" + "internal/status/ErrorCode" , "0", hostname = brokerIP, client_id= clientId, will=None, auth=None, tls=None)
            logger.debug( org + "/" + place + "/" + "internal/status/ErrorCode = 0")
            if (login) :
                logger.debug(login)
                #with open(logName, 'a') as logfile:
                #    logfile.write(logon + "\n")
        except:
            logger.warning("Connecting Error")
        time.sleep(30)


def mesure(org,place,brokerIP,clientId):
    logger.debug(mesure)
    info('mesure')

    while True:
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
            humidity, temperature = Adafruit_DHT.read_retry(sensorType, pin)
    
    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).  
    # If this happens try again!
            if humidity is not None and temperature is not None:
    
                now = datetime.datetime.now()
                hora = now.strftime("%Y-%m-%d %H:%M:%S")
    
                log = hora + " | " + clientId + " | " + brokerIP + " : " + sensorTemp + "/" + str(temperature) +" C " + sensorHum + "/" + str(humidity) + " %\n"
                tjson = '{ "org" : "' + org + '", "place" : "' + place + '", "what" : "' + what + '", "sensor" : "' + sensorName + '", "type" : "temperature", "value" : ' + str(round(temperature,2)) + ',  "timestamp" : "' + hora + '" }'
                hjson = '{ "org" : "' + org + '", "place" : "' + place + '", "what" : "' + what + '", "sensor" : "' + sensorName + '", "type" : "humidity", "value" : ' + str(round(humidity,2)) + ', "timestamp" : "' + hora + '" }'
    
    #
                logger.debug(tjson)
                logger.debug(hjson)
    #
    
                publish.single(topic + sensorName + "/temperature" , tjson, hostname = brokerIP, client_id= clientId, will=None, auth=None, tls=None)
                publish.single(topic + sensorName + "/humidity" , hjson, hostname = brokerIP, client_id= clientId, will=None, auth=None, tls=None)
    
                if (writeLog) :
                    with open(logName, 'a') as logfile:
                        logfile.write(tjson + "\n" + hjson + "\n")
    
                time.sleep(sleepTime)
            else:
                logger.warning( "Failed to get reading. Try again!")
                time.sleep(sleepTime)

#
#
#

def broker(org,place,brokerIP,clientId):
    logger.debug(broker)
    info('broker')
    while True:
        publish.single(org + "/" + place + "/" + "internal/status/publish" , "0", hostname = brokerIP, client_id= clientId, will=None, auth=None,tls=None)
        logger.debug('Sleeping 12 sec')
        time.sleep(12) #seconds




if __name__ == '__main__':
    logger.debug('Starting Main')
    info('main line')
    #p = Process(target=logon, args=('sens.solutions','pool','84.88.95.122','Raspi1'))
    p = Process(target=logon, args=(org,place,brokerIP,clientId))
    p.start()

    #o = Process(target=mesure, args=('sens.solutions','pool','84.88.95.122','Raspi2'))
    o = Process(target=mesure, args=(org,place,brokerIP,clientId))
    o.start()

    p.join()
    o.join()
