#!/usr/bin/env python

import argparse
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

	# pull scan name from dicom header and write to json
	scanname = {}
	scanname['asl'] = ds_asl.SeriesDescription
	scanname['m0'] = ds_m0.SeriesDescription
	with open(outdir + '/SeriesDescription.json','w') as outfile:
		json.dump(scanname,outfile)

	# Make BIDS directories
    anatdir = 'f{outdir}/BIDS/sub-01/ses-01/anat'
    os.makedirs(anatdir)
    perfdir = 'f{outdir}/BIDS/sub-01/ses-01/perf'
    os.makedirs(perfdir)

	# run dcm2niix on source and m0 scans, with BIDS-compliant filenames. 
    # "Source" is the ASL secondary recon from the scanner and is 
    # relabeled as 'asl' for BIDS
	os.system(f'dcm2niix -s y -f sub-01_ses-01_T1w -o {anatdir} {t1_dcm}')
	os.system(f'dcm2niix -s y -f sub-01_ses-01_m0scan -o {perfdir} {m0_dcm}')
	os.system(f'dcm2niix -s y -f sub-01_ses-01_asl -o {perfdir} {source_dcm}')
	
	#ds_t1w.SeriesDescription = ds_t1w.SeriesDescription.replace(" ","").replace('/', "").replace(":", "").replace("_", "")
	#ds_asl.SeriesDescription = ds_asl.SeriesDescription.replace(" ","").replace('/', "").replace(":", "").replace("_", "")
	#ds_m0.SeriesDescription = ds_m0.SeriesDescription.replace(" ","").replace('/', "").replace(":", "").replace("_", "")

	# create dataset_description.json
    # FIXME what can we do that's better than NA?
	dataset_description = {
	  "BIDSVersion": "1.0.1",
	  "Name": "NA",
  	  "DatasetDOI": "NA",
  	  "Author": "NA"
	  }
	
	with open(indir + '/BIDS/dataset_description.json','w') as outfile:
		json.dump(dataset_description,outfile)


if __name__ == '__main__':
	main(sys.argv[1:])
