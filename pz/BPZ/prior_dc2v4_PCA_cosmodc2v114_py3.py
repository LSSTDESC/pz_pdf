from bpz_tools_py3 import *
def function(z,m,nt):
  
  """January 11, 2018. Sam Schmidt
  see directory /sandbox/sschmidt/TMP/DC2TEMPLATES/TESTBPZ/PRIOR/EYEBALL/
  prior trained on ~100k galaxies from cosmodc2v.1.4_small catalog and 100
  templates dc2_kmeans_ugsorted.list (100 templates chosen using Bryce
  Kalmbach's notebook on github which chooses 100 templates based on
  k-means clustering on the PCA components.  Templates are sorted by rest frame
  u-g color and are named dc2_ug_sorted_[0-99].sed
  Templates 0-12 (13) are "early", 13-64(51) "spiral, and 65-99(36) "Im/SB"
  so 13 early, 51 spiral, and 36 Im/SB templates.

  Trained for 20<i_mag<25.3 galaxies with m0 = 20.0
  *You should use the LSST i band magnitude for the column to compare against!*
  """       

  if nt != 229:
    print ("Wrong number of template spectra!")
    sys.exit()

  global zt_at_a
  nz=len(z)
  if m > 32: m = 32.0
  if m < 20.0: m = 20.0 #Treat all galaxies with i<20 with i=20 prior
  momin_hdf = 20.0 #m0 value

  a = zeros(229)
  a[:36] = 1.96 #36 "El" templates
  a[36:83] = 1.72 #47 "S0" templates
  a[83:172] = 1.71 #89 "Sp" templates
  a[172:] = 3.10 #57 "Im/SB" templates
  zo = zeros(229)
  zo[:36] = 0.33
  zo[36:83] = 0.33
  zo[83:172] = 0.38
  zo[172:] = 0.74
  km = zeros(229)
  km[:36] = 0.068
  km[36:83] = 0.065
  km[83:172] = 0.067
  km[172:] = 0.133
  fo_t = zeros(229)
  fo_t[:36] = 0.010278 #f0e = 0.37/36 templates = 0.010278
  fo_t[36:83] = 0.007021 #f0S0 = 0.33/47 templates = 0.007021
  fo_t[83:172] = 0.0020225 #f0s = (1-(.36+.33+.12))/89 = 0.0020225
  fo_t[172:] = 0.002105 #f0i = 0.12/57 temps = 0.002105 
  k_t = zeros(229)
  k_t[:36] = 0.68
  k_t[36:83] = 0.17
  k_t[172:] = -0.21
  try:
    zt_at_a.shape
  except NameError:
    zt_at_a=power.outer(z,a)
 
 
  
  dm=m-momin_hdf
  zmt=clip(zo+km*dm,0.01,15.)
  zmt_at_a=zmt**(a)
  #We define z**a as global to keep it 
  #between function calls. That way it is 
  # estimated only once

    
  #Morphological fractions
  f_t=zeros((len(a),),float)
  f_t[:36]=fo_t[:36]*exp(-k_t[:36]*dm)
  f_t[36:83]=fo_t[36:83]*exp(-k_t[36:83]*dm)
  f_t[172:]=fo_t[172:]*exp(-k_t[172:]*dm)
  f_t[83:172]=(1.-add.reduce(f_t[:83])-add.reduce(f_t[172:]))/89.
  #Formula:
  #zm=zo+km*(m_m_min)
  #p(z|T,m)=(z**a)*exp(-(z/zm)**a)
  p_i=zt_at_a[:nz,:nt]*exp(-clip(zt_at_a[:nz,:nt]/zmt_at_a[:nt],0.,700.))
  #This eliminates the very low level tails of the priors
  #norm=add.reduce(p_i[:nz,:6],0)
  #p_i[:nz,:6]=where(less(p_i[:nz,:6]/norm[:6],1e-2/float(nz)),
  #0.,p_i[:nz,:6]/norm[:6])
  norm=add.reduce(p_i[:nz,:nt],0)
  p_i[:nz,:nt]=p_i[:nz,:nt]/norm[:nt]*f_t[:nt]
  return p_i
