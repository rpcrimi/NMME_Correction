import os
import re
import sys
import shlex
import argparse
import subprocess

def convert_file(inputFile):
	print inputFile
	print "Original Size:\t%s" % (os.path.getsize(inputFile))

	outputFile = inputFile.split(".nc")[0] + ".nc4"
	call = "nccopy -k 4 -d 2 %s %s" % (inputFile, outputFile)
	p = subprocess.Popen(shlex.split(call.encode('ascii')))
	returnCode = p.returncode

	out = "None"
	while out:
		call = "/usr/sbin/lsof"
		grep = "grep %s" % (inputFile)
		p2 = subprocess.Popen(call, stdout=subprocess.PIPE)
		p3 = subprocess.Popen(shlex.split(grep), stdin=p2.stdout, stdout=subprocess.PIPE)
		p2.stdout.close()
		out, err = p3.communicate()
		p3.stdout.close()
		returnCode = p.returncode

	print "New Size:\t%s" % (os.path.getsize(outputFile))


# Return a list of all netCDF files in "direrctory"
def get_nc_files(directory, regexFilter):
	print "Gathering Files..."
	if ".nc" in directory:
		return [directory]
	else:
		matches = []
		# Do a walk through input directory
		for root, dirnames, files in os.walk(directory):
			# Find all filenames with .nc type
			for filename in files:
				filename = os.path.join(root, filename)
				if filename.endswith(('.nc', '.nc4')) and re.match(regexFilter, filename):
					matches.append(filename)
		return matches


def main():
	parser = argparse.ArgumentParser(description='Pad Header Script')
	parser.add_argument("-s", "--scrDir",   dest="scrDir",   help = "Directory to pad headers")
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
		for f in files:
			convert_file(f)

if __name__ == "__main__":
	main()