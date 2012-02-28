#!/usr/bin/env python
# -*- coding: utf-8 -*-
from web import form
import XMLDict
import markdown2
import web
import urlparse
import json
import urllib
import os
import hashlib
import uuid
import logging

# SITE ROOT URL
root_url = 'http://gabrenya.com:8080'
# ROOT PATH to application
root_path = ''
# sendmail path
web.config.sendmail_path='/usr/sbin/sendmail'

urls = ('^'+root_path+'/api/(corporations|politicians|model_bills|task_forces)/(get|getList).(xml|json)','dispatch',
	'^'+root_path+'/docs/(|corporations|politicians|model_bills|task_forces|todo)','docs',
	'^'+root_path+'/register','register',
	'^'+root_path+'/register/activate/(.*)','activate')

# database
db = web.database(dbn='sqlite', db='alecdata.db')

logging.basicConfig(filename='logs/api.log',level=logging.DEBUG)
templates = web.template.render('templates/')
app = web.application(urls,globals())

		
class dispatch:
	''' dispatch api url to proper class'''
	def GET(self,api,method,format):
		params = dict([part.split('=') for part in web.ctx.query[1:].split('&')])
		if params.has_key('apikey'):
			if self._check_apikey(params['apikey'],api,params):
				del params['apikey']
				if format == 'xml':
					ctype = 'text/xml'
				else:
					ctype = 'application/json'
				web.header('Content-Type', ctype)
			
				# run api with proper parameters
				maxlen = None
				if method == 'get':
					maxlen = 1
				tablename = api
				if api == 'corporations':
					getparams = ['id','name','forprofit','sourcewatch_url','background_info']
				elif api == 'politicians':
					getparams = ['id','title','name','party','state','district','background_info','ae_url']
					tablename = 'legislators'		
				elif api == 'model_bills':
					getparams = ['id','name','filename','text']
				elif api == 'task_forces':
					getparams = ['id','name']
				return self._get(format,params,maxlen,tablename,api,getparams)
				'''api = globals()[api]()

				return api.get(format,params,maxlen)'''
		else:
			return "Error: apikey is incorrect given"
		
	def _check_apikey(self,apikey,api,params):
		''' check that apikey is legitimate '''
		hash_key = hashlib.md5(apikey).digest().decode('latin-1')
		res = db.select('users',where='apikey=$apikey',vars={'apikey':hash_key})
		res = res.list()
		if len(res) > 0:
			logging.info('user %s with key %s accessed api %s with %s' %(res[0]['email'],api,apikey,params))
			return True
		else:
			logging.info('non-user %s with bad key %s accessed api %s with %s' %(res[0]['email'],api,apikey,params))
			return False

	def _get(self,format,params,maxlen,tablename,api,getparams):
		# define response
		data = {'response':{}}
		# turn params into database request
		wherecond = []
		paramerror = []
		for each in params:
			if each in getparams:
				wherecond.append('%s=$%s' %(each,each))
			else:
				paramerror.append(each+" is not an accepted key.")
		# stop if param errors
		if len(paramerror) > 0:
			" and ".join(paramerror)
			data['response']['error'] = get_error(paramerror)
		else:
			if len(wherecond) == 0:
				results = db.select(tablename)
				rlist = results.list()	
			elif len(wherecond) > 0:
				wherecond = ' AND '.join(wherecond)
				results = db.select(tablename,where=wherecond,vars=params)
				rlist = results.list()
			# errors
			if len(rlist) == 0:
				data['response']['error'] = get_error(1)
			elif maxlen == 1 and len(rlist) > 1:
				data['response']['error'] = get_error(2)
			# accepts
			elif maxlen == 1 and len(rlist) == 1:		
				if params.has_key('include_citations'):
					include_citations = params['include_citations']
				else:
					include_citations = 0			
				data['response'][api] = self._build_data(rlist[0],format,getparams,int(include_citations))
			elif maxlen == None and len(rlist) >= 1:
				data['response'][api] = []
				for each in rlist:
					if params.has_key('include_citations'):
						ic = params['include_citations']
					else:
						ic = 0
					item = self._build_data(each,format,getparams,int(ic))
					data['response'][api].append({api[:-1]:item})
		if format == 'json':
			return json.dumps(data)
		elif format == 'xml':
			res =  XMLDict.convert_dict_to_xml(data)
			return res

	def _build_data(self,row,format,getparams,includecitations=0):
		ditem = {}
		for key in getparams:
			if key in row.keys() and row[key] is not None and row[key] != "" and row[key] != "<div></div>":
				ditem[key] = row[key]
		if includecitations == 1:
			results = db.select('corporation_to_citation',where="corporation_id=$lid",vars={'lid':row['id']})
			rlist = results.list()
			if len(rlist) > 0:
				ditem['citations'] = []
				for each in rlist:
					citations = db.select('citations',where="id=$eid",vars={'eid':each['id']})
					citations = citations.list()
					for cit in citations:
						ditem['citations'].append({'citation': cit['text']})
		return ditem



class activate:
	''' confirm user accounts '''
	def GET(self,key):
		key_hash = hashlib.md5(str(key)).digest().decode('latin-1')
		res = db.select('users',where='apikey=$apikey',vars={'apikey':key_hash})
		if len(res.list()) == 1:
			db.update('users',where='apikey=$apikey',vars={'apikey':key_hash},is_active=1)
			return docs().thanks('Your API Key is activated and can now be used') 
		else:
			return register().ERR('Not a valid API Key, double check your email')


class register:
	''' generate user accounts'''
	login = form.Form(form.Textbox('email'),form.Textbox('name'),form.Textbox('organization name'),form.Textbox('organization url'), form.Textarea('intended use'),form.Button('submit',type='submit',html='Register'))
	def POST(self):
		form = web.input()
		if form.email != None:
			if len(form.email) > 0:
				# generate api key info
				key = uuid.uuid4()
				key_hash = hashlib.md5(str(key)).digest().encode('utf-8')
				# add info to database
				email = form.email
				name = form.name
				org_name = form['organization name']
				org_url = form['organization url']
				use = form['intended use']
				reschk = db.select('users',where='email=$email OR apikey=$key_hash',vars={'email':email, 'key_hash':key_hash})
				if len(reschk.list()) > 0:
					return self.ERR('This email address is already registered, check your records for your API Key')
				else:
					res = db.insert('users',name=name,email=email,organization_name=org_name,organization_url=org_url,intended_use=use,apikey=key_hash,is_active=0)
					# send email with api key			
					text = """Thank you for registering for a ALEC Exposed API key.

Please visit the following URL to verify your email address and activate your key
%s/register/activate/%s

Your details are included below for your records:
    Email: %s
    API Key: %s
""" %(root_url,key,email,key)
					web.sendmail('noreply@derp.com',email,"ALEC Exposed Registration",text)
					return docs().thanks('Thank you for registering, click the link in your email to activate your API Key')
			else:
				return self.ERR('A valid email address is required')
		else:
			return self.ERR('A valid email address is required')
	def GET(self):
		return templates.docs("""<h3>Register to get an API Key</h3><form action="/register" method="POST"> """+self.login.render()+"</form>")
	def ERR(self,error):
		return templates.docs("""<h3>Register to get an API Key</h3><p>%s</p><form action="/register" method="POST"> """ %(error)+self.login.render()+"</form>")



def get_error(number):
	if type(number) is int:
		if number == 1:
			text = 'No results'
		elif number == 2:
			text = 'More than 1 result (when using get)'
		else:
			text = ''
	else:
		text = number
		number = 0
	return {'number':number,'text':text}


class docs:
	def GET(self,page):
		cwd = os.getcwd()
		if page == '':
			# Main api docs page
			htmldoc = markdown2.markdown_path(cwd+'/templates/main.md')
			return templates.docs(htmldoc)
		else:
			# Politician api docs page
			htmldoc = markdown2.markdown_path(cwd+'/templates/'+page+'.md')
			return templates.docs(htmldoc)
	
	def thanks(self,message):
		# Mainapi docs page, thanks for registering
		cwd = os.getcwd()
		htmldoc = markdown2.markdown_path(cwd+'/templates/main.md')
		return templates.docs("<h3>%s</h3>%s" %(message,htmldoc))



if __name__ == "__main__":
	app.run()
