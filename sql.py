#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
##
##	Script to create/modificate the SQL DB
##
#####

db = "/media/sf_VMFiles/coins/db.sqlite"


import sqlite3 as lite
import sys

con = lite.connect(db)


### INSERT ROW IN KM
def insert_row_km():
	with con:
		d = [5, 'Country DDD', None, '142', 'desc', 'mat', None]

		cur = con.cursor()
		cur.execute("INSERT INTO `COIN_KM`(`COUNTRY`,`DENOMINATION`,`KM`,`DESCRIPTION`,`MATERIAL`,`COLLECTION`) VALUES (?,?,?,?,?,?)", 
				( d[1],d[2], d[3], d[4], d[5], d[6]))
		cur.execute("SELECT last_insert_rowid()")
		last_row = cur.fetchall()
		print last_row[0][0]
		con.commit()

###SPLIT COLUMN KM INTO KM_SYSTEM AND KM_NUM
def split_col_KM():
	with con:
		cur = con.cursor()    
		local_id_km = 1

		for row in range(local_id_km, 1400):

			# message = "Debuggeando, processing row:"+str(local_id_km)
			# sys.stdout.write("%s\r" %message)
			# sys.stdout.flush()

			cur.execute("SELECT KM FROM COIN_KM WHERE ID_KM = ? ", (local_id_km,))
			row = cur.fetchall()
			print row[0][0]

			if row[0][0][0] in ['Y', 'K']:
				try:
					km_sys = row[0][0].split(' ')[0]
					km_num = row[0][0].split(' ')[1]

				## trick to avoid problems with encoding
				except:
					if row[0][0][0] is 'Y':
						km_sys = "Y#"
					else:
						km_sys = "KM#"
					km_num = row[0][0].split('#')[1][1:]

				cur.execute("UPDATE COIN_KM SET KM_SYSTEM = ?, KM_NUM =? WHERE ID_KM = ?", (km_sys, km_num, local_id_km))
				con.commit()

				
				# print km_sys, km_num



			local_id_km +=1
		

split_col_KM()

###
def read_km():
	with con:
		cur = con.cursor()    
		cur.execute("SELECT rowid, ID_KM, KM FROM COIN_KM ORDER BY KM")
		rows = cur.fetchall()
		for row in rows:
			print row

def insert_pack():
	with con:
		pack = ['id', 'namepack', 'date', 'cost', 'who', None]
		cur = con.cursor()
		print last_row[0][0], coin[2], coin[3], coin[4], coin[5], coin[6]
		cur.execute("INSERT INTO `COIN_PIECE`(`ID_KM`, `YEAR`, `COMMENT`, `TOSWAP`, `FROMWHERE`, `WHERE`) VALUES (?,?,?,?,?,?)", 
				(last_row[0][0], coin[2], coin[3], coin[4], coin[5], coin[6]))
		con.commit()


#inser row in coin
def insert_coin():
	with con:
		coin = ['id', 'idkm', '1987', None, 0, None, None]
		cur = con.cursor()
		print last_row[0][0], coin[2], coin[3], coin[4], coin[5], coin[6]
		cur.execute("INSERT INTO `COIN_PIECE`(`ID_KM`, `YEAR`, `COMMENT`, `TOSWAP`, `FROMWHERE`, `WHERE`) VALUES (?,?,?,?,?,?)", 
				(last_row[0][0], coin[2], coin[3], coin[4], coin[5], coin[6]))
		con.commit()
    

def create_view():
	with con:
		cur = con.cursor()
		# cur.execute("SELECT ID_KM FROM COIN_COLLECTION WHERE YEAR = ? ", ("",))
		cur.execute("SELECT COIN_COLLECTION.ID_KM, COIN_COLLECTION.ID_COINS, COIN_KM.COUNTRY, COIN_KM.KM FROM COIN_COLLECTION JOIN COIN_KM ON COIN_COLLECTION.ID_KM = COIN_KM.ID_KM WHERE COIN_COLLECTION.YEAR = ? ",
		 ("1996",))

		
		for row in cur.fetchall():
			print row

def printer():
	import sys
	import time

	for i in range(10):
		sys.stdout.write("\r{0}>".format("="*i))
		sys.stdout.flush()
		time.sleep(0.5)





# SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT
#         ON COMPANY.ID = DEPARTMENT.EMP_ID
#    UNION
#      SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
#         ON COMPANY.ID = DEPARTMENT.EMP_ID;