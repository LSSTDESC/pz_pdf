import numpy as np
import h5py
import sys
import copy
import yaml
import subprocess

"""
Take BPZ output prob file (in ascii by default) and turn it into standard style hdf5 file, to go into pdf_combine.

Output name must include code identifier (BPZ), perhaps version, some info regarding the data source (cosmoDC2) and perhaps some idea of the block of objects run.

h5 file should have two datasets, /ID/ and /PDF/. Can add a further info - date, data blocks, version etc. as attributes of /ID/?
"""

def reform_bpz(block_num, block_size):

    config = yaml.load(config_file)

    fname = 'BPZ_{0}_{1}_{2}.probs'.format(config['SOURCE'][0], block_num, block_size)
    out_name = fname.split('.')+'.h5'

    probs = np.loadtxt(fname)
    ID = copy.copy(probs[:,0])
    probs = probs[:,1:]

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
    subprocess.call("rm {0} {1} *.bpz *.probs".format(fname.split('.')+'.fits',
                                                      fname.split('.')+'.columns'), shell=True)
