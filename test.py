import re

strs = ["(R-39); derp","(R-2, derp)", "(R -5) derp"]

strs = ["<p>Cindy Hyde-Smith (R-39); Energy, Environment and Agriculture Task Force</p>","""<p>Michael Thompson (R-2, candidate for U.S. House of Representatives 2010), ALEC Energy, Environment and Agriculture Task Force Alternate</p>""","""<p>Brad Drake (R -5)</p>""","""<span>Bill Posey (now Congressman, R-Rockledge), ALEC Alumni in Congress</span>""","""<span>Gen Olson (R - 33), ALEC Education Task Force Member,</span>""","""<p>King Banaian (R - 15B), ALEC Member</p>"""]

#F+o+r+m+e+r+ +[Rep|Sen|Gov|Del]+[. ]*
# *\(([A-Z/]+)[ -]*([\w]+)[ \);,]*(.*)
regex2 = r"<?\w*>?[[\w]*[,. ]]*(.*)<?/?\w*>?"

for each in strs:
	print each
	split = re.match(regex2,each)
	print split.groups()
'''
data = '3K2-TH~1.PDF'
res = re.match("^([A-Z0-9a-z]*)-([A-Za-z0-9_ \-\(\)~']*).[pdf|PDF]",data)
print res.groups()

#res = scrape("""{* <sup></sup> *} {{|html}}""",str)
#print res
'''

#html = lxml.html.fromstring(str)
#for each in html:
#	if each.tag == 'sup':
#		each.drop_tree()
#
#print lxml.html.tostring(html)
