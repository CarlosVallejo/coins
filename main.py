#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
##
##	Script to convert my Coin Collection (Excel format) into SQLite DB
##	SQLite DB must exist already
##
#####


from __future__ import unicode_literals

from pyeasy import OpenExcel
import sqlite3 as lite
import sys

db = "/media/sf_VMFiles/coins/db.sqlite"
con = lite.connect(db)

f = OpenExcel('/media/sf_VMFiles/coins/test-coins3.xls')

#FUNTION ADD NEW ROW IN PACK TABLE
def add_row_pack(comment, element = None):
	cur.execute("INSERT INTO `PACKS`(`NAME`,`COMMENT`) VALUES (?,?)", 
	( element, comment))
	cur.execute("SELECT last_insert_rowid()")
	id_pack = cur.fetchall()[0][0]
	con.commit()
	return id_pack

#READ EXCEL FILE ROW BY ROW
initial_row = 2
final_row = 1400
actual_row = initial_row
for row in range(initial_row, final_row):
	message = "Debuggeando, processing row:"+str(actual_row)
	sys.stdout.write("%s\r" %message)
	sys.stdout.flush()
	# print "Debuggeando, processing row:", actual_row
	actual_row += 1
	data = f.read(row) #read row 
	# print data[0], data[2] 

	#BREAK IF EMPTLY ROW
	if not data[0]:
		break


	#INSERT NEW ROW IN KM TABLE
	with con:
		d = ['ID_KM', data[0], data[1], data[2], data[4], data[5], None]

		cur = con.cursor()
		cur.execute("INSERT INTO `COIN_KM`(`COUNTRY`,`DENOMINATION`,`KM`,`DESCRIPTION`,`MATERIAL`,`COLLECTION`) VALUES (?,?,?,?,?,?)", 
				( d[1],d[2], d[3], d[4], d[5], d[6]))
		cur.execute("SELECT last_insert_rowid()")
		last_row = cur.fetchall()
		last_row_km = last_row[0][0]
		con.commit()
		# print "ID KM:", last_row_km
		
		


		#TAKE PROCENCENDIA and split by &, we have list
		pro_list = []
		for procecencia in data[6].split('&'):
			pro_list.append( procecencia.strip() )
		pro_comment = data[8].split('&')

		# print pro_list, len(pro_list[0])
		# print pro_comment, len(pro_comment[0])

		pack_ID_list = []

		if len(pro_list[0]) == 0:
			if len(pro_comment[0]) > 0:
				for ePACK in pro_comment:
					pack_ID_list.append(add_row_pack(ePACK))
			elif len(pro_comment[0]) == 0:
				pass
				
		else:
			position = 0
			for element in pro_list:
				if element == '':
					pack_ID_list.append(add_row_pack(pro_comment[position]))
				else:
					cur.execute("SELECT `ID_PACK` FROM `PACKS` WHERE `NAME`= ?", (element,))
					id_pack_raw = cur.fetchall()

					if len(id_pack_raw) == 0 :
						try:
							pack_ID_list.append(add_row_pack(pro_comment[position], pro_list[position]) )
						except:
							pack_ID_list.append(add_row_pack(None, pro_list[position]) )
					else:
						pack_ID_list.append( id_pack_raw[0][0] )
				position +=1


		# print "IDs for packs:", pack_ID_list
		# print "List of years:",data[10]

		if type(data[10]) is float:
			data[10] = str(int(data[10]))

		ix = 0
		pack_for_anno = None
		amount_years = len(data[10].split(' '))

		for anno in data[10].split(' '):
			try:
				pack_for_anno = pack_ID_list[ix]
			except:
				pass

			ix += 1
			# print anno, pack_for_anno

			#CHECK TOSWAP
			# print "col 11:", data[11], type(data[11])

			if type(data[11]) is float:
				inAlbum = str(int(data[11]))
			else:
				inAlbum = data[11]

			# print "In album is this year:",inAlbum
			# print "This coin is from:", anno

			if inAlbum == anno:
				toswap_boolean = 0
			else:
				toswap_boolean = 1

			if amount_years == 1:
				toswap_boolean =0

			# print "Coin to swap:",toswap_boolean


			### coin = [ idcoin, idkm, year, comment, toswap, fromwhere, where]
			### 
			#START ADDING COINS TO COIN COLLECTION
			# idcoin
			# idkm == last_row_km
			# year == anno
			# comment == data[12]
			# toswap == toswap_boolean
			# fromwhere == pack_for_anno
			# where

			cur.execute("INSERT INTO `COIN_COLLECTION`(`ID_KM`,`YEAR`, `COMMENT`, `TOSWAP`,`FROMPACK`) VALUES (?,?,?,?,?)", 
			( last_row_km, anno, data[12], toswap_boolean, pack_for_anno ))
		con.commit()






		#if not exist or name = "", insert row in pack table (colum J => Packs.comment)
		#take pack_ID for each element, save in a list

		# all_years = data[10]
		# # print all_years

		# #INSERT NEW ROW IN PIECE TABLE
		# for year in all_years.split(' '):
		# 	print year
		# 	#TODO: for each row, in fromwhere add one ID from the previous list
		# 	cur.execute("INSERT INTO `COIN_PIECE`(`ID_KM`,`YEAR`, `COMMENT`, `FROMWHERE`) VALUES (?,?,?,?)", 
		# 		( last_row_km, year, "fool", None ))

		# print '-------------------'
print ("\nDone")

