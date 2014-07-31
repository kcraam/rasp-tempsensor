#!/usr/bin/python
# -*- coding: utf-8 -*-

from bsddb3 import db                   # the Berkeley db data base
import time

# Part 1: Create database and insert 4 elements
#
filename = 'fruit.db'

# Get an instance of BerkeleyDB 
fruitDB = db.DB()
# Create a database in file "fruit" with a Hash access method
# 	There are also, B+tree and Recno access methods
fruitDB.open(filename, None, db.DB_HASH, db.DB_CREATE)

# Print version information
print '\t', db.DB_VERSION_STRING

# Insert new elements in database 
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

fruitDB.put(timestamp,"apple","red")

timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
fruitDB.put(timestamp,"orange","orange")
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
fruitDB.put(timestamp,"banana","yellow")
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
fruitDB.put(timestamp,"tomato","red")

# Close database
fruitDB.close()

# Part 2: Open database and write its contents out
#
fruitDB = db.DB()
# Open database
#	Access method: Hash
#	set isolation level to "dirty read (read uncommited)"
fruitDB.open(filename, None, db.DB_HASH, db.DB_DIRTY_READ)

# get database cursor and print out database content
cursor = fruitDB.cursor()
rec = cursor.first()
while rec:
        print rec
        rec = cursor.next()
fruitDB.close()

