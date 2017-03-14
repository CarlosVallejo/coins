#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#####
##
##	Script to update DB using a template
##
##
##
#####

from __future__ import unicode_literals

from pyeasy import OpenExcel

import sys
from lib import *


template_excel = OpenExcel('/media/sf_VMFiles/coins/plantilla.xls')

#by default:
pack_id = None

def main():

	#READ EXCEL FILE ROW BY ROW
	initial_row = 3
	final_row = 40
	actual_row = initial_row
	for row in range(initial_row, final_row):

		actual_row += 1
		data = template_excel.read(row) #read row 

		#If New Pack, add it and get its ID
		#
		if len(str(data[1])) !=0:
			temp_data = [None]*5
			temp_data[0] = str(data[1])			#Name
			temp_data[1] = str(int(data[3]))	#Date
			temp_data[2] = str(data[4])			#Cost
			temp_data[3] = str(data[5])			#FromWhere
			temp_data[4] = str(data[6])			#Comment

			# pack_id = add_new_pack(temp_data)

			# print pack_id

		#Coin to add:
		if len(str(data[1])) == 0:


			#coin (by KM) already in DB
			if len(str(data[7])) != 0:
				temp_data = [None]*6
				temp_data[0] = str(int(data[7]))			#ID_KM
				temp_data[1] = str(data[3]).split('.')[0]	#Year
				temp_data[2] = str(data[6])					#Comment
				temp_data[3] = str(data[5])					#ToSwap
				temp_data[4] = pack_id						#Pack
				temp_data[5] = str(data[10])				#Location

				print temp_data







########################
main()