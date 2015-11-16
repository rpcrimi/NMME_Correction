import os
import re
import argparse

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
	parser.add_argument("-s", "--scrDir", dest="scrDir", help = "Directory to pad headers")
	parser.add_argument("-f", "--filter", dest="filter", help = "Regex filter for filenames")


	if args.filter:
		regexFilter = re.compile(args.filter)
	else:
		regexFilter = re.compile(".*")

	l = get_nc_files(args.scrDir, regexFilter)
	print l

if __name__ == "__main__":
	main()
