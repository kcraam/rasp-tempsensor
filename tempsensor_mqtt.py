#!/usr/bin/python
# -*- coding: utf-8 -*-
#"""
#created on Tue Jul 29 10:12:58 2014

#@author: mcollado
#"""

# permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# the above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# the sOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# impliED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# fitneSS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# authoRS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# liabiLITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# out oF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# softwARE.

# https://www.eclipse.org/paho/clients/python/docs/

# TODO
# * Add protection from sensor error readings (Â X % last value)
# * Move settings to a external file
# ** https://wiki.python.org/moin/ConfigParserExamples
# * Capture signal handling (^C and friends)
# * Write logs somewhere?
# * Daemonize?


import Adafruit_DHT
import time
import paho.mqtt.publish as publish
import datetime
import random
import ConfigParser
from ConfigParser import SafeConfigParser

Config = SafeConfigParser()
Config.read("tempsensor.cfg")


sensorType = Config.getint('Sensor', 'sensor')
sensorName = Config.get('Sensor', 'sensor_name')
pin        = Config.getint('Sensor', 'pin')

brokerIP   = Config.get('Broker', 'broker_ip')
clientId   = Config.get('Broker', 'client_id') + "/" +  str(random.randint(1000,9999))
sensorTemp = Config.get('Broker', 'sensor_temp')
sensorHum  = Config.get('Broker', 'sensor_hum')
sleepTime  = Config.getfloat('Broker', 'sleep_time')

writeLog   = Config.getboolean('Log','write_log')
#logName    = ConfigSectionMap("Log")['logname']
logName    = Config.get('Log', 'logname')


#
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

            publish.single(sensorTemp, temperature, hostname = brokerIP, client_id= clientId, will=None, auth=None, tls=None)
            publish.single(sensorHum, humidity, hostname = brokerIP, client_id= clientId, will=None, auth=None, tls=None)

            if (writeLog) :
                with open(logName, 'a') as logfile:
                    logfile.write(log)

            time.sleep(sleepTime)
        else:
            print "Failed to get reading. Try again!"
            time.sleep(sleepTime)
