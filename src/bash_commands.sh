#!/bin/bash

export indir=$1
export source=$2
export m0=$3
export t1w=$4
export source_base=$5
export m0_base=$6
export t1w_base=$7

# move scans to BIDS directories
mkdir -p $indir/BIDS/sub-01/ses-01/anat/
mkdir -p $indir/BIDS/sub-01/ses-01/perf/

cp $source $indir/BIDS/sub-01/ses-01/perf/$source_base
cp $m0 $indir/BIDS/sub-01/ses-01/perf/m0$m0_base
cp $t1w $indir/BIDS/sub-01/ses-01/anat/$t1w_base

# run dcm2niix on source and m0 scans
/data/mcr/centos7/dcm2niix/v1.0.20240202/console/dcm2niix -z y -f %b $indir/BIDS/sub-01/ses-01/anat
/data/mcr/centos7/dcm2niix/v1.0.20240202/console/dcm2niix -z y -f %b $indir/BIDS/sub-01/ses-01/perf
