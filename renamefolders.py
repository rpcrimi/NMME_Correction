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
				matches.append(filename.split(args.folderName+"/")[0])
	
	s = set(matches)
	matches = list(s)
	for file in matches:
		originalFolder = file + args.folderName
		renamedFolder = file + args.replacementName
		print originalFolder
		os.rename(originalFolder, renamedFolder)
		print renamedFolder

if __name__ == "__main__":
	main()