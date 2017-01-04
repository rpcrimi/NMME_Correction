import os
import re

srcDir = "/datazone/nmme/output1/UM-RSMAS/CCSM4/"
regexFilter = re.compile(".*(g|ta|ua|va)_day.*")

matches = []
for root, dirnames, files in os.walk(srcDir):
	# Find all filenames with .nc type
	for filename in files:
		filename = os.path.join(root, filename)
		if filename.endswith(('.nc', '.nc4')) and re.match(regexFilter, filename):
				matches.append(filename)

print matches