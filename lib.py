#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
##
##	Library with all the defitions used
##
#####


import sqlite3 as lite

db = "/media/sf_VMFiles/db.sqlite"
con = lite.connect(db)

#ADD NEW PACK IN DB
def add_new_pack(i):
	#Input: i[4]
	#Output: Last row inserted

	with con:

		cur = con.cursor()
		cur.execute("INSERT INTO PACKS (NAME, DATE, COST, WHO, COMMENT) VALUES (?,?,?,?,?)", (i[0], i[1], i[2], i[3], i[4]) )
		cur.execute("SELECT last_insert_rowid()")
		id = cur.fetchall()[0][0]
		con.commit()

		return id

#ADD NEW COIN IN COIN_COLLETION DB
def add_coin_colletion(i):
	#Input: i[5]
	#Output: None
	with con:

		cur = con.cursor()
		cur.execute("INSERT INTO `COIN_COLLECTION`(`ID_KM`,`YEAR`, `COMMENT`, `TOSWAP`,`FROMPACK`, LOCATION) VALUES (?,?,?,?,?)", 
				(i[0], i[1], i[2], i[3], i[4], i[5] ))
		con.commit()


####
#END
####