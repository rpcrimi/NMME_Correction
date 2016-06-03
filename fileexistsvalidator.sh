#!/bin/bash

DD=$(date +%Y)_$(date +%m)_$(date +%d)
fileexistsvalidator=/datazone/nmme/convert_final/NMME_Correction/fileexistsvalidator.py

institutions=(NCAR NASA-GMAO NOAA-GFDL CCCMA CCCMA NCEP)
models=(CESM1 GEOS-5 CCSM4 FLORB-01 CanCM3 CanCM4 CFSV2-2011)
years=([[[1980,1],[2010,12]]] [[[1982,1],[2012,12]]] [[[1982,1],[2015,10]]] [[[1980,1],[2014,7]]] [[[1981,1],[2012,8]]] [[[1981,1],[2012,8]]] [[[1982,1],[2010,12]]])

for i in {0..5} 
do
	mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/
	mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/3hr/
	mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/6hr/
	mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/day/
	mkdir /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/mon/

	python $fileexistsvalidator -s /datazone/nmme/output1/${institutions[$i]}/ -m ${models[$i]} -f 3hr -r atmos -d ${years[$i]} -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/3hr/ -u
	python $fileexistsvalidator -s /datazone/nmme/output1/${institutions[$i]}/ -m ${models[$i]} -f 6hr -r atmos -d ${years[$i]} -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/6hr/ -u
	python $fileexistsvalidator -s /datazone/nmme/output1/${institutions[$i]}/ -m ${models[$i]} -f day -r atmos -d ${years[$i]} -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/day/ -u
	python $fileexistsvalidator -s /datazone/nmme/output1/${institutions[$i]}/ -m ${models[$i]} -f mon -r ocean -d ${years[$i]} -l /datazone/nmme/convert_final/NMME_Correction/cron_logfiles/${models[$i]}/logs_$DD/mon/ -u
done
