#!/bin/bash

DD=$(date +%Y)_$(date +%d)_$(date +%m)

# CESM1
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/3hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/6hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/day/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/mon/

python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NCAR/ -m CESM1 -f 3hr -r atmos -d [[[1980,1],[2010,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/3hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NCAR/ -m CESM1 -f 6hr -r atmos -d [[[1980,1],[2010,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/6hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NCAR/ -m CESM1 -f day -r atmos -d [[[1980,1],[2010,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/day/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NCAR/ -m CESM1 -f mon -r ocean -d [[[1980,1],[2010,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CESM1/logs_$DD/mon/ -u

# GEOS-5
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/3hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/6hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/day/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/mon/

python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NASA-GMAO/ -m GEOS-5 -f 3hr -r atmos -d [[[1982,1],[2012,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/3hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NASA-GMAO/ -m GEOS-5 -f 6hr -r atmos -d [[[1982,1],[2012,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/6hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NASA-GMAO/ -m GEOS-5 -f day -r atmos -d [[[1982,1],[2012,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/day/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NASA-GMAO/ -m GEOS-5 -f mon -r ocean -d [[[1982,1],[2012,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/GEOS-5/logs_$DD/mon/ -u

# CCSM4
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CCSM4/logs_$DD/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CCSM4/logs_$DD/3hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CCSM4/logs_$DD/6hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CCSM4/logs_$DD/day/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CCSM4/logs_$DD/mon/

python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/UM-RSMAS/ -m CCSM4 -f 3hr -r atmos -d [[[1982,1],[2015,10]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/UM-RSMAS/logs_$DD/3hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/UM-RSMAS/ -m CCSM4 -f 6hr -r atmos -d [[[1982,1],[2015,10]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/UM-RSMAS/logs_$DD/6hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/UM-RSMAS/ -m CCSM4 -f day -r atmos -d [[[1982,1],[2015,10]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/UM-RSMAS/logs_$DD/day/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/UM-RSMAS/ -m CCSM4 -f mon -r ocean -d [[[1982,1],[2015,10]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/UM-RSMAS/logs_$DD/mon/ -u

# FLORB-01
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/FLORB-01/logs_$DD/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/FLORB-01/logs_$DD/3hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/FLORB-01/logs_$DD/6hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/FLORB-01/logs_$DD/day/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/FLORB-01/logs_$DD/mon/

python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NOAA-GFDL/ -m FLORB-01 -f 3hr -r atmos -d [[[1980,1],[2014,7]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/NOAA-GFDL/logs_$DD/3hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NOAA-GFDL/ -m FLORB-01 -f 6hr -r atmos -d [[[1980,1],[2014,7]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/NOAA-GFDL/logs_$DD/6hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NOAA-GFDL/ -m FLORB-01 -f day -r atmos -d [[[1980,1],[2014,7]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/NOAA-GFDL/logs_$DD/day/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NOAA-GFDL/ -m FLORB-01 -f mon -r ocean -d [[[1980,1],[2014,7]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/NOAA-GFDL/logs_$DD/mon/ -u

# CanCM3
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/3hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/6hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/day/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/mon/

python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/CCCMA/ -m CanCM3 -f 3hr -r atmos -d [[[1981,1],[2012,8]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/3hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/CCCMA/ -m CanCM3 -f 6hr -r atmos -d [[[1981,1],[2012,8]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/6hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/CCCMA/ -m CanCM3 -f day -r atmos -d [[[1981,1],[2012,8]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/day/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/CCCMA/ -m CanCM3 -f mon -r ocean -d [[[1981,1],[2012,8]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM3/logs_$DD/mon/ -u

# CanCM4
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/3hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/6hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/day/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/mon/

python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/CCCMA/ -m CanCM4 -f 3hr -r atmos -d [[[1981,1],[2012,8]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/3hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/CCCMA/ -m CanCM4 -f 6hr -r atmos -d [[[1981,1],[2012,8]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/6hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/CCCMA/ -m CanCM4 -f day -r atmos -d [[[1981,1],[2012,8]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/day/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/CCCMA/ -m CanCM4 -f mon -r ocean -d [[[1981,1],[2012,8]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CanCM4/logs_$DD/mon/ -u

# CFSV2-2011
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/3hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/6hr/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/day/
mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/mon/

python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NCEP/ -m CFSV2-2011 -f 3hr -d -r atmos [[[1982,1],[2010,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/3hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NCEP/ -m CFSV2-2011 -f 6hr -d -r atmos [[[1982,1],[2010,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/6hr/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NCEP/ -m CFSV2-2011 -f day -d -r atmos [[[1982,1],[2010,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/day/ -u
python /datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py -s /datazone/nmme/output1/NCEP/ -m CFSV2-2011 -f mon -d -r ocean [[[1982,1],[2010,12]]] -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/CFSV2-2011/logs_$DD/mon/ -u
