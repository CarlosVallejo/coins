#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
##
##	Script to scrap the numimaster web
##
#####


import urllib2
from bs4 import BeautifulSoup
import re
import urllib


wiki = "http://secure.numismaster.com/ta/Coins.admin?rnd=SMSXJXBC&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=YRELZ&Origin=3&AdvanceSearch=0&PRefine=&Country=Poland&Denom=&CountryId=&DenomId=&KM=446&Comp=&Date="
wiki = "http://secure.numismaster.com/ta/Coins.admin?rnd=ANHXLNVW&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=BLXYH&Origin=3&AdvanceSearch=0&PRefine=&Country=Spain&Denom=&CountryId=292&DenomId=&KM=666&Comp=&Date="
wiki = "http://secure.numismaster.com/ta/Coins.admin?rnd=ANHXLNVW&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=BLXYH&Origin=3&AdvanceSearch=0&PRefine=&Country=Spain&Denom=&CountryId=292&DenomId=&KM=1041&Comp=&Date="

wiki_list = ["http://secure.numismaster.com/ta/Coins.admin?rnd=SMSXJXBC&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=YRELZ&Origin=3&AdvanceSearch=0&PRefine=&Country=Poland&Denom=&CountryId=&DenomId=&KM=446&Comp=&Date=", 
"http://secure.numismaster.com/ta/Coins.admin?rnd=ANHXLNVW&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=BLXYH&Origin=3&AdvanceSearch=0&PRefine=&Country=Spain&Denom=&CountryId=292&DenomId=&KM=666&Comp=&Date=", 
"http://secure.numismaster.com/ta/Coins.admin?rnd=ANHXLNVW&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=BLXYH&Origin=3&AdvanceSearch=0&PRefine=&Country=Spain&Denom=&CountryId=292&DenomId=&KM=1041&Comp=&Date=",
"http://secure.numismaster.com/ta/Coins.admin?rnd=ANHXLNVW&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=BLXYH&Origin=3&AdvanceSearch=0&PRefine=&Country=Gibraltar&Denom=&CountryId=153&DenomId=-%20Enter%20Denomination%20-&KM=1092&Comp=&Date=", 
"http://secure.numismaster.com/ta/Coins.admin?rnd=SMSXJXBC&@impl=coins.ui.ucatalog.flat.coin.UiControl_FindResults&@prms=536561726368547970653d31&@windowId=YRELZ&Origin=3&AdvanceSearch=0&PRefine=&Country=Poland&Denom=&CountryId=&DenomId=&KM=848&Comp=&Date="]


# page = urllib2.urlopen(wiki)

# soup = BeautifulSoup(page)

def giveme_soup(web):
	page = urllib2.urlopen(web)
	soup = BeautifulSoup(page)
	return soup



print '///////////////////////////////////'

# SEARCHING FOR THE PICS, and donwnloading them.
# input: 	local_id: Coin's ID, it became the filename/s
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

	print pictures

	base_pic = "http://secure.numismaster.com"

	reverso = 1
	for pic in pictures:
		url_pic = base_pic+pic
		
		if reverso == 1:
			local_pic = "pic/" + local_id + ".jpg"
		else:
			local_pic = "pic/" + local_id + "_" + str(reverso) + ".jpg"

		try:
			urllib.urlretrieve(url_pic, local_pic)
		except:
			print "ERROR DOWNLOADING PICTURES FOR COIN: ", local_id
		reverso += 1

#DONE, return right date
def scrap_date(soup):
	right_table=soup.find('td', class_='dates')
	text = str(right_table)

	print right_table.text
	# print repr(right_table.text)
	return repr(right_table.text)[2:-1]


#DONE, return right desc
def scrap_description(soup):
	right_table=soup.find('td', class_='desc')
	text = str(right_table)

	print right_table.text[1:]
	# print repr(right_table.text)
	return repr(right_table.text)[3:-5]

#DONE, return right material
def scrap_material(soup):
	right_table=soup.find('td', class_='comp')
	text = str(right_table)

	print right_table.text

	return repr(right_table.text)[2:-5]



myid = 777
for i in wiki_list:
	print "----------------------"
	soup = giveme_soup(i)
	# scrap_pic(soup, str(myid))
	scrap_date(soup)
	scrap_description(soup)
	scrap_material(soup)
	myid += 10

	