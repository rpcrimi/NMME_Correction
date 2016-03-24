import re
import os
import argparse

def main():
	parser = argparse.ArgumentParser(description='File Name Correction Algorithm')
	parser.add_argument("-srcDir",          dest="srcDir", help = "")
	parser.add_argument("-folderName",      dest="folderName")
	parser.add_argument("-replacementName", dest="replacementName")
	args = parser.parse_args()

	print "Gathering Files..."

	regexFilter = re.compile(".*/%s/.*" % args.folderName)
	matches = []
	# Do a walk through input directory
	for root, dirnames, files in os.walk(args.srcDir):
		# Find all filenames with .nc type
		for filename in files:
			filename = os.path.join(root, filename)
			if filename.endswith(('.nc')) and re.match(regexFilter, filename):
				dstFileName = dstFolder + filename
				if not os.path.isfile(dstFileName):
					# Add full path of netCDF file to matches list
					matches.append(filename)
	print matches

if __name__ == "__main__":
	main()