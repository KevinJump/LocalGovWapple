import os
import sys
import PyV8
import requests
from urlparse import urlparse
import sqlite3 as lite
import sys

feature_insert = "INSERT INTO Features(SiteId, Application, Category, Version) VALUES({0},'{1}','{2}','{3}');"

try:
    import json
except ImportError:
    import simplejson as json
	
class LocalWapple(object):

	def __init__(self):
	
		self.file_dir = os.path.dirname(__file__)
		f = open(os.path.join(self.file_dir, 'apps.json'))
		data = json.loads(f.read())
		f.close()
		
		self.categories = data['categories']
		self.apps = data['apps']
		
		self.con = lite.connect('wapple.db')
		self.cur = self.con.cursor()
	
	def process(self):
	
		self.cur.execute("SELECT * FROM Sites")
		
		rows = self.cur.fetchall()
		
		for row in rows:
			siteId = row[0]
			site = row[1]
			url = row[2]
			
			self.wapple(siteId, url)
		
	def wapple(self, id, url):
		ctxt = PyV8.JSContext()
		ctxt.enter()

		f1 = open(os.path.join(self.file_dir, 'js/wappalyzer.js'))
		f2 = open(os.path.join(self.file_dir, 'js/driver.js'))
		ctxt.eval(f1.read())
		ctxt.eval(f2.read())
		f1.close()
		f2.close()

		host = urlparse(url).hostname
		response = requests.get(url)
		html = response.text
		headers = dict(response.headers)
		data = {'host': host, 'url': url, 'html': html, 'headers': headers}
		apps = json.dumps(self.apps)
		categories = json.dumps(self.categories)

		results = ctxt.eval("w.apps = %s; w.categories = %s; w.driver.data = %s; w.driver.init();" % (apps, categories, json.dumps(data)))
		
		#print results 
		answers = json.loads(results) 
		print "{0}:		{1} - {2}".format(id, url, answers.__len__())
		for app, thing in answers.items():
			categories = "" 
			version = thing["version"]
			for c in thing["categories"]: 
				categories = c + "," 
			
			self.cur.execute( feature_insert.format(id, app, categories.strip(","), version) ) 

		self.con.commit() 
	
if __name__ == '__main__':
    try:
        w = LocalWapple()
        w.process()
    except IndexError:
        print ('Usage: python %s <url>' % sys.argv[0])
	