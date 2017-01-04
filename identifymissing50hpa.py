import os
import re
import shlex
import subprocess
from progressbar import *

srcDir = "/datazone/nmme/output1/UM-RSMAS/CCSM4/"
regexFilter = re.compile(".*(g|ta|ua|va)_day.*")

print "Gathering Files..."
matches = []
for root, dirnames, files in os.walk(srcDir):
	# Find all filenames with .nc type
	for filename in files:
		filename = os.path.join(root, filename)
		if filename.endswith(('.nc', '.nc4')) and re.match(regexFilter, filename):
				matches.append(filename)

print "Analyzing Files..."
missingData = []
i = 1
widgets = ['Percent Done: ', Percentage(), ' ', AnimatedMarker(), ' ', ETA()]
bar = ProgressBar(widgets=widgets, maxval=len(matches)).start()
for f in matches:
	call = "ncdump -v lev_p %s" % (f) 
	p = subprocess.Popen(shlex.split(call.encode('ascii')), stdout=subprocess.PIPE)
	out, err = p.communicate()
	p.stdout.close()
	if err: print(err)
	else:
		levels = out.split("data:")[-1]
		if "850, 500, 200, 100, 50, 10 ;" not in levels:
			missingData.append(f)
	bar.update(i)
	i = i + 1

print missingData