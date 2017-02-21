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

#Scrap Coin Name
def scrap_coin_name(soup):
	# <h1>2 Euro - Juan Carlos I <span style="font-size:50%;">1st type - 2nd map</span></h1>
	return soup.h1.get_text()
	
def scrap_coin_years(soup):
	# 
	ficha = soup.find('section', id="fiche_caracteristiques")
	info_ficha = ficha.table.find_all("td")

	years = info_ficha[1].string
	material = info_ficha[3].string
	print years
	# m = re.search("Years</th><td>(.+?)</td", str(ficha))
	# print m
	# if m:
	# 	  return m.group(1)
	# else:
	# 	return None




def main():
	soup = giveme_soup( create_link_search("spain", "KM#", "1074") )
	print "-------------------------->>>>>>>>>"

	soup = giveme_soup( create_link_ID( scrap_id_numista(soup) ))

	# scrap_coin_name(soup)
	print scrap_coin_years(soup)



main()