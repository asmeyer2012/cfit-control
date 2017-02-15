import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines      as df
import define_prior as dfp
from lsqfit._utilities import gammaQ

import matplotlib as mpl
mpl.use('TkAgg')

def plot_stability(fit_collector,**kwargs):
 """
 """
 fitCount  = 0
 hVal  = [] ## -- horizontal axis value, ~ fit
 hName = [] ## -- fit name, e.g. 1+1, 2+1...
 hChi2 = [] ## -- fit chi2, for color coding
 hQval = [] ## -- fit Q, for color coding
 hValDatn  = [] ## -- mostly same as hVal, but match size of enCentral and offset
 hValDato  = [] ## -- mostly same as hVal, but match size of eoCentral and offset
 enCentral = []
 eoCentral = []
 enError = []
 eoError = []
 ## -- tkey should be tuple: nst,ost, and 'fit' or 'prior' or other descriptor
 for nst in range(1,15):
  for ost in range(1,15):
   tkey=(nst,ost,'fit')
   ### -- ignore fits with large chi2
   try:
    fit_collector[tkey] # check that this works
   # dof = float(fit_collector[tkey]['dof'])
   # npr = float(len(df.define_prior['nkey']))
   # if (dof-npr*(nst+ost))*fit_collector[tkey]['chi2']/dof > df.max_chi2\
   #    or (dof-npr*(nst+ost))*fit_collector[tkey]['chi2']/dof < df.min_chi2:
   #  print (dof-npr*(nst+ost))*fit_collector[tkey]['chi2']/dof 
   #  continue 
   except KeyError:
    ## -- lots of key errors; not a big deal
    #print "KeyError"
    continue
   #except ZeroDivisionError:
   # print "ZeroDivisionError"
   # continue
   ## -- collect only important info
   try:
    Qval = gammaQ(fit_collector[tkey]['rdof']/2.,fit_collector[tkey]['chi2']/2.)
    if Qval < 0.001:
     continue
    hQval.append(Qval)
   except:
    continue
    #hQval.append(0)
   hVal.append(fitCount+0.5)
   if fit_collector[tkey]['rdof'] > 0:
    hName.append(str(nst) +'+'+ str(ost)
    +' (%.2g)' % gammaQ(fit_collector[tkey]['rdof']/2.,fit_collector[tkey]['chi2']/2.))
    #+' ('+ str(round((dof-npr*(nst+ost))*fit_collector[tkey]['chi2']/dof,2))+')'
   else:
    hName.append(str(nst) +'+'+ str(ost) +' (?)')
   #hChi2.append(fit_collector[tkey]['chi2'])
   for key in fit_collector[tkey]:
    sum=0
    bkey = utf.get_basekey(key)
    if bkey[1][-2:] == 'En' and (bkey[0] is None):
     for x in fit_collector[tkey][key]:
      hValDatn.append(fitCount+0.25)
      sum += x.mean
      enCentral.append(sum)
      enError.append(x.sdev)
    elif bkey[1][-2:] == 'Eo' and (bkey[0] is None):
     for x in fit_collector[tkey][key]:
      hValDato.append(fitCount+0.75)
      sum += x.mean
      eoCentral.append(sum)
      eoError.append(x.sdev)
   fitCount += 1
 fig = plt.figure()
 ax = fig.add_subplot(111)
 plt.xticks(hVal,hName,rotation='vertical')
 ax.set_xlim([0,fitCount])
 ax.set_ylim([0.6,1.5])
 ax.errorbar(hValDatn,enCentral,enError,
  color='r',marker='o',linestyle='')
 ax.errorbar(hValDato,eoCentral,eoError,
  color='b',marker='o',linestyle='')
 for x in range(1,fitCount):
  ax.axvline(x,color='k')
 plt.show()
