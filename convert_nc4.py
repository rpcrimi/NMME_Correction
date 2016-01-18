import os
import re
import sys
import shlex
import argparse
import subprocess
from progressbar import *

sys.stdout.flush()

def convert_file(inputFile, dstDir):
	newFile = dstDir + inputFile.split("incoming/")[-1] + "4"
	directory = ""

	for folder in newFile.split("/")[:-1]:
		directory += folder + "/"
		if not os.path.exists(directory):
			print "Creating folder:\t%s" % (directory)
			os.makedirs(directory)

	print "Converting File:\t%s" % (newFile)
	call = "nccopy -k 4 -d 2 %s %s" % (inputFile, newFile)
	p = subprocess.check_call(shlex.split(call.encode('ascii')))


# Return a list of all netCDF files in "directory"
def get_nc_files(directory, regexFilter):
	print "Gathering Files..."
	matches = []
	# Do a walk through input directory
	for root, dirnames, files in os.walk(directory):
		# Find all filenames with .nc type
		for filename in files:
			filename = os.path.join(root, filename)
			if filename.endswith('.nc') and re.match(regexFilter, filename):
				matches.append(filename)
	return matches


def main():
	parser = argparse.ArgumentParser(description='Pad Header Script')
	parser.add_argument("-s", "--scrDir",   dest="scrDir",   help = "Directory to convert files")
	parser.add_argument("-d", "--dstDir",   dest="dstDir",   help = "Diretory to move files to")
	parser.add_argument("-f", "--filter",   dest="filter",   help = "Regex filter for filenames")
	
	args = parser.parse_args()
	if(len(sys.argv) == 1):
		parser.print_help()

	else:
		if args.filter:
			regexFilter = re.compile(args.filter)
		else:
			regexFilter = re.compile(".*")

		files = get_nc_files(args.scrDir, regexFilter)

		i = 1
		widgets = ['Percent Done: ', Percentage(), ' ', AnimatedMarker(), ' ', ETA()]
		bar = ProgressBar(widgets=widgets, maxval=len(files)).start()
		for f in files:
			convert_file(f, args.dstDir)
			bar.update(i)
			i = i + 1
		bar.finish()

if __name__ == "__main__":
	main()