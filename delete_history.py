import re
import os
import shlex
import subprocess

# Return a list of all netCDF files in "direrctory"
def get_nc_files(directory, dstFolder, regexFilter):
	print "Gathering Files..."

	matches = []
	# Do a walk through input directory
	for root, dirnames, files in os.walk(directory):
		# Find all filenames with .nc type
		for filename in files:
			filename = os.path.join(root, filename)
			#if filename.endswith(('.nc', '.nc4')) and re.match(regexFilter, filename):
			if filename.endswith(('.nc')) and re.match(regexFilter, filename):
				dstFileName = dstFolder + filename
				if not os.path.isfile(dstFileName):
					# Add full path of netCDF file to matches list
					matches.append(filename)
	return matches

r = re.compile(".*198[0-9].*/hus")
files = get_nc_files("../../convert_nc3_pad/NASA-GMAO/", "NONE", r)

for f in files:
	call = "ncatted -a history,global,d,c, -h %s" % (f)
	p = subprocess.Popen(shlex.split(call.encode('ascii')))
	returnCode = p.returncode
	print "%s\t%s" % (returnCode, f)