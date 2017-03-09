#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
##
##	Script to convert my Packs table from Coin Collection (Excel format) into SQLite DB
##	SQLite DB must exist already
##
#####

import sqlite3 as lite
from pyeasy import OpenExcel


db = "/media/sf_VMFiles/coins/db.sqlite"
con = lite.connect(db)

f = OpenExcel('/media/sf_VMFiles/coins/test-coins3.xls')

def read_row_excel(i):
	data = f.read(i) #read row 
	# print data

	return data

def searcher_pack(id):

	try:
		with con:
			cur = con.cursor()
			
			#Select row without restrictions 
			cur.execute("SELECT ID_PACK FROM PACKS WHERE NAME is ? ",(id, ))

			return cur.fetchall()[0][0]
	except:
		return None

def main():
	for row in range(2,57):
		data = read_row_excel(row)
		#data[0] = Pack Name
		#data[1] = Countries
		#data[2] = Who
		#data[3] = Price
		#data[4] = What
		#data[5] = Date

		#BREAK IF EMPTLY ROW
		if not data[0]:
			break

		# #Joining all common entries
		# seq = ":"
		# if data[0] == "Regalo":
		# 	list = data[2], data[1], data[4]
		# 	print seq.join( list )

		who = data[2]
		cost = data[3]
		date = data[5]

		if len(data[1]) != 0 and len(data[4]) != 0:
			comment = data[1]+": "+data[4]
		elif len(data[1]) != 0 and len(data[4]) == 0:
			comment = data[1]
		elif len(data[1]) == 0 and len(data[4]) != 0:
			comment = data[4]
		else:
			comment = None
			

		id = searcher_pack(data[0])

		#Not entry in SQL DB
		if id is None:
			# insert new row sql
			with con:
				cur = con.cursor()
				cur.execute("INSERT INTO `PACKS`(NAME, DATE, COST, WHO, COMMENT) VALUES (?,?,?,?,?)", 	( data[0], date, cost, who, comment))
				con.commit()
		
		else:
			#add info in sql
			with con:
				cur = con.cursor()
				cur.execute("UPDATE PACKS SET DATE =?, COST =?, WHO=?, COMMENT=? WHERE ID_PACK = ?", (date, cost, who, comment, id))
				con.commit()


###########################################

main()