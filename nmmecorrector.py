import pymongo
import logging
import os
import shutil
import argparse
import datetime
import subprocess
import shlex
import sys
import re
import ast
import dropDB
import mongoinit
import pprint
import getpass
from progressbar import *
from difflib import SequenceMatcher

connection        = pymongo.MongoClient()
db                = connection["Attribute_Correction"]
CFVars            = db["CFVars"]
ValidFreq         = db["ValidFreq"]
StandardNameFixes = db["StandardNameFixes"]
VarNameFixes      = db["VarNameFixes"]
FreqFixes         = db["FreqFixes"]
FileNameChanges   = db["FileNameChanges"]

ensembleRegex  = re.compile('.*r[0-9]+i[0-9]+p[0-9]+.*')

class MongoController:
	# Find all documents in collection that match query
	def query_DB(self, collection, query):
		l = []

		if collection   == "CFVars":
			cursor      = db.CFVars.find(query)
		elif collection == "ValidFreq":
			cursor      = db.ValidFreq.find(query)
		elif collection == "StandardNameFixes":
			cursor      = db.StandardNameFixes.find(query)
		elif collection == "VarNameFixes":
			cursor      = db.VarNameFixes.find(query)
		elif collection == "FreqFixes":
			cursor      = db.FreqFixes.find(query)
		elif collection == "FileNameChanges":
			cursor      = db.FileNameChanges.find(query)
		else:
			return "No Matching Collection"
		if cursor:
			for record in cursor:
				l.append(record)
			return l

	# Find one document in collection that mateches query
	def find_one(self, collection, query):
		if collection   == "CFVars":
			cursor      = db.CFVars.find_one(query)
		elif collection == "ValidFreq":
			cursor      = db.ValidFreq.find_one(query)
		elif collection == "StandardNameFixes":
			cursor      = db.StandardNameFixes.find_one(query)
		elif collection == "VarNameFixes":
			cursor      = db.VarNameFixes.find_one(query)
		elif collection == "FreqFixes":
			cursor      = db.FreqFixes.find_one(query)
		elif collection == "FileNameChanges":
			cursor      = db.FileNameChanges.find_one(query)
		else:
			print "No Matching Collection"
		if cursor:
			return cursor
		else:
			return None

	# Return the history of fileName
	def traverse_history(self, fileName):
		changeList = []
		cursor     = db.FileNameChanges.find({"Info.fullPath": {'$regex': fileName}})
		for record in cursor:
			changeList.append(record)
			# If the file has a new name ==> Recurse with the New File Name
			if "New File Name" in record["Info"]:
				changeList.append(self.traverse_history(record["Info"]["New File Name"]))
		return changeList

	# Store file info into FileNameChanges collection
	def store_file_info(self, pathDict):
		db.FileNameChanges.insert_one({"File Name": pathDict["fullPath"], "Info": pathDict, "Time": Logger.get_datetime()})

# Class to handle logging calls
class Logger:
	def __init__(self, logFile=None):
		self.logFile = logFile
		if self.logFile:
			self.logger  = logging.getLogger(self.logFile)
			self.logger.setLevel(logging.DEBUG)
			self.handler = logging.FileHandler(self.logFile)
			self.handler.setLevel(logging.DEBUG)

			self.formatter = logging.Formatter('%(levelname)-8s %(message)s')
			self.handler.setFormatter(self.formatter)

			self.logger.addHandler(self.handler)

	def remove_file_handler(self):
		self.logger.removeHandler(self.handler)

	# Return formated date/time for logfile
	@staticmethod
	def get_datetime(): return str(datetime.datetime.now()).split(".")[0].replace(" ", "T")

	# Set logfile based on srcDir or fileName if logFile not provided
	def set_logfile(self, src):
		if self.logFile == None: 
			if ".nc" in src:
				self.logFile = os.path.basename(src).replace(".nc", "").rstrip("4") + self.get_datetime() + ".log"
			else:
				self.logFile = src.replace("/", "") + "_" + self.get_datetime() + ".log"

			self.logger  = logging.getLogger(self.logFile)
			self.logger.setLevel(logging.DEBUG)
			self.handler = logging.FileHandler(self.logFile)
			self.handler.setLevel(logging.DEBUG)

			self.formatter = logging.Formatter('%(levelname)-8s %(message)s')
			self.handler.setFormatter(self.formatter)

			self.logger.addHandler(self.handler)

	# Log info of type==logType about changes to fileName
	# Text is a list of info to log
	def log(self, fileName, text, logType):
		if logType == 'File Started':
			self.logger.info("-" * 100)
			self.logger.info("Starting in file: [%s]", fileName)

		elif logType == 'File Confirmed':
			self.logger.info("Confirmed file: [%s]", fileName)

		# Standard Name/Units Logs
		elif logType == 'Standard Name Confirmed':
			self.logger.info("Standard Name [%s] confirmed", text)

		elif logType == 'Switched Standard Name':
			self.logger.debug("Switched [%s] standard_name from [%s] to [%s]", text[0], text[1], text[2])

		elif logType == 'Switched Variable':
			self.logger.debug("Switched variable name from [%s:%s] to [%s:%s]", text[0], text[2], text[1], text[2])

		elif logType == 'Estimated Standard Name':
			self.logger.debug("Standard Name [%s:%s] best 3 estimates: %s", text[0], text[1], text[2])

		elif logType == 'No Standard Names':
			self.logger.debug("[%s]: no standard names defined", fileName)

		elif logType == 'No Matching Var Name':
			self.logger.debug("[%s] recommended Variable Names: %s", text[0], text[1])

		elif logType == 'Changed Units':
			self.logger.debug("Changed [%s] units from [%s] to [%s]", text[0], text[1], text[2])

		elif logType == 'Confirmed Units':
			self.logger.info("Units [%s:%s] confirmed", text[0], text[1])


		# File Name Logs
		elif logType == 'Var Error':
			self.logger.debug("Variable [%s] not recognized", text)

		elif logType == 'Freq Error':
			self.logger.debug("Frequency [%s] not recognized", text)

		elif logType == 'Model Error':
			self.logger.debug("Model [%s] not recognized", text)	

		elif logType == 'Realization Error':
			self.logger.debug("Metadata Realization [%s] does not match File Name Realization [%s]", text[0], text[1])

		elif logType == 'File Name Error':
			self.logger.debug("File Name [%s] does not match created File Name [%s]", text[0], text[1])

		elif logType == 'Renamed File Name':
			self.logger.debug("File Name [%s] renamed to [%s]", fileName, text)

		elif logType == 'Realization Fix':
			self.logger.debug("Metadata Realization changed from [%s] to [%s]", text[0], text[1])

		elif logType == 'Var Name Fix':
			self.logger.debug("Variable [%s] changed to [%s]", text[0], text[1])

		elif logType == 'Renamed Var Folder':
			self.logger.debug("Folder [%s] renamed to [%s]", text[0], text[1])

		elif logType == 'Renamed Freq Folder':
			self.logger.debug("Renamed Frequency folder name [%s] to [%s]", text[0], text[1])

		elif logType == 'Metadata Fix':
			self.logger.debug("[%s] in metadata changed from [%s] to [%s]", text[0], text[1], text[2])

# Class to handle Metadata queries and changes
class MetadataController:
	def __init__(self, metadataFolder, waitFlag):
		self.metadataFolder = metadataFolder
		self.waitFlag       = waitFlag

	# Return the location of file==fileName
	def get_file_name_location(self, fileName):
		scriptDir = os.path.dirname(os.path.abspath(__file__))
		for root, dirs, files in os.walk(scriptDir):
			if fileName in files:
				return os.path.join(root, fileName) + " "

	# Grab the attribute==attr from the file==fullPath
	# This should only be used for global attributes
	def get_metadata(self, fullPath, var, attr):
		# Create the grep string
		if var:
			grep = "grep %s:%s" % (var,attr)
		else:
			grep = "grep :%s" % (attr)
		dump = "ncdump -h %s" % (fullPath)
		# Dump metadata and grep for attribute
		p  = subprocess.Popen(shlex.split(dump.encode('ascii')), stdout=subprocess.PIPE)
		p2 = subprocess.Popen(shlex.split(grep.encode('ascii')), stdin=p.stdout, stdout=subprocess.PIPE)
		p.stdout.close()
		out, err = p2.communicate()
		p2.stdout.close()
		# Format metadata by removing tabs, newlines, and semicolons and grabbing the value
		if out:
			metadata = out.replace("\t", "").replace("\n", "").replace(" ;", "").split(" = ")[1].strip('"')
			if metadata.isdigit():
				return int(metadata)
			else:
				return metadata
		else:
			return "No Metadata"

	# Grab the header from file==fullPath
	def ncdump(self, fullPath):
		call = "ncdump -h %s" % (fullPath) 
		p = subprocess.Popen(shlex.split(call.encode('ascii')), stdout=subprocess.PIPE)
		out, err = p.communicate()
		p.stdout.close()
		if err: print(err)
		else: return out

	# Edit the attribute in the metadata of file == inputFile
	# histFlag == True means update history
	def ncatted(self, att_nm, var_nm, mode, att_type, att_val, inputFile, histFlag, outputFile=""):
		if att_type == int:
			att_type = "i"
		else:
			att_type = "c"
			att_val = "'%s'" % att_val
		call = "ncatted -a %s,%s,%s,%s,%s %s %s" % (att_nm, var_nm, mode, att_type, att_val, ("" if histFlag else "-h"), inputFile)
		p = subprocess.Popen(shlex.split(call.encode('ascii')))
		returnCode = p.returncode

		if self.waitFlag:
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

		if returnCode == 1:
			return False
		else:
			return True

	# Rename the variable from oldName to newName in file == inputFile
	def ncrename(self, oldName, newName, inputFile, histFlag, outputFile=""):
		call = "ncrename -v %s,%s -d .%s,%s %s %s" % (oldName, newName, oldName, newName, ("" if histFlag else "-h"), inputFile)
		p = subprocess.Popen(shlex.split(call.encode('ascii')))
		returnCode = p.returncode

		if self.waitFlag:
			out = "None"
			while out:
				call = "/usr/sbin/lsof"
				grep = "grep %s" % (inputFile)
				p = subprocess.Popen(call, stdout=subprocess.PIPE)
				p2 = subprocess.Popen(shlex.split(grep), stdin=p.stdout, stdout=subprocess.PIPE)
				p.stdout.close()
				out, err = p2.communicate()
				p2.stdout.close()

		if returnCode == 1:
			return False
		else:

			return True

	# Dump the header of file in pathDict to same directory structure under defined metadataFolder
	def dump_metadata(self, pathDict):
		if self.metadataFolder:
			out = self.ncdump(pathDict["fullPath"])
			dstDir = self.metadataFolder+pathDict["dirName"]
			# If path does not exist ==> create directory structure
			if not os.path.exists(dstDir):
				os.makedirs(dstDir)

			fileName = dstDir+pathDict["fileName"].replace(pathDict["extension"], ".txt")
			with open(fileName, "w") as text_file:
				text_file.write(out)

	# Return formated output of grep call
	def format_output(self, out):
		# Remove tabs and newlines and split on " ;"
		out = out.replace("\t", "").replace("\n", "").replace("standard_name = ", "").replace("\"", "").split(" ;")
		# Return list without empty elements
		return filter(None, out)

	# Return a list of all netCDF files in "direrctory"
	def get_nc_files(self, directory, dstFolder, regexFilter):
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
					#if filename.endswith(('.nc', '.nc4')) and re.match(regexFilter, filename):
					if filename.endswith(('.nc')) and re.match(regexFilter, filename):
						dstFileName = dstFolder + filename
						if not os.path.isfile(dstFileName):
							# Add full path of netCDF file to matches list
							matches.append(filename)
			return matches


	# Return a list of filenames and corresponding standard names in "ncFolder"
	def get_standard_names(self, ncFolder, dstFolder, regexFilter):
		standardNames = []
		# Call ncdump and grep for :standard_name for each netCDF file in ncFolder
		for f in self.get_nc_files(ncFolder, dstFolder, regexFilter):
			call = "ncdump -h %s" % (f) 
			p = subprocess.Popen(shlex.split(call.encode('ascii')), stdout=subprocess.PIPE)
			p2 = subprocess.Popen(shlex.split('grep :standard_name'), stdin=p.stdout, stdout=subprocess.PIPE)
			p.stdout.close()
			out, err = p2.communicate()
			standardNames.append((f, self.format_output(out)))
			p2.stdout.close()
		return standardNames

# Class to validate file names and metadata
class FileNameValidator:
	def __init__(self, srcDir, fileName, regexFilter, metadataFolder, logger, fixFlag, histFlag, waitFlag):
		if srcDir: 
			self.srcDir   = srcDir
			self.fileName = None
		else:
			self.srcDir   = None      
			self.fileName = fileName

 		if regexFilter:
			self.regexFilter     = re.compile(regexFilter)
		else:
			self.regexFilter     = re.compile(".*")

 		self.mongoController     = MongoController()
		self.metadataController  = MetadataController(metadataFolder, waitFlag)
		self.logger              = logger
		self.fixFlag             = fixFlag
		self.histFlag            = histFlag
		self.pathDicts           = {}

	# Return a list of all netCDF files in srcDir or just list of single fileName
	def get_nc_files(self):
		print "Gathering Files..."
		if self.fileName and re.match(self.regexFilter, fileName):
			return [self.fileName]
		else:
			matches = []
			# Do a walk through input directory
			for root, dirnames, files in os.walk(self.srcDir):
				# Find all filenames with .nc type
				for filename in files:
					filename = os.path.join(root, filename)
					#if filename.endswith(('.nc', '.nc4')) and re.match(self.regexFilter, filename):
					if filename.endswith(('.nc')) and re.match(self.regexFilter, filename):
							matches.append(filename)
			return matches

	# Save all path info to pathDicts[fullPath] entry
	def get_path_info(self, fullPath):
		dictionary = {}
		if "/" in fullPath:
			splitFileName = fullPath.split("/")
			if 'NOAA-GFDL' in fullPath:
				institute_id_index              = splitFileName.index('NOAA-GFDL')
				dictionary["institute_id"]      = splitFileName[institute_id_index]
				dictionary["model_id"]          = splitFileName[institute_id_index+1]
				dictionary["experiment_id"]     = int(splitFileName[institute_id_index+2])
				dictionary["frequency"]         = splitFileName[institute_id_index+3]
				dictionary["modeling_realm"]    = splitFileName[institute_id_index+4]
				dictionary["variable"]          = splitFileName[institute_id_index+6]
			elif 'CCCMA' in fullPath:
				institute_id_index              = splitFileName.index('CCCMA')
				dictionary["institute_id"]      = splitFileName[institute_id_index]
				dictionary["model_id"]          = splitFileName[institute_id_index+1]
				dictionary["experiment_id"]     = int(splitFileName[institute_id_index+2])
				dictionary["frequency"]         = splitFileName[institute_id_index+3]
				dictionary["modeling_realm"]    = splitFileName[institute_id_index+4]
				dictionary["variable"]          = splitFileName[institute_id_index+6]
			elif 'UM-RSMAS' in fullPath:
				institute_id_index              = splitFileName.index('UM-RSMAS')
				dictionary["institute_id"]      = splitFileName[institute_id_index]
				dictionary["model_id"]          = splitFileName[institute_id_index+1]
				dictionary["experiment_id"]     = int(splitFileName[institute_id_index+2])
				dictionary["frequency"]         = splitFileName[institute_id_index+3]
				dictionary["modeling_realm"]    = splitFileName[institute_id_index+4]
				dictionary["variable"]          = splitFileName[institute_id_index+5]
			elif 'NASA-GMAO' in fullPath:
				institute_id_index              = splitFileName.index('NASA-GMAO')
				dictionary["institute_id"]      = splitFileName[institute_id_index]
				dictionary["model_id"]          = splitFileName[institute_id_index+1]
				dictionary["experiment_id"]     = int(splitFileName[institute_id_index+2])
				dictionary["frequency"]         = splitFileName[institute_id_index+3]
				dictionary["modeling_realm"]    = splitFileName[institute_id_index+4]
				dictionary["variable"]          = splitFileName[institute_id_index+5]
		
		dictionary["project_id"]            = "NMME"
		dictionary["startyear"]             = int(str(dictionary["experiment_id"])[:4])
		dictionary["startmonth"]            = int(str(dictionary["experiment_id"])[4:6])

		dictionary["fileName"]              = os.path.basename(fullPath)
		dictionary["dirName"]               = os.path.dirname(fullPath)
		dictionary["fullPath"]              = fullPath
		dictionary["extension"]             = "."+fullPath.split(".")[-1]

		if re.match(ensembleRegex, fullPath):
			dictionary["ensemble"]          = [match for match in fullPath.split("_") if re.match(ensembleRegex, match)][0].replace(dictionary["extension"], "")
		elif "ens" in fullPath:
			ens                             = [match for match in fullPath.split("_") if "ens" in match][0]
			realization                     = ens.split("s")[-1].lstrip('0')
			dictionary["ensemble"]          = "r%si1p1" % realization
		else:
			realization                     = self.metadataController.get_metadata(fullPath, None, "realization").lstrip('0')
			dictionary["ensemble"]          = "r%si1p1" % realization
		dictionary["realization"]           = int(dictionary["ensemble"].replace("r", "").split("i")[0])


		dictionary["rootFileName"]          = ".".join(fullPath.split(".")[:-1])
		if not re.match(ensembleRegex, dictionary["rootFileName"].split("_")[-1]):
			dictionary["endDate"]           = dictionary["rootFileName"].split("-")[-1]
			dictionary["endyear"]           = dictionary["endDate"][:4]
			dictionary["endmonth"]          = dictionary["endDate"][4:6]
			dictionary["startEnd"]          = "_"+dictionary["experiment_id"] + "-" + dictionary["endDate"]
		else:
			dictionary["startEnd"]          = ""

		dictionary["I/O Error"]             = False
		dictionary["Log File"]              = self.logger.logFile
		dictionary["Changes"]               = []
		self.pathDicts[fullPath] = dictionary

	# Return new file name based on path information
	def get_new_filename(self, pathDict):
		return pathDict["variable"]+"_"+pathDict["frequency"]+"_"+pathDict["model_id"]+"_"+str(pathDict["experiment_id"])+"_"+pathDict["ensemble"]+pathDict["startEnd"]+pathDict["extension"]

	# Validate the variable provided in fileName
	def validate_variable(self, fileName):
		pathDict = self.pathDicts[fileName]
		# Variable does not exist in CF Standards collection
		if not self.mongoController.find_one("CFVars", {"Var Name": pathDict["variable"]}):
			# Try to find known fix for provided variable
			#--------------------------------------------
			cursor = self.mongoController.find_one("VarNameFixes", {"Incorrect Var Name": pathDict["variable"]})
			if cursor:
				self.logger.log(self.pathDicts[fileName]["fileName"], [self.pathDicts[fileName]["variable"], cursor["Known Fix"]], 'Var Name Fix')
				if self.fixFlag:
					self.pathDicts[fileName]["Changes"].append("In File Name: " + self.pathDicts[fileName]["variable"] + " --> " + cursor["Known Fix"])
				self.pathDicts[fileName]["variable"] = cursor["Known Fix"]

				# Fix the folder that is named after the variable
				#------------------------------------------------
				oldDir      = self.pathDicts[fileName]["dirName"]
				# Get the name of the variable folder
				parDirIndex = oldDir.rfind('/')
				parDir      = oldDir[parDirIndex+1:]
				# Change variable directory to the known fix
				parDir = cursor["Known Fix"]
				newDir = oldDir[:parDirIndex+1]+parDir
				if self.fixFlag:
					os.rename(oldDir, newDir)
					self.pathDicts[fileName]["Changes"].append("In Folder Name: " + oldDir + " --> " + newDir)
				self.logger.log(self.pathDicts[fileName]["fileName"], [oldDir, newDir], 'Renamed Var Folder')
			else:
				self.logger.log(self.pathDicts[fileName]["fileName"], self.pathDicts[fileName]["variable"], 'Var Error')
			# Error seen	
			return False
		else:
			return True

	# Validate the frequency provided in fileName
	def validate_frequency(self, fileName):
		pathDict = self.pathDicts[fileName]
		# Frequency does not exist in CF Standards collection
		if not self.mongoController.find_one("ValidFreq", {"Frequency": pathDict["frequency"]}):
			# Try to find known fix for provided variable
			cursor = self.mongoController.find_one("FreqFixes", {"Incorrect Freq": pathDict["frequency"]})
			if cursor:
				# Fix the folder that is named after the variable
				#------------------------------------------------
				oldDir = pathDict["fullPath"].split(pathDict["frequency"])[0]+pathDict["frequency"]+"/"
				newDir = pathDict["fullPath"].split(pathDict["frequency"])[0]+cursor["Known Fix"]+"/"
				if self.fixFlag:
					os.rename(oldDir, newDir)
					self.pathDicts[fileName]["Changes"].append(["In Folder Name: " + oldDir + " --> " + newDir, "In File Name: " + pathDict["frequency"] + " --> " + cursor["Known Fix"]])
				self.logger.log(pathDict["fileName"], [pathDict["frequency"], cursor["Known Fix"]], 'Renamed Freq Folder')
				pathDict["fullPath"]  = pathDict["fullPath"].replace(pathDict["frequency"], cursor["Known Fix"])
				pathDict["frequency"] = cursor["Known Fix"]

			else:
				log(logFile, pathDict["fileName"], pathDict["frequency"], 'Freq Error')
			# Error seen
			return False
		else:
			return True

	# Validate the metadata in fileName
	def validate_metadata(self, fileName):
		pathDict = self.pathDicts[fileName]
		flag = True
		# For each desired value of metadata ==> Check against path information and update accordingly
		for meta in ["frequency", "realization", "model_id", "modeling_realm", "institute_id", "startyear", "startmonth", "endyear", "endmonth", "experiment_id", "project_id"]:
			metadata = self.metadataController.get_metadata(pathDict["fullPath"], None , meta)
			if meta in pathDict and metadata != pathDict[meta]:
				if self.fixFlag:
					# Update the metadata to path information
					if not self.metadataController.ncatted(meta, "global", "d", type(pathDict[meta]), pathDict[meta], pathDict["fullPath"], self.histFlag):
						self.pathDicts[fileName]["I/O Error"] = True
					if not self.metadataController.ncatted(meta, "global", "c", type(pathDict[meta]), pathDict[meta], pathDict["fullPath"], self.histFlag):
						self.pathDicts[fileName]["I/O Error"] = True
					self.pathDicts[fileName]["Changes"].append(str(metadata) + " --> " + str(pathDict[meta]))
				self.logger.log(pathDict["fileName"], [meta, metadata, str(pathDict[meta])], 'Metadata Fix')
				flag = False

		return flag

	# Validate the provided fileName
	def validate_filename(self, fileName):
		pathDict    = self.pathDicts[fileName]
		# Create new file name based on path information
		newFileName = self.get_new_filename(pathDict)
		# If filename differs from created filename ==> rename file to created filename
		if pathDict["fileName"] != newFileName:
			self.logger.log(pathDict["fileName"], [pathDict["fileName"], newFileName], 'File Name Error')
			if self.fixFlag:
				newFullPath = pathDict["dirName"]+"/"+newFileName
				os.rename(pathDict["fullPath"], newFullPath)
				self.logger.log(pathDict["fileName"], newFileName, 'Renamed File Name')
				self.pathDicts[fileName]["New File Name"] = newFileName
			# Error seen
			return False
		else:
			return True

	def validate_contact(self, fileName):
		contact = self.metadataController.get_metadata(fileName, None, "contact")
		if contact == "No Metadata":
			self.pathDicts[fileName]["Contact"] = False

	# Fix the file name and metadata of file=fileName
	def fix_filename(self, fileName):
		varFlag         = self.validate_variable(fileName)
		freqFlag        = self.validate_frequency(fileName)
		metadataFlag    = self.validate_metadata(fileName)
		fileFlag        = self.validate_filename(fileName)
		self.validate_contact(fileName)
		return (varFlag and freqFlag and metadataFlag and fileFlag)

	# Validate the input's file names and metadata
	def validate(self, filt=None):
		print "Starting File Name Validation on variable %s" % filt.strip(".*/").upper()
		# Create list of all netCDF files in input
		files = self.get_nc_files()
		i = 1
		widgets = ['Percent Done: ', Percentage(), ' ', AnimatedMarker(), ' ', ETA()]
		bar = ProgressBar(widgets=widgets, maxval=len(files)).start()
		# Fix each file in files list
		for f in files:
			# Set pathDicts[f] entry
			self.get_path_info(f)
			# Dump metadata to same folder structure
			self.metadataController.dump_metadata(self.pathDicts[f])
 			self.logger.log(self.pathDicts[f]["fullPath"], "", 'File Started')
 			# fix_filename saw no errors ==> file is confirmed
			if self.fix_filename(f):
				self.pathDicts[f]["Status"] = "Confirmed"
				self.logger.log(self.pathDicts[f]["fullPath"], "", "File Confirmed")
			else:
				self.pathDicts[f]["Status"] = "Not Confirmed"
			if self.fixFlag:
				if self.pathDicts[f]["Changes"] != []:
					changeInfo = Logger.get_datetime() + " " + getpass.getuser() + ": " + ", ".join(self.pathDicts[f]["Changes"]) + ". "
					self.metadataController.ncatted("history", "global", "a", "c", changeInfo, f, self.histFlag)
				self.mongoController.store_file_info(self.pathDicts[f])
			bar.update(i)
			i = i + 1
		bar.finish()	

class StandardNameValidator:
	def __init__(self, srcDir, fileName, dstDir, regexFilter, metadataFolder, logger, fixFlag, fixUnits, histFlag, waitFlag):
		if srcDir: 
			self.srcDir          = srcDir
			self.fileName        = None
		else:
			self.srcDir          = None      
			self.fileName        = fileName
		self.dstDir              = dstDir
		if regexFilter:
			self.regexFilter     = re.compile(regexFilter)
		else:
			self.regexFilter     = re.compile(".*")
		self.mongoController     = MongoController()
		self.metadataController  = MetadataController(metadataFolder, waitFlag)
		self.logger              = logger
		self.fileFlag            = True
		self.fixFlag             = fixFlag
		self.fixUnits            = fixUnits
		self.histFlag            = histFlag
		self.pathDicts           = {}

	# Save all path info to pathDicts[fullPath] entry
	def get_path_info(self, fullPath):
		dictionary = {}
		if "/" in fullPath:
			splitFileName = fullPath.split("/")
			if 'NOAA-GFDL' in fullPath:
				institute_id_index              = splitFileName.index('NOAA-GFDL')
				dictionary["institute_id"]      = splitFileName[institute_id_index]
				dictionary["model_id"]          = splitFileName[institute_id_index+1]
				dictionary["experiment_id"]     = splitFileName[institute_id_index+2]
				dictionary["frequency"]         = splitFileName[institute_id_index+3]
				dictionary["modeling_realm"]    = splitFileName[institute_id_index+5]
				dictionary["variable"]          = splitFileName[institute_id_index+6]
			elif 'CCCMA' in fullPath:
				institute_id_index              = splitFileName.index('CCCMA')
				dictionary["institute_id"]      = splitFileName[institute_id_index]
				dictionary["model_id"]          = splitFileName[institute_id_index+1]
				dictionary["experiment_id"]     = splitFileName[institute_id_index+2]
				dictionary["frequency"]         = splitFileName[institute_id_index+3]
				dictionary["modeling_realm"]    = splitFileName[institute_id_index+4]
				dictionary["variable"]          = splitFileName[institute_id_index+6]
			elif 'UM-RSMAS' in fullPath:
				institute_id_index              = splitFileName.index('UM-RSMAS')
				dictionary["institute_id"]      = splitFileName[institute_id_index]
				dictionary["model_id"]          = splitFileName[institute_id_index+1]
				dictionary["experiment_id"]     = splitFileName[institute_id_index+2]
				dictionary["frequency"]         = splitFileName[institute_id_index+3]
				dictionary["modeling_realm"]    = splitFileName[institute_id_index+4]
				dictionary["variable"]          = splitFileName[institute_id_index+5]
			elif 'NASA-GMAO' in fullPath:
				institute_id_index              = splitFileName.index('NASA-GMAO')
				dictionary["institute_id"]      = splitFileName[institute_id_index]
				dictionary["model_id"]          = splitFileName[institute_id_index+1]
				dictionary["experiment_id"]     = splitFileName[institute_id_index+2]
				dictionary["frequency"]         = splitFileName[institute_id_index+3]
				dictionary["modeling_realm"]    = splitFileName[institute_id_index+4]
				dictionary["variable"]          = splitFileName[institute_id_index+5]
		
		dictionary["project_id"]            = "NMME"
		dictionary["startyear"]             = dictionary["experiment_id"][:4]
		dictionary["startmonth"]            = dictionary["experiment_id"][4:6]

		dictionary["fileName"]              = os.path.basename(fullPath)
		dictionary["dirName"]               = os.path.dirname(fullPath)
		dictionary["fullPath"]              = fullPath
		dictionary["extension"]             = "."+fullPath.split(".")[-1]

		if re.match(ensembleRegex, fullPath):
			dictionary["ensemble"]          = [match for match in fullPath.split("_") if re.match(ensembleRegex, match)][0].replace(dictionary["extension"], "")
		elif "ens" in fullPath:
			ens                             = [match for match in fullPath.split("_") if "ens" in match][0]
			realization                     = ens.split("s")[-1].lstrip('0')
			dictionary["ensemble"]          = "r%si1p1" % realization
		else:
			realization                     = self.metadataController.get_metadata(fullPath, None, "realization").lstrip('0')
			dictionary["ensemble"]          = "r%si1p1" % realization
		dictionary["realization"]           = dictionary["ensemble"].replace("r", "").split("i")[0]


		dictionary["rootFileName"]          = ".".join(fullPath.split(".")[:-1])
		if not re.match(ensembleRegex, dictionary["rootFileName"].split("_")[-1]):
			dictionary["endDate"]           = dictionary["rootFileName"][-8:]
			dictionary["endyear"]           = dictionary["endDate"][:4]
			dictionary["endmonth"]          = dictionary["endDate"][4:6]
			dictionary["startEnd"]          = "_"+dictionary["experiment_id"] + "-" + dictionary["endDate"]
		else:
			dictionary["startEnd"]          = ""

		dictionary["I/O Error"]             = False
		dictionary["Log File"]              = self.logger.logFile
		dictionary["Changes"]               = []
		self.pathDicts[fullPath] = dictionary

	# Return list of CF Standard Names from CFVars Collection
	def get_CF_Standard_Names(self):
		# Query CFVars for all Variables
		cursor = self.mongoController.query_DB("CFVars", None)
		CFStandards = []
		# Append each CF STandard Name to CFStandards list
		for standardName in cursor:
			CFStandards.append(standardName["CF Standard Name"])
		return CFStandards

	# Return similarity ratio of string "a" and "b"
	def similar(self, a, b):
		a = a.lower()
		b = b.lower()
		return SequenceMatcher(None, a, b).ratio()*100

	# Return the "N" # of CF Standard Vars with the most similarity to "wrongAttr"
	def best_estimates(self, wrongAttr):
		# Grab CF Standard Names
		CFStandards = self.get_CF_Standard_Names()
		similarities = []
		# Calculate percent difference between the wrong attribute and each CF Standard Name
		# Append (standardName, percentOff) tuple to similarities for future sorting
		for standardName in CFStandards:
			percentOff = self.similar(wrongAttr, standardName)
			similarities.append((standardName, percentOff))
		# Sort similarities list by second element in tuple
		similarities.sort(key=lambda x: x[1])

		return list(reversed(similarities[-3:]))

	def estimate_standard_name(self, var, standardName, fileName):
		bestEstimatesList = self.best_estimates(standardName)
		bestEstimates = ""
		for e in bestEstimatesList:
			bestEstimates += str(e[0]) + " | "
		self.logger.log(fileName, [var, standardName, bestEstimates], 'Estimated Standard Name')

	def estimate_var_name(self, var, standardName, fileName):
		cursor = self.mongoController.query_DB("CFVars", {"Var Name": { '$eq': var.lower()}})
		recommendations = ""
		for v in cursor:
			recommendations += v["Var Name"] + " | "
		self.logger.log(fileName, [var+":"+standardName, recommendations], 'No Matching Var Name')	

	def validate_var_standard_name_pair(self, var, standardName, fileName):
		# Check if (var, standardName) is valid CF Standard Name pair
		cursor = self.mongoController.find_one("CFVars", { '$and': [{"CF Standard Name": { '$eq': standardName}}, {"Var Name": {'$eq': var}}]})
		# Log notification of correct attribute
		if cursor:
			metadataUnits = self.metadataController.get_metadata(fileName, var, "units")
			self.pathDicts[fileName]["Units"] = metadataUnits
			if self.fixUnits:
				# Check units for var, standardName pair
				if cursor["Units"] != metadataUnits:
					# Fix and Units flags must be set to true to fix units
					if self.fixFlag:
						if not self.metadataController.ncatted("units", var, "d", "c", cursor["Units"], fileName, self.histFlag):
							self.pathDicts[fileName]["I/O Error"] = True
						if not self.metadataController.ncatted("units", var, "c", "c", cursor["Units"], fileName, self.histFlag):
							self.pathDicts[fileName]["I/O Error"] = True
					self.logger.log(fileName, [var, metadataUnits, cursor["Units"]], 'Changed Units')
				else:
					self.logger.log(fileName, [var, metadataUnits], 'Confirmed Units')

			text = var + ":" + standardName
			self.logger.log(fileName, text, "Standard Name Confirmed")
			# Return true for confirming file
			return True
		else:
			return False

	def find_var_known_fix(self, var, standardName, fileName):
		# Check if (var, standardName) pair is in VarNameFixes collection
		cursor = self.mongoController.find_one("VarNameFixes", { '$and': [{"Incorrect Var Name": { '$eq': var}}, {"CF Standard Name": {'$eq': standardName}}]})
		if cursor:
			if self.fixFlag:
				if not self.metadataController.ncrename(var, cursor["Known Fix"], fileName, self.histFlag):
					self.pathDicts[fileName]["I/O Error"] = True
				self.pathDicts[fileName]["Changes"].append(var + " --> " + cursor["Known Fix"])
			# Log the fix
			self.logger.log(fileName, [var, cursor["Known Fix"], standardName], 'Switched Variable')
			return (cursor["Known Fix"], True)
		else:
			return (var, False)

	def find_standard_name_fix(self, var, standardName, fileName):
		# Set all characters to lowercase
		standardName = standardName.lower()
		# Check if KnownFixes has seen this error before
		cursor = self.mongoController.find_one("StandardNameFixes", { '$and': [{"Incorrect Standard Name": { '$eq': standardName}}, {"Var Name": {'$eq': var}}]})
		# If standardName exists in StandardNameFixes collection
		if cursor:
			# Overwrite standard_name of var to the known fix
			if self.fixFlag:
				if not self.metadataController.ncatted("standard_name", var, "d", "c", cursor["Known Fix"], fileName, self.histFlag):
					self.pathDicts[fileName]["I/O Error"] = True
				if not self.metadataController.ncatted("standard_name", var, "c", "c", cursor["Known Fix"], fileName, self.histFlag):
					self.pathDicts[fileName]["I/O Error"] = True
				self.pathDicts[fileName]["Changes"].append(var + " --> " + cursor["Known Fix"])
			# Log the fix
			self.logger.log(fileName, [var, standardName, cursor["Known Fix"]], 'Switched Standard Name')
			return (cursor["Known Fix"], True)
		else:
			return (standardName, False)

	def confirm_file(self, fileName):
		if self.fileFlag:
			if self.fixFlag:
				# New path for copying file
				dstdir = self.dstDir+os.path.dirname(fileName).replace("../", "")
				# If path does not exist ==> create directory structure
				if not os.path.exists(dstdir):
					os.makedirs(dstdir)
				# Copy original file to dstdir
				shutil.move(fileName, dstdir)
				self.pathDicts[fileName]["Status"]        = "Confirmed"
				self.pathDicts[fileName]["New File Name"] = dstdir + "/" + os.path.basename(fileName)
				self.mongoController.store_file_info(self.pathDicts[fileName])
				if self.pathDicts[fileName]["Changes"] != []:
					changeInfo = Logger.get_datetime() + " " + getpass.getuser() + ": " + ", ".join(self.pathDicts[fileName]["Changes"]) + ". "
					self.metadataController.ncatted("history", "global", "a", "c", changeInfo, fileName, self.histFlag)
			# Log the confirmed file
			self.logger.log(fileName, "", 'File Confirmed')
		
		elif self.fixFlag:
			if self.pathDicts[fileName]["Changes"] == []:
				self.pathDicts[fileName]["Status"] = "No Changes/Not Confirmed"
			else:
				self.pathDicts[fileName]["Status"] = "Changes/Not Confirmed"
				changeInfo = Logger.get_datetime() + " " + getpass.getuser() + ": " + ", ".join(self.pathDicts[fileName]["Changes"]) + ". "
				self.metadataController.ncatted("history", "global", "a", "c", changeInfo, fileName, self.histFlag)
			self.mongoController.store_file_info(self.pathDicts[fileName])

	# Return validation of correct attribute
	# or corrected attribute from Known fixes collection
	# or return the top 3 matches from CFVars collection
	def identify_attribute(self, var, standardName, fileName):
		# Check if (var, standardName) is valid CF Standard Name pair
		if self.validate_var_standard_name_pair(var, standardName, fileName):
			return True

		# Attempt to find standard_name fix
		(standardName, sFlag) = self.find_standard_name_fix(var, standardName, fileName)
		if self.validate_var_standard_name_pair(var, standardName, fileName):
			return False	

		# Attempt to find var name fix
		(var, vFlag) = self.find_var_known_fix(var, standardName, fileName)
		if self.validate_var_standard_name_pair(var, standardName, fileName):
			return False

		# If no fixes found
		if not sFlag:
			self.estimate_standard_name(var, standardName, fileName)
		if not vFlag:
			self.estimate_var_name(var, standardName, fileName)
		return False

	def validate(self, filt=None):
		print "Starting Standard Name Validation on variable %s" % filt.strip(".*/").upper()
		# (filename, standard_name, units) list of all files in ncFolder
		standardNamesUnits = self.metadataController.get_standard_names(self.srcDir or self.fileName, self.dstDir, self.regexFilter)
		if standardNamesUnits:
			# Number of files for use in progress bar
			i = 1
			widgets = ['Percent Done: ', Percentage(), ' ', AnimatedMarker(), ' ', ETA()]
			bar = ProgressBar(widgets=widgets, maxval=len(standardNamesUnits)).start()
			# For each file in the list
			for f in standardNamesUnits:
				fileName   = f[0]
				standNames = f[1]
				self.get_path_info(fileName)
				self.metadataController.dump_metadata(self.pathDicts[fileName])
				self.logger.log(fileName, "", 'File Started')
				# If the file has no standard names, log the issue
				if not standNames:
					self.logger.log(fileName, "", 'No Standard Names')
					self.fileFlag = False
				# For each attribute in standard_name list, format and identify attribute
				else:
					for attr in standNames:
						splitAttr = attr.split(":")
						# Check if something in file was changed
						flag = self.identify_attribute(splitAttr[0], splitAttr[1], fileName)
						if not flag:
							self.fileFlag = False
				# If file had no errors or KnownFix occured ==> Confirm file
				self.confirm_file(fileName)
				# Reset fileFlag
				self.fileFlag = True
				# Update progress bar
				bar.update(i)
				i = i + 1
			bar.finish()

def main():
	parser = argparse.ArgumentParser(description='File Name Correction Algorithm')
	parser.add_argument("-o", "--op", "--operation",           dest="operation",       help = "Operation to run (initDB, resetDB, query, find_one, traverse_history, snf=standard names fix, fnf=file names fix)")
	parser.add_argument("-s", "--src", "--srcDir",             dest="srcDir",          help = "Source Directory")
	parser.add_argument("-f", "--fileName",                    dest="fileName",        help = "File Name for single file fix")
	parser.add_argument("-d", "--dstDir",                      dest="dstDir",          help = "Folder to move fixed files to")
	parser.add_argument("-m", "--metadata",                    dest="metadataFolder",  help = "Folder to dump original metadata to")
	parser.add_argument("-l", "--logFile",                     dest="logFile",         help = "File to log metadata changes to")
	parser.add_argument("--filter",                            dest="filter",          help = "File name filter (REGEX). Will only pull files that match regex. For example --filter .*r10i1p1.* will fix all files with ensemble numbers == r10i1p1")
	parser.add_argument("-q", "--query",                       dest="query",           help = "JSON Query")
	parser.add_argument("-c", "-t", "--table", "--collection", dest="collection",      help = "Collection to query")
	parser.add_argument("--fileNameChanges",                   dest="fileNameChanges", help = "Flag to reset FileNameChanges Collection during database reset",                   action='store_true',  default=False)
	parser.add_argument("--fix", "--fixFlag",                  dest="fixFlag",         help = "Flag to fix data or only report possible changes (--fix = Fix Data)",  action='store_true',  default=False)
	parser.add_argument("--fixUnits",                          dest="fixUnits",        help = "Flag to fix units or only report possible changes (--fixUnits = Fix units)",       action='store_true',  default=False)
	parser.add_argument("--hist", "--histFlag",                dest="histFlag",        help = "Flag to append changes to history metadata (--hist = append to history)",          action='store_true',  default=False)
	parser.add_argument("--wait",                              dest="wait",            help = "Flag to wait for NCO operations to finish. This takes substantially longer but ensures completeness", action='store_true', default=False)

	args = parser.parse_args()
	if(len(sys.argv) == 1):
		parser.print_help()

	elif args.operation:
		# INITIALIZE DATABASE
		if args.operation == "initDB":
			mongoinit.run()

		# RESET DATABASE
		elif args.operation == "resetDB":
			dropDB.run(args.fileNameChanges)
			mongoinit.run()

		# STANDARD NAME FIX
		elif args.operation == "snf":
			if (args.srcDir or args.fileName) and args.dstDir:
				l = Logger(args.logFile)
				l.set_logfile(args.srcDir or args.fileName)
				v = StandardNameValidator(args.srcDir, args.fileName, args.dstDir, args.filter, args.metadataFolder, l, args.fixFlag, args.fixUnits ,args.histFlag, args.wait)
				v.validate(args.filter)
			else:
				parser.error("Source directory (-s, --src, --srcDir) or file name (-f, --fileName) and destination directory (-d, --dstDir) required for standard name fix")

		# FILE NAME FIX
		elif args.operation == "fnf":
			if (args.srcDir or args.fileName):
				l = Logger(args.logFile)
				l.set_logfile(args.srcDir or args.fileName)
				v = FileNameValidator(args.srcDir, args.fileName, args.filter, args.metadataFolder, l, args.fixFlag, args.histFlag, args.wait)
				v.validate(args.filter)
			else:
				parser.error("Source directory (-s, --src, --srcDir) or file name (-f, --fileName) required for file name fix")

		# QUERY
		elif args.operation == "query":
			if args.collection and args.query:
				query = ast.literal_eval(args.query)
				m     = MongoController()
				pprint.pprint(m.query_DB(args.collection, query))
			else:
				parser.error("Collection (-c, -t, --collection, --table) and Query (-q, --query) are required")

		# FIND ONE
		elif args.operation == "find_one":
			if args.collection and args.query:
				query = ast.literal_eval(args.query)
				m     = MongoController()
				pprint.pprint(m.find_one(args.collection, query))
			else:
				parser.error("Collection (-c, -t, --collection, --table) and Query (-q, --query) are required")

		# TRAVERSE HISTORY
		elif args.operation == "traverse_history":
			if args.fileName:
				m = MongoController()
				hist = m.traverse_history(args.fileName)
				for f in hist:
					pprint.pprint(f)
			else:
				parser.error("File name (-f, --fileName) required to traverse history")

	else:
		parser.error("Operation (-o) required")

if __name__ == "__main__":
	main()
