#!/global/common/software/lsst/common/miniconda/py3-4.2.12/bin/python
import numpy as np
import astropy.io.fits as pyfits
import yaml


"""
Author: Will Hartley

** This is currently written specifically for protoDC2...
** Number of LSST bands is hard-coded to be 6


(Should write in python3)
Prepare the photometric catalogue in some standard form.
We'll use a yaml file to perform the translations.
For the minute, we'll just add an explicit protoDC2 form.

The routine extracts a subset from the database (or gc catalogue of dc2), writes it out as a fits file with a unique name that has standard column names (so that the .columns file BPZ needs can just be copied).

Use yaml file to set what these are.

Want to use arg parsing to set flags, e.g. protoDC2, so we know where to get the data from. Want sample size, and whether it is to be sequential or random.
If sequential, we want to know which number it is in sequence. Random can take a seed. i.e. --sequential 5 or --random 15

Should make the class more generic. save_cat should not depend on the source, for instance. Want specific dc2 (etc.) attribute that just changes how data is read in. 
Can we assume that we will interact with DC2 and other sources in a similar way?
"""

class LSST_cat:

    def __init__(self, config, source, ):
        self._config = config

        if source=='DC2':
            # load dc2 modules
            import GCRCatalogs as GC
            self.gc = GC.load_catalog('protoDC2')

        if self._config['READ_ERRORS']:
            self.subset_IDs, self.subset_mags, self.subset_errs, self.subset_z = select_data(self, self.gc, self._config, read_mags=True)
        else:
            self.subset_IDs, self.subset_mags, self.subset_z = select_data(self, self.gc, self._config)

    def select_data(self):
        # set-up the arrays
        if self._config['CAT_SIZE'] > 0:
            n_obj = self._config['CAT_SIZE']
        else:
            n_obj = len(self.gc.get_quantities(self._config['ID_NAME']))
            self.fullcat_flag = 1

        self.subset_IDs = np.zeros((n_obj))
        self.subset_mags = np.zeros((n_obj, 6))
        self.subset_errs = np.zeros((n_obj, 6)) # we make this array even if we're not filling it yet
        self.subset_z = np.zeros((n_obj))

        # check for the error case of defining a cat_size, but not subsampling type
        if self._config['CAT_SIZE'] > 0 & self._config['SELECT_TYPE'] != 'sequential' & self._config['SELECT_TYPE'] != 'random':
            print('Warning, limited catalogue size requested, but no subsampling type given. Using first '+str(self._config['CAT_SIZE'])+' objects.') # do the formatting better, output as a warn (stderr?), rather than just to sdtout.
            self._config['SELECT_TYPE'] = 'sequential'
            self._config['SELECT_ARG'] = 0

        # define the index list for the two cases: random, sequential
        if self._config['SELECT_TYPE'] == 'sequential':
            idxes =
        else if self._config['SELECT_TYPE'] == 'random':
            idxes =
        else:
            print('No subsampling requested, using whole catalogue.')
            self.fullcat_flag = 1



        
        if self._config['READ_ERRORS']:
            
    def save_cat(self):
        # save cat in fits form with standard names for cols
        # create a sensible file name
        # copy the .columns file to match


if __name__ == '__main__':

    # set-up flags

    
    # parse arguments, includes the path to the yaml file,
    # source identifier (e.g. DC2) and any subset args.

    
    # first, check that the source is in the dictionary from the
    # yaml file


    # add the other args to the config
    config['SELECT_TYPE'] = select_type
    config['SELECT_ARG'] = select_arg
    config['CAT_SIZE'] = cat_size

    
    if DC2_flag:

        
        cat = LSST_cat(config, 'DC2',)

        # do we need to do any further operations, like create errors?
        # arg is the depth of the images - take these from the yaml
        cat.make_errors(config['IMG_DEPTHS'])

        # output the catalogue with some unique and reproducible name
        # e.g. dc2_cat_seq_$seq_num.fits
        # or dc2_cat_rand_$cat_size_$seed.fits
        cat.save_cat()
