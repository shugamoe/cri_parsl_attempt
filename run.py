#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import re

import parsl
from config import sbayesr_config, id_for_memo_File
from parsl.data_provider.files import File
from parsl.app.app import bash_app
from functools import partial
from library import filter_dose, dose_to_bbf, write_bbf_parts_list, merge_bbf_parts, echo_hello, ll_file

parsl.set_stream_logger() # log lines to screen
dfk = parsl.load(sbayesr_config)

### Step 0 ###
### Filter dosage files ###
PVAL = "0.2"
AVGINFSCORE = "0.9"
MAF = "0.01"


# Base files to work with
dose_paths = glob.glob("../input/geno_train/*train.gz")

dose_paths = [path for path in dose_paths if "chr23" not in path] # Remove chr23
# dose_paths = [path for path in dose_paths if "chr22.p1" in path] # Works, run 000
dose_paths = [path for path in dose_paths if ("chr22.p1" in path) or ("chr22.p2" in path)] # Hangs for some reason run 001
# dose_paths = [path for path in dose_paths if "chr22" in path] # Select Chr22 only (testing)

dose_files = [File(path) for path in dose_paths] # Input 0
gwas_files = [File("../input/gwas_combined/RAGOC.MAF005R7.overall.train.chr{chr_num}.logistic.gz".format(
             chr_num=re.search(r'chr([\d]{1,2})', path).group(1))) for path in dose_paths] # Input 1

filtered_dose_dir = "../input/processed_geno_train/genotype" # Output file directory
filtered_dose_files = [File(os.path.join(filtered_dose_dir, 
                         os.path.basename(path).replace("gz", 
                           "pval{0}_avginfscore{1}_maf{2}.gz".format(PVAL, AVGINFSCORE, MAF))))
                      for path in dose_paths] # Output File Objects
filtered_dose_res = [filter_dose(ogeno=filtered_dose_dir,
                                 source="train",
                                 pval=PVAL,
                                 avginfscore=AVGINFSCORE,
                                 maf=MAF,
                                 inputs=[dose_file, gwas_file],
                                 outputs=[filtered_dose_file])
                        for dose_file, gwas_file, filtered_dose_file in 
                          zip(dose_files, gwas_files, filtered_dose_files)
                       ]

### Step 1 ###
### Convert dosages to .bed/.bim/.fam ###
fam_file = File("../input/geno_train/RAGOC.chr1_22.train.fam")
out_dir = "../input/processed_geno_train/bbf_genotype/"
bed_files = [File(os.path.join(out_dir, os.path.basename(data_fut.outputs[0].filepath).replace(".gz", ".bed"))) 
             for data_fut in filtered_dose_res] # Output
dose_to_bbf_res = [dose_to_bbf(fam=fam_file, dose_file=filtered_dose_file.outputs[0], outputs=[bed_file]) for
                         filtered_dose_file, bed_file in zip(filtered_dose_res, bed_files)
                       ]

### Step 2 ###
### Write 1 file per chromosome listing the different part names with corresponding .bed/.bim/.fam/.log files ###
def filter_res(chr_num, data_fut):
    """
    Function to filter a list of DataFuture Objects. Combine with partial from functools.
    """
    import re
    has_match = re.search("chr{}".format(chr_num), data_fut.outputs[0].filepath)
    return has_match


list_dir = "../input/bbf_lists/" # Where to store the list files
# chroms_to_list = [i for i in range(1, 23)] # List of ints 1-22 for corresponding chromosomes
chroms_to_list = [22]
list_files = [File(os.path.join(list_dir, "bbf_geno_train_chr{}_list.txt".format(chr_num))) for chr_num in chroms_to_list] # Outputs
write_bbf_parts_list_res = [write_bbf_parts_list(chr_num, "train",
			      inputs=list(filter(partial(filter_res, chr_num),
                                                 dose_to_bbf_res)),
                              outputs=[list_file]) for 
                              chr_num, list_file in zip(chroms_to_list, list_files)
                           ]
### Step 3 ###
### Merge .bed/.bim/.fam parts together ###
out_dir = "../input/processed_geno_train/bbf_genotype/merged/"
merged_files = [File(os.path.join(out_dir, 
                                  "chr{0}.pval{1}_avginfscore{2}_maf{3}.bed".format(
                                   chr_num, PVAL, AVGINFSCORE, MAF)
                                 )) for
                chr_num in chroms_to_list
                ] # Output
merge_bbf_parts_res = [merge_bbf_parts(list_file=list(filter(partial(filter_res, chr_num),
                                                            write_bbf_parts_list_res
                                                            ))[0].outputs[0],
                                       outputs=[File(os.path.join(out_dir,
                                                     "chr{0}.pval{1}_avginfscore{2}_maf{3}.bed".format(
                                                     chr_num, PVAL, AVGINFSCORE, MAF)))]
                                      ) for chr_num in chroms_to_list
                      ]
for i in merge_bbf_parts_res:
    print(i.result())   
# ### Step 4 ###
# ### Create LD matrices from merged .bed/.bim/.fam files ###
# 
