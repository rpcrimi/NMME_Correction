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
       `python fileexistsvalidator.py -d <[[date_range],[date_range]]> -f <frequencies> -r <realms> -s <srcDir> -m <model_id> -u`
   NOTE: This command will update the Google Spreadsheet


## File Name Correction

This module will correct NetCDF file names and corresponding global attributes. This script uses the path of the file as the authoritative source of what contents are in the file. For example, the typical NMME file structure is institution-id/model-id/experiment-id/frequency/modeling-realm/variable. The script will use the information provided by this file structure to determine the name of the file and global attributes.

Below is a description of each available argument for this module:
- -o, --operation:		Operation to run. In this case, use `-o fnf`.
- -s, --srcDir:			The base directory to run the script over (NOAA-GFDL/, NASA-GMAO/).
- -f, --fileName:		Filename to run script over. Do not use if srcDir argument provided.
- --filter:				File name filter (REGEX). Will only pull files that match regex. For example, `--filter .*r10i1p1.*` will fix all files with ensemble numbers == r10i1p1".
- -m, --metadata:		OPTIONAL. Folder to dump original metadata to. This will run `ncdump -h` on each file and dump the data to corresponding files under this folder.
- --fix, --fixFlag:		Flag to fix file names or only report possible changes (--fix = Fix Data).
- --hist, --histFlag:	Flag to append changes to history metadata (--hist = append to history)
- --wait:				Flag to wait for NCO operations to finish. This takes substantially longer but ensures completeness

### Example Usage:

1. SSH into vetspubdev
2. `cd` into /datazone/nmme/convert/NMME_Correction
3. Locate desired institution folder. For example, from the current directory, CCCMA would be ../../output1/CCCMA
4. `ls` the institution folder followed by model_id to find the experiment_ids (initialization dates) in the model
5. After deciding your date ranges run:
       `python nmmecorrector.py -o fnf -d <[[date_range],[date_range]]> -s <srcDir> --filter .*/<variable>/.* -l <log_file> --fix --wait`
       NOTE: This command will filter for a given variable and wait for operations to finish.