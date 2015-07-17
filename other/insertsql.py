#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 15:57:18 2014

@author: marck
"""
"""
http://zetcode.com/db/sqlitepythontutorial/

sqlite> .mode column
sqlite> .header on
sqlite> select rowid,data,temp,hum from temps;
rowid       data                 temp        hum
----------  -------------------  ----------  ----------
1           2014-08-01 11:23:47  27,5        40,3
2           2014-08-01 11:23:50  27,5        40,3
3           2014-08-01 11:23:51  27,5        40,3


"""
import sqlite3 as lite
import sys
import time

try:
    con = lite.connect('temps.db')

    cur = con.cursor()
    # insert into temps(data, temp,uum) values("2014-08-01 11:10:00",'27,4','40,3');
    data = "INSERT INTO temps(data, temp, hum) VALUES (\"" + time.strftime("%Y-%m-%d %H:%M:%S") + "\",'27,5','40,3')"
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