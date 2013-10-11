#!/usr/bin/python

import sys
import csv 
import os

file = csv.reader(open('emails','r'))
outfile = open('emails.txt','w')

for row in file:
    outfile.write("%s\n" %row[0])

outfile.close()
file.close()
