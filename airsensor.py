import Adafruit_DHT
import datetime
import random
import paho.mqtt.publish as publish
import time
import logging
from ConfigParser import SafeConfigParser

logger = logging.getLogger('PSENSv0.1')


def airSensor(org,place,brokerIP,clientId,cfgfile):
    logger.debug(airSensor)

    Config = SafeConfigParser()
    #Config.read("tempsensor.cfg")
    Config.read(cfgfile)
    
    topic      = Config.get('Broker', 'topic') 
    sensorType = Config.getint('Sensor', 'sensor')
    sensorName = Config.get('Sensor', 'sensor_name')
    pin        = Config.getint('Sensor', 'pin')
    sensorTemp = Config.get('Broker', 'sensor_temp')
    sensorHum  = Config.get('Broker', 'sensor_hum')
    sleepTime  = Config.getfloat('Broker', 'sleep_time')
    writeLog   = Config.getboolean('Log','write_log')
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
        logger.warning("Error: No topic")

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
