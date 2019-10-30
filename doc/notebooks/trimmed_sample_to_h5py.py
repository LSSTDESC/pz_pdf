import pandas as pd
import h5py
import numpy as np
import glob
#code to cut at a magnitude limit and write out data in the h5py format expected
#by BPZpipe version of BPZ
#
#We do not want to remove dropout galaxies, so in addition to a straight
#magnitude cut, include an option to also output z- and y-band dropouts
#with 10-year S/N > 5 (y<25.2 or z<26.0)

class photometryHealpix(object):
    """
    class for manipulating each cosmoDC2 healpix pixel of photometry

    """

    def __init__(self):
        """
        Parameters:
        filters: ugrizy filters for LSST
        [izy]SN_5: 10-year depth S/N =5 limits for i,z, and y bands
        """
        self.filters = ["u","g","r","i","z","y"]
        self.iSN_5 = 26.5 #S/N=5 in i-band 10 year
        self.zSN_5 = 26.0 #S/N=5 in z-band 10 year
        self.ySN_5 = 25.2 #S/N=5 in y-band 10 year
        mags = []
        magerrs = []
        newmags = []
        newmagerrs = []
        for filt in self.filters:
            mags.append(f"mag_{filt}_obs")
            magerrs.append(f"magerr_{filt}_obs")
            newmags.append(f"mag_{filt}_lsst")
            newmagerrs.append(f"mag_err_{filt}_lsst")
        self.mags = mags
        self.magerrs = magerrs
        self.newmags = newmags
        self.newmagerrs = newmagerrs
        
    def makeTrimmedFile(self,infile):
        """
        Parameters:
        infile: hdf5 file
          pandas format hdf5 file containing the photometry
        """
        #setup output file
        basefile = infile.split(".h5")[0]
        outfile = basefile+"SNtrim.hdf5"
        f = h5py.File(outfile,"w")
        group = f.create_group("photometry")
        #grab data from infile
        df = pd.read_hdf(infile)
        sz = df['redshift']
        id = df['baseDC2/galaxy_id']

        tmpi = df['mag_i_obs']
        tmpz = df['mag_z_obs']
        tmpy = df['mag_y_obs']

        mask = np.logical_or(tmpy<self.ySN_5,
                             np.logical_or(np.logical_and(tmpy<self.ySN_5,
                                                          tmpz<self.zSN_5),
                                           tmpi<self.iSN_5))
        
        for mag,magerr,xmag,xmagerr in zip(self.mags,self.magerrs,
                                           self.newmags,self.newmagerrs):
            #print (mag,magerr)
            group[f"{xmag}"] = df[mag][mask]
            group[f"{xmagerr}"] = df[magerr][mask]

        group['redshift'] = df['redshift'][mask]
        group['id'] = df['baseDC2/galaxy_id'][mask] #rename galaxy_id to id
        f.close()
        print (f"wrote file {outfile}")



def main():
    filelist = glob.glob("*_magwerr.h5")
    print("writing out %d files"%len(filelist))
    #testfile = "z_1_2.step_all.healpix_10070_magwerr.h5"
    makefileobj = photometryHealpix()
    for xfile in filelist:
        makefileobj.makeTrimmedFile(xfile)
if __name__=="__main__":
    main()
