import time
import shlex
import requests
import multiprocessing
import subprocess
from progressbar import *
from bs4 import BeautifulSoup, SoupStrainer

http_source = 'http://collaboration.cmc.ec.gc.ca/cmc/cccma/CanSIPS/NMME/CanCM%d/01/'
for model_id in [3,4]:
	print "Current model:\tCanCM%d" % model_id
	print "Gathering Files..."
	model_http_source = http_source % model_id
	files = []
	response = requests.get(model_http_source).content
	for link in BeautifulSoup(response, 'lxml', parse_only=SoupStrainer('a', href=True)).find_all("a", href=True):
		if '.nc4' in link['href']:
			files.append(link['href'])

	def process_url(file):
		call = "wget -O CanCM%d/%s %s" % (model_id, file, model_http_source+file)
		p = subprocess.Popen(shlex.split(call.encode('ascii')))
		p.wait()

	print "Downloading files..."
	pool = multiprocessing.Pool(processes=4)
	pool.map(process_url, files)