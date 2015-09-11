import matplotlib.pyplot as plt
from   matplotlib.ticker import MaxNLocator
#from   matplotlib        import gridspec
import numpy as np
import copy
import gvar as gv
import lsqfit as lsf
import util_funcs as ut
import defines as df

def make_plot(models,data,fit):
 key=models[0].datatag
 kwargs={}
 #kwargs['testEn']=gv.gvar(0.302,0.012)
 #kwargs['testEo']=gv.gvar(0.268,0.011)
 #kwargs['testan']=gv.gvar(0.70,0.12) #actual
 #kwargs['testao']=gv.gvar(0.441,0.032) #actual
 #kwargs['erbaroff']=True

 kwargs['ylim']=[1e-5,1e1]
 fig1 = plt.figure()
 plot_correlator(models,data,fit,fig1,key,"correlator",**kwargs)
 #kwargs['ylim']=[-3,5]
 #kwargs['ylim']=[-1,2]
 #fig3 = plt.figure()
 #plot_correlator(models,data,fit,fig3,key,"fit_normalized",**kwargs)
 ## --
 plt.show()

def make_plot_1plus1(models,data,fit):
 key=models[0].datatag
 kwargs={}
 #del kwargs['ylim']
 kwargs['ylim']=[-0.5,1.5]
 kwargs['pfit']=range(5,19)

 fig1 = plt.figure()
 plot_correlator(models,data,fit,fig1,key,"log_ratio2",**kwargs)
 ## --
 kwargs['ylim']=[0.0,3.0]
 #kwargs['pfit']=range(6,19)
 fig2 = plt.figure()
 plot_correlator(models,data,fit,fig2,key,"log_ratio123",**kwargs)
 ## --
 kwargs['ylim']=[1e-3,1e1]
 #kwargs['pfit']=range(12,18)
 fig3 = plt.figure()
 plot_correlator(models,data,fit,fig3,key,"simple_sum_even",**kwargs)
 ## --
 #kwargs['pfit']=range(10,18)
 kwargs['ylim']=[5e-4,5e0]
 fig4 = plt.figure()
 plot_correlator(models,data,fit,fig4,key,"simple_sum_odd",**kwargs)
 ## --
 kwargs['ylim']=[1e-4,1e1]
 kwargs['pfit']=range(12,18)
 fig5 = plt.figure()
 plot_correlator(models,data,fit,fig5,key,"sum_even",**kwargs)
 ## --
 #kwargs['pfit']=range(10,21)
 kwargs['ylim']=[5e-4,5e0]
 fig6 = plt.figure()
 plot_correlator(models,data,fit,fig6,key,"sum_odd",**kwargs)
 plt.show()

def make_plot_corr_neg(models,data,fit,prior):
 ## -- determine index of models to use
 key=models[0].datatag
 curr_mod=models[models[0].all_datatags.index(key)]

 ## -- show the fit normalized plot as well
 kwargs={}
 #kwargs['plotTitle']="Normalized Class 7 MILC (sss) Correlator"
 kwargs['yaxisTitle']=r'$C(t)/C_{prior}(t)$'
 #kwargs['ylim']=[0.8,1.2]
 kwargs['ylim']=[0.5,1.5]
 #kwargs['ylim']=[-1.0,3.0]
 #fig4 = plt.figure()
 #plot_correlator(models,data,prior,fig4,key,"prior_normalized",**kwargs)
 kwargs['yaxisTitle']=r'$C(t)/C_{fit}(t)$'
 fig3 = plt.figure()
 plot_correlator(models,data,fit,fig3,key,"fit_normalized",**kwargs)
 #plt.show()
 #plt.show()

 #if False:
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

 yplim=[1e-12,1e2]
 ymlim=[1e-12,1e2]
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
 minval = 1e-15
 dpp_sdev = [ dsdev[i] if dmean[i]+dsdev[i] > 0 else minval for i in range(len(dsdev))]
 dpm_sdev = [ dsdev[i] if (dmean[i]-dsdev[i] > 0 and dmean[i] > 0) else 
  (max(dmean[i]-minval,minval) if dmean[i] > 0 else -minval)
  for i in range(len(dsdev))]
 dmm_sdev = [ dsdev[i] if dmean[i]-dsdev[i] < 0 else minval for i in range(len(dsdev))]
 dmp_sdev = [ dsdev[i] if (dmean[i]+dsdev[i] < 0 and dmean[i] < 0) else 
  (max(-dmean[i]-minval,minval) if dmean[i] < 0 else -minval)
  for i in range(len(dsdev))]
 axp.errorbar(tslc,dp_mean,yerr=(dpm_sdev,dpp_sdev),ls=ls,mfc=mfc,mec=mec,\
  color=mec,marker=marker,ms=ms)
 axm.errorbar(tslc,dm_mean,yerr=(dmp_sdev,dmm_sdev),ls=ls,mfc=mfc,mec=mec,\
  color=mec,marker=marker,ms=ms)
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

 if not (kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "tslc":
    tslc = value
   elif akey == "tfit":
    tfit = value
   elif akey == "pfit":
    pfit = value
   elif akey == "ls":
    ls = value
   elif akey == "ls2":
    ls2 = value
   elif akey == "mfc":
    mfc = value
   elif akey == "mec":
    mec = value
   elif akey == "color":
    color = value
   elif akey == "color2":
    color2 = value
   elif akey == "color3":
    color3 = value
   elif akey == "marker":
    marker = value
   elif akey == "ms":
    ms = value
   elif akey == "xlim":
    xlim = value
   elif akey == "ylim":
    ylim = value
   elif akey == "testao":
    testao = value
   elif akey == "testan":
    testan = value
   elif akey == "testEo":
    testEo = value
   elif akey == "testEn":
    testEn = value
   elif akey == "erbaroff":
    ## -- turn errors off for fit functions in pure correlator plot
    erbaroff = True
   elif akey == "plotTitle":
    plottitle = value
   elif akey == "yaxisTitle":
    yaxistitle = value
 ##endif kwargs

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

def create_fit_func(models,fit,modeln=0):
 ## -- get a/b key information from models[index].a, etc...
 #
 try:
  tfp=fit.transformed_p
 except AttributeError:
  # prior was input instead
  tfp=fit
  for key in fit.keys():
   if key[:3] == 'log':
    tfp[key[3:]] = gv.exp(fit[key])
 pass
 tfk=tfp.keys()
 tps=(1 if models[0].tp > 0 else -1)
 tpa=abs(models[0].tp)
 #
 la={}
 lb={}
 lE={}
 for akey in ['a','an','ao']:
  if any([tfk[i][-len(akey):]==akey for i in range(len(tfk))]):
   la[akey]=tfp[akey]
 for bkey in ['b','bn','bo']:
  if any([tfk[i][-len(bkey):]==bkey for i in range(len(tfk))]):
   lb[bkey]=tfp[bkey]
 for ekey in ['dE','dEn','dEo','E','En','Eo']:
  if any([tfk[i][-len(ekey):]==ekey for i in range(len(tfk))]):
   lE[ekey]=tfp[ekey]
 try:
  do_odd = abs(models[0].s[1]) > 0
 except TypeError:
  do_odd = False
 try:
  do_evn = abs(models[0].s[0]) > 0
 except TypeError:
  do_evn = True
 if do_odd and do_evn:
  if len(la['an']) == 0:
   #print "even priors not available"
   do_evn = False
  if len(la['ao']) == 0:
   #print "odd priors not available"
   do_odd = False
 pass
 ## --
 if bool(do_odd) ^ bool(do_evn): # xor
  if len(lE.keys()) > 1:
   if len(lE[lE.keys()[0]]) == 0:
    lE = ut.sum_dE(lE[lE.keys()[1]])
    if len(lb.keys()) > 0:
     lc = la[la.keys()[1]]*lb[lb.keys()[1]]
    else:
     lc = la[la.keys()[1]]*la[la.keys()[1]]
   else:
    lE = ut.sum_dE(lE[lE.keys()[0]])
    if len(lb.keys()) > 0:
     lc = la[la.keys()[0]]*lb[lb.keys()[0]]
    else:
     lc = la[la.keys()[0]]*la[la.keys()[0]]
  else:
   lE = ut.sum_dE(lE[lE.keys()[0]])
   if len(lb.keys()) > 0:
    lc = la[la.keys()[0]]*lb[lb.keys()[0]]
   else:
    lc = la[la.keys()[0]]*la[la.keys()[0]]
  pass
  if do_odd:
   def new_func(t):
    return models[0].s[1]*np.dot(lc,
     [gv.cos(t*np.pi)*(gv.exp(-lE[i]*t)+tps*gv.exp(-lE[i]*(tpa-t)))
     for i in range(len(lE))])
  else:
   try:
    def new_func(t):
     return models[0].s[0]*np.dot(lc,
      [gv.exp(-lE[i]*t)+tps*gv.exp(-lE[i]*(tpa-t)) for i in range(len(lE))])
   except TypeError:
    def new_func(t):
     return models[0].s*np.dot(lc,
      [gv.exp(-lE[i]*t)+tps*gv.exp(-lE[i]*(tpa-t)) for i in range(len(lE))])
  return new_func
 ## --
 else:
  if len(lb.keys()) > 0:
   lcn=la['an']*lb['bn']
   lco=la['ao']*lb['bo']
  else:
   lcn=la['an']*la['an']
   lco=la['ao']*la['ao']
  for key in lE:
   if key[-1] is 'n':
    lEn = ut.sum_dE(lE[key])
   elif key[-1] is 'o':
    lEo = ut.sum_dE(lE[key])
  def new_func(t):
   return models[0].s[0]*np.dot(lcn,
        [ gv.exp(-lEn[i]*t)+tps*gv.exp(-lEn[i]*(tpa-t))
          for i in range(len(lEn)) ]) +\
          models[0].s[1]*np.dot(lco,
        [ gv.cos(t*np.pi)*(gv.exp(-lEo[i]*t)+tps*gv.exp(-lEo[i]*(tpa-t)))
          for i in range(len(lEo)) ])
  return new_func
 ## --
pass

#def create_fit_func(models,fit,tmax=0,prekey=None):
# ## -- get a/b key information from models[index].a, etc...
# #
# tfp=fit.transformed_p
# #
# la={}
# lb={}
# lE={}
# if prekey is None:
#  for akey in ['a','an','ao']:
#   try:
#    la[akey]=tfp[akey]
#   except KeyError:
#    continue
#  for bkey in ['b','bn','bo']:
#   try:
#    lb[bkey]=tfp[bkey]
#   except KeyError:
#    continue
#  pass
#  if lb is {}:
#   lb = la
#  elif len(lb) < len(la):
#   for akey in la:
#    try:
#     lb['b'+akey[-1]]
#    except KeyError:
#     lb['b'+akey[-1]]=la[akey]
#  for ekey in ['dE','dEn','dEo','E','En','Eo']:
#   try:
#    lE[ekey]=tfp[ekey]
#   except KeyError:
#    continue
#  pass
#  ## --
#  if not (len(la) == len(lb) == len(lE)):
#   print "Error: unmatched energies/amplitudes"
#   return None
#  if (len(la) == 1):
#   do_odd = False
#   for key in la:
#    la=la[key]
#   for key in lb:
#    lb=lb[key]
#   for key in lE:
#    lE=lE[key]
#    if key[-1] is 'o':
#     do_odd = True
#   lc = la*lb
#   lE = ut.sum_dE(lE)
#   #lE = ut.sum_dE(lE[0])
#   #print models[0].s[0]
#   if do_odd:
#    def new_func(t):
#     return models[0].s[1]*np.dot(lc,\
#      [gv.cos(t*np.pi)*(gv.exp(-lE[i]*t)+gv.exp(-lE[i]*(tmax-t))) for i in range(len(lE))])
#   else:
#    def new_func(t):
#     return models[0].s[0]*np.dot(lc,\
#      [gv.exp(-lE[i]*t)+gv.exp(-lE[i]*(tmax-t)) for i in range(len(lE))])
#   return new_func
#   ## --
#  elif (len(la) == 2):
#   lcn=la['an']*lb['bn']
#   lco=la['ao']*lb['bo']
#   for key in lE:
#    if key[-1] is 'n':
#     lEn = ut.sum_dE(lE[key])
#    elif key[-1] is 'o':
#     lEo = ut.sum_dE(lE[key])
#   def new_func(t):
#    return models[0].s[0]*\
#           np.dot(lcn,[gv.exp(-lEn[i]*t)+gv.exp(-lEn[i]*(tmax-t)) for i in range(len(lEn))])\
#         + models[0].s[1]* np.dot(lco,\
#         [ gv.cos(t*np.pi)*(gv.exp(-lEo[i]*t)+gv.exp(-lEo[i]*(tmax-t)))\
#           for i in range(len(lEo))])
#   return new_func
#  else:
#   print "Error: too many energies/amplitudes N = ",str(len(la))
#   return None
#  pass
#  ## --
# else:
#  return None
# pass

#def create_fit_func(models,fit,tmax=0):
# ## -- get a/b key information from models[index].a, etc...
# #
# lparm=fit.transformed_p
# #
# try: # vanilla
#  a =gv.mean(ut.sqr_arr(lparm['a']))
#  E =gv.mean(ut.sum_dE(lparm['E']))
#  def new_func(t):
#   return models[0].s*np.dot(a,[gv.exp(-E[i]*t)+gv.exp(-E[i]*(tmax-t)) for i in range(len(E))])
#  return new_func
# #
# except KeyError:
#  pass
# #
# try: # even
#  an =ut.sqr_arr(lparm['an'])
#  En =ut.sum_dE(lparm['En'])
#  #
#  try: # even+odd
#   ao =ut.sqr_arr(lparm['ao'])
#   Eo =ut.sum_dE(lparm['Eo'])
#   def new_func(t):
#    return models[0].s[0]*\
#           np.dot(an,[gv.exp(-En[i]*t)+gv.exp(-En[i]*(tmax-t)) for i in range(len(En))])\
#         + models[0].s[1]* np.dot(ao,[gv.cos(t*np.pi)*\
#          (gv.exp(-Eo[i]*t)+gv.exp(-Eo[i]*(tmax-t)))\
#           for i in range(len(Eo))])
#   return new_func
#  #
#  except KeyError: # even only
#   def new_func(t):
#    return models[0].s[0]*\
#           np.dot(an,[gv.exp(-En[i]*t)+gv.exp(-En[i]*(tmax-t)) for i in range(len(En))])
#   return new_func
# #
# except KeyError: # even did not work
#  #
#  try: # odd only
#   ao =gv.mean(ut.sqr_arr(lparm['ao']))
#   Eo =gv.mean(ut.sum_dE(lparm['Eo']))
#   def new_func(t):
#    return models[0].s*np.dot(ao,[gv.cos(t*np.pi)*\
#          (gv.exp(-Eo[i]*t)+gv.exp(-Eo[i]*(tmax-t)))\
#           for i in range(len(Eo))])
#   return new_func
#  #
#  except KeyError: # nothing worked
#   pass
# print "No fit function generated"
# return None
