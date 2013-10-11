#!/usr/bin/python

import csv
import re
import smtplib

c = csv.reader(open('people.txt'))
letter = open('emails.txt')

server = smtplib.SMTP('localhost')
server.ehlo()

fromAddr = 'xxx@gmail.com'
fromName = 'Mr. X <xxx@gmail.com>'
toAddr = 'xxx@gmail.com'
toName = 'Mr. X <xxx@gmai.com>'
for person in c:
	toAddr = person[1]
	toName = '%s <%s>' % (person[0],person[1])
	msg = ''
	msg = msg + 'To: %s\r\n' % toName
	msg = msg + 'From: %s\r\n' % fromName
	msg = msg + 'Subject: Greetings, here is your username and password\r\n'
	msg = msg + '\r\n\r\n'
	letter.seek(0)
	while 1:
		line=letter.readline()
		if not line:
			break
		line = line.strip()
		line = re.sub('Colleagues',person[0],line)	
		line = re.sub('Your username is:','Your username is: %s' % person[0],line)
		line = re.sub('Your password is:','Your password is: %s' % person[2],line)
		msg = msg + line + '\r\n'
	server.sendmail(fromAddr,toAddr,msg)
server.close()
