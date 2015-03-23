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

import Adafruit_DHT
import time
import sqlite3 as lite
import sys
import paho.mqtt.publish as publish
import datetime
import random


# mqtt broker info:
#broker = "192.168.2.69"
broker = "192.168.1.30"
clientid="Silmak/"+str(random.randint(1000,9999))
sensorTemp="Estudi/temp/1"
sensorHum="Estudi/hum/1"

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT22, or Adafruit_DTH.AM2302.
sensor = Adafruit_DHT.AM2302

# Example using a Raspberry Pi with DHT sensor
# connected to pin 23.
pin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).  
# If this happens try again!
if humidity is not None and temperature is not None:
     #print  time.strftime("%Y-%m-%d %H:%M:%S") + ' Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
#     try:
#        con = lite.connect('temps.db')
#
#        cur = con.cursor()
#        # insert into temps(data, temp,uum) values("2014-08-01 11:10:00",'27,4','40,3');
#        data = "INSERT INTO temps(data, temp, hum) VALUES (\"" + time.strftime("%Y-%m-%d %H:%M:%S") + "\",'{0:0.1f}','{1:0.1f}')".format(temperature, humidity)
#        print data
#        cur.execute(data)
#
#        con.commit()
#     except lite.Error, e:
#        if con:
#            con.rollback()
#            
#        print "Error %s:" % e.args[0]
#        sys.exit(1)
#     finally:
#        if con:
#            con.close() 
#          
#else:
#     print 'Failed to get reading. Try again!'

        while True:
            now = datetime.datetime.now()
            hora = now.strftime("%Y-%m-%d %H:%M:%S")
        
            print broker + " | " + clientId + " | " + hora + " : " + temperature +"C " + humidity + "%"
        
            publish.single(sensorTemp, temperature, hostname = broker, client_id= clientId, will=None, auth=None, tls=None)
            publish.single(sensorHum, humidity, hostname = broker, client_id= clientId, will=None, auth=None, tls=None)
        
        
            time.sleep(5)
else:
        print "Failed to get reading. Try again!"
        time.sleep(5)
