from bpz_tools_py3 import *
def function(z,m,nt):
  
  """January 11, 2017. Sam Schmidt
  see directory /sandbox/sschmidt/SIMULATIONS/RISA/FINALDATACHALLENGE/PRIOR/BPZ/
  prior trained on 111k galaxies from Buzzard simulation and a summary set of
  templates kmeans100sort.list (100 representative templates chosen using
  k-means clustering in the space of 5 basis coefficients, named "kmeansbuzzard_[0-99].sed).

  Templates 0-15 are "early", 16-63 "spiral, and 64-99 "Im/SB"
  so 16 early, 48 spiral, and 36 Im/SB templates.

  Trained in two chunks m0 = 19 for m<23 and m0=23 for m>23
  *You should use the LSST i band magnitude for the column to compare against!*
  """       
  mmax=27.0

  if nt != 100:
    print ("Wrong number of template spectra!")
    sys.exit()

  global zt_at_a1
  global zt_at_a2
  nz=len(z)
  if m > 28: m = 28.0
  if m < 19.0: m = 19.0 #Treat all galaxies with i<19 as i=19

  if m < 23.0:
    a = zeros(100)
    a[:15] = 3.33
    a[15:63] = 1.85
    a[63:] = 1.18
    zo = zeros(100)
    zo[:15] = 0.297
    zo[15:63] = 0.200
    zo[63:] = 0.072
    km = zeros(100)
    km[:15] = 0.122
    km[15:63] = 0.0824
    km[63:] = 0.0527
    fo_t = zeros(100)
    fo_t[:15] = 0.04181 #f0e = 0.669/16 templates
    fo_t[15:63] = 0.005917 #f0s = 0.284/48
    fo_t[63:] = 0.001306 #f0i = 0.047/36
    k_t = zeros(100)
    k_t[:15] = 0.241
    k_t[63:] = -0.391
    momin_hdf = 19.0
    try:
      zt_at_a1.shape
    except NameError:
      zt_at_a1=power.outer(z,a)
 
  else:
    a = zeros(100)
    a[:15] = 3.29
    a[15:63] = 1.63
    a[63:] = 1.38
    zo = zeros(100)
    zo[:15] = 0.822
    zo[15:63] = 0.499
    zo[63:] = 0.310
    km = zeros(100)
    km[:15] = 0.145
    km[15:63] = 0.0917
    km[63:] = 0.0790
    fo_t = zeros(100)
    fo_t[:15] = 0.01594 #f0e = 0.255/16 templates
    fo_t[15:63] = 0.01083 #f0s = 0.520/48
    fo_t[63:] = 0.00625 #f0i = 0.225/36
    k_t = zeros(100)
    k_t[:15] = 0.344
    k_t[63:] = -0.238
    momin_hdf = 23.0
    try:
      zt_at_a2.shape
    except NameError:
      zt_at_a2=power.outer(z,a)

  if m < 23.0:
    zt_at_a = zt_at_a1
  else:
    zt_at_a = zt_at_a2

  dm=m-momin_hdf
  zmt=clip(zo+km*dm,0.01,15.)
  zmt_at_a=zmt**(a)
  #We define z**a as global to keep it 
  #between function calls. That way it is 
  # estimated only once

    
  #Morphological fractions
  f_t=zeros((len(a),),float)
  f_t[:15]=fo_t[:15]*exp(-k_t[:15]*dm)
  f_t[63:]=fo_t[63:]*exp(-k_t[63:]*dm)
  f_t[15:63]=(1.-add.reduce(f_t[:15])-add.reduce(f_t[63:]))/48.
  #Formula:
  #zm=zo+km*(m_m_min)
  #p(z|T,m)=(z**a)*exp(-(z/zm)**a)
  p_i=zt_at_a[:nz,:100]*exp(-clip(zt_at_a[:nz,:100]/zmt_at_a[:100],0.,700.))
  #This eliminates the very low level tails of the priors
  #norm=add.reduce(p_i[:nz,:6],0)
  #p_i[:nz,:6]=where(less(p_i[:nz,:6]/norm[:6],1e-2/float(nz)),
  #0.,p_i[:nz,:6]/norm[:6])
  norm=add.reduce(p_i[:nz,:100],0)
  p_i[:nz,:100]=p_i[:nz,:100]/norm[:100]*f_t[:100]
  return p_i
