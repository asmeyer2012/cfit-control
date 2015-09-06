import matplotlib.pyplot as plt
from   matplotlib.ticker import MaxNLocator
#from   matplotlib        import gridspec
import numpy as np
import copy
import gvar as gv
import lsqfit as lsf
import util_funcs as ut
import defines as df

def plot_corr_double_log(models,data,fit,plot,**kwargs):
 ## -- use models to determine fit ranges, etc
 tslc = curr_mod.tdata
 tfit = list(curr_mod.tfit)
 ls='None'   # linestyle
 ls2='--'
 mfc='None'  # marker face color (errorbar plot)
 mec='k'     # marker edge color
 color='r'   # marker/line color (non-error plot)
 color2='b'  # marker/line color (fit plot)
 color3='g'  # marker/line color (plateau plot)
 marker='o'  # marker shape
 ms=6.0      # marker size
 #testao=None # test fit function for 1+1 - ao
 #testan=None # test fit function for 1+1 - an
 #testEo=None # test fit function for 1+1 - Eo
 #testEn=None # test fit function for 1+1 - En
 fig,(axp,axm) = plt.subplots(2,sharex=True,figsize=(8,16))
 fig.subplots_adjust(hspace=0)
 
 axp.set_yscale('log')
 axm.set_yscale('log')
 axp.set_ylim(yplim)
 axm.set_ylim(ymlim)
 axm.set_ylim(axm.get_ylim()[::-1])
 #axp.set_yticklabels([])
 #axm.set_yticklabels([])
 #yticklabels = axp.get_yticklabels() + axm.get_yticklabels()
 #plt.setp(yticklabels, visible=False)
 #nbinsp = len(axp.get_yticklabels())
 #nbinsm = len(axm.get_yticklabels())
 #axp.yaxis.set_major_locator(MaxNLocator(nbins=nbinsp))
 #axm.yaxis.set_major_locator(MaxNLocator(nbins=nbinsm))
 ## --
 fit_func = create_fit_func(models,fit,len(tslc))
 tfit.extend(list(sorted([len(tslc) - x for x in tfit])))
 #tfit = range(tfit[0],tfit[0]+len(tfit)*2-1)
 t_all = np.linspace(0.,len(tslc),len(tslc)+1)
 gvfit_all = models[0].s[0]*fit_func(t_all)
 fit_mean = gv.mean(gvfit_all)
 fit_sdev = gv.sdev(gvfit_all)
 fitp_mean = ut.pos_arr(fit_mean,yplim[0]/100)
 fitm_mean = ut.neg_arr(fit_mean,ymlim[0]/100)
 axp.plot(t_all,fitp_mean,color=color2)
 axm.plot(t_all,fitm_mean,color=color2)
 try:
  erbaroff
 except:
  fitp_up = ut.pos_arr(fit_mean+fit_sdev,yplim[0]/100)
  fitm_up = ut.neg_arr(fit_mean+fit_sdev,ymlim[0]/100)
  fitp_lo = ut.pos_arr(fit_mean-fit_sdev,yplim[0]/100)
  fitm_lo = ut.neg_arr(fit_mean-fit_sdev,ymlim[0]/100)
  axp.plot(t_all,fitp_up,color=color2,ls=ls2)
  axm.plot(t_all,fitm_up,color=color2,ls=ls2)
  axp.plot(t_all,fitp_lo,color=color2,ls=ls2)
  axm.plot(t_all,fitm_lo,color=color2,ls=ls2)
 ## -- see what the fit function would look like from 1+1 analysis
 ##if not (fake_func is None):
 ## gvfake_all = models[0].s[0]*fake_func(t_all)
 ## fake_mean = gv.mean(gvfake_all)
 ## fake_sdev = gv.sdev(gvfake_all)
 ## ax.plot(t_all,fake_mean,color=color3)
 ## try:
 ##  erbaroff
 ## except:
 ##  ax.plot(t_all,fake_mean+fit_sdev,color=color3,ls=ls2)
 ##  ax.plot(t_all,fake_mean-fit_sdev,color=color3,ls=ls2)
 #
 ## -- data
 dmean = models[0].s[0]*gv.mean(data[key])
 dsdev = gv.sdev(data[key])
 dp_mean = ut.pos_arr(dmean)
 dm_mean = ut.neg_arr(dmean)
 dp_sdev = [ dsdev[i] if dmean[i]+dsdev[i] > 0 else 0 for i in range(len(dsdev))]
 dm_sdev = [ dsdev[i] if dmean[i]-dsdev[i] < 0 else 0 for i in range(len(dsdev))]
 axp.errorbar(tslc,dp_mean,yerr=(dsdev,dp_sdev),ls=ls,mfc=mfc,mec=mec,\
  color=color,marker=marker,ms=ms)
 axm.errorbar(tslc,dm_mean,yerr=(dsdev,dm_sdev),ls=ls,mfc=mfc,mec=mec,\
  color=color,marker=marker,ms=ms)
 axp.scatter(tfit,[dp_mean[i] for i in tfit],color=color,marker=marker,s=ms*ms)
 axm.scatter(tfit,[dm_mean[i] for i in tfit],color=color,marker=marker,s=ms*ms)
 #
 ## -- axis modifications
 kwargs2={}
 #kwargs2['plotTitle']="Class 7 MILC (sss) Correlator"
 kwargs2['yaxisTitle']="C(t)"
 #try:
 # kwargs2['ylim']=ylim
 #except NameError:
 # pass
 axis_mods_correlator(fig,key,len(tslc),**kwargs2)
 plt.show()

def plot_correlator(models,data,fit,fig,key,plot_type,**kwargs):
 ## -- use data to make plots
 ## -- all data points shown with error bars
 ## -- points used in fit are filled in, others are not
 #

 ## -- determine index of models to use
 curr_mod=models[models[0].all_datatags.index(key)]

 ## -- set up figure objects
 ax  = fig.gca()
 rect= fig.patch

 ## -- use models to determine fit ranges, etc
 tslc = curr_mod.tdata
 tfit = curr_mod.tfit
 pfit = None # plateau fit range
 ls='None'   # linestyle
 ls2='--'
 mfc='None'  # marker face color (errorbar plot)
 mec='k'     # marker edge color
 color='r'   # marker/line color (non-error plot)
 color2='b'  # marker/line color (fit plot)
 color3='g'  # marker/line color (plateau plot)
 marker='o'  # marker shape
 ms=6.0      # marker size
 sep=2       # separation between correlators in ratio/sum
 testao=None # test fit function for 1+1 - ao
 testan=None # test fit function for 1+1 - an
 testEo=None # test fit function for 1+1 - Eo
 testEn=None # test fit function for 1+1 - En

 ## -- set up fit 
 ## -- if test.. are defined, do a fake 1+1 parameter fit as well
 fit_func = create_fit_func(models,fit,len(tslc))
 fake_func=None
 if not (testao is None or testan is None or testEo is None or testEn is None):
  fakefit = copy.deepcopy(fit)
  fakefit.transformed_p['ao']=[testao]
  fakefit.transformed_p['an']=[testan]
  fakefit.transformed_p['Eo']=[testEo]
  fakefit.transformed_p['En']=[testEn]
  fake_func = create_fit_func(models,fakefit,len(tslc))
 #
 if plot_type is "correlator":
  tfit = range(tfit[0],tfit[0]+len(tfit)*2-1)
  t_all = np.linspace(0.,len(tslc),len(tslc)+1)
  gvfit_all = models[0].s[0]*fit_func(t_all)
  fit_mean = gv.mean(gvfit_all)
  fit_sdev = gv.sdev(gvfit_all)
  ax.plot(t_all,fit_mean,color=color2)
  try:
   erbaroff
  except:
   ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2)
   ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2)
  ## -- see what the fit function would look like from 1+1 analysis
  if not (fake_func is None):
   gvfake_all = models[0].s[0]*fake_func(t_all)
   fake_mean = gv.mean(gvfake_all)
   fake_sdev = gv.sdev(gvfake_all)
   ax.plot(t_all,fake_mean,color=color3)
   try:
    erbaroff
   except:
    ax.plot(t_all,fake_mean+fit_sdev,color=color3,ls=ls2)
    ax.plot(t_all,fake_mean-fit_sdev,color=color3,ls=ls2)
  #
  ## -- data
  dmean = models[0].s[0]*gv.mean(data[key])
  dsdev = gv.sdev(data[key])
  ax.errorbar(tslc,dmean,yerr=dsdev,ls=ls,mfc=mfc,mec=mec,color=color,marker=marker,ms=ms)
  ax.scatter(tfit,dmean[tfit[0:len(tfit)]],color=color,marker=marker,s=ms*ms)
  #
  ## -- axis modifications
  kwargs2={}
  try:
   kwargs2['ylim']=ylim
  except NameError:
   pass
  try:
   kwargs2['plotTitle']=plottitle
  except NameError:
   kwargs2['plotTitle']="default title"
  try:
   kwargs2['yaxisTitle']=yaxistitle
  except NameError:
   kwargs2['yaxisTitle']="default y-axis title"
  axis_mods_correlator(fig,key,len(tslc),**kwargs2)
  #
 ## ------
 ##
 elif plot_type is "log_ratio":
  sep=df.sep # timeslice separation between correlators in ratio
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-0.5-sep,100)
  try:
   gvfit_all = fit.transformed_p['E'][0]*np.ones(len(t_all))
  except KeyError:
   gvfit_all = fit.transformed_p['En'][0]*np.ones(len(t_all))
  fit_mean = gv.mean(gvfit_all)
  fit_sdev = gv.sdev(gvfit_all)
  ax.plot(t_all,fit_mean,color=color2)
  try:
   erbaroff
  except:
   ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2)
   ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2)
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [ls.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]))
  rdat = gv.log([avdat[i]/avdat[i+sep] for i in range(len(avdat)-sep)])/sep
  #
  dmean = gv.mean(rdat)
  dsdev = gv.sdev(rdat)
  #
  ax.errorbar(tslc[0:len(tslc)/2+1-sep],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms)
  ax.scatter(tfit[0:len(tfit)-sep],dmean[tfit[0:len(tfit)-sep]],color=color,marker=marker,s=ms*ms)
  #
  ## -- axis modifications
  kwargs2={}
  try:
   kwargs2['ylim']=ylim
  except NameError:
   pass
  axis_mods_log_ratio(fig,key,len(tslc),sep=sep,**kwargs2)
  #
 ## ------
 ##
 elif plot_type is "fit_normalized":
  ## -- fit
  if df.do_baryon:
   tlen = len(tslc)/2-1
  else:
   tlen = len(tslc)/2
  t_all = np.linspace(1,tlen,tlen)
  gvfit_all = fit_func(t_all)
  fit_norm = np.ones(len(t_all))
  fit_mean = gv.mean(gvfit_all)
  fit_sdev = gv.sdev(gvfit_all)/np.abs(fit_mean)
  ax.plot(t_all,fit_norm,color=color2)
  ax.plot(t_all,fit_norm+fit_sdev,color=color2,ls=ls2)
  ax.plot(t_all,fit_norm-fit_sdev,color=color2,ls=ls2)
  if not (fake_func is None):
   ## -- see what the fit function would look like from 1+1 analysis
   gvfake_all = models[0].s[0]*fake_func(t_all)
   fake_mean = gv.mean(gvfake_all)/gv.mean(gvfit_all)
   fake_sdev = gv.sdev(gvfake_all)/gv.mean(gvfit_all)
   ax.plot(t_all,fake_mean,color=color3)
   ax.plot(t_all,fake_mean+fit_sdev,color=color3,ls=ls2)
   ax.plot(t_all,fake_mean-fit_sdev,color=color3,ls=ls2)
  #
  ## -- data
  tps = (1 if models[0].tp > 0 else -1)
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],tps*data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]))
  tav = np.array(range(len(avdat)))
  tav =[x for x in tav if abs(gv.mean(fit_func(x))) > 0]
  tfit2 = [t for t in tav if t in tfit]
  ndat=[avdat[x]/gv.mean(fit_func(x)) for x in tav]
  #
  dmean = gv.mean(ndat)
  dsdev = gv.sdev(ndat)
  #
  ax.errorbar(tslc[0:tlen+1],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms)
  ax.scatter(tfit2,dmean[tfit2],color=color,marker=marker,s=ms*ms)
  #
  ### -- axis modifications
  kwargs2={}
  try:
   kwargs2['ylim']=ylim
  except NameError:
   pass
  try:
   kwargs2['plotTitle']=plottitle
  except NameError:
   kwargs2['plotTitle']="default title"
  try:
   kwargs2['yaxisTitle']=yaxistitle
  except NameError:
   kwargs2['yaxisTitle']="default y-axis title"
  axis_mods_fit_normalized(fig,key,len(tslc),**kwargs2)
  #
 elif plot_type is "prior_normalized":
  ## -- fit
  if df.do_baryon:
   tlen = len(tslc)/2-1
  else:
   tlen = len(tslc)/2
  t_all = np.linspace(1,tlen,tlen)
  gvfit_all = fit_func(t_all)
  fit_norm = np.ones(len(t_all))
  fit_mean = gv.mean(gvfit_all)
  fit_sdev = gv.sdev(gvfit_all)/np.abs(fit_mean)
  ax.plot(t_all,fit_norm,color=color3)
  ax.plot(t_all,fit_norm+fit_sdev,color=color3,ls=ls2)
  ax.plot(t_all,fit_norm-fit_sdev,color=color3,ls=ls2)
  #
  ## -- data
  tps = (1 if models[0].tp > 0 else -1)
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],tps*data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]))
  tav = np.array(range(len(avdat)))
  tav =[t for t in tav if abs(gv.mean(fit_func(t))) > 0]
  trem =[(0 if abs(gv.mean(fit_func(t))) > 0 else 1) for t in range(len(tslc)/2)]
  tslc2 =[t for t in range(len(tslc)/2) if abs(gv.mean(fit_func(t))) > 0]
  trem2 = [sum(trem[:i+1]) for i in range(len(trem))]
  tfit2 = [t for t in tav if t in tfit]
  ndat=[avdat[t]/gv.mean(fit_func(t)) for t in tav]
  #
  dmean = gv.mean(ndat)
  dsdev = gv.sdev(ndat)
  #
  ax.errorbar(tslc2,dmean[range(len(tslc2))],yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms)
  ax.scatter(tfit2,dmean[[x-y for x,y in zip(tfit2,[trem2[t] for t in tfit2])]],\
   color=color,marker=marker,s=ms*ms)
  #
  ### -- axis modifications
  kwargs2={}
  try:
   kwargs2['ylim']=ylim
  except NameError:
   pass
  try:
   kwargs2['plotTitle']=plottitle
  except NameError:
   kwargs2['plotTitle']="default title"
  try:
   kwargs2['yaxisTitle']=yaxistitle
  except NameError:
   kwargs2['yaxisTitle']="default y-axis title"
  axis_mods_fit_normalized(fig,key,len(tslc),**kwargs2)
  #
 elif plot_type is "log_ratio2":
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-2.5,100)
  gvfit_all = fit.transformed_p['En'][0]*np.ones(len(t_all))
  ## -- 
  fit_mean = gv.mean(gvfit_all)
  fit_sdev = gv.sdev(gvfit_all)
  ax.plot(t_all,fit_mean,color=color2)
  ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2)
  ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2)
  #
  ## -- data
  tps=(1 if models[0].tp > 0 else -1)
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],tps*data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]))
  ## --
  rdat = gv.log([avdat[i]/avdat[i+2] if avdat[i]/avdat[i+2] > 0 else gv.gvar(1,1)
   for i in range(len(avdat)-2)]) / 2
  dmean = gv.mean(rdat)
  dsdev = gv.sdev(rdat)
  #
  ax.errorbar(tslc[0:len(tslc)/2+1-2],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms)
  ax.scatter(tfit[0:len(tfit)-2],dmean[tfit[0:len(tfit)-2]],color=color,marker=marker,s=ms*ms)
  if not(pfit is None):
   pavg = lsf.wavg(rdat[pfit])
   pmean= pavg.mean*np.ones(len(pfit))
   psdev= pavg.sdev*np.ones(len(pfit))
   print "              Fit value for ",plot_type," plot: ",fit.transformed_p['En'][0]
   try:
    print "Wghtd avg plateau value for ",plot_type," plot: ",pavg
   except:
    print
   ax.scatter(pfit,dmean[pfit],color=color3,marker=marker,s=ms*ms)
   ax.plot(pfit,pmean,color=color3)
   ax.plot(pfit,pmean+psdev,color=color3,ls=ls2)
   ax.plot(pfit,pmean-psdev,color=color3,ls=ls2)
  #
  ## -- axis modifications
  kwargs2={}
  try:
   kwargs2['ylim']=ylim
  except NameError:
   pass
  try:
   kwargs2['plotTitle']=plottitle
  except NameError:
   kwargs2['plotTitle']="default title"
  try:
   kwargs2['yaxisTitle']=yaxistitle
  except NameError:
   kwargs2['yaxisTitle']="default y-axis title"
  axis_mods_log_ratio(fig,key,len(tslc),sep=2,**kwargs2)
  #
 ## ------
 ##
 elif plot_type is "log_ratio123":
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-2.5,100)
  gvfit_all = (fit.transformed_p['Eo'][0])*np.ones(len(t_all))
  ## -- 
  fit_mean = gv.mean(gvfit_all)
  fit_sdev = gv.sdev(gvfit_all)
  ax.plot(t_all,fit_mean,color=color2)
  ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2)
  ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2)
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]))
  ## --
  sep=1
  sep2=2
  sgn=-1
  entmp=fit.transformed_p['En'][0]
  rdat = np.divide([np.power(-1,i)*
         ((avdat[i+sep]+sgn*avdat[i])
         -gv.exp(entmp)*(avdat[i+sep+1]+sgn*avdat[i+1]))
         for i in range(len(avdat)-sep-1)],
         models[0].s[1])
  rpdat=np.divide(gv.log([rdat[i]/rdat[i+sep2] if rdat[i]/rdat[i+sep2] > 0 else gv.gvar(1,1)
   for i in range(len(rdat)-sep2)]),sep2)
  dmean = gv.mean(rpdat)
  dsdev = gv.sdev(rpdat)
  #
  ax.errorbar(tslc[0:len(tslc)/2-sep-sep2],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms)
  ax.scatter(tfit[0:len(tfit)-1-sep-sep2],dmean[tfit[0:len(tfit)-1-sep-sep2]],\
   color=color,marker=marker,s=ms*ms)
  if not(pfit is None):
   pavg = lsf.wavg(rpdat[pfit])
   pmean= pavg.mean*np.ones(len(pfit))
   psdev= pavg.sdev*np.ones(len(pfit))
   print "              Fit value for ",plot_type," plot: ",fit.transformed_p['Eo'][0]
   print "Wghtd avg plateau value for ",plot_type," plot: ",pavg
   ax.scatter(pfit,dmean[pfit],color=color3,marker=marker,s=ms*ms)
   ax.plot(pfit,pmean,color=color3)
   ax.plot(pfit,pmean+psdev,color=color3,ls=ls2)
   ax.plot(pfit,pmean-psdev,color=color3,ls=ls2)
  #
  ## -- axis modifications
  kwargs2={}
  try:
   kwargs2['ylim']=ylim
  except NameError:
   pass
  try:
   kwargs2['plotTitle']=plottitle
  except NameError:
   kwargs2['plotTitle']="default title"
  try:
   kwargs2['yaxisTitle']=yaxistitle
  except NameError:
   kwargs2['yaxisTitle']="default y-axis title"
  axis_mods_log_ratio123(fig,key,len(tslc),**kwargs2)
  #
 ## ------
 ##
 elif plot_type is "sum_odd" or \
      plot_type is "sum_even":
  eotag  ='Eo'
  entag  ='En'
  if plot_type is "sum_even":
   sep=1
   #do_odd=0
   atag  ='an'
   sgn=1
  else:
   sep=1
   #do_odd=1
   atag  ='ao'
   sgn=-1
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-2.5,100)
  gvfit_all = fit.transformed_p[atag][0]*\
              fit.transformed_p[atag][0]*np.ones(len(t_all))
  ## -- 
  fit_mean = gv.mean(gvfit_all)
  fit_sdev = gv.sdev(gvfit_all)
  ax.plot(t_all,fit_mean,color=color2)
  ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2)
  ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2)
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]))
  ## --
  entmp=fit.transformed_p[entag][0]
  eotmp=fit.transformed_p[eotag][0]
  if plot_type is "sum_even":
   ## -- this works for En0 < Eo0
   #rdat = [(gv.exp(entmp*i)
   #        /gv.exp(-entmp*sep)+sgn*1)
   #       *(avdat[i+sep]+sgn*avdat[i])*np.power(-1,do_odd*i) for i in range(len(avdat)-sep)]
   ## -- improved version
   rdat = np.divide([gv.exp(entmp*i)*
          ((avdat[i+sep]+sgn*avdat[i])
          +gv.exp(eotmp)*(avdat[i+sep+1]+sgn*avdat[i+1]))
          for i in range(len(avdat)-sep-1)],
          (models[0].s[0]*
          (gv.exp(-entmp*sep)+sgn*1)*
          (gv.exp(-entmp+eotmp)+1)))
  else:
   rdat = np.divide([np.power(-1,i)*gv.exp(eotmp*i)*
          ((avdat[i+sep]+sgn*avdat[i])
          -gv.exp(entmp)*(avdat[i+sep+1]+sgn*avdat[i+1]))
          for i in range(len(avdat)-sep-1)],
          (models[0].s[1]*
          (np.power(-1,sep)*gv.exp(-eotmp*sep)+sgn*1)*
          (gv.exp(-eotmp+entmp)+1)))
  dmean = gv.mean(rdat)
  dsdev = gv.sdev(rdat)
  #
  if plot_type is "sum_even":
   ax.errorbar(tslc[0:len(tslc)/2-sep],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
    mec=mec,color=color,marker=marker,ms=ms)
   ax.scatter(tfit[0:len(tfit)-sep-1],dmean[tfit[0:len(tfit)-sep-1]],\
    color=color,marker=marker,s=ms*ms)
  else:
   ax.errorbar(tslc[0:len(tslc)/2-sep],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
    mec=mec,color=color,marker=marker,ms=ms)
   ax.scatter(tfit[0:len(tfit)-sep-1],dmean[tfit[0:len(tfit)-sep-1]],\
    color=color,marker=marker,s=ms*ms)
  #
  if not(pfit is None):
   pavg = lsf.wavg([rdat[i] if rdat[i] > 0 else gv.gvar(0,1) for i in pfit])
   #pavg = lsf.wavg(rdat[pfit])
   pmean= pavg.mean*np.ones(len(pfit))
   psdev= pavg.sdev*np.ones(len(pfit))
   print "              Fit value for ",plot_type," plot: ",fit.transformed_p[atag][0]
   print "Wghtd avg plateau value for ",plot_type," plot: ",gv.sqrt(pavg)
   ax.scatter(pfit,dmean[pfit],color=color3,marker=marker,s=ms*ms)
   ax.plot(pfit,pmean,color=color3)
   ax.plot(pfit,pmean+psdev,color=color3,ls=ls2)
   ax.plot(pfit,pmean-psdev,color=color3,ls=ls2)
  #
  ## -- axis modifications
  kwargs2={}
  kwargs2['plot_type']=plot_type
  try:
   kwargs2['ylim']=ylim
  except NameError:
   pass
  try:
   kwargs2['plotTitle']=plottitle
  except NameError:
   kwargs2['plotTitle']="default title"
  try:
   kwargs2['yaxisTitle']=yaxistitle
  except NameError:
   kwargs2['yaxisTitle']="default y-axis title"
  axis_mods_sum(fig,key,len(tslc),sep=sep,sgn=sgn,**kwargs2)
  #
 ## ------
 ##
 elif plot_type is "simple_sum_odd" or \
      plot_type is "simple_sum_even":
  eotag  ='Eo'
  entag  ='En'
  sep=1
  if plot_type is "simple_sum_even":
   atag  ='an'
   sgn=1
  else:
   atag  ='ao'
   sgn=-1
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-2.5,100)
  gvfit_all = fit.transformed_p[atag][0]*\
              fit.transformed_p[atag][0]*np.ones(len(t_all))
  ## -- 
  fit_mean = gv.mean(gvfit_all)
  fit_sdev = gv.sdev(gvfit_all)
  ax.plot(t_all,fit_mean,color=color2)
  ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2)
  ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2)
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]))
  ## --
  entmp=fit.transformed_p[entag][0]
  eotmp=fit.transformed_p[eotag][0]
  #
  if plot_type is "simple_sum_even":
   rdat = np.divide([gv.exp(entmp*i)*(gv.exp(entmp*sep)*avdat[i+sep]+sgn*avdat[i])
          for i in range(len(avdat)-sep)],
          (models[0].s[0]*2.))
  else:
   rdat = np.divide([np.power(-1,i)*gv.exp(eotmp*i)*
          (gv.exp(entmp*sep)*avdat[i+sep]+sgn*avdat[i])
          for i in range(len(avdat)-sep)],
          (models[0].s[1])*
          (-gv.exp(-eotmp+entmp)-1))
  dmean = gv.mean(rdat)
  dsdev = gv.sdev(rdat)
  #
  if plot_type is "simple_sum_even":
   ax.errorbar(tslc[0:len(tslc)/2-sep+1],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
    mec=mec,color=color,marker=marker,ms=ms)
   ax.scatter(tfit[0:len(tfit)-sep],dmean[tfit[0:len(tfit)-sep]],\
    color=color,marker=marker,s=ms*ms)
  else:
   ax.errorbar(tslc[0:len(tslc)/2-sep+1],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
    mec=mec,color=color,marker=marker,ms=ms)
   ax.scatter(tfit[0:len(tfit)-sep],dmean[tfit[0:len(tfit)-sep]],\
    color=color,marker=marker,s=ms*ms)
  if not(pfit is None):
   pavg = lsf.wavg([rdat[i] if rdat[i] > 0 else gv.gvar(0,1) for i in pfit])
   pmean= pavg.mean*np.ones(len(pfit))
   psdev= pavg.sdev*np.ones(len(pfit))
   print "              Fit value for ",plot_type," plot: ",fit.transformed_p[atag][0]
   print "Wghtd avg plateau value for ",plot_type," plot: ",gv.sqrt(pavg)
   ax.scatter(pfit,dmean[pfit],color=color3,marker=marker,s=ms*ms)
   ax.plot(pfit,pmean,color=color3)
   ax.plot(pfit,pmean+psdev,color=color3,ls=ls2)
   ax.plot(pfit,pmean-psdev,color=color3,ls=ls2)
  #
  ## -- axis modifications
  kwargs2={}
  kwargs2['plot_type']=plot_type
  try:
   kwargs2['ylim']=ylim
  except NameError:
   pass
  try:
   kwargs2['plotTitle']=plottitle
  except NameError:
   kwargs2['plotTitle']="default title"
  try:
   kwargs2['yaxisTitle']=yaxistitle
  except NameError:
   kwargs2['yaxisTitle']="default y-axis title"
  axis_mods_simple_sum(fig,key,len(tslc),sep=sep,sgn=sgn,**kwargs2)
  #
 else:
  print "Not a valid plot type"
  return
## ------
##

def axis_mods_correlator(fig,key,tmax=None,**kwargs):
 fontsize=20
 if not tmax is None:
  xlim=[-1,tmax+1]
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value
   elif akey == "ylim":
    ylim = value
   elif akey == "fontsize":
    fontsize = value
   elif akey == "plotTitle":
    plottitle = value
   elif akey == "yaxisTitle":
    yaxistitle = value
 try:
  yaxistitle
 except UnboundLocalError:
  yaxistitle = ""
 try:
  plottitle
 except UnboundLocalError:
  plottitle = "default title"
 ##endif kwargs
 #
 ax   =fig.gca()
 rect =fig.patch
 fig.suptitle(plottitle,fontsize=fontsize)
 ax.set_xlabel(r'$t$ slice')
 ax.set_ylabel(yaxistitle)
 if not tmax is None:
  ax.set_xlim(xlim)
 try:
  ax.set_ylim(ylim)
 except NameError:
  pass
 ax.set_yscale('log')
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize) # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white')
## ------

def axis_mods_log_ratio(fig,key,tmax=None,sep=1,**kwargs):
 fontsize=20
 if not tmax is None:
  xlim=[-1,tmax/2+1-sep]
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value
   elif akey == "ylim":
    ylim = value
   elif akey == "fontsize":
    fontsize = value
   elif akey == "plotTitle":
    plottitle = value
   elif akey == "yaxisTitle":
    yaxistitle = value
 ##endif kwargs
 #
 ax   =fig.gca()
 rect =fig.patch
 fig.suptitle(plottitle,fontsize=fontsize)
 ax.set_xlabel(r'$t$ slice')
 #if sep > 1:
 # ax.set_ylabel(r'$-log(C_\pi(t+'+str(sep)+r'a) / C_\pi(t))$')
 #else:
 # ax.set_ylabel(r'$-log(C_\pi(t+a) / C_\pi(t))$')
 ax.set_ylabel(yaxistitle)
 if not tmax is None:
  ax.set_xlim(xlim)
 try:
  ax.set_ylim(ylim)
 except NameError:
  pass
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize) # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white')
## ------

def axis_mods_fit_normalized(fig,key,tmax=None,**kwargs):
 fontsize=20
 if not tmax is None:
  xlim=[-1,tmax/2+1]
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value
   elif akey == "ylim":
    ylim = value
   elif akey == "fontsize":
    fontsize = value
   elif akey == "plotTitle":
    plottitle = value
   elif akey == "yaxisTitle":
    yaxistitle = value
 ##endif kwargs
 #
 ax   =fig.gca()
 rect =fig.patch
 fig.suptitle(plottitle,fontsize=fontsize)
 ax.set_xlabel(r'$t$ slice')
 ax.set_ylabel(yaxistitle)
 if not tmax is None:
  ax.set_xlim(xlim)
 try:
  ax.set_ylim(ylim)
 except NameError:
  pass
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize) # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white')
## ------

def axis_mods_log_ratio123(fig,key,tmax=None,sep=1,**kwargs):
 fontsize=20
 if not tmax is None:
  xlim=[-1,tmax/2+1-sep]
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value
   elif akey == "ylim":
    ylim = value
   elif akey == "fontsize":
    fontsize = value
   elif akey == "plotTitle":
    plottitle = value
   elif akey == "yaxisTitle":
    yaxistitle = value
 ##endif kwargs
 #
 ax   =fig.gca()
 rect =fig.patch
 fig.suptitle(key+r' $\pi$ 2-pt Log Sum-Ratio',fontsize=fontsize)
 ax.set_xlabel(r'$t$ slice')
 #ax.set_ylabel(r'$log[(-1)^{t+1} log[\frac{C_\pi(t+1a) C_\pi(t+2a)}{C_\pi(t) C_\pi(t+3a)}]]$')
 ax.set_ylabel('-log[ratio of sums]')
 if not tmax is None:
  ax.set_xlim(xlim)
 try:
  ax.set_ylim(ylim)
 except NameError:
  pass
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize) # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white')
## ------

def axis_mods_sum(fig,key,tmax=None,sep=1,sgn=1,**kwargs):
 if sgn == 1:
  sgnstr='+'
 else:
  sgnstr='-'
 fontsize=20
 plot_type="sum_even"
 if not tmax is None:
  xlim=[-1,tmax/2+1-sep]
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value
   elif akey == "ylim":
    ylim = value
   elif akey == "fontsize":
    fontsize = value
   elif akey == "plot_type":
    plot_type = value
   elif akey == "plotTitle":
    plottitle = value
   elif akey == "yaxisTitle":
    yaxistitle = value
 ##endif kwargs
 #
 ax   =fig.gca()
 rect =fig.patch
 if plot_type is "sum_even":
  fig.suptitle(key+r' $\pi$ 2-pt Normalized Correlator Sum (Even)',fontsize=fontsize)
 else: 
  fig.suptitle(key+r' $\pi$ 2-pt Normalized Correlator Sum (Odd)',fontsize=fontsize)
 ax.set_xlabel(r'$t$ slice')
 ax.set_ylabel('Normalized Correlator Sum')
 if not tmax is None:
  ax.set_xlim(xlim)
 try:
  ax.set_ylim(ylim)
 except NameError:
  pass
 ax.set_yscale('log')
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize) # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white')
## ------

def axis_mods_simple_sum(fig,key,tmax=None,sep=1,sgn=1,**kwargs):
 if sgn == 1:
  sgnstr='+'
 else:
  sgnstr='-'
 fontsize=20
 plot_type="simple_sum_even"
 if not tmax is None:
  xlim=[-1,tmax/2+1-sep]
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value
   elif akey == "ylim":
    ylim = value
   elif akey == "fontsize":
    fontsize = value
   elif akey == "plot_type":
    plot_type = value
   elif akey == "plotTitle":
    plottitle = value
   elif akey == "yaxisTitle":
    yaxistitle = value
 ##endif kwargs
 #
 ax   =fig.gca()
 rect =fig.patch
 if plot_type is "simple_sum_even":
  fig.suptitle(key+r' $\pi$ 2-pt Simple Correlator Sum (Even)',fontsize=fontsize)
 else: 
  fig.suptitle(key+r' $\pi$ 2-pt Simple Correlator Sum (Odd)',fontsize=fontsize)
 ax.set_xlabel(r'$t$ slice')
 if sep > 1:
  if plot_type is "simple_sum_even":
   ax.set_ylabel(r'$[C_\pi(t)'+sgnstr+r'C_\pi(t+'+str(sep)+r'a)e^{+E'+str(sep)+r'a}]e^{+Et}/2$')
  else:
   ax.set_ylabel(r'$[C_\pi(t)'+sgnstr+r'C_\pi(t+'+str(sep)+r'a)e^{+E'+str(sep)+r'a}]'\
    +r'(-1)^{t}e^{+Et}/(-e^{-(F-E)a}-1)$')
 else:
  if plot_type is "simple_sum_even":
   ax.set_ylabel(r'$[C_\pi(t)'+sgnstr+r'C_\pi(t+a)e^{+En a}]e^{+En t}/2$')
  else:
   ax.set_ylabel(r'$[C_\pi(t)'+sgnstr+r'C_\pi(t+a)e^{+En a}](-1)^{t}e^{+En t}\frac{1}'\
    +r'{(-e^{-(Eo-En)a}-1)}$')
 if not tmax is None:
  ax.set_xlim(xlim)
 try:
  ax.set_ylim(ylim)
 except NameError:
  pass
 ax.set_yscale('log')
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize) # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white')
## ------
