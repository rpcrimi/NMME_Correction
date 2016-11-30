import argparse
import datetime
import os
import sys
import ast
import re
import pprint
import pymongo
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from progressbar import *
from dateutil import rrule

connection            = pymongo.MongoClient()
db                    = connection["Attribute_Correction"]
CFVars                = db["CFVars"]
versionRegex          = re.compile('v[0-9]+')
json_key              = json.load(open('/datazone/nmme/convert_final/NMME_Correction/NMME Archive Status-fbde24980f40.json'))
scope                 = ['https://spreadsheets.google.com/feeds']
credentials           = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc                    = gspread.authorize(credentials)
sheets                = gc.open("NMME Archive Status")
spreadsheets          = {}
spreadsheets['atmos'] = {}
spreadsheets['ocean'] = {}
spreadsheets['atmos']['day'] = sheets.get_worksheet(0)
spreadsheets['atmos']['3hr'] = sheets.get_worksheet(1)
spreadsheets['atmos']['6hr'] = sheets.get_worksheet(2)
spreadsheets['ocean']['mon'] = sheets.get_worksheet(3)

class FileExistsValidator:
	def __init__(self, srcDir, frequencies, variable, realms, dateRanges, fileOrder, ensembleRange, logFile, model_id=None):
		self.srcDirs = []
		if model_id:
			self.srcDirs.append(srcDir+model_id)
			self.model_id = model_id
		else:
			for model_id in self.get_model_ids(srcDir):
				self.srcDirs.append(srcDir+model_id)
		self.frequencies        = frequencies
		self.variable           = [variable]
		self.realms             = realms
		self.logFile            = logFile
		self.ensembleRange      = ensembleRange

		self.initializationDates = []
		for RANGE in dateRanges:
			start = datetime.date(RANGE[0][0], RANGE[0][1], 1)
			end   = datetime.date(RANGE[1][0], RANGE[1][1], 1)
			for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
				self.initializationDates.append(str(dt.year) + format(dt.month, '02') + format(dt.day, '02'))

		self.fileOrder         = fileOrder
		self.numEnsembles      = self.ensembleRange[1] - self.ensembleRange[0] + 1
		self.totalFiles        = float(len(self.initializationDates)*len(self.frequencies)*len(self.variable)*len(self.realms)*self.numEnsembles)
		self.totalFilesMissing = 0.0

	def print_missing_info(self):
		print >> open(self.logFile, 'a'), "Total Files Expected: [%d]" % self.totalFiles
		totalFilesFound = self.totalFiles - self.totalFilesMissing
		print >> open(self.logFile, 'a'), "Total Files Found:    [%d]" % totalFilesFound
		percentMissing = (100.0 * totalFilesFound)/self.totalFiles
		print >> open(self.logFile, 'a'), "Percent Found:        [%.2f]" % percentMissing
		return percentMissing

	def get_missing_files(self, folderType):
		missing     = 1
		folderIndex = self.fileOrder.index(folderType)
		for i in range(folderIndex+1, len(self.fileOrder)):
			missing *= len(eval('self.'+self.fileOrder[i]))
		missing *= self.numEnsembles
		return missing

	def get_model_ids(self, srcDir):
		if "UM-RSMAS" in srcDir:
			return ["CCSM4"]
		elif "CCCMA" in srcDir:
			return ["CanCM3", "CanCM4"]
		elif "NASA-GMAO" in srcDir:
			return ["GEOS-5"]
		elif "NOAA-GFDL" in srcDir:
			return ["FLORB-01"]	
		elif "NCEP" in srcDir:
			return ["CFSV2-2011"]

	def print_dict(self, missingType, dictionary):
		print >> open(self.logFile, 'a'), "MISSING %s: " % missingType.upper()
		for key, val in dictionary.iteritems():
			if val != []:
				print >> open(self.logFile, 'a'), ""
				print >> open(self.logFile, 'a'), key + ":"
				with open(self.logFile, 'a') as out:
					pprint.pprint(dictionary[key], out)
		print >> open(self.logFile, 'a'), "\n"

	def check_ensembles(self, parentFolders):
		doesNotExist = {}
		doesExist    = {}
		for parentFolder in parentFolders:
			doesNotExist[parentFolder] = []
			doesExist[parentFolder]    = []
			files                      = [f for f in os.listdir(parentFolder) if ".nc" in f]
			for realization in range(self.ensembleRange[0], self.ensembleRange[1]+1):
				ensemble = "r%si1p1" % realization
				ens      = "ens%s" % format(realization, '02')
				found = [s for s in files if ensemble in s] or [s for s in files if ens in s]
				if found:
					doesExist[parentFolder].append(ensemble)
				else:
					self.totalFilesMissing += 1
					doesNotExist[parentFolder].append(ensemble)
				found = False

		self.print_dict("ensembles", doesNotExist)

	def check_folders(self, parentFolders, folderType):
		doesNotExist = {}
		doesExist    = {}
		if folderType not in ["initializationDates", "frequencies", "realms", "variable"]:
			return [(parentFolder + "/" + folderType) for parentFolder in parentFolders]
		else:
			for parentFolder in parentFolders:
				if os.path.exists(parentFolder):
					subdir = [name for name in os.listdir(parentFolder) if os.path.isdir(os.path.join(parentFolder, name))][0]
					if re.match(versionRegex, subdir):
						parentFolder += "/" + subdir
					doesNotExist[parentFolder] = []
					doesExist[parentFolder]    = []
					for folder in eval('self.'+folderType):
						desiredFolder = parentFolder + "/" + folder
						if not os.path.exists(desiredFolder):
							self.totalFilesMissing += self.get_missing_files(folderType)
							doesNotExist[parentFolder].append(desiredFolder)
						else:
							doesExist[parentFolder].append(desiredFolder)
				else:
					print >> open(self.logFile, 'a'), "WARNING: MISSING FOLDER [%s] \n" % parentFolder


			self.print_dict(folderType, doesNotExist)

			if doesExist:
				fullList = []
				for val in doesExist.values():
					fullList += val
				return fullList

	def validate(self):
		parentFolders = self.srcDirs
		for folder in self.fileOrder:
			parentFolders = self.check_folders(parentFolders, folder)
			if not parentFolders:
				break

		self.check_ensembles(parentFolders)

		return self.print_missing_info()

def update_cell(spreadsheet, var, column, dictionary):
	cursor = db.CFVars.find_one({"Var Name": {'$eq': var}})

	try:
		row = spreadsheet.find(var.upper()).row
	except:
		lastRow = len(spreadsheet.get_all_values())
		spreadsheet.update_cell(lastRow+1, 1, var.upper())
		row = spreadsheet.find(var.upper()).row

	column = spreadsheet.find(column).col
	# Update cell value to contain percentage
	spreadsheet.update_cell(row, column, "%.2f" % round(dictionary["Percentage"], 2))
	# Update Standard Name Field
	if cursor:
		spreadsheet.update_cell(row, 2, cursor["CF Standard Name"])
	# Update Realm and Freq Fields
	spreadsheet.update_cell(row, 3, dictionary["Realm"])
	spreadsheet.update_cell(row, 4, dictionary["Frequencies"])

def main():
	parser = argparse.ArgumentParser(description='File Name Creator:\n All arguments should be comma seperated. For example, checking for variables "pr, hus, g" should be "-v g,hus,pr"', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-s", "--srcDir",      dest="srcDir",            help="Source Directory (IGNORE MODEL_ID) (ex. -s CCCMA/, UM-RSMAS/ not CCCMA/CanCM3 or UM-RSMAS/CCSM4)")
	parser.add_argument("-m", "--model_id",    dest="model_id",          help="Optional Model ID for cases when only one model is desired (ex. Just look at CanCM3 instead of CanCM3 and CanCM4")
	parser.add_argument("-f", "--frequencies", dest="frequencies",       help="Frequencies (ex. -f day,mon)")
	parser.add_argument("-v", "--vars",        dest="vars",              help="Variable Name (ex. -v g,hus,pr)")
	parser.add_argument("-r", "--realm",       dest="realms",            help="Modeling Realms (ex. -r atmos,land)")
	parser.add_argument("-d", "--dates",       dest="dates",             help="Date Ranges (NON-OCTAL FORMAT) (ex. 1982-01 to 1984-12 and 1990-01 to 1991-01 would be [[[1982,1],[1984,12]], [[1990,1],[1991,1]]]")
	parser.add_argument("-o", "--order",       dest="order",             help="Optionaly order of folders under srcDir (ex. -o initializationDates,frequencies,realms,variables for NMME data)")
	parser.add_argument("-u", "--update",      dest="updateSpreadsheet", help="If set, script will update Google Spreadsheet that represents the modeling realm and frequency", default=False, action='store_true')
	parser.add_argument("-l", "--logfileDir",  dest="logfileDir",        help="logfile directory (REQUIRED)")
	parser.add_argument("-e", "--ensembles",   dest="ensembles",         help="ensemble range (ex. [1,10] is default)", default="[1,10]")
	args = parser.parse_args()
	if(len(sys.argv) == 1):
		parser.print_help()

	elif args.srcDir and args.frequencies and args.realms and args.dates and args.logfileDir:
		srcDir        = args.srcDir
		frequencies   = args.frequencies.split(",")
		realms        = args.realms.split(",")
		dateRanges    = ast.literal_eval(args.dates)
		ensembleRange = ast.literal_eval(args.ensembles)

		if args.vars:
			variables = args.vars.split(",")
		else:
			cursor = db.CFVars.find()
			variables = [var["Var Name"] for var in cursor]

		if args.order:
			fileOrder = args.order.split(",")
		else:
			fileOrder = ["initializationDates", "frequencies", "realms", "variable"]

		results = {}
		totalVars = len(variables)
		widgets = ['Percent Done: ', Percentage(), ' ', AnimatedMarker(), ' ', ETA()]
		bar = ProgressBar(widgets=widgets, maxval=totalVars).start()
		for i,var in enumerate(variables):
			logFile = args.logfileDir+frequencies[0]+"_"+realms[0]+"_"+var+".log"
			f = FileExistsValidator(srcDir, frequencies, var, realms, dateRanges, fileOrder, ensembleRange, logFile, args.model_id)

			results[var] = f.validate()
			if args.updateSpreadsheet and f.model_id:
				spreadsheet = spreadsheets[realms[0]][frequencies[0]]
				d = {"Percentage": results[var], "Realm": realms[0], "Frequencies": frequencies[0]}
				update_cell(spreadsheet, var, f.model_id, d)
			bar.update(i)
		bar.finish()

		pprint.pprint(results)

	else:
		parser.error("Frequencies, Realms, Date Ranges, and logfile directory are required")

if __name__ == "__main__":
	main()
	