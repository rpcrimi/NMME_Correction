import argparse
import os
import sys
import ast
import shlex
import subprocess

def main():
	parser = argparse.ArgumentParser(description='File Name Creator:\n All arguments should be comma seperated. For example, checking for variables "pr, hus, g" should be "-v g,hus,pr"', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-o", "--op", "--operation", dest="operation",   help="Operation to run (initDB, resetDB, query, find_one, traverse_history, snf=standard names fix, fnf=file names fix)")
	parser.add_argument("-s", "--srcDir",            dest="srcDir",      help="Source Directory (IGNORE MODEL_ID) (ex. -s CCCMA/, UM-RSMAS/ not CCCMA/CanCM3 or UM-RSMAS/CCSM4)")
	parser.add_argument("-d", "--dstDir",            dest="dstDir",      help="Folder to copy fixed files to")
	parser.add_argument("-m", "--model_id",          dest="model_id",    help="Optional Model ID for cases when only one model is desired (ex. Just look at CanCM3 instead of CanCM3 and CanCM4")
	parser.add_argument("-v", "--vars",              dest="vars",        help="Variable Name (ex. -v g,hus,pr)")
	parser.add_argument("--fix", "--fixFlag",        dest="fixFlag",     help="Flag to fix file names or only report possible changes (--fix = Fix File Names)",  action='store_true',  default=False)
	parser.add_argument("--fixUnits",                dest="fixUnits",    help="Flag to fix units or only report possible changes (--fixUnits = Fix Units)",       action='store_true',  default=False)
	parser.add_argument("-m", "--metadata",          dest="metadataFolder",  help = "Folder to dump original metadata to")
	parser.add_argument("--hist", "--histFlag",      dest="histFlag",        help = "Flag to append changes to history metadata (--hist = append to history)",          action='store_true',  default=False)
	parser.add_argument("--wait",                    dest="wait",            help = "Flag to wait for NCO operations to finish. This takes substantially longer but ensures completeness", action='store_true', default=False)


	args = parser.parse_args()
	if(len(sys.argv) == 1):
		parser.print_help()

	operation = args.operation
	srcDir = args.srcDir if args.srcDir[-1] == "/" else args.srcDir+"/"
	dstDir = args.dstDir
	variables = args.vars.split(",")

	for var in variables:
		newOut = "foo"
		oldOut = "bar"
		logNum = 1
		while newOut != oldOut:
			oldOut = newOut
			logFile = "%s_%s_%s_%d.log" % (args.model_id, operation, var, logNum)
			call = "python nmmecorrector.py -o %s -s %s -d %s --filter .*/%s/.* -l %s %s %s %s %s" % (operation, srcDir, dstDir, var, logFile, "--fix" if args.fixFlag else "", "--fixUnits" if args.fixUnits else "", "--wait" if args.wait else "", "--hist" if args.histFlag else "")
			p = os.system(call)
			
			grep = "grep DEBUG %s" % (logFile)
			p2 = subprocess.Popen(shlex.split(grep), stdout=subprocess.PIPE)
			newOut, err = p2.communicate()
			p2.stdout.close()
			logNum += 1

			#CHECK FOR KILL
			inp = raw_input()
			if inp == "Q":
				sys.exit()


if __name__ == "__main__":
	main()