#!/bin/ksh 
set -xe
# NCO commands
module load nco/4.2.0
module load ncl/6.2.0
# home and I/O directories

infile1=$1
infile2=$2
infile3=$3
infile4=$4
outfile=$5
tmpdir=/glade/p/vetssg/data/nmme_convert/tmpdir
var='tmin'

 # 1. Subsetting to have forecast_time0 fixed to 299 days.
 #   Since data is every 6h, that is 4x per day it implies 1196 records
 ncea -d time,1,1196 $infile1 $tmpdir/foo1.nc4
 ncea -d time,1,1196 $infile2 $tmpdir/foo2.nc4
 ncea -d time,1,1196 $infile3 $tmpdir/foo3.nc4
 ncea -d time,1,1196 $infile4 $tmpdir/foo4.nc4
 if [ $? -ne 0 ] ; then
   echo "Subsetting failed for $var.19820101"
   exit 8
 fi

 # 2. adding the variable time
 ncecat -u time $tmpdir/foo1.nc4 $tmpdir/goo1.nc4
 ncecat -u time $tmpdir/foo2.nc4 $tmpdir/goo2.nc4
 ncecat -u time $tmpdir/foo3.nc4 $tmpdir/goo3.nc4
 ncecat -u time $tmpdir/foo4.nc4 $tmpdir/goo4.nc4
 if [ $? -ne 0 ] ; then
   echo "Adding Variable Time failed for $var.19820101"
   exit 8
 else
   rm -f $tmpdir/foo?.nc4
 fi

 # 3. find min or max
 ncra -y min $tmpdir/goo[1234].nc4 $tmpdir/tmin.nc4
 if [ $? -ne 0 ] ; then
   echo "Getting average failed for $var.19820101"
   exit 8
 else
   rm -f $tmpdir/goo?.nc4
 fi

 # 4. remove "time" variable
 # $ncwa -a time $tmpdir/goo1.nc4 $tmpdir/hoo1.nc4
 # $ncwa -a time $tmpdir/goo2.nc4 $tmpdir/hoo2.nc4
 # $ncwa -a time $tmpdir/goo3.nc4 $tmpdir/hoo3.nc4
 # $ncwa -a time $tmpdir/goo4.nc4 $tmpdir/hoo4.nc4
 ncwa -a time $tmpdir/tmin.nc4 $outfile
 if [ $? -ne 0 ] ; then
   echo "Removing Time variable failed for $var.19820101"
   exit 8
 else
   rm -f $tmpdir/tmin.nc4
 fi

