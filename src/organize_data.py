#!/usr/bin/env python

import argparse
import getopt
import glob
import os
import sys
from pydicom import dcmread
import json

def main(argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('outdir')
    parser.add_argument('t1_dcm')
    parser.add_argument('asl_dcm')
    parser.add_argument('m0_dcm')
    parser.add_argument('source_dcm')
    args = parser.parse_args()
    outdir = args.outdir
    t1_dcm = args.t1_dcm
    asl_dcm = args.asl_dcm
    m0_dcm = args.m0_dcm
    source_dcm = args.source_dcm

	# get pydicom info for each scan
	ds_asl = dcmread(asl_dcm)
	ds_m0 = dcmread(m0_dcm)
	ds_t1w = dcmread(t1_dcm)
	ds_source = dcmread(source_dcm)

	# pull scan name from dicom header
	scanname = {}
	scanname['asl'] = ds_asl.SeriesDescription
	scanname['m0'] = ds_m0.SeriesDescription

	# write scanname dict to json
	with open(outdir + '/SeriesDescription.json','w') as outfile:
		json.dump(scanname,outfile)

	# move scans to BIDS directories
    anatdir = 'f{outdir}/BIDS/sub-01/ses-01/anat'
    os.makedirs(anatdir)
    perfdir = 'f{outdir}/BIDS/sub-01/ses-01/perf'
    os.makedirs(perfdir)

	# run dcm2niix on source and m0 scans
	os.system(f'dcm2niix -s y -f sub-01_ses-01_T1w -o {anatdir} {t1_dcm}')
    ## FIXME we are here - dcm2niix with outputs to bids dirs
	os.system(f'dcm2niix -s y -f sub-01_ses-01_T1w -o {perfdir} {asl_dcm}')
	os.system(f'dcm2niix -s y -f %b -o {outdir} /BIDS/sub-01/ses-01/perf')

	# rename nii/json files to match bids formatting
	
	#ds_t1w.SeriesDescription = ds_t1w.SeriesDescription.replace(" ","").replace('/', "").replace(":", "").replace("_", "")
	#ds_asl.SeriesDescription = ds_asl.SeriesDescription.replace(" ","").replace('/', "").replace(":", "").replace("_", "")
	#ds_m0.SeriesDescription = ds_m0.SeriesDescription.replace(" ","").replace('/', "").replace(":", "").replace("_", "")

	anat_rename = 'sub-01_ses-01_T1w'
	for file in glob.glob(indir + '/BIDS/sub-01/ses-01/anat/*'):
		if file.endswith('.json'):
			os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + anat_rename + '.json')
		else:
			os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + anat_rename + '.nii')
			os.system('gzip ' + os.path.dirname(file) + '/' + anat_rename + '.nii')

	asl_rename = 'sub-01_ses-01_asl'
	m0_rename = 'sub-01_ses-01_m0scan'
	for file in glob.glob(indir + '/BIDS/sub-01/ses-01/perf/*'):
		if 'M0' in file or 'm0' in file:
			if file.endswith('.json'):
				os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + m0_rename + '.json')
			else:
				os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + m0_rename + '.nii')
				os.system('gzip ' + os.path.dirname(file) + '/' + m0_rename + '.nii')
		else:
			if file.endswith('.json'):
				os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + asl_rename + '.json')
			else:
				os.system('mv ' + file + ' ' + os.path.dirname(file) + '/' + asl_rename + '.nii')
				os.system('gzip ' + os.path.dirname(file) + '/' + asl_rename + '.nii')
	
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
