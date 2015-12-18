import os
import re
import sys
import ast
import shlex
import argparse
import datetime
import subprocess
from dateutil import rrule

def pad_hdr(inputFile, pad_size):
	print inputFile
	print "Original Size:\t%s" % (os.path.getsize(inputFile))

	dstFolder = "/datazone/nmme/convert_nc3_pad/"
	for folder in inputFile.split("output1/")[-1].split("/"):
		if ".nc" not in folder:
			dstFolder += folder + "/"
			if not os.path.exists(dstFolder):
				os.makedirs(dstFolder)
	outputFile = "/datazone/nmme/convert_nc3_pad/" + inputFile.split("output1/")[-1]
	call = "ncatted -a foo,global,d,c, -h --hdr_pad %s %s -o %s" % (pad_size, inputFile, outputFile)
	p = subprocess.Popen(shlex.split(call.encode('ascii')))
	returnCode = p.returncode

	out = "None"
	while out:
		print out
		call = "/usr/sbin/lsof"
		grep = "grep %s" % (outputFile)
		p2 = subprocess.Popen(call, stdout=subprocess.PIPE)
		p3 = subprocess.Popen(shlex.split(grep), stdin=p2.stdout, stdout=subprocess.PIPE)
		p2.stdout.close()
		out, err = p3.communicate()
		p3.stdout.close()
		returnCode = p.returncode

	print outputFile
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
	parser.add_argument("-s", "--scrDir",   dest="scrDir",   help="Directory to pad headers")
	parser.add_argument("-d", "--dates",    dest="dates",    help="Date Ranges (NON-OCTAL FORMAT) (ex. 1982-01 to 1984-12 and 1990-01 to 1991-01 would be [[[1982,1],[1984,12]], [[1990,1],[1991,1]]]")
	parser.add_argument("-p", "--pad_size", dest="pad_size", help="Pad size in bytes (default = 2000)", default=2000)
	
	args = parser.parse_args()
	if(len(sys.argv) == 1):
		parser.print_help()

	else:
		dateRanges = ast.literal_eval(args.dates)
		initializationDates = []
		for RANGE in dateRanges:
			start = datetime.date(RANGE[0][0], RANGE[0][1], 1)
			end   = datetime.date(RANGE[1][0], RANGE[1][1], 1)
			for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
				initializationDates.append(str(dt.year) + format(dt.month, '02') + format(dt.day, '02'))

		for initDate in initializationDates:
			regexFilter = re.compile((".*/%s/.*") % initDate)
			files = get_nc_files(args.scrDir, regexFilter)
			for f in files:
				pad_hdr(f, args.pad_size)

if __name__ == "__main__":
	main()
