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

db = "/media/sf_VMFiles/coins/db.sqlite"
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
		return ""

#Search in numista site
def create_link_search(country, km_sys, km_num):

	return "https://en.numista.com/catalogue/index.php?mode=simplifie&p=1&r=" + country.replace(" ", "_") + "+" + str(km_sys).replace("#", "%23") + km_num

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

	return "https://en.numista.com/catalogue/pieces" + str(numistaID) + ".html"

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

	id = new_data[0]

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


#####
#####
#####
#####


#Main Script
def main(a, z):
	for row in range(a, z):
	
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

		if data_coin is None:
			break

		data_coin = list(data_coin)
		new_data_coin = [None]*11

		new_data_coin[0] = data_coin[0]


		print "--------------------------------------@ ", data_coin[0]

		link_coin = link_creator(data_coin[1], data_coin[6], data_coin[2], data_coin[3])
		soup = giveme_soup(link_coin)
		print len(scrap_description(soup))

		# #If there is KM Number:
		# if data_coin[3] is not None:

		# 	# If there is not ID NUMISTA: Create link Numista search, soup it and get its ID numista
		# 	if data_coin[4] is None:
		# 		link_coin = create_link_search(data_coin[1], data_coin[2], data_coin[3])
		# 		# print link_coin
		# 		soup = giveme_soup(link_coin)

		# 		new_data_coin[4] = data_coin[4] = scrap_id_numista(soup)

		# 		#Couldnt find NumistaID due KM nomination: 787.1 search 787
		# 		if new_data_coin[4] is None:

		# 			link_coin = create_link_search(data_coin[1], data_coin[2], data_coin[3].split(".")[0])
		# 			soup = giveme_soup(link_coin)
		# 			new_data_coin[4] = data_coin[4] = scrap_id_numista(soup)


		# #If there is Numista ID:
		# if data_coin[4] is not None:

		# 	#Create link with ID numista, soup it
		# 	link_coin = create_link_ID_numista(data_coin[4])
		# 	soup = giveme_soup(link_coin)

		# 	#if KM is null, find it
		# 	if data_coin[3] is None or len(data_coin[3]) == 0:
		# 		new_data_coin[3] = data_coin[3] = scrap_km_numista(soup)

		# 	#title
		# 	if data_coin[7] is None:
		# 		new_data_coin[7] = scrap_title_numista(soup)

		# 	#years and material
		# 	i = scrap_yema_numista(soup)

		# 	new_data_coin[5] = data_coin[5] = i[0]

		# 	if data_coin[10] is None or len(data_coin[10]) == 0 or data_coin[10][0] == "#":
		# 		new_data_coin[10] = data_coin[10] = i[1]

		# 	#get new description from numismaster:
		# 	if data_coin[3] is not None:

		# 		#if description is NULL or emptly
		# 		if data_coin[8] is None or len(data_coin[8]) == 0:
		# 			link_coin = link_creator(data_coin[1], data_coin[6], data_coin[2], data_coin[3])
		# 			soup = giveme_soup(link_coin)
		# 			new_data_coin[8] = scrap_description(soup)

		# 		#if descrption is a comment: first char is "#": add official desc and keep comment
		# 		if data_coin[8] is not None:
		# 			if data_coin[8][0] == "#":
		# 				link_coin = link_creator(data_coin[1], data_coin[6], data_coin[2], data_coin[3])
		# 				soup = giveme_soup(link_coin)
		# 				print scrap_description(soup)
		# 				new_data_coin[8] = scrap_description(soup) + " " + str(data_coin[8])



		# print new_data_coin
		# update_coin(new_data_coin)

	 
#############################################################
#############################################################
#############################################################


main(1030, 1032)
