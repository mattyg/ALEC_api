from scrapemark import scrape
import sunlight
import lxml.html
import lxml.html.clean
import urllib2,urllib
import re
import logging
import web

db = web.database(dbn='sqlite', db='alecdata.db')
logging.basicConfig(filename='logs/webscraping.log',level=logging.DEBUG)
sunlight.config.API_KEY = 'b281fd9d3a124f53970f623de12b0596'

class corporations:
	def __index__(self):
		pass
	def get(self):
		# page ALEC_Corporations
		html = urllib2.urlopen("http://www.sourcewatch.org/index.php?title=ALEC_Corporations").read()
		
		# get for-profit corporation citations
		references = scrape("""<ol class="references"> {* <li> {{ []|html }} </li> *} </ol>""",html)
		self._add_citations(references,'ALEC_Corporations')

		# get for-profit corporations
		letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		corporations = []
		for letter in letters:
			corps = scrape("""<h3> <span class="mw-headline">"""+letter+""" </span> </h3> <ul> {* <li> {{ []|html }} </li> *} </ul> """,html)
			corpdata = []
			for each in corps:
				refs = scrape(""" {* <sup class="reference">[ {{ []|int }} ]</sup> *}""",each)
				datas = scrape(""" {* {{ [] }} <sup class="reference"> </sup> *} """,each)
				name = ''
				if len(datas) > 0:
					name = datas[0]

				info = ''
				if len(datas) > 2:
					for d in datas[0:]:
						info = info+d
				elif len(datas) > 1:
					info = datas[1]
				corpdata.append((name,info,refs))
			corporations.extend(corpdata)
		self._add_corporations(corporations,1)
		
		# page ALEC_Non-Profits
		html2 = urllib2.urlopen("http://www.sourcewatch.org/index.php?title=ALEC_Non-Profits").read()
		
		# get non-profit corporation citations
		references = scrape("""<ol class="references"> {* <li> {{ []|html }} </li> *} </ol>""",html2)
		self._add_citations(npcitations,'ALEC_Non-Profits')

		# get non-profit corporations
		nonprofits = []
		for letter in letters:
			np = scrape("""<h3> <span class="mw-headline">"""+letter+"""</span> </h3> <ul> {* <li> {{ []|html }} </li> *} </ul> """,html2)
			npdata = []
			for each in np:
				refs = scrape(""" {* <sup class="reference">[ {{ []|int }} ]</sup> *}""",each)
				datas = scrape(""" {* {{ [] }} <sup class="reference"> </sup> *} """,each)
				name = ''
				if len(datas) > 0:
					name = datas[0]
				info = ''
				if len(datas) > 2:
					for d in datas[0:]:
						info = info+d
				elif len(datas) > 1:
					info = datas[1]
				npdata.append((name,info,refs))
			nonprofits.extend(npdata)
		self._add_corporations(nonprofits,0)


	def _add_corporations(self,corporations,forprofit=1):
		''' Add for-profit corporations data to database '''
		for corp in corporations:
			# add corporation
			results = db.select('corporations',{'name': corp[0], 'forprofit':forprofit}, where="name=$name AND forprofit=$forprofit")
			rlist = results.list()
			if len(rlist) == 0:
				cid = db.insert('corporations',name=corp[0],forprofit=forprofit,background_info=corp[1])
			else:
				cid = rlist[0]['id']
			
			if forprofit == 1:
				page = 'ALEC_Corporations'
			else:
				page = 'ALEC_Non-Profits'
			# add citations
			for ref in corp[2]:
				# get citation_ids from ref #s
				results = db.select('citations',{'number':ref,'page':page},where="number=$number AND page=$page")
				rlist= results.list()
				if len(rlist) == 0:
					logging.error("Couldn't Find citation when adding corporations")
				else:
					citid = rlist[0]['id']
				results = db.select('corporation_to_citation',where="corporation_id=$cid AND citation_id=$citid",vars={'cid':cid,'citid':citid})
				rlist = results.list()
				if len(rlist) == 0:
					res =  db.insert('corporation_to_citation', corporation_id=cid, citation_id=ref)

	def _add_citations(self,citations,page):
		''' Clean &  Add citations to database '''
		refs = []
		for each in citations:
			each = scrape("""<a title=""></a> {{ |html}}""",each)
			html = lxml.html.fromstring(each)
			for t in html:
				if t.tag == 'sup':
					t.drop_tree()
			refs.append(lxml.html.tostring(html))
		corpcitations = enumerate(refs,start=1)
		for num,each in corpcitations:
			result = db.select('citations',where="number=$num AND text=$txt AND page=$page",vars={'num':num,'txt':each,'page':page})
			rlist = result.list()
			if len(rlist) == 0:
				db.insert('citations',number=num,text=each,page=page)



class legislators:
	def __index__(self):
		pass
	def get(self):
		# page ALEC_Politicians
		html = urllib2.urlopen("http://www.sourcewatch.org/index.php?title=ALEC_Politicians").read()
		
		# get legislator citations
		references = scrape("""<ol class="references"> {* <li> {{ []|html }} </li> *} </ol>""",html)
		self._add_citations(references,'ALEC_Politicians')

		# get legislators by state
		legislators = {}
		parties = {'D':'Democratic','R':'Republican','R/D':'Republicrat'}
		states ={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}
		for state in states.keys():
			legislators[state] = scrape("""<h3> <span class="mw-headline">"""+state+""" Legislators with ALEC Ties</span></h3> <h4> <span class="mw-headline">House of Representatives</span> </h4> <ul> {* <li>{{ [house]|html }}</li> *}</ul> <h4> <span class="mw-headline">Senate</span> </h4> <ul> {* <li>{{ [senate]|html }}</li> *} </ul>""",html)
			stateleg = legislators[state]['senate']
			stateleg.extend(legislators[state]['house'])
			for each in stateleg:
				if stateleg != "":
					split = re.match(r"([\w ]+)\. (.*)",each)
					if split is not None:
						title = split.groups()[0]
						htmldata = lxml.html.fromstring(split.groups()[1])
						url = ''
						for count,each in enumerate(htmldata):
							if count <= 1 and each.tag == 'a':
								each.drop_tag()
								url = each.attrib['href']
						htmldata.drop_tag()
						content = lxml.html.tostring(htmldata)
						#regex2 = r"<?\w*>?([\w. ]+)<?/?\w*>? *\(([A-Z/]+)-([0-9]+)\)?;?,?(.*)"
						regex2 = r"<?\w*>?([\w., ]+) *\(([A-Z/]+)-([\w]+)\)[,; ]*(.*)<?/?\w*>?"						
						split = re.match(regex2,content)
						if split is not None:
							name = split.groups()[0]
							party = split.groups()[1]
							district = split.groups()[2]
							info = split.groups()[3]
							citations = scrape("""<sup><a>[{{ []|int }}]</a></sup>""",info)
							try:
								clnr = lxml.html.clean.Cleaner(kill_tags=['sup'],remove_tags=['p'])
								info = clnr.clean_html(info)
							except:
								info = ''
							# get open states id
							state_short = states[state]
							party_long = parties[party]
							full_name = name.split(' ')
							first_name = full_name[0]
							last_name = full_name[-1]
							osl = sunlight.openstates.legislators(first_name=first_name,last_name=last_name,party=party_long,state=state_short,active=False)
							if len(osl) == 1:
								osid = osl[0]['id']
							else:
								osid = None
								print "********",osl
							self._add_legislator(name,title,party,state,district,info,osid,citations)
						else:
							logging.error('legislator data was not accepted by regex 2 '+str(content))
			
					else:
						logging.error('legislator data was not accepted by regex 1')

		# page ALEC_Task_Force_Politicians
		html = urllib2.urlopen("http://www.sourcewatch.org/index.php?title=ALEC_Task_Force_Politicians").read()
		tfile = open('task_force.txt','r+')
		tfile.write(html)
		#tfile.close()
		#tfile = open('task_force.txt','r+')
		#html = 
		# get legislator task force citations
		references = scrape("""<ol class="references"> {* <li> {{ []|html }} </li> *} </ol>""",html)
		self._add_citations(references,'ALEC_Task_Force_Politicians')

		# get task force legislators
		taskforces = ['Commerce, Insurance and Economic Development', 'Civil Justice', 'Education', 'Energy, Environment and Agriculture', 'Health and Human Services', 'International Relations', 'Public Safety and Elections', 'Tax and Fiscal Policy', 'Telecommunications and Information Technology']
		for taskforce in taskforces:
			legislators[taskforce] = scrape("""<h3><span class="mw-headline">"""+taskforce+""" Task Force</span></h3> <ul>{* <li>{{ []|html }}</li> *}</ul>""",html)
			for each in legislators[taskforce]:
				split = re.match(r"([\w ]+)\. (.*)",each)
				if split is not None:
					title = split.groups()[0]
					htmldata = lxml.html.fromstring(split.groups()[1])
					url = ''
					for count,each in enumerate(htmldata):
						if count <= 1 and each.tag == 'a':
							each.drop_tag()
							url = each.attrib['href']
					content = lxml.html.tostring(htmldata)
					split = re.match(r"<?\w*>?([\w. ]+)<?/?\w*>? *\(\w* *([A-Z]+)-([0-9]+)\)(.*)",content)
					if split is not None:
						name = split.groups()[0]
						party = split.groups()[1]
						district = split.groups()[2]
						info = split.groups()[3]
						citations = scrape("""<sup><a>[{{ []|int }}]</a></sup>""",info)
						try:
							clnr = lxml.html.clean.Cleaner(kill_tags=['sup'],remove_tags=['p'])
							info = clnr.clean_html(info)
						except:
							info = ''
						self._legislator_in_taskforce(name,title,district,info,taskforce,citations)						
					else:
						logging.error('legislator data was not accepted by regex 2')
		

		# get alec state chairmen
		# http://www.sourcewatch.org/index.php?title=ALEC_State_Chairmen

		# get award winning legislators		
		'''
		html2 = urllib2.urlopen("http://www.sourcewatch.org/index.php?title=ALEC_Award_Winners").read()
		awlegislators = {}
		years = ['1981','1990','1991','1996','1998','1999','2001','2002','2004','2005','2006','2007','2008','2009','2010','2011']
		for year in years:
			awlegislators[year] = scrape("""<h2> <span class="mw-headline">"""+year+""" Award-Winners</span></h2> <ul> {* <li>{{ [] }}</li> *} </ul> """,html2)
			if awlegislators[year] is not None:
				for each in awlegislators[year]:
					#TODO: PARSE AW DATA
					self._is_awardwinner(each,year)
			else:
				logging.error("Award winners could not be scraped")
		'''

	def _legislator_in_taskforce(self,name,title,district,info,taskforce,citations):
		name = name.strip()
		title = title.strip()
		info = urllib.unquote(info.strip())
		taskforce = taskforce.strip()
		# get legislator_id from name
		results = db.select('legislators',{'name':name,'title':title,'district':district},where="full_name=$name AND title=$title AND district=$district")
		rlist = results.list()
		if len(rlist) == 0:
			logging.error("Legislator not found to put in taskforce")
		else:
			lid = rlist[0]['id']

		#FIXBELOW TODO
		# get taskforce_id from name			
		results = db.select('tags',{'name':taskforce},where="text=$name")
		rlist = results.list()
		if len(rlist) == 0:
			logging.error("Task Force not found (name=%s)" %(taskforce))
		else:
			tfid = rlist[0]['id']

		# get/add legislator_taskforces (tags)
		results = db.select('legislator_to_taskforce',{'lid':lid,'tfid':tfid},where="legislator_id=$lid AND tag_id=$tfid")
		rlist = results.list()
		if len(rlist) == 0:
			results = db.insert('legislator_to_taskforce',legislator_id=lid,tag_id=tfid,background_info=info)
			logging.info('+ Added legislator_to_taskforce')
			ltfid = db.insert()
		else:
			ltfid = rlist[0]['id']

		# get/add legislator_taskforce_citations
		for ref in citations:
			results = db.select('citations',{'number':ref,'page':'ALEC_Task_Force_Politicians'},where="number=$number AND page=$page")
			rlist= results.list()
			if len(rlist) == 0:
				logging.error("Couldn't Find citation when adding corporations")
			else:
				citid = rlist[0]['id']
			results = db.select('legislator_taskforce_to_citation',where="legislator_to_taskforce_id=$cid AND citation_id=$citid",vars={'cid':cid,'citid':ref})
			rlist = results.list()
			if len(rlist) == 0:
				res =  db.insert('legislator_taskforce_to_citation', legislator_to_taskforce_id=cid, citation_id=ref)


	def _is_awardwinner(self,name,year):
		#TODO: add award winner data 		
		pass

	def _add_legislator(self,name,title,party,state,district,info,osid,citations=[]):
		''' add legislator to database '''
		name = name.strip()
		title = title.strip()
		party = party.strip()
		state = state.strip()
		print '+++',info
		info = urllib.unquote(info.strip()).decode('utf-8')
		print '----',info
		district = district.strip()
		#try:
		# add legislator
		results = db.select('legislators',{'full_name': name, 'title':title, 'state':state, 'district':district, 'os_id':osid}, where="full_name=$full_name AND title=$title AND state=$state AND district=$district AND os_id=$os_id")
		rlist = results.list()
		if len(rlist) == 0:
			lid = db.insert('legislators',full_name=name,title=title,party=party,state=state,district=district,background_info=info,os_id=osid)
		else:
			lid = rlist[0]['id']
		
		# add citations
		if citations is not None:
			for ref in citations:
				# get citation_ids from ref #s
				results = db.select('citations',{'number':ref,'page':'ALEC_Politicians'},where="number=$number AND page=$page")
				rlist= results.list()
				if len(rlist) == 0:
					logging.error("Couldn't Find citation when adding corporations")
				else:
					citid = rlist[0]['id']
				results = db.select('legislator_to_citation',where="legislator_id=$lid AND citation_id=$citid",vars={'lid':lid,'citid':citid})
				rlist = results.list()
				if len(rlist) == 0:
					res =  db.insert('legislator_to_citation', legislator_id=lid, citation_id=ref)
			#logging.info('+ added legislator to database')
			#except:
			#	logging.error('Failed adding legislator to database')

	def _add_citations(self,citations,page):
		''' Clean &  Add citations to database '''
		refs = []
		for each in citations:
			each = scrape("""<a title=""></a> {{ |html}}""",each)
			html = lxml.html.fromstring(each)
			for t in html:
				if t.tag == 'sup':
					t.drop_tree()
			refs.append(lxml.html.tostring(html))
		corpcitations = enumerate(refs,start=1)
		for num,each in corpcitations:
			result = db.select('citations',where="number=$num AND text=$txt AND page=$page",vars={'num':num,'txt':each,'page':page})
			rlist = result.list()
			if len(rlist) == 0:
				db.insert('citations',number=num,text=each,page=page)

class task_forces:
	def __init__(self):
		pass
	def get(self):
		pass
	
if __name__ == "__main__":
	legislators().get()
