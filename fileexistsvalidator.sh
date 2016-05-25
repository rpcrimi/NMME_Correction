#!/bin/ksh 

DD=$(date +%Y)_$(date +%d)_$(date +%m)

mkdir cron_logfiles/CESM1/logs_$DD/
mkdir cron_logfiles/GEOS-5/logs_$DD/
mkdir cron_logfiles/CCSM4/logs_$DD/
mkdir cron_logfiles/FLORB-01/logs_$DD/
mkdir cron_logfiles/CanCM3/logs_$DD/
mkdir cron_logfiles/CanCM4/logs_$DD/
mkdir cron_logfiles/CFSV2-2011/logs_$DD/


#python fileexistsvalidator.py -s ../../output1/NCAR/ -m CESM1 -f day -d [[[1980,1],[2010,12]]] -r atmos -l cron_logfiles/CESM1/logs_$DD/ -u
#python fileexistsvalidator.py -s ../../output1/NASA-GMAO/ -m GEOS-5 -f day -d [[[1982,1],[2012,12]]] -r atmos -l cron_logfiles/GEOS-5/logs_$DD/ -u
#python fileexistsvalidator.py -s ../../output1/UM-RSMAS/ -m CCSM4 -f day -d [[[1982,1],[2015,10]]] -r atmos -l cron_logfiles/UM-RSMAS/logs_$DD/ -u
#python fileexistsvalidator.py -s ../../output1/NOAA-GFDL/ -m FLORB-01 -f day -d [[[1980,1],[2014,7]]] -r atmos -l cron_logfiles/NOAA-GFDL/logs_$DD/ -u
#python fileexistsvalidator.py -s ../../output1/CCCMA/ -m CanCM3 -f day -d [[[1981,1],[2012,8]]] -r atmos -l cron_logfiles/CanCM3/logs_$DD/ -u
#python fileexistsvalidator.py -s ../../output1/CCCMA/ -m CanCM4 -f day -d [[[1981,1],[2012,8]]] -r atmos -l cron_logfiles/CanCM4/logs_$DD/ -u
#python fileexistsvalidator.py -s ../../output1/NCEP/ -m CFSV2-2011 -f day -d [[[1982,1],[2010,12]]] -r atmos -l cron_logfiles/CFSV2-2011/logs_$DD/ -u