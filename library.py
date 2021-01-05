#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parsl.app.app import bash_app
from config import id_for_memo_File
import parsl

@bash_app(executors=["standard_16gb_1core"], cache=False, ignore_for_cache=["stdout", "stderr"])
def filter_dose(ogeno, source, pval, avginfscore, maf, inputs=[], outputs=[],
                stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME):
    import os
    PY_APP="/gpfs/data/gao-lab/Julian/gaolab_hub/apps/ragoc_to_ldpred2/ragoc_to_ldpred2.py"
    geno, gwas = inputs

    bash_args = {
      "py_app": PY_APP,
      "idir": os.path.dirname(geno.filepath), # Input directory
      "ifile": os.path.basename(geno.filepath), # Input file
      "osnp": None,
      "ogeno": ogeno,
      "source": source,
      "gwas": gwas.filepath,
      "pval": pval,
      "avginfscore": avginfscore,
      "maf": maf
    }
    bash_command = \
    """
    python3 {py_app} geno \
      --idir "{idir}" \
      --ipat "{ifile}" \
      --osnp "{osnp}" \
      --ogeno "{ogeno}" \
      --source "{source}" \
      --gwas "{gwas}" \
      --pval "{pval}" \
      --avginfscore "{avginfscore}" \
      --maf "{maf}" \
      --filter-only
    """.format(**bash_args)
    return bash_command
    # return "python3 {py_app} geno -h".format(py_app=PY_APP)
    
    

@bash_app(executors=["plink2_express_2gb_1core"], cache=True, ignore_for_cache=["stdout", "stderr"])
def dose_to_bbf(fam, dose_file, outputs=[], stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME):

    bash_command = \
    """
    plink2 --fam {fam} \
      --import-dosage {dose_file} noheader ref-first chr-col-num=2 pos-col-num=3 format=1 skip1=2 \
      --import-dosage-certainty 0.1 \
      --make-bed \
      --geno 0.05 \
      --out {opath}
    """.format(fam=fam.filepath, dose_file=dose_file.filepath, opath=outputs[0].filepath.replace(".bed", ""))
    return bash_command

@bash_app(executors=["plink1_express_2gb_1core"])
def write_bbf_parts_list(chr_num, geno_type, inputs=[], outputs=[], 
                         stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME):
    bash_command = \
    """
    ls -d ../input/processed_geno_{geno_type}/bbf_genotype/* | grep "chr{chr_num}.p" | \
    sed -e 's/\.log//' -e 's/\.fam//' -e 's/\.bim//' -e 's/\.bed//' | \
    sort --version-sort | uniq > {output.filepath}
    """.format(chr_num=chr_num, geno_type=geno_type, output=outputs[0])
    return bash_command

@bash_app(executors=["plink1_express_2gb_1core"])
def merge_bbf_parts(list_file, outputs=[], 
                    stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME):
    bash_command = \
    """
    plink --merge-list {list_file} --make-bed --out {out_prefix}
    """.format(list_file=list_file.filepath, out_prefix=outputs[0].filepath.replace(".bed", ""))
    return bash_command

@bash_app
def echo_hello(stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME):
    return 'echo "Hello World!"'

@bash_app
def ll_file(inputs=[], stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME):
    return 'ls -l {0}'.format(inputs[0])

