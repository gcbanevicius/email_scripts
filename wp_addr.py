#!/usr/bin/python

import sys
import csv
import os
import time
import MySQLdb
import _mysql
import _mysql_exceptions

os.chdir('~/Desktop/profiles')

rows = csv.reader(open('./csv_file.csv', 'rb'))
db = MySQLdb.connect(user='root', db='drupal_username')
c = db.cursor()

def try_query(c,query):
	try:
		c.execute(query)	
	except:
		print "Error with %s" % query
		return False
	return True

for row in rows:
    	varname = row[1] + ' ' + row[2]
	#get the nid/vid from the node table
	print "***" + varname
	print
	if (try_query(c,'SELECT nid FROM node WHERE title = "%s";' % ( varname ) ) == False):
		continue
	id = c.fetchone()[0]
	inst = row[4]
	cat1 = row[6]
	grad_date = row[7]
	eth = row[12]	
	
	#insert category 1 (undergrad, grad, postdoc...)
	if (try_query(c,'INSERT INTO content_field_category (nid, vid, field_category_value) VALUES (%d,%d,"%s");' % (id, id, cat1) ) == False):
		continue

	#if undergrads, insert school and grad date
	if cat1 == 'Undergraduate Student':
		if try_query(c,'INSERT INTO content_field_bachelors_institution (nid, vid, field_bachelors_institution_value) VALUES (%d,%d,"%s");' % (id, id, inst) ) == False:
			continue
		if try_query(c,'INSERT INTO content_field_bachelors_year (nid, vid, field_bachelors_year_value) VALUES (%d,%d,"%s");' % (id, id, grad_date) ) == False:
			continue
 
	#insert id numbers, ethnicity, and the address of their current institution as home address
	addr = row[5].split('\n')
	#make sure the "name" field isn't longer than 75 characters
	if len(inst + ' ' + addr[2]) > 75:
		inst = inst
	else:
		inst = inst + ' ' + addr[2]
	try_query(c,'INSERT INTO content_type_profile (nid, vid, field_public_value, field_ethnicity_value, field_home_address_aname, field_home_address_street, field_home_address_city, field_home_address_province, field_home_address_country, field_home_address_postal_code) VALUES (%d,%d,%d,"%s","%s","%s","%s","%s","%s","%s");' % (id, id, 1, eth, inst, addr[3], addr[4], addr[5], addr[6], addr[7]) )

c.close()
db.close()
