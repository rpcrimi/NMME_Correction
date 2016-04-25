#!/bin/ksh 
# on zeus computer use: 
# module load nco/4.2.0-intel-12.0.4.191 
# module load ncl/6.2.0.intel

set -xe
# home and I/O directories
homedir=/home/mpena/scripts/average
datadir=/glade/p/work/mpena/outputs
outputs=/glade/p/work/mpena/outputs/average
tmpdir=/glade/p/work/mpena/outputs/tmpdir

# NCO commands
ncea=/usr/local/bin/ncea
ncecat=/usr/local/bin/ncecat
ncra=/usr/local/bin/ncra
ncwa=/usr/local/bin/ncwa
#
#varlist='t850 t700 t200 t50'
varlist='t850'
for var in $varlist
do
   infile1=$datadir/$var/$var.1982010100.time.grb2.nc4
   infile2=$datadir/$var/$var.1982010106.time.grb2.nc4
   infile3=$datadir/$var/$var.1982010112.time.grb2.nc4
   infile4=$datadir/$var/$var.1982010118.time.grb2.nc4

   # 1. Subsetting to have forecast_time0 fixed to 299 days.
   #   Since data is every 6h, that is 4x per day it implies 1196 records
   $ncea -d forecast_time0,1,1196 $infile1 $tmpdir/foo1.nc4
   $ncea -d forecast_time0,1,1196 $infile2 $tmpdir/foo2.nc4
   $ncea -d forecast_time0,1,1196 $infile3 $tmpdir/foo3.nc4
   $ncea -d forecast_time0,1,1196 $infile4 $tmpdir/foo4.nc4
   if [ $? -ne 0 ] ; then
     echo "Subsetting failed for $var.19820101"
     exit 8
   fi

   # 2. adding the variable time
   $ncecat -u time $tmpdir/foo1.nc4 $tmpdir/goo1.nc4
   $ncecat -u time $tmpdir/foo2.nc4 $tmpdir/goo2.nc4
   $ncecat -u time $tmpdir/foo3.nc4 $tmpdir/goo3.nc4
   $ncecat -u time $tmpdir/foo4.nc4 $tmpdir/goo4.nc4
   if [ $? -ne 0 ] ; then
     echo "Adding Variable Time failed for $var.19820101"
     exit 8
   else
     rm -f $tmpdir/foo?.nc4
   fi

   # 3. get average   
   $ncra $tmpdir/goo[1234].nc4 $tmpdir/$var.19820101.average.nc4
   if [ $? -ne 0 ] ; then
     echo "Getting average failed for $var.19820101"
     exit 8
   else
     rm -f $tmpdir/goo?.nc4
   fi

   # 4. remove "time" variable
#   ncwa -a time $tmpdir/goo1.nc4 $tmpdir/hoo1.nc4
#   ncwa -a time $tmpdir/goo2.nc4 $tmpdir/hoo2.nc4
#   ncwa -a time $tmpdir/goo3.nc4 $tmpdir/hoo3.nc4
#   ncwa -a time $tmpdir/goo4.nc4 $tmpdir/hoo4.nc4
   $ncwa -a time $tmpdir/$var.19820101.average.nc4 $outputs/$var.19820101.daily.nc4
   if [ $? -ne 0 ] ; then
     echo "Removing Time variable failed for $var.19820101"
     exit 8
   else
     rm -f $tmpdir/$var.19820101.average.nc4
   fi

done
