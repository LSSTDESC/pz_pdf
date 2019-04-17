

Two new versions of bpz that involve HDF5 files are included here:


bpz_py3_readhdf5.py has been modified to read in an HDF5 file created by Pandas, and uses a modified .columns file that contains the column names rather than their column number.  The output remains the standard BPZ ascii file format.


bpz_py3_readwritehdf5.py has been modified to read in pandas hdf5 data, and outputs in h5py-generated HDF5 files for the ".bpz" and "_probs.out" files containing the point estimates and marginalized 1-D posteriors.  A new keyword, H5_CHUNK_SIZE, has been added, which sets the size of the chunks of HDF5 file added to the end of the file. This does not seem to have a large impact on runtime, so the default value of 10000 should be fine for almost all cases.

