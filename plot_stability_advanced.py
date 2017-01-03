import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import gvar as gv
import make_prior_advanced as mpa
import util_funcs as utf
import util_plots as utp
import defines      as df
import define_prior as dfp
from lsqfit._utilities import gammaQ

## -- works better for X11 forwarding
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
   try:
    fit_collector[tkey] # check that this works
   except KeyError:
    ## -- lots of key errors; not a big deal
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

   tspec = utf.retrieve_spectrum_advanced(fit_collector[tkey])
   #print tspec
   for key in tspec:
    it = 0
    if key[-2:] == 'En' and not(key[3:] == 'log' or key[4:] == 'sqrt'):
     for e in tspec[key]:
      hValDatn.append(fitCount+0.25)
      enCentral.append(e.mean)
      enError.append(e.sdev)
    elif key[-2:] == 'Eo' and not(key[3:] == 'log' or key[4:] == 'sqrt'):
     for e in tspec[key]:
      hValDato.append(fitCount+0.75)
      eoCentral.append(e.mean)
      eoError.append(e.sdev)
    
   #for key in fit_collector[tkey]:
   # sum=0
   # #if key[:2] == 'En' and not(key[3:] == 'log'):
   # if key[-2:] == 'En' and not(key[3:] == 'log'):
   #  #print "test",key,key[-2:],(key[:2] == 'En')
   #  for x in fit_collector[tkey][key]:
   #   hValDatn.append(fitCount+0.25)
   #   sum += x.mean
   #   enCentral.append(sum)
   #   enError.append(x.sdev)
   # elif key[-2:] == 'Eo' and not(key[3:] == 'log'):
   #  for x in fit_collector[tkey][key]:
   #   hValDato.append(fitCount+0.75)
   #   sum += x.mean
   #   eoCentral.append(sum)
   #   eoError.append(x.sdev)
   fitCount += 1
 fig = plt.figure()
 ax = fig.add_subplot(111)
 plt.xticks(hVal,hName,rotation='vertical')
 ax.set_xlim([0,fitCount])
 ax.set_ylim([0.5,1.5])
 pe = mpa.retrieve_linear_prior(df.define_prior_adv.copy())
 pe = utf.retrieve_spectrum_advanced(pe)
 for i,en in enumerate(pe['En']):
   if i==0:
    ax.axhline(en.mean,color='r')
    ax.fill_between([0,fitCount],[en.mean-en.sdev,en.mean-en.sdev],
     [en.mean+en.sdev,en.mean+en.sdev],hatch='/',facecolor='r',alpha=0.1)
   else:
    ax.axhline(en.mean,color='r')
    if i<df.plot_n_maxprior:
     ax.fill_between([0,fitCount],[en.mean-en.sdev,en.mean-en.sdev],
      [en.mean+en.sdev,en.mean+en.sdev],facecolor='r',alpha=0.2)
 for i,eo in enumerate(pe['Eo']):
   if i==0:
    ax.axhline(eo.mean,color='b')
    ax.fill_between([0,fitCount],[eo.mean-eo.sdev,eo.mean-eo.sdev],
     [eo.mean+eo.sdev,eo.mean+eo.sdev],hatch='\\',facecolor='b',alpha=0.1)
   else:
    ax.axhline(eo.mean,color='b')
    if i<df.plot_o_maxprior:
     ax.fill_between([0,fitCount],[eo.mean-eo.sdev,eo.mean-eo.sdev],
      [eo.mean+eo.sdev,eo.mean+eo.sdev],facecolor='b',alpha=0.2)
 ax.errorbar(hValDatn,enCentral,enError,
  color='r',marker='o',linestyle='')
 ax.errorbar(hValDato,eoCentral,eoError,
  color='b',marker='o',linestyle='')
 for x in range(1,fitCount):
  ax.axvline(x,color='k')
 if True:
  plt.show()
 else:
  mng = plt.get_current_fig_manager()
  mng.resize(*mng.window.maxsize())
  fig.set_size_inches(8,5)
  plt.subplots_adjust(bottom=0.30)
  fig.savefig('/home/asm58/stability_out_tmp.pdf',dpi=400)
  #plt.savefig('/home/asm58/stability_out_tmp.pdf')
