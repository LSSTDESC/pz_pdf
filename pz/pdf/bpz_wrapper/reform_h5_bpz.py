import numpy as np
import h5py
import sys
import copy
import yaml
import subprocess

"""
call like:
python reform_h5_bpz.py <yaml-file> <bpz-prob-file>

(Should write in python3)
Take BPZ output prob file (in ascii by default) and turn it into standard style hdf5 file, to go into pdf_combine.

May as well take filename as argument.
Output name is derived from input name.

h5 file should have two datasets, /ID/ and /PDF/.
"""

fname = sys.argv[2]
out_name = fname.split('.')+'.h5'

config = yaml.load(open(sys.argv[1]))

probs = np.loadtxt(fname)
ID = copy.copy(probs[:,0])
probs = probs[:,1:]

# switch this to come from yaml (have a single pipeline yaml, together
# with prep_cat)
# z-array is assumed to be linear intervals in redshift.
# [n_interval, centre of lowest bin, centre of highest bin]
zarr = [config['N_BIN'], config['MIN_z'], config['Dz']]

f = h5py.File(out_name, "w")
ids = f.create_dataset("ID", (len(ID),), dtype='i', compression='lzf')
pdfs = f.create_dataset("PDF", (zarr[0],len(ID)), dtype='f', compression='lzf')

ids.attrs['N_objects'] = len(ID)
pdfs.attrs['PDF_length'] = zarr[0]
pdfs.attrs['PDF_interval'] = zarr[1]
pdfs.attrs['PDF_start'] = zarr[2]

ids = ID
pdfs = probs

f.close()

# clean up by deleting the BPZ input .fits and .column files, and the BPZ outputs, .bpz and .probs
subprocess.call(....)
