#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
##
##	Script to fill data missed in SQL
##	Version 2.0
##
##	Scrap info from Numismaster and Numista websites
##
#####

import sqlite3 as lite
import urllib2
from bs4 import BeautifulSoup
import re
import urllib
import time

db = "/media/sf_VMFiles/db.sqlite"
con = lite.connect(db)


#Search the coin (by KM) in our SQL DB
def searcher_coin(id):

	try:
		with con:
			cur = con.cursor()
			
			#Select row without restrictions 
			cur.execute("SELECT ID_KM, COUNTRY, KM_SYSTEM, KM_NUM, ID_NUMISTA, DDATE, DENOMINATION, TITLE, DESCRIPTION, PHOTO, MATERIAL FROM COIN_KM WHERE ID_KM is ? ",(id, ))

			return cur.fetchall()[0]
	except:
		return None

#Beatifulsoup funtion necesary to scrapt the website
def giveme_soup(web):

	page = urllib2.urlopen(web)
	soup = BeautifulSoup(page)
	return soup

#Create the link to numismaster, Input: Country, Value, KM System, KM Number
def link_creator(country, value, km_sys, km_num):
	country = country.replace(" ", "%20")  #replace emptly spaces by "%20" to avoid problems with urllib
	
	if value[:2] == "1 ":
		value = value.replace("1 ", "")

	value_list = value.split(' ', 1)

	if len(value_list) == 2:
		value = value.replace(" ", "%20") 
	else:
		value = value_list[0].replace(" ", "%20")

	return "http://secure.numismaster.com/ta/Coins.admin?rnd=SMSXJXBC&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=YRELZ&Origin=3&AdvanceSearch=0&PRefine=&Country=" + country + "&Denom=" + value + "&CountryId=&DenomId=&KM=" + km_num + "&Comp=&Date="

#Scrap the website looking for the coin description, return STR var
def scrap_description(soup):
	right_table=soup.find('td', class_='desc')

	if right_table:
		text = str(right_table)
		return repr(right_table.text)[3:-5]

	else:
		return None

#Search in numista site
def create_link_search(country, km_sys, km_num):

	return "https://en.numista.com/catalogue/index.php?mode=simplifie&p=1&r=" + country + "+" + str(km_sys).replace("#", "%23") + km_num

#scrap ID numista from search website
def scrap_id_numista(soup):
	right_table=soup.find('div', class_='description_piece')
	text = str(right_table)

	m = re.search("<strong><a href=\"pieces(.+?).html\">", text)
	if m:
		  return m.group(1)
	else:
		return None

#Create link for specific coin in Numista site
def create_link_ID_numista(numistaID):

	return "https://en.numista.com/catalogue/pieces" + numistaID + ".html"

#Scrap title coin from numista	
def scrap_title_numista(soup):

	#title coin
	# <h1>2 Euro - Juan Carlos I <span style="font-size:50%;">1st type - 2nd map</span></h1>
	return soup.h1.get_text()

#Scrap title coin from numista	
def scrap_km_numista(soup):
	
	#years, KM and material are in 'Features' table
	ficha = soup.find('section', id="fiche_caracteristiques")
	info_ficha = ficha.table.find_all("td")

	#
	#TODO Improve km_num output, it can be "906Modern"
	#
	system = ("KM", "Y#")
	km_raw = info_ficha[-1].get_text().split(",")[0]
	if km_raw[:2] in system:
		try:
			# km_sys = km_raw.split(" ")[0]
			km_num = km_raw.split(" ")[1]
		except:
			# km_sys = None
			km_num = None
	else:
		# km_sys = None
		km_num = None


	return km_num

#Scrap title coin from numista	
def scrap_yema_numista(soup):
	
	#years, KM and material are in 'Features' table
	ficha = soup.find('section', id="fiche_caracteristiques")
	info_ficha = ficha.table.find_all("td")

	years = info_ficha[1].string
	material = info_ficha[3].string

	return years, material

#Select one coin by its ID_KM
def update_coin(new_data):
		#data_coin[0] = ID
		#data_coin[1] = Country
		#data_coin[2] = KM system
		#data_coin[3] = KM number
		#data_coin[4] = ID_Numista
		#data_coin[5] = ddate
		#data_coin[6] = denomination
		#data_coin[7] = title
		#data_coin[8] = description
		#data_coin[9] = photo
		#data_coin[10] = material

	with con:
		cur = con.cursor()

		#Update KM Number
		if new_data[3] is not None:
			cur.execute("UPDATE COIN_KM SET KM_NUM =? WHERE ID_KM = ?", (new_data[3], id))

		#Update ID Numista
		if new_data[4] is not None:
			cur.execute("UPDATE COIN_KM SET ID_NUMISTA =? WHERE ID_KM = ?", (new_data[4], id))

		#Update Date
		if new_data[5] is not None:
			cur.execute("UPDATE COIN_KM SET DDATE =? WHERE ID_KM = ?", (new_data[5], id))

		#Update Title
		if new_data[7] is not None:
			cur.execute("UPDATE COIN_KM SET TITLE =? WHERE ID_KM = ?", (new_data[7], id))

		#Update Description
		if new_data[8] is not None:
			cur.execute("UPDATE COIN_KM SET DESCRIPTION =? WHERE ID_KM = ?", (new_data[8], id))

		#Update Material
		if new_data[10] is not None:
			cur.execute("UPDATE COIN_KM SET MATERIAL =? WHERE ID_KM = ?", (new_data[10], id))

		con.commit()


############
############
#####################Done, review till here
############
############




#Scrapt the website looking for the date, return STR var
def scrap_date(soup):
	right_table=soup.find('td', class_='dates')
	text = str(right_table)

	return repr(right_table.text)[2:-1]


#Scrap the website looking for the coin material, return STR
def scrap_material(soup):
	right_table=soup.find('td', class_='comp')

	print right_table

	try:
		text = str(right_table)
		return repr(right_table.text)[2:-5]
	except:
		return None


#Scrap the webiste, searching and downloading the coin pictures
def scrap_pic(soup, local_id):

	right_table=soup.find('td', class_='pic')
	text_pic = str(right_table)

	# <td class="pic"><script>document.write("<" + "img  id='Img62261104' src='/ta/fwimg/284745/62261104/4.jpg'>");</script>
	# <script>document.write("<" + "img  id='Img62261103' src='/ta/fwimg/284745/62261103/4.jpg'>");</script></td>


	try:
	    pictures = re.findall('src=\'(.+?)\'>', text_pic)
	except AttributeError:
	    # AAA, ZZZ not found in the original string
	    pictures = [] # apply your error handling
	    return 0

	if len(pictures) == 0:
		return 0

	i = 0
	for pic in pictures:
		s = list(pictures[i])
		s[-5] = '3'
		pictures[i] = "".join(s)
		i =+ 1

	# print pictures

	base_pic = "http://secure.numismaster.com"

	reverso = 1
	for pic in pictures:
		url_pic = base_pic+pic
		
		if reverso == 1:
			local_pic = "/media/sf_VMFiles/coins/pictures/" + local_id + ".jpg"
		else:
			local_pic = "/media/sf_VMFiles/coins/pictures/" + local_id + "_" + str(reverso) + ".jpg"
		
		try:
			urllib.urlretrieve(url_pic, local_pic)
		except:
			print "ERROR DOWNLOADING PICTURES FOR COIN: ", local_id
			return 0
		reverso += 1
	return 1


#Script to update the SQL DB with info scraped from website (1st version) BUG FOUND IN THIS VERSION.
def updater_sql_db():
	for row in range(1, 10044):
		
		data_coin = searcher_coin(row)
		#data_coin[0] = ID
		#data_coin[1] = Country
		#data_coin[2] = KM system
		#data_coin[3] = KM number
		#data_coin[4] = ddate
		#data_coin[5] = denomination
		#data_coin[6] = description

		# print data_coin
	 
	 	# print row
		if data_coin is None:
			break
		

		if data_coin[3] is not None and data_coin[4] is None:
			link_coin = link_creator(data_coin[1], data_coin[3], data_coin[5], data_coin[2] )
			
			# print link_coin

			soup = giveme_soup(link_coin)
			print "-----> ID: ", row

			ddate_coin = scrap_date(soup)
			desc_coin = scrap_description(soup)
			mate_coin = scrap_material(soup)
			pic_coin = scrap_pic(soup, str(data_coin[0]+10000))
			# print data_coin, ddate_coin, desc_coin, mate_coin, pic_coin
			print data_coin[6]
			print desc_coin
			update_coin(data_coin[0], ddate_coin, desc_coin, mate_coin, pic_coin)

#Script to fix entries updated before to fix bug in pic cel
def fixer_pic():
	for row in range(530, 1042):
		
		data_coin = searcher_coin(row)
		#data_coin[0] = ID
		#data_coin[1] = Country
		#data_coin[2] = KM system
		#data_coin[3] = KM number
		#data_coin[4] = ddate
		#data_coin[5] = denomination
		#data_coin[6] = description

		# print data_coin
	 
		if row%10 == 0:
			print "-----> ID: ", row

		if data_coin is None:
			pass
		else:
		
			link_coin = link_creator(data_coin[1], data_coin[3], data_coin[5], data_coin[2] )
			# print link_coin

			soup = giveme_soup(link_coin)


			pic_coin = scrap_pic(soup, str(data_coin[0]+10000))


			if pic_coin == 0:
				print "-----> ID: ", row
				print "No photo"
			update_coin(data_coin[0], 0,0,0, pic_coin)

#####
#####
#####
#####


#Main Script
def main():
	for row in range(1317, 1323):
	
		data_coin = searcher_coin(row)
		#data_coin[0] = ID
		#data_coin[1] = Country
		#data_coin[2] = KM system
		#data_coin[3] = KM number
		#data_coin[4] = ID_Numista
		#data_coin[5] = ddate
		#data_coin[6] = denomination
		#data_coin[7] = title
		#data_coin[8] = description
		#data_coin[9] = photo
		#data_coin[10] = material

		data_coin = list(data_coin)
		new_data_coin = [None]*11


		print "--------------------------------------@ ", data_coin[0]

		#If there is KM Number:
		if data_coin[3] is not None:

			# If there is not ID NUMISTA: Create link Numista search, soup it and get its ID numista
			if data_coin[4] is None:
				link_coin = create_link_search(data_coin[1], data_coin[2], data_coin[3])
				soup = giveme_soup(link_coin)

				new_data_coin[4] = data_coin[4] = scrap_id_numista(soup)


		#If there is Numista ID:
		if data_coin[4] is not None:

			#Create link with ID numista, soup it
			link_coin = create_link_ID_numista(data_coin[4])
			soup = giveme_soup(link_coin)

			#if KM is null, find it
			if data_coin[3] is None or len(data_coin[3]) == 0:
				new_data_coin[3] = data_coin[3] = scrap_km_numista(soup)

			#title
			new_data_coin[7] = scrap_title_numista(soup)

			#years and material
			i = scrap_yema_numista
			new_data_coin[5] = data_coin[5] = i[0]

			if data_coin[10] is None or len(data_coin[10]) == 0 or data_coin[10][0] == "#":
				new_data_coin[10] = data_coin[10] = i[1]

			#get new description from numismaster:
			link_coin = link_creator(data_coin[1], data_coin[6], data_coin[2], data_coin[3])
			soup = giveme_soup(link_coin)

			if data_coin[8] is None or len(data_coin[8]) == 0 or data_coin[8][0] == "#":
				new_data_coin[8] = scrap_material(soup)

		update_coin(new_data_coin)

	 
#############################################################
#############################################################
#############################################################


main()
