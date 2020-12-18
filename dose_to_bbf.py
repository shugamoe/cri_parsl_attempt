#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob

import parsl
from config import sbayesr_config
from parsl.data_provider.files import File
from library import dose_to_bbf, echo_hello

parsl.set_stream_logger() # log lines to screen
parsl.load(sbayesr_config)

echo_hello().result()
with open('echo-hello.stdout', 'r') as f:
     print(f.read())

#  out_dir = "../input/processed_geno_train/bbf_genotype/"
#  fam_file = "../input/geno_train/RAGOC.chr1_22.train.fam"
#
#  Acquire list of input files *train.gz
#  dose_paths = glob.glob("../input/geno_train/*train.gz")
#
#  dose_files = [File(path) for path in dose_paths]
#  bed_files = [File(os.path.join(out_dir, os.path.basename(path).replace(".gz", ".bed"))) for path in dose_paths]
#
#  print("Number of dosage file paths:")
#  print(len(dose_paths))
#
#  count = 0
#  for iput, oput in zip(dose_files, bed_files):
    #  count +=1
    #  print("Attempting to convert: {0}".format(iput))
    #  dose_to_bbf(fam=fam_file, out_dir=out_dir, inputs=[iput], outputs=[oput])
    #  if count == 1:
        #  break
