#!/usr/bin/python

import sys
import csv
import os
import time
import MySQLdb
import _mysql
import _mysql_exceptions

from random import Random

def mkpasswd():
	passwd = list()
	rng = Random()
	righthand = '23456qwertasdfgzxcvbQWERTASDFGZXCVB'
	lefthand = '789yuiophjknmYUIPHJKLNM'
	allchars = righthand + lefthand
	passwordLength=12
	for i in range(passwordLength):
		passwd.append(rng.choice(allchars))
	return ''.join(passwd)

def check_data(c,data):
	c.execute('SELECT * FROM node where title="%s";' %data) 
	set = c.fetchall()
	if not set:
		return False
	return True 

os.chdir('~/Desktop/profiles')

rows = csv.reader(open('./emaillist.csv', 'rb'))
db = MySQLdb.connect(user='root', db='drupal_username')
c = db.cursor()

passes = open('passes.csv','w')


for row in rows:
    #for the 2012 participants...
    if row[4] == '2012': 
	#set name var if they have a middle name
        if row[1] != '':
	    varname = row[2] + ' ' + row[1] + ' ' + row[0]
	#set name var if they don't have a middle name elif row[1] == '':
        else:
	    varname = row[2] + ' ' + row[0]

	# make a password for the user
	passwd=mkpasswd()
	passes.write("%s,%s,%s\n" % (varname,row[3],passwd))

	try:
		c.execute('INSERT INTO users (name,mail,created,pass) VALUES ("%s","%s",%d,md5("%s"));' % ( varname,row[3],time.time(),passwd ) )
	#skip over existing entries from earlier years
	except _mysql_exceptions.IntegrityError:
		print '%s has an identical entry!' %(varname)
		# try to update passwords for all users
		try:
			c.execute("UPDATE users SET pass=md5('%s') WHERE name='%s';" % (passwd,varname))
		except:
			print 'failed to update password for %s' % varname
			pass	

	# update user status
	c.execute('UPDATE users SET status=1 WHERE status <> 1;')

	# get the uid for the current user
      	c.execute('SELECT uid FROM users WHERE name = "%s";' % ( varname ) )
      	id = c.fetchone()[0]

	# try to update rid for user
	try:
		c.execute('INSERT INTO users_roles (uid,rid) VALUES (%d,%d);' % (id,3) )
	except _mysql_exceptions.IntegrityError:
		print 'Role ID for "%s" is already set' %varname
		c.execute('UPDATE users_roles SET rid=3 WHERE rid=0 AND uid=%d;' %id )	

	# try to update the nid, vid, and created fields for nodes
	if check_data(c,varname) == False:
		c.execute('INSERT INTO node (type,title,uid,created) VALUES ("%s","%s",%d,%d);' % ( 'profile',varname,id,time.time() ) )
		c.execute('SELECT last_insert_id();')
		nid = c.fetchone()[0]
		c.execute('UPDATE node SET vid = nid WHERE nid=%d;' % nid) 
		c.execute('INSERT INTO node_revisions (title,uid,nid,vid,timestamp) VALUES ("%s",%d,%d,%d,%d);' % ( varname,id,nid,nid,time.time() ) )
	else:
		c.execute('SELECT nid FROM node WHERE title="%s";' %varname )
		nid = c.fetchone()[0]
	
	#now try to insert 2012 into the proper year field
	try:
		c.execute('INSERT INTO content_field_years (nid,vid,field_years_value) VALUES (%d,%d,"%s");' % (nid,nid,'2012') )
	except _mysql_exceptions.IntegrityError:
		print "Failed to update year for %s" % varname
		pass	

passes.close()
c.close()
db.close()
