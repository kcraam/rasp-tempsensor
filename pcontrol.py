import random
import paho.mqtt.publish as publish
import time
import logging

logger = logging.getLogger('PSENSv0.1')

def pControl(org,place,brokerIP,clientId):
    logger.debug(pControl)
#    info('pControl')
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
