import pymongo

def run(fileNameChanges):
	c = pymongo.MongoClient()

	c["Attribute_Correction"].drop_collection("CFVars")
	c["Attribute_Correction"].drop_collection("ValidFreq")
	c["Attribute_Correction"].drop_collection("StandardNameFixes")
	c["Attribute_Correction"].drop_collection("VarNameFixes")
	c["Attribute_Correction"].drop_collection("FreqFixes")
	if fileNameChanges:
		c["Attribute_Correction"].drop_collection("FileNameChanges")
