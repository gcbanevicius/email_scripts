#!/usr/bin/python

import sys
import csv
import os

f1 = open("passes1.csv", "r")
f2 = open("passes2.csv", "r")
f3 = open("passes3.csv", "r") 

c1 = csv.reader(f1)
c2 = csv.reader(f2)
c3 = csv.reader(f3)
outfi = open("passes_bounced.txt", "w")

for row1 in c1:
	found = False
	email = row1[3]

	#set name var if they have a middle name
        if row1[1] != '':
	    name = row1[2] + ' ' + row1[1] + ' ' + row1[0]
	#set name var if they don't have a middle name elif row[1] == '':
        else:
	    name = row1[2] + ' ' + row1[0]

	outfi.write("%s,%s," %(name,email) )

	for row2 in c2:
		if name in row2[0]:
			outfi.write("%s\n" %row2[2] )
			found = True
			break
	f2.seek(0)
	
	if found == True:
		continue
	
	for row3 in c3:
		if name in row3[0]:
			outfi.write("%s\n" %row3[2] )
			found = True
			break
	f3.seek(0)	

	if found == True:
		continue

	outfi.write("NO PASSWORD...\n")

outfi.close()
