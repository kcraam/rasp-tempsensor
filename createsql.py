#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 15:57:18 2014

@author: marck
"""

# http://zetcode.com/db/sqlitepythontutorial/
import sqlite3 as lite
import sys

try:
    con = lite.connect('temps.db')

    cur = con.cursor()  

    cur.executescript("""
        DROP TABLE IF EXISTS temps;
        CREATE TABLE temps( data TEXT PRIMARY KEY, temp REAL, hum REAL );
        """)

    con.commit()
    
except lite.Error, e:
    
    if con:
        con.rollback()
        
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close() 