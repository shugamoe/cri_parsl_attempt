#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parsl.app.app import bash_app
    

@bash_app
def dose_to_bbf(fam, out_dir, inputs=[], outputs=[], stdout="dose_to_bbf.stdout", stderr="dose_to_bbf.stderr"):
    import os

    bash_command = \
    """
    plink2 --fam {fam} \
      --import-dosage {dose_file} noheader ref-first chr-col-num=2 pos-col-num=3 format=1 skip1=2 \ 
      --import-dosage-certainty 0.1 \
      --make-bed \
      --geno 0.05 \
      --out {opath}
    """.format(fam=fam, dose_file=inputs[0], opath=outputs[0])
    return bash_command

@bash_app
def echo_hello(stdout='echo-hello.stdout', stderr='echo-hello.stderr'):
    return 'echo "Hello World!"'

