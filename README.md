# NMME Data Correction Algorithms

## File Exists Validator

This module will detect missing files in a source directory. These source directories should be the base directory for
a model. Some example source directories might be UM-RSMAS/, CCCMA/, or NASA-GMAO/. The script will attempt to locate 
10 ensemble files for each variable provided by the -v argument. If -v is not provided, the script will pull from the
CF Standard Names table. Below is a description of each available argument for this module:

- -s, --srcDir:      The base directory to run the script from
- -m, --model_id:    Optional model_id for institutions with multiple models. For example, if only CanCM3 is desired, use "-m CanCM3"
- -d, --dates:       Date ranges to run the script over. For example, [[[1980,3], [1990,1]],[[2000,1], [2010,12]]] corresponds to January
				     1st, 1980 to January 1st, 1990 and March 1st, 2000 to December 1st, 2010.
- -f, --frequencies: Comma seperated frequencies. For example, if only day frequencies are required, use "-m day". If multiple frequencies
                     are required use "-m day,mon,3hr"
- -r, --realms:      Comma seperated realms. Use the same format as frequencies argument. For example, "-r atmos,land,ocean"
- -v, --vars:        Comma seperated variables. For example, "-v g,tasmin,tasmax,soilm". If this argument is not provided, the script will
                     pull all variables from the CF Standard Names table.
- -o, --order:       Optional order of folders to go through. This argument should only be provided for non-NMME models.
- -u, --update:      Boolean flag to update Google Spreadsheet. If provided, script will fill in cells in spreadsheet corresponding to the
                     realm and frequency provided. This argument should only be set true if there is a single model_id,realm,frequency provided

### Example Usage:

1. SSH into vetspubdev
2. cd into /datazone/nmme/convert/NMME_Correction
3. locate desired institution folder. For example, from the current directory, CCCMA would be ../../output1/CCCMA
4. ls the institution folder followed by model_id to find the experiment_ids (dates) in the model
5. After deciding your date ranges run:
       python fileexistsvalidator.py -d <[[date_range],[date_range]]> -f <frequences> -r <realms> -s <srcDir> -m <model_id> -u
   Note: this command will update the Google Spreadsheet