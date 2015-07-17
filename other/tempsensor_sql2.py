#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
#Created on Tue Jul 29 10:12:58 2014

#@author: mcollado
"""


import Adafruit_DHT
import time
import sqlite3 as lite
import sys
import ConfigParser
import os

# If ConfigParser code fails this values are hardcoded
# To be removed when code works
sensor = Adafruit_DHT.AM2302
pin = 4

config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.curdir,'tempsensor.cfg'))

# getfloat() raises an exception if the value is not a float
# getint() and getboolean() also do this for their respective types
sensor = config.get('Sensor', 'sensor')
pin = config.getint('Sensor', 'pin')

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).  
# If this happens try again!
if humidity is not None and temperature is not None:
     #print  time.strftime("%Y-%m-%d %H:%M:%S") + ' Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
     try:
        con = lite.connect('temps.db')

        cur = con.cursor()
        # insert into temps(data, temp,uum) values("2014-08-01 11:10:00",'27,4','40,3');
        data = "INSERT INTO temps(data, temp, hum) VALUES (\"" + time.strftime("%Y-%m-%d %H:%M:%S") + "\",'{0:0.1f}','{1:0.1f}')".format(temperature, humidity)
        print data
        cur.execute(data)

        con.commit()
     except lite.Error, e:
        if con:
            con.rollback()
            
        print "Error %s:" % e.args[0]
        sys.exit(1)
     finally:
        if con:
            con.close() 
          
else:
     print 'Failed to get reading. Try again!'
