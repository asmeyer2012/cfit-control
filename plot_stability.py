import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines      as df
import define_prior as dfp

def plot_stability(fit_collector,**kwargs):
 """
 """
 fitCount  = 0
 hVal  = [] ## -- horizontal axis value, ~ fit
 hName = [] ## -- fit name, e.g. 1+1, 2+1...
 hChi2 = [] ## -- fit chi2, for color coding
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
   ## -- ignore fits with large chi2
   try:
    dof = float(fit_collector[tkey]['dof'])
    npr = float(len(dfp.define_prior['nkey']))
    if dof/(dof-npr*(nst+ost))*fit_collector[tkey]['chi2'] > df.max_chi2 or (dof-npr*(nst+ost)) < 0:
     continue 
   except KeyError:
    continue
   except ZeroDivisionError:
    continue
   ## -- collect only important info
   hVal.append(fitCount+0.5)
   hName.append(str(nst) +'+'+ str(ost) +' ('+
    str(round(dof/(dof-npr*(nst+ost))*fit_collector[tkey]['chi2'],2))+')')
   hChi2.append(fit_collector[tkey]['chi2'])
   for key in fit_collector[tkey]:
    sum=0
    if key[:2] == 'En' and not(key[3:] == 'log'):
     for x in fit_collector[tkey][key]:
      hValDatn.append(fitCount+0.25)
      sum += x.mean
      enCentral.append(sum)
      enError.append(x.sdev)
    elif key[:2] == 'Eo' and not(key[3:] == 'log'):
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
 ax.set_ylim([0.8,1.8])
 ax.errorbar(hValDatn,enCentral,enError,
  color='r',marker='o',linestyle='')
 ax.errorbar(hValDato,eoCentral,eoError,
  color='b',marker='o',linestyle='')
 for x in range(1,fitCount):
  ax.axvline(x,color='k')
 plt.show()
