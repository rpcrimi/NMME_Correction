#!/bin/ksh 

read YYYY MM DD <<<$(date +'%Y %m %d')
echo $DD
echo $MM

#python fileexistsvalidator.py -s ../../output1/NCAR/ -m CESM1 -f day -d [[[1980,1],[2010,12]]] -r atmos -l logfiles_cesm1_may9_day -u