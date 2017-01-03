import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines      as df
import define_prior as dfp
from lsqfit._utilities import gammaQ
from matplotlib import gridspec

## -- works better for X11 forwarding
mpl.use('TkAgg')

def plot_splitting(fit_collector,**kwargs):
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
   try:
    fit_collector[tkey] # check that this works
   except KeyError:
    ## -- lots of key errors; not a big deal
    #print tkey,"continuing"
    continue
   ## -- collect only important info
   try:
    Qval = gammaQ(fit_collector[tkey]['rdof']/2.,fit_collector[tkey]['chi2']/2.)
    #if Qval < 0.001:
    # continue
    print tkey,fit_collector[tkey]['rdof'],fit_collector[tkey]['chi2'],Qval
    hQval.append(' (%.2g)' % Qval)
   except:
    #continue
    hQval.append(' (?)')
   hVal.append(fitCount+0.5)
   if fit_collector[tkey]['rdof'] > 0:
    hName.append(str(nst) +'+'+ str(ost)
    +' (%.2g)' % gammaQ(fit_collector[tkey]['rdof']/2.,fit_collector[tkey]['chi2']/2.))
    #+' ('+ str(round((dof-npr*(nst+ost))*fit_collector[tkey]['chi2']/dof,2))+')'
   else:
    hName.append(str(nst) +'+'+ str(ost) +' (?)')

  ## -- TODO here
   for key in fit_collector[tkey]:
    #sum=0
    if key[-2:] == 'En' and not(key[3:] == 'log'):
     hValDatn.append(list())
     enCentral.append(list())
     enError.append(list())
     for x in fit_collector[tkey][key]:
      hValDatn[-1].append(fitCount+0.25)
      enCentral[-1].append(x.mean)
      enError[-1].append(x.sdev)
    elif key[-2:] == 'Eo' and not(key[3:] == 'log'):
     hValDato.append(list())
     eoCentral.append(list())
     eoError.append(list())
     for x in fit_collector[tkey][key]:
      hValDato[-1].append(fitCount+0.75)
      eoCentral[-1].append(x.mean)
      eoError[-1].append(x.sdev)
   fitCount += 1
 nspl = 4
 ospl = 4
 #fig,ax = plt.subplots(nspl+ospl,1,sharex=True)
 #plt.subplots_adjust(hspace=0)
 ax = []
 fig = plt.figure()
 spllarge = 3
 splrng = nspl+ospl+2*spllarge-2
 def subplot_size(i):
  if i == nspl+ospl-1:
   return (nspl+ospl+spllarge-1,nspl+ospl+2*spllarge-2)
  elif i == ospl-1:
   return (ospl,ospl+spllarge-1)
  elif i < ospl-1:
   return i+1
  elif i > ospl-1 and i < nspl+ospl-1:
   return i+spllarge
  else:
   raise IndexError("Unknown index")
 for i in range(nspl+ospl):
  if i == 0:
   ax.append(plt.subplot(splrng,1,subplot_size(i)))
  else:
   ax.append(plt.subplot(splrng,1,subplot_size(i),sharex=ax[0]))
  if i < nspl+ospl-1:
   ax[i].xaxis.set_visible(False)
  plt.subplots_adjust(hspace=0)
 plt.xticks(hVal,hName,rotation='vertical')
 ax[0].set_xlim([0,fitCount])
 for i in range(nspl+ospl):
  ax[i].set_ylim([0,0.35])
 ax[nspl+ospl-1].set_ylim([0.5,0.8])    ## -- even state 0
 ax[ospl-1].set_ylim([0.5,1.2]) ## -- odd state 0

 ## -- temporarily remove prior lines
 #
 #for i,en,den in zip(range(len(df.define_prior['logEn'])),
 # utf.sum_dE(df.define_prior['logEn']),df.define_prior['logEn']):
 #  if i==0:
 #   ax.axhline(en.mean,color='r')
 #   ax.fill_between([0,fitCount],[en.mean-den.sdev,en.mean-den.sdev],
 #    [en.mean+den.sdev,en.mean+den.sdev],hatch='/',facecolor='r',alpha=0.1)
 #  else:
 #   ax.axhline(en.mean,color='r')
 #   if i<df.plot_n_maxprior:
 #    ax.fill_between([0,fitCount],[en.mean-den.sdev,en.mean-den.sdev],
 #     [en.mean+den.sdev,en.mean+den.sdev],facecolor='r',alpha=0.2)
 #for i,eo,deo in zip(range(len(df.define_prior['logEo'])),
 # utf.sum_dE(df.define_prior['logEo']),df.define_prior['logEo']):
 #  if i==0:
 #   ax.axhline(eo.mean,color='b')
 #   ax.fill_between([0,fitCount],[eo.mean-deo.sdev,eo.mean-deo.sdev],
 #    [eo.mean+deo.sdev,eo.mean+deo.sdev],hatch='\\',facecolor='b',alpha=0.1)
 #  else:
 #   ax.axhline(eo.mean,color='b')
 #   if i<df.plot_o_maxprior:
 #    ax.fill_between([0,fitCount],[eo.mean-deo.sdev,eo.mean-deo.sdev],
 #     [eo.mean+deo.sdev,eo.mean+deo.sdev],facecolor='b',alpha=0.2)

 hValDat = list()
 hCenDat = list()
 hErrDat = list()
 for i in range(nspl+ospl):
  hValDat.append(list())
  hCenDat.append(list())
  hErrDat.append(list())
 for x,y,s in zip(hValDatn,enCentral,enError):
  for i in range(nspl): ## -- pseudo-transpose data
   try:
    hValDat[i].append(x[i])
    hCenDat[i].append(y[i])
    hErrDat[i].append(s[i])
   except:
    pass
 for x,y,s in zip(hValDato,eoCentral,eoError):
  for i in range(ospl):
   try:
    hValDat[i+nspl].append(x[i])
    hCenDat[i+nspl].append(y[i])
    hErrDat[i+nspl].append(s[i])
   except:
    pass

 for i in range(nspl):
  ax[::-1][i].errorbar(hValDat[i],hCenDat[i],hErrDat[i],
   color='r',marker='o',linestyle='')
 for i in range(nspl,nspl+ospl):
  ax[::-1][i].errorbar(hValDat[i],hCenDat[i],hErrDat[i],
   color='b',marker='o',linestyle='')
 for i in range(nspl+ospl):
  for x in range(1,fitCount):
   ax[i].axvline(x,color='k')
 if True:
  plt.show()
 else:
  mng = plt.get_current_fig_manager()
  mng.resize(*mng.window.maxsize())
  fig.set_size_inches(8,5)
  plt.subplots_adjust(bottom=0.30)
  fig.savefig('/home/asm58/stability_out_tmp.pdf',dpi=400)
  #plt.savefig('/home/asm58/stability_out_tmp.pdf')
