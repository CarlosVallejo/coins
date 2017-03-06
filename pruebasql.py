import sqlite3 as lite
import urllib2
from bs4 import BeautifulSoup
import re
import urllib
import time

db = "/media/sf_VMFiles/db.sqlite"
con = lite.connect(db)


with con:
	cur = con.cursor()
	cur.execute("UPDATE COIN_KM SET TITLE =? WHERE ID_KM = ?", ("IN3", 1))


	cur.execute('SELECT * FROM COIN_KM WHERE ID_KM = ?', (1,))
	print cur.fetchall()
	con.commit()