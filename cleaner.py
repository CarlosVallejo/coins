
#####
##
##	Script to clean my SQLite DB
##
#####


db = "/media/sf_VMFiles/coins/db.sqlite"


import sqlite3 as lite
import sys

con = lite.connect(db)

cur = con.cursor()
cur.execute("DELETE FROM `COIN_KM`")
cur.execute("DELETE FROM `COIN_COLLECTION`")
cur.execute("DELETE FROM `PACKS`")
con.commit()

print 'Done'

