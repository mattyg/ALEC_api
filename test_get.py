import urllib2
html = urllib2.urlopen("http://www.sourcewatch.org/index.php?title=ALEC_Task_Force_Politicians").read()
tfile = open('task_force.txt','r+')
tfile.write(html)
tfile.close()
