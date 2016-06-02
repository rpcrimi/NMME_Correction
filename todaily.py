import os
import re
import sys
import shlex
import pprint
import argparse
import subprocess
from progressbar import *

sys.stdout.flush()

def convert_files(inputFiles, srcDir, dstDir):
	i1 = inputFiles[0].split("_r")[0][-2:] == "00"
	i2 = inputFiles[1].split("_r")[0][-2:] == "06"
	i3 = inputFiles[2].split("_r")[0][-2:] == "12"
	i4 = inputFiles[3].split("_r")[0][-2:] == "18"
	if i1:
		if not (i2 and i3 and i4):
			print "DEBUG: %s" % str(inputFiles)
			return
		

		newFile = dstDir + inputFiles[0].split(srcDir)[-1].replace("6hr", "day").replace("00_", "_")
		directory = ""

		for folder in newFile.split("/")[:-1]:
			directory += folder + "/"
			if not os.path.exists(directory):
				print "INFO: Creating folder:\t%s" % (directory)
				os.makedirs(directory)

		print "INFO: Converting File:\t%s" % (newFile)
		command = "./tmin %s %s %s %s %s" % (" ".join(inputFiles), newFile)
		print command
		p  = subprocess.Popen(shlex.split(command.encode('ascii')), stdout=subprocess.PIPE)
		out, err = p.communicate()
		p.stdout.close()
	
	else:
		return

# Return a list of all netCDF files in "directory"
def get_nc_files(directory, dstDir, regexFilter):
	print "Gathering Files..."
	matches = []
	# Do a walk through input directory
	for root, dirnames, files in os.walk(directory):
		# Find all filenames with .nc type
		for filename in files:
			filename = os.path.join(root, filename)
			if filename.endswith('.nc4') and re.match(regexFilter, filename):
				matches.append(filename)
	return matches


def main():
	parser = argparse.ArgumentParser(description='Pad Header Script')
	parser.add_argument("-s", "--srcDir",   dest="srcDir",   help = "Directory to convert files")
	parser.add_argument("-d", "--dstDir",   dest="dstDir",   help = "Diretory to move files to")
	parser.add_argument("-v", "--vars",     dest="vars",     help = "Variables")
	
	args = parser.parse_args()
	if(len(sys.argv) == 1):
		parser.print_help()

	else:
		for var in args.vars.split(","):
			print "Converting 6hr to Daily: %s" % var
			regexFilter = re.compile(".*/%s/.*" % var)

			files = get_nc_files(args.srcDir, args.dstDir, regexFilter)

			i = 1
			widgets = ['Percent Done: ', Percentage(), ' ', AnimatedMarker(), ' ', ETA()]
			bar = ProgressBar(widgets=widgets, maxval=len(files)).start()
			for k, f in enumerate(files):
				if k+3 < len(files):
					convert_files([f, files[k+1], files[k+2], files[k+3]], args.srcDir, args.dstDir)
					bar.update(i)
					i = i + 1
					break
			bar.finish()

if __name__ == "__main__":
	main()