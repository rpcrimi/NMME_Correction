# NMME Data Correction Algorithms

## File Exists Validator

This module will detect missing NetCDF files in a source directory. These source directories should be the base directory for a model (UM-RSMAS/, CCCMA/, NASA-GMAO/). The script will attempt to locate 10 ensemble files (unless otherwise specified) for each variable provided by the -v argument. If -v is not provided, the script will pull from the CF Standard Names table. 

Below is a description of each available argument for this module:
- -s, --srcDir:      The base directory to run the script over (NOAA-GFDL/, NASA-GMAO/).
- -m, --model_id:    Optional model_id for institutions with multiple models. For example, if only CanCM3 is desired, use "-m CanCM3"
- -d, --dates:       Date ranges to run the script over. For example, [[[1980,3], [1990,1]],[[2000,1], [2010,12]]] corresponds to January
				     1st, 1980 to January 1st, 1990 and March 1st, 2000 to December 1st, 2010.
- -f, --frequencies: Comma separated frequencies. For example, if only day frequencies are required, use "-m day". If multiple frequencies
                     are required use "-m day,mon,3hr"
- -r, --realms:      Comma separated realms. Use the same format as frequencies argument. For example, "-r atmos,land,ocean"
- -v, --vars:        Comma separated variables. For example, "-v g,tasmin,tasmax,soilm". If this argument is not provided, the script will
                     pull all variables from the CF Standard Names table.
- -o, --order:       Optional order of folders to go through. This argument should only be provided for non-NMME models.
- -u, --update:      Boolean flag to update Google Spreadsheet. If provided, script will fill in cells in spreadsheet corresponding to the
                     realm and frequency provided. This argument should only be set true if there is a single model_id,realm,frequency provided
- -e, --ensembles"   Optional range of ensembles to run over. For example, `-e [1,5]` If argument is provided, the script will only run over the specified ensemble numbers (ex, [1,5])


### Example Usage:

1. SSH into vetspubdev
2. `cd` into /datazone/nmme/convert/NMME_Correction
3. Locate desired institution folder. For example, from the current directory, CCCMA would be ../../output1/CCCMA
4. `ls` the institution folder followed by model_id to find the experiment_ids (dates) in the model
5. After deciding your date ranges run:
	- `python fileexistsvalidator.py -d <[[date_range],[date_range]]> -f <frequencies> -r <realms> -s <srcDir> -m <model_id> -u`
	- NOTE: This command will update the Google Spreadsheet


## Standard Name Correction

This module will correct the standard names in NetCDF files to their CF standard. It uses MongoDB as an authoritative source for CF standards and common changes. For example, if the script comes across the variable "tasmax", it would check if the standard name matched the corresponding entry in the CF Standards Table (air_temperature). If it did not match, the script would check the Standard Name Fixes table for an suggested fix. For example, if the standard name in the file was "air temp", the script would use the following entry to change the standard name:
	`StandardNameFixes.insert({"Incorrect Standard Name": "air temp", "Var Name": "tasmax", "Known Fix": "air_temperature"})`

Below is a description of each available argument for this module:
- -o, --operation:		Operation to run. In this case, use `-o snf`.
- -s, --srcDir:			The base directory to run the script over (NOAA-GFDL/, NASA-GMAO/).
- -f, --fileName:		Filename to run script over. Do not use if srcDir argument provided.
- -d, --dstDir:			Folder to move fixed files to (finished/, foo/).
- --filter:				File name filter (REGEX). Will only pull files that match regex. For example, `--filter .*r10i1p1.*` will fix all files with ensemble numbers == r10i1p1".
- -m, --metadata:		OPTIONAL. Folder to dump original metadata to. This will run `ncdump -h` on each file and dump the data to corresponding files under this folder.
- --fix, --fixFlag:		Flag to fix file names or only report possible changes (--fix: Fix Data = TRUE).
- --hist, --histFlag:	Flag to append changes to history metadata (--hist: append to history = TRUE).
- --fixUnits:			Flag to fix units (--fixUnits: fix units = TRUE).
- --wait:				Flag to wait for NCO operations to finish. This takes substantially longer but ensures completeness

### Example Usage:

1. SSH into vetspubdev
2. `cd` into /datazone/nmme/convert/NMME_Correction
3. Locate desired institution folder. For example, from the current directory, CCCMA would be ../../output1/CCCMA
4. `ls` the institution folder followed by model_id to find the experiment_ids (initialization dates) in the model
5. After deciding your date ranges run:
	- `python nmmecorrector.py -o snf -d <[[date_range],[date_range]]> -s <srcDir> -d <dstDir> --filter .*/<variable>/.* -l <log_file> --fix --wait`
	- NOTE: This command will filter for a given variable and wait for operations to finish.


## File Name Correction

This module will correct NetCDF file names and corresponding global attributes. It uses the path of the file as the authoritative source of what contents are in the file. For example, the typical NMME file structure is institution-id/model-id/experiment-id/frequency/modeling-realm/variable. The script will use the information provided by this file structure to determine the name of the file and global attributes.

Below is a description of each available argument for this module:
- -o, --operation:		Operation to run. In this case, use `-o fnf`.
- -s, --srcDir:			The base directory to run the script over (NOAA-GFDL/, NASA-GMAO/).
- -f, --fileName:		Filename to run script over. Do not use if srcDir argument provided.
- --filter:				File name filter (REGEX). Will only pull files that match regex. For example, `--filter .*r10i1p1.*` will fix all files with ensemble numbers == r10i1p1".
- -m, --metadata:		OPTIONAL. Folder to dump original metadata to. This will run `ncdump -h` on each file and dump the data to corresponding files under this folder.
- --fix, --fixFlag:		Flag to fix file names or only report possible changes (--fix: Fix Data = TRUE).
- --hist, --histFlag:	Flag to append changes to history metadata (--hist: append to history = TRUE).
- --wait:				Flag to wait for NCO operations to finish. This takes substantially longer but ensures completeness

### Example Usage:

1. SSH into vetspubdev
2. `cd` into /datazone/nmme/convert/NMME_Correction
3. Locate desired institution folder. For example, from the current directory, CCCMA would be ../../output1/CCCMA
4. `ls` the institution folder followed by model_id to find the experiment_ids (initialization dates) in the model
5. After deciding your date ranges run:
	- `python nmmecorrector.py -o fnf -d <[[date_range],[date_range]]> -s <srcDir> --filter .*/<variable>/.* -l <log_file> --fix --wait`
	- NOTE: This command will filter for a given variable and wait for operations to finish.

## Batch Job

This module will run snf/fnf passes over each variable provided until there are no more changes to be made. It calls the nmmecorrector script for each variable and checks the logfile to see whether files are finished being fixed.

Arguments are the same as File Name and Standard Name Correction algorithms with the exception of the following:
- --filter argument is replaced with -v, --vars. The --vars argument should be comma separated variable names (g,pr,tas,tasmax).
	- This will call the nmmecorrector script with each variable as the filter argument for each pass.

### Example Usage:

1. SSH into vetspubdev
2. `cd` into /datazone/nmme/convert/NMME_Correction
3. Locate desired institution folder. For example, from the current directory, CCCMA would be ../../output1/CCCMA
4. `ls` the institution folder followed by model_id to find the experiment_ids (initialization dates) in the model
5. After deciding your date ranges run:
	- `python batchjob.py -o snf -d <[[date_range],[date_range]]> -s <srcDir> -d <dstDir> --vars <var1>,<var2>,<var3> -l <log_file> --fix --wait`
	- NOTE: This command will filter for each given variable and wait for operations to finish.


