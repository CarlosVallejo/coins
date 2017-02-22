#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
##
##	Script to scrap the numista web
##
#####

"""
Search in numista website:
"https://en.numista.com/catalogue/index.php?mode=simplifie&p=1&r=" + COUNTRY + "+" + KM_SYS.replace("#", "%23") + KM_NUM

EXAMPLE: 
https://en.numista.com/catalogue/index.php?mode=simplifie&p=1&r=spain+KM%23890



https://en.numista.com/catalogue/pieces45401.html
###
"""

import urllib2
from bs4 import BeautifulSoup
import re
import urllib

#Search in numista site
def create_link_search(country, km_sys, km_num):
	return "https://en.numista.com/catalogue/index.php?mode=simplifie&p=1&r=" + country + "+" + km_sys.replace("#", "%23") + km_num


def giveme_soup(web):
	page = urllib2.urlopen(web)
	soup = BeautifulSoup(page)
	return soup

#Scrap coinID 
def scrap_id_numista(soup):
	right_table=soup.find('div', class_='description_piece')
	text = str(right_table)

	m = re.search("<strong><a href=\"pieces(.+?).html\">", text)
	if m:
		  return m.group(1)
	else:
		return None	 

def create_link_ID(numistaID):
	return "https://en.numista.com/catalogue/pieces" + numistaID + ".html"


#Scrap info from numista	
def scrap_coin_data(soup):

	#title coin
	# <h1>2 Euro - Juan Carlos I <span style="font-size:50%;">1st type - 2nd map</span></h1>
	title = soup.h1.get_text()
	
	#years, KM and material are in 'Features' table
	ficha = soup.find('section', id="fiche_caracteristiques")
	info_ficha = ficha.table.find_all("td")

	years = info_ficha[1].string
	material = info_ficha[3].string

	#KM v2
	#
	#TODO Improve km_num output, it can be "906Modern"
	#
	system = ("KM", "Y#")
	km_raw = info_ficha[-1].get_text().split(",")[0]
	if km_raw[:2] in system:
		try:
			km_sys = km_raw.split(" ")[0]
			km_num = km_raw.split(" ")[1]
		except:
			km_sys = None
			km_num = None
	else:
		km_sys = None
		km_num = None


	return title, years, material, km_sys, km_num



#TODO
#Scrap photo from numista



def main(i):
	soup = giveme_soup( create_link_search("poland", "Y#", i) )
	print "-------------------------->>>>>>>>>"

	id_numista = scrap_id_numista(soup)

	if id_numista is not None:
		soup = giveme_soup( create_link_ID( id_numista ))
		data = scrap_coin_data(soup)

		# for i in data:
		# 	print i
	else:
		#Coin no found in numista site
		pass




for i in range(904, 908):
	main(str(i))