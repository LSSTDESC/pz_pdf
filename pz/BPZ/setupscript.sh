#!/bin/sh
module load python/3.6-anaconda-4.4
export BPZPY3PATH='/global/projecta/projectdirs/lsst/groups/PZ/BPZ/BPZpy3/pz_pdf/pz/BPZ'
export NUMERIX=numpy
alias bpz_py3 python $BPZPY3PATH/bpz_tcorr_fits_py3.py
