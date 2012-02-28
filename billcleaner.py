#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,re
import logging
import web
import subprocess

db = web.database(dbn='sqlite', db='alecdata.db')
logging.basicConfig(filename='logs/billcleaner.log',level=logging.DEBUG)



''' used to add tags from error log, DERP
cl = open('billcleaner.log','r')
for line in cl:
	if line != '':
		splits = line.split()
		tag_id = int(splits[0])
		name = ' '.join(splits[1:])
		print name
		data = db.select('model_bills',where="name=$name",vars={'name':name})
		data = data.list()
		db.insert('model_bill_to_tag',model_bill_id=data[0]['id'],tag_id=tag_id)
exit()'''

categories = os.listdir('static/bills/')
bnames = []
for category in categories:
	# get tag id from database
	tag = db.select('tags',where="text=$category",vars={'category':category})
	tag = tag.list()
	tag_id = tag[0]['id']
	bill_names = os.listdir('static/bills/'+category+'/')
	for bill in bill_names:
		billinfo = re.match("^([A-Z0-9a-z]*)-([A-Za-z0-9_ \-\(\)~']*).[pdf|PDF]",bill)
		if billinfo is not None:
			bill_id = billinfo.groups()[0]
			bill_name = billinfo.groups()[1]
			bill_name = bill_name.replace('_',' ')
			bill_name = bill_name.replace(' exposed','')
			bill_name = bill_name.replace(' Exposed','')
			bill_name = ' '.join(i.capitalize() for i in bill_name.split(' '))

			bill_text = unicode(subprocess.check_output(['pdf2txt.py','static/bills/'+category+'/'+bill]),'utf-8')
			if bill_name not in bnames:
				res = db.insert('model_bills',bill_id=bill_id,name=bill_name,filename=bill,text=bill_text)
				bnames.append(bill_name)
				res = db.insert('model_bill_to_tag',model_bill_id=res,tag_id=tag_id)
			else:
				logging.error('duplicate bill'+str(tag_id)+' '+bill_name)
		else:
			logging.error('could not parse bill with regex: %s' %(category+'/'+bill))
