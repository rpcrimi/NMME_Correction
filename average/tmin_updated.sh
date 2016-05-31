#!/bin/ksh 
# NCO commands used: ncrename, ncea, ncecat, ncra, ncwa
# This script fixes the number of records processed to 299 days. Since data are every 6h, that is 4x per day: 299x4= 1196 records
set -xe
inpday=19820101
nrecords=1196
var='tasmin'

# work directory
tmpdir=/glade/p/work/rcrimi/tmp
mkdir -p $tmpdir
datadir=/glade/u/home/mpena/average
outputs=/glade/u/home/rcrimi/average


   infile1=$datadir/tasmin_6hr_CFSV2-2011_${inpday}00_r1i1p1_19820101-20111227.nc4
   infile2=$datadir/tasmin_6hr_CFSV2-2011_${inpday}06_r1i1p1_19820101-20111227.nc4
   infile3=$datadir/tasmin_6hr_CFSV2-2011_${inpday}12_r1i1p1_19820101-20111227.nc4
   infile4=$datadir/tasmin_6hr_CFSV2-2011_${inpday}18_r1i1p1_19820101-20111227.nc4

   # 1. Rename time to forecast_time
   ncrename -h -O -v time,forecast_time $infile1 $tmpdir/foo1.nc4
   ncrename -h -O -v time,forecast_time $infile2 $tmpdir/foo2.nc4
   ncrename -h -O -v time,forecast_time $infile3 $tmpdir/foo3.nc4
   ncrename -h -O -v time,forecast_time $infile4 $tmpdir/foo4.nc4

   # 2. Subsetting to have forecast_time0 fixed to nrecords
   ncea -d forecast_time,1,$nrecords $tmpdir/foo1.nc4 $tmpdir/goo1.nc4
   ncea -d forecast_time,1,$nrecords $tmpdir/foo2.nc4 $tmpdir/goo2.nc4
   ncea -d forecast_time,1,$nrecords $tmpdir/foo3.nc4 $tmpdir/goo3.nc4
   ncea -d forecast_time,1,$nrecords $tmpdir/foo4.nc4 $tmpdir/goo4.nc4
   if [ $? -ne 0 ] ; then
     echo "ERROR: Subsetting failed for subsetting of $var.$inpday"
     exit 8
#   else
#     rm -f $tmpdir/foo?.nc4
   fi

   # 3. Adding the variable time
   ncecat -u time $tmpdir/goo1.nc4 $tmpdir/hoo1.nc4
   ncecat -u time $tmpdir/goo2.nc4 $tmpdir/hoo2.nc4
   ncecat -u time $tmpdir/goo3.nc4 $tmpdir/hoo3.nc4
   ncecat -u time $tmpdir/goo4.nc4 $tmpdir/hoo4.nc4
   if [ $? -ne 0 ] ; then
     echo "ERROR: Adding Variable Time failed"
     exit 8
#   else
#     rm -f $tmpdir/goo?.nc4
   fi

   # 4. find min or max
   ncra -y min $tmpdir/hoo[1234].nc4 $tmpdir/output1.nc4
   if [ $? -ne 0 ] ; then
     echo "ERROR: Getting min/max/average failed for $var.$day"
     exit 8
#   else
#     rm -f $tmpdir/hoo?.nc4
   fi

   # 5. Remove "time" variable to the output
   ncwa -a time $tmpdir/output1.nc4 $outputs/$var.$inpday.min.daily.nc4
   if [ $? -ne 0 ] ; then
     echo "ERROR: Removing Time variable failed for $var.$inpday"
     exit 8
#   else
#     rm -f $tmpdir/output1.nc4
   fi

echo "task completed"