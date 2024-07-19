#!/usr/bin/env python

# Script for organizing ASL data to BIDS format
# Pull scan name from asl and m0 image, NEED TO DO: output to examcard2json
# Remove asl image (or just don't put it in the BIDS folder?)
# Convert dicom to nifti

import argparse
import glob
import os
import sys, getopt
from pydicom import dcmread
import json

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--indir')
    parser.add_argument('-a','--asl')
    parser.add_argument('-m','--m0')
    parser.add_argument('-s','--source')
    parser.add_argument('-t','--t1w')
    args = parser.parse_args()
    indir = args.indir
    asl = args.asl
    m0 = args.m0
    source = args.source
    t1w = args.t1w

    # check if file paths are absolute
    if os.path.isabs(asl) == False:
        asl = indir + '/' + asl
        m0 = indir + '/' + m0
        source = indir + '/' + source

    # get pydicom info for each scan
    ds_asl = dcmread(asl)
    ds_m0 = dcmread(m0)
    ds_t1w = dcmread(t1w)
    ds_source = dcmread(source)

    # pull scan name from dicom header
    scanname = {}
    scanname['asl'] = ds_asl.SeriesDescription
    scanname['m0'] = ds_m0.SeriesDescription

    # write scanname dict to json
    with open(indir + '/SeriesDescription.json','w') as outfile:
        json.dump(scanname,outfile)

    subprocess.call(['./bash_commands.sh', str(indir), str(source), str(m0), str(t1w), str(source_base), str(m0_base), str(t1w_base)])

    # remove leftover dicoms
    for file in glob.glob(indir + '/BIDS/sub-01/ses-01/*/*'):
        if file.endswith('.dcm'):
            os.system('rm ' + file)

    anat_rename = 'sub-01_ses-01_T1w'
    for file in glob.glob(indir + '/BIDS/sub-01/ses-01/anat/*'):
        if file.endswith('.json'):
            os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + anat_rename + '.json')
        else:
            os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + anat_rename + '.nii')
#            os.system('gzip ' + os.path.dirname(file) + '/' + anat_rename + '.nii')

    asl_rename = 'sub-01_ses-01_asl'
    m0_rename = 'sub-01_ses-01_m0scan'
    for file in glob.glob(indir + '/BIDS/sub-01/ses-01/perf/*'):
        if 'M0' in file or 'm0' in file:
            if file.endswith('.json'):
                os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + m0_rename + '.json')
            else:
                os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + m0_rename + '.nii')
#                os.system('gzip ' + os.path.dirname(file) + '/' + m0_rename + '.nii')
        else:
            if file.endswith('.json'):
                os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + asl_rename + '.json')
            else:
                os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + asl_rename + '.nii')
#                os.system('gzip ' + os.path.dirname(file) + '/' + asl_rename + '.nii')

    # create dataset_description.json
    dataset_description = {
      "BIDSVersion": "1.0.1",
      "Name": "XNAT Project",
      "DatasetDOI": "https://xnat2.vanderbilt.edu/xnat",
      "Author": "No Author defined on XNAT"
      }

    with open(indir + '/BIDS/dataset_description.json','w') as outfile:
        json.dump(dataset_description,outfile)


if __name__ == '__main__':
    main(sys.argv[1:])
