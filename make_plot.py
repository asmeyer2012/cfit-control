import matplotlib.pyplot as plt
import numpy as np
import copy
import gvar as gv
import lsqfit as lsf
import util_funcs as ut
import defines as df

def make_plot(models,data,fit):
 key=models[0].datatag;
 kwargs={};
 #kwargs['testEn']=gv.gvar(0.302,0.012);
 #kwargs['testEo']=gv.gvar(0.268,0.011);
 #kwargs['testan']=gv.gvar(0.70,0.12); #actual
 #kwargs['testao']=gv.gvar(0.441,0.032); #actual
 #kwargs['erbaroff']=True;

 fig1 = plt.figure();
 plot_correlator(models,data,fit,fig1,key,"correlator",**kwargs);
 kwargs['ylim']=[-3,5];
 fig3 = plt.figure();
 plot_correlator(models,data,fit,fig3,key,"fit_normalized",**kwargs);
 ## --
 plt.show();

def make_plot_1plus1(models,data,fit):
 key=models[0].datatag;
 kwargs={};
 kwargs['pfit']=range(10,19);
 #del kwargs['ylim'];

 fig1 = plt.figure();
 plot_correlator(models,data,fit,fig1,key,"log_ratio2",**kwargs);
 ## --
 kwargs['ylim']=[-0.5,1];
 kwargs['pfit']=range(6,19);
 fig2 = plt.figure();
 plot_correlator(models,data,fit,fig2,key,"log_ratio123",**kwargs);
 ## --
 kwargs['ylim']=[1e-1,1e1];
 kwargs['pfit']=range(10,21);
 fig3 = plt.figure();
 plot_correlator(models,data,fit,fig3,key,"simple_sum_even",**kwargs);
 ## --
 kwargs['pfit']=range(10,21);
 kwargs['ylim']=[5e-2,5e0];
 fig4 = plt.figure();
 plot_correlator(models,data,fit,fig4,key,"simple_sum_odd",**kwargs);
 ## --
 kwargs['ylim']=[1e-1,1e1];
 kwargs['pfit']=range(10,21);
 fig5 = plt.figure();
 plot_correlator(models,data,fit,fig5,key,"sum_even",**kwargs);
 ## --
 kwargs['pfit']=range(10,21);
 kwargs['ylim']=[5e-2,5e0];
 fig6 = plt.figure();
 plot_correlator(models,data,fit,fig6,key,"sum_odd",**kwargs);
 plt.show();

def plot_correlator(models,data,fit,fig,key,plot_type,**kwargs):
 ## -- use data to make plots
 ## -- all data points shown with error bars
 ## -- points used in fit are filled in, others are not
 #

 ## -- determine index of models to use
 curr_mod=models[models[0].all_datatags.index(key)];

 ## -- set up figure objects
 ax  = fig.gca()
 rect= fig.patch;

 ## -- use models to determine fit ranges, etc
 tslc = curr_mod.tdata;
 tfit = curr_mod.tfit;
 pfit = None; # plateau fit range
 ls='None';   # linestyle
 ls2='--';
 mfc='None';  # marker face color (errorbar plot)
 mec='k';     # marker edge color
 color='r';   # marker/line color (non-error plot)
 color2='b';  # marker/line color (fit plot)
 color3='g';  # marker/line color (plateau plot)
 marker='o';  # marker shape
 ms=6.0;      # marker size
 sep=2;       # separation between correlators in ratio/sum
 testao=None; # test fit function for 1+1 - ao
 testan=None; # test fit function for 1+1 - an
 testEo=None; # test fit function for 1+1 - Eo
 testEn=None; # test fit function for 1+1 - En
 if not (kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "tslc":
    tslc = value;
   elif akey == "tfit":
    tfit = value;
   elif akey == "pfit":
    pfit = value;
   elif akey == "ls":
    ls = value;
   elif akey == "ls2":
    ls2 = value;
   elif akey == "mfc":
    mfc = value;
   elif akey == "mec":
    mec = value;
   elif akey == "color":
    color = value;
   elif akey == "color2":
    color2 = value;
   elif akey == "color3":
    color3 = value;
   elif akey == "marker":
    marker = value;
   elif akey == "ms":
    ms = value;
   elif akey == "xlim":
    xlim = value;
   elif akey == "ylim":
    ylim = value;
   elif akey == "testao":
    testao = value;
   elif akey == "testan":
    testan = value;
   elif akey == "testEo":
    testEo = value;
   elif akey == "testEn":
    testEn = value;
   elif akey == "erbaroff":
    ## -- turn errors off for fit functions in pure correlator plot
    erbaroff = True;
 ##endif kwargs

 ## -- set up fit 
 ## -- if test.. are defined, do a fake 1+1 parameter fit as well
 fit_func = create_fit_func(models,fit,len(tslc));
 fake_func=None;
 if not (testao is None or testan is None or testEo is None or testEn is None):
  fakefit = copy.deepcopy(fit);
  fakefit.transformed_p['ao']=[testao];
  fakefit.transformed_p['an']=[testan];
  fakefit.transformed_p['Eo']=[testEo];
  fakefit.transformed_p['En']=[testEn];
  fake_func = create_fit_func(models,fakefit,len(tslc));
 #
 if plot_type is "correlator":
  tfit = range(tfit[0],tfit[0]+len(tfit)*2-1);
  t_all = np.linspace(0.,len(tslc),49);
  gvfit_all = models[0].s[0]*fit_func(t_all);
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all);
  ax.plot(t_all,fit_mean,color=color2);
  try:
   erbaroff;
  except:
   ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2);
   ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2);
  ## -- see what the fit function would look like from 1+1 analysis
  if not (fake_func is None):
   gvfake_all = models[0].s[0]*fake_func(t_all);
   fake_mean = gv.mean(gvfake_all);
   fake_sdev = gv.sdev(gvfake_all);
   ax.plot(t_all,fake_mean,color=color3);
   try:
    erbaroff;
   except:
    ax.plot(t_all,fake_mean+fit_sdev,color=color3,ls=ls2);
    ax.plot(t_all,fake_mean-fit_sdev,color=color3,ls=ls2);
  #
  ## -- data
  dmean = models[0].s[0]*gv.mean(data[key]);
  dsdev = gv.sdev(data[key]);
  ax.errorbar(tslc,dmean,yerr=dsdev,ls=ls,mfc=mfc,mec=mec,color=color,marker=marker,ms=ms);
  ax.scatter(tfit,dmean[tfit[0:len(tfit)]],color=color,marker=marker,s=ms*ms);
  ax.scatter(tfit,dmean[tfit[0:len(tfit)]],color=color,marker=marker,s=ms*ms);
  #
  ## -- axis modifications
  kwargs2={};
  try:
   kwargs2['ylim']=ylim;
  except NameError:
   pass;
  axis_mods_correlator(fig,key,len(tslc),**kwargs2);
  #
 ## ------
 ##
 elif plot_type is "log_ratio":
  sep=df.sep; # timeslice separation between correlators in ratio
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-0.5-sep,100);
  try:
   gvfit_all = fit.transformed_p['E'][0]*np.ones(len(t_all));
  except KeyError:
   gvfit_all = fit.transformed_p['En'][0]*np.ones(len(t_all));
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all);
  ax.plot(t_all,fit_mean,color=color2);
  try:
   erbaroff;
  except:
   ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2);
   ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2);
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [ls.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]));
  rdat = gv.log([avdat[i]/avdat[i+sep] for i in range(len(avdat)-sep)])/sep;
  #
  dmean = gv.mean(rdat);
  dsdev = gv.sdev(rdat);
  #
  ax.errorbar(tslc[0:len(tslc)/2+1-sep],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms);
  ax.scatter(tfit[0:len(tfit)-sep],dmean[tfit[0:len(tfit)-sep]],color=color,marker=marker,s=ms*ms);
  #
  ## -- axis modifications
  kwargs2={};
  try:
   kwargs2['ylim']=ylim;
  except NameError:
   pass;
  axis_mods_log_ratio(fig,key,len(tslc),sep=sep,**kwargs2);
  #
 ## ------
 ##
 elif plot_type is "fit_normalized":
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-0.5,100);
  gvfit_all = fit_func(t_all);
  fit_norm = np.ones(len(t_all));
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all)/fit_mean;
  ax.plot(t_all,fit_norm,color=color2);
  ax.plot(t_all,fit_norm+fit_sdev,color=color2,ls=ls2);
  ax.plot(t_all,fit_norm-fit_sdev,color=color2,ls=ls2);
  if not (fake_func is None):
   ## -- see what the fit function would look like from 1+1 analysis
   gvfake_all = models[0].s[0]*fake_func(t_all);
   fake_mean = gv.mean(gvfake_all)/gv.mean(gvfit_all);
   fake_sdev = gv.sdev(gvfake_all)/gv.mean(gvfit_all);
   ax.plot(t_all,fake_mean,color=color3);
   ax.plot(t_all,fake_mean+fit_sdev,color=color3,ls=ls2);
   ax.plot(t_all,fake_mean-fit_sdev,color=color3,ls=ls2);
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]));
  tav =np.array(range(len(avdat)));
  ndat=avdat/gv.mean(fit_func(tav));
  #
  dmean = gv.mean(ndat);
  dsdev = gv.sdev(ndat);
  #
  ax.errorbar(tslc[0:len(tslc)/2+1],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms);
  ax.scatter(tfit,dmean[tfit],color=color,marker=marker,s=ms*ms);
  #
  ### -- axis modifications
  kwargs2={};
  try:
   kwargs2['ylim']=ylim;
  except NameError:
   pass;
  axis_mods_fit_normalized(fig,key,len(tslc),**kwargs2);
  #
 elif plot_type is "log_ratio2":
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-2.5,100);
  gvfit_all = fit.transformed_p['En'][0]*np.ones(len(t_all));
  ## -- 
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all);
  ax.plot(t_all,fit_mean,color=color2);
  ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2);
  ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2);
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]));
  ## --
  rdat = gv.log([avdat[i]/avdat[i+2] for i in range(len(avdat)-2)])/2;
  dmean = gv.mean(rdat);
  dsdev = gv.sdev(rdat);
  #
  ax.errorbar(tslc[0:len(tslc)/2+1-2],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms);
  ax.scatter(tfit[0:len(tfit)-2],dmean[tfit[0:len(tfit)-2]],color=color,marker=marker,s=ms*ms);
  if not(pfit is None):
   pavg = lsf.wavg(rdat[pfit]);
   pmean= pavg.mean*np.ones(len(pfit));
   psdev= pavg.sdev*np.ones(len(pfit));
   print "              Fit value for ",plot_type," plot: ",fit.transformed_p['En'][0];
   print "Wghtd avg plateau value for ",plot_type," plot: ",pavg;
   ax.scatter(pfit,dmean[pfit],color=color3,marker=marker,s=ms*ms);
   ax.plot(pfit,pmean,color=color3);
   ax.plot(pfit,pmean+psdev,color=color3,ls=ls2);
   ax.plot(pfit,pmean-psdev,color=color3,ls=ls2);
  #
  ## -- axis modifications
  kwargs2={};
  try:
   kwargs2['ylim']=ylim;
  except NameError:
   pass;
  axis_mods_log_ratio(fig,key,len(tslc),sep=2,**kwargs2);
  #
 ## ------
 ##
 elif plot_type is "log_ratio123":
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-2.5,100);
  gvfit_all = (fit.transformed_p['Eo'][0])*np.ones(len(t_all));
  ## -- 
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all);
  ax.plot(t_all,fit_mean,color=color2);
  ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2);
  ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2);
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]));
  ## --
  sep=1;
  sep2=2;
  sgn=-1;
  entmp=fit.transformed_p['En'][0];
  rdat = np.divide([np.power(-1,i)*
         ((avdat[i+sep]+sgn*avdat[i])
         -gv.exp(entmp)*(avdat[i+sep+1]+sgn*avdat[i+1]))
         for i in range(len(avdat)-sep-1)],
         models[0].s[1]);
  rpdat=np.divide(gv.log([rdat[i]/rdat[i+sep2] for i in range(len(rdat)-sep2)]),sep2);
  dmean = gv.mean(rpdat);
  dsdev = gv.sdev(rpdat);
  #
  ax.errorbar(tslc[0:len(tslc)/2-sep-sep2],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
   mec=mec,color=color,marker=marker,ms=ms);
  ax.scatter(tfit[0:len(tfit)-1-sep-sep2],dmean[tfit[0:len(tfit)-1-sep-sep2]],\
   color=color,marker=marker,s=ms*ms);
  if not(pfit is None):
   pavg = lsf.wavg(rpdat[pfit]);
   pmean= pavg.mean*np.ones(len(pfit));
   psdev= pavg.sdev*np.ones(len(pfit));
   print "              Fit value for ",plot_type," plot: ",fit.transformed_p['Eo'][0];
   print "Wghtd avg plateau value for ",plot_type," plot: ",pavg;
   ax.scatter(pfit,dmean[pfit],color=color3,marker=marker,s=ms*ms);
   ax.plot(pfit,pmean,color=color3);
   ax.plot(pfit,pmean+psdev,color=color3,ls=ls2);
   ax.plot(pfit,pmean-psdev,color=color3,ls=ls2);
  #
  ## -- axis modifications
  kwargs2={};
  try:
   kwargs2['ylim']=ylim;
  except NameError:
   pass;
  axis_mods_log_ratio123(fig,key,len(tslc),**kwargs2);
  #
 ## ------
 ##
 elif plot_type is "sum_odd" or \
      plot_type is "sum_even":
  eotag  ='Eo';
  entag  ='En';
  if plot_type is "sum_even":
   sep=1;
   #do_odd=0;
   atag  ='an';
   sgn=1;
  else:
   sep=1;
   #do_odd=1;
   atag  ='ao';
   sgn=-1;
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-2.5,100);
  gvfit_all = fit.transformed_p[atag][0]*\
              fit.transformed_p[atag][0]*np.ones(len(t_all));
  ## -- 
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all);
  ax.plot(t_all,fit_mean,color=color2);
  ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2);
  ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2);
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]));
  ## --
  entmp=fit.transformed_p[entag][0];
  eotmp=fit.transformed_p[eotag][0];
  if plot_type is "sum_even":
   ## -- this works for En0 < Eo0
   #rdat = [(gv.exp(entmp*i)
   #        /gv.exp(-entmp*sep)+sgn*1)
   #       *(avdat[i+sep]+sgn*avdat[i])*np.power(-1,do_odd*i) for i in range(len(avdat)-sep)];
   ## -- improved version
   rdat = np.divide([gv.exp(entmp*i)*
          ((avdat[i+sep]+sgn*avdat[i])
          +gv.exp(eotmp)*(avdat[i+sep+1]+sgn*avdat[i+1]))
          for i in range(len(avdat)-sep-1)],
          (models[0].s[0]*
          (gv.exp(-entmp*sep)+sgn*1)*
          (gv.exp(-entmp+eotmp)+1)));
  else:
   rdat = np.divide([np.power(-1,i)*gv.exp(eotmp*i)*
          ((avdat[i+sep]+sgn*avdat[i])
          -gv.exp(entmp)*(avdat[i+sep+1]+sgn*avdat[i+1]))
          for i in range(len(avdat)-sep-1)],
          (models[0].s[1]*
          (np.power(-1,sep)*gv.exp(-eotmp*sep)+sgn*1)*
          (gv.exp(-eotmp+entmp)+1)));
  dmean = gv.mean(rdat);
  dsdev = gv.sdev(rdat);
  #
  if plot_type is "sum_even":
   ax.errorbar(tslc[0:len(tslc)/2-sep],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
    mec=mec,color=color,marker=marker,ms=ms);
   ax.scatter(tfit[0:len(tfit)-sep-1],dmean[tfit[0:len(tfit)-sep-1]],\
    color=color,marker=marker,s=ms*ms);
  else:
   ax.errorbar(tslc[0:len(tslc)/2-sep],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
    mec=mec,color=color,marker=marker,ms=ms);
   ax.scatter(tfit[0:len(tfit)-sep-1],dmean[tfit[0:len(tfit)-sep-1]],\
    color=color,marker=marker,s=ms*ms);
  #
  if not(pfit is None):
   pavg = lsf.wavg(rdat[pfit]);
   pmean= pavg.mean*np.ones(len(pfit));
   psdev= pavg.sdev*np.ones(len(pfit));
   print "              Fit value for ",plot_type," plot: ",fit.transformed_p[atag][0];
   print "Wghtd avg plateau value for ",plot_type," plot: ",gv.sqrt(pavg);
   ax.scatter(pfit,dmean[pfit],color=color3,marker=marker,s=ms*ms);
   ax.plot(pfit,pmean,color=color3);
   ax.plot(pfit,pmean+psdev,color=color3,ls=ls2);
   ax.plot(pfit,pmean-psdev,color=color3,ls=ls2);
  #
  ## -- axis modifications
  kwargs2={};
  kwargs2['plot_type']=plot_type;
  try:
   kwargs2['ylim']=ylim;
  except NameError:
   pass;
  axis_mods_sum(fig,key,len(tslc),sep=sep,sgn=sgn,**kwargs2);
  #
 ## ------
 ##
 elif plot_type is "simple_sum_odd" or \
      plot_type is "simple_sum_even":
  eotag  ='Eo';
  entag  ='En';
  sep=1;
  if plot_type is "simple_sum_even":
   atag  ='an';
   sgn=1;
  else:
   atag  ='ao';
   sgn=-1;
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-2.5,100);
  gvfit_all = fit.transformed_p[atag][0]*\
              fit.transformed_p[atag][0]*np.ones(len(t_all));
  ## -- 
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all);
  ax.plot(t_all,fit_mean,color=color2);
  ax.plot(t_all,fit_mean+fit_sdev,color=color2,ls=ls2);
  ax.plot(t_all,fit_mean-fit_sdev,color=color2,ls=ls2);
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [lsf.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]));
  ## --
  entmp=fit.transformed_p[entag][0];
  eotmp=fit.transformed_p[eotag][0];
  #
  if plot_type is "simple_sum_even":
   rdat = np.divide([gv.exp(entmp*i)*(gv.exp(entmp*sep)*avdat[i+sep]+sgn*avdat[i])
          for i in range(len(avdat)-sep)],
          (models[0].s[0]*2.));
  else:
   rdat = np.divide([np.power(-1,i)*gv.exp(eotmp*i)*
          (gv.exp(entmp*sep)*avdat[i+sep]+sgn*avdat[i])
          for i in range(len(avdat)-sep)],
          (models[0].s[1])*
          (-gv.exp(-eotmp+entmp)-1));
  dmean = gv.mean(rdat);
  dsdev = gv.sdev(rdat);
  #
  if plot_type is "simple_sum_even":
   ax.errorbar(tslc[0:len(tslc)/2-sep+1],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
    mec=mec,color=color,marker=marker,ms=ms);
   ax.scatter(tfit[0:len(tfit)-sep],dmean[tfit[0:len(tfit)-sep]],\
    color=color,marker=marker,s=ms*ms);
  else:
   ax.errorbar(tslc[0:len(tslc)/2-sep+1],dmean,yerr=dsdev,ls=ls,mfc=mfc,\
    mec=mec,color=color,marker=marker,ms=ms);
   ax.scatter(tfit[0:len(tfit)-sep],dmean[tfit[0:len(tfit)-sep]],\
    color=color,marker=marker,s=ms*ms);
  if not(pfit is None):
   pavg = lsf.wavg(rdat[pfit]);
   pmean= pavg.mean*np.ones(len(pfit));
   psdev= pavg.sdev*np.ones(len(pfit));
   print "              Fit value for ",plot_type," plot: ",fit.transformed_p[atag][0];
   print "Wghtd avg plateau value for ",plot_type," plot: ",gv.sqrt(pavg);
   ax.scatter(pfit,dmean[pfit],color=color3,marker=marker,s=ms*ms);
   ax.plot(pfit,pmean,color=color3);
   ax.plot(pfit,pmean+psdev,color=color3,ls=ls2);
   ax.plot(pfit,pmean-psdev,color=color3,ls=ls2);
  #
  ## -- axis modifications
  kwargs2={};
  kwargs2['plot_type']=plot_type;
  try:
   kwargs2['ylim']=ylim;
  except NameError:
   pass;
  axis_mods_simple_sum(fig,key,len(tslc),sep=sep,sgn=sgn,**kwargs2);
  #
 else:
  print "Not a valid plot type";
  return;
## ------
##

def axis_mods_correlator(fig,key,tmax=None,**kwargs):
 fontsize=20;
 if not tmax is None:
  xlim=[-1,tmax+1];
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value;
   elif akey == "ylim":
    ylim = value;
   elif akey == "fontsize":
    fontsize = value;
 ##endif kwargs
 #
 ax   =fig.gca();
 rect =fig.patch;
 fig.suptitle(key+r' $\pi$ 2-pt Function',fontsize=fontsize);
 ax.set_xlabel(r'$t$ slice');
 ax.set_ylabel(r'$C_\pi(t)$');
 if not tmax is None:
  ax.set_xlim(xlim);
 try:
  ax.set_ylim(ylim);
 except NameError:
  pass;
 ax.set_yscale('log');
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize); # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white');
## ------

def axis_mods_log_ratio(fig,key,tmax=None,sep=1,**kwargs):
 fontsize=20;
 if not tmax is None:
  xlim=[-1,tmax/2+1-sep];
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value;
   elif akey == "ylim":
    ylim = value;
   elif akey == "fontsize":
    fontsize = value;
 ##endif kwargs
 #
 ax   =fig.gca();
 rect =fig.patch;
 fig.suptitle(key+r' $\pi$ 2-pt Log Ratio',fontsize=fontsize);
 ax.set_xlabel(r'$t$ slice');
 if sep > 1:
  ax.set_ylabel(r'$-log(C_\pi(t+'+str(sep)+r'a) / C_\pi(t))$');
 else:
  ax.set_ylabel(r'$-log(C_\pi(t+a) / C_\pi(t))$');
 if not tmax is None:
  ax.set_xlim(xlim);
 try:
  ax.set_ylim(ylim);
 except NameError:
  pass;
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize); # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white');
## ------

def axis_mods_fit_normalized(fig,key,tmax=None,**kwargs):
 fontsize=20;
 if not tmax is None:
  xlim=[-1,tmax/2+1];
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value;
   elif akey == "ylim":
    ylim = value;
   elif akey == "fontsize":
    fontsize = value;
 ##endif kwargs
 #
 ax   =fig.gca();
 rect =fig.patch;
 fig.suptitle(key+r' $\pi$ 2-pt Fit-Normalized',fontsize=fontsize);
 ax.set_xlabel(r'$t$ slice');
 ax.set_ylabel(r'$C_\pi(t)/C_\pi$ fit');
 if not tmax is None:
  ax.set_xlim(xlim);
 try:
  ax.set_ylim(ylim);
 except NameError:
  pass;
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize); # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white');
## ------

def axis_mods_log_ratio123(fig,key,tmax=None,sep=1,**kwargs):
 fontsize=20;
 if not tmax is None:
  xlim=[-1,tmax/2+1-sep];
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value;
   elif akey == "ylim":
    ylim = value;
   elif akey == "fontsize":
    fontsize = value;
 ##endif kwargs
 #
 ax   =fig.gca();
 rect =fig.patch;
 fig.suptitle(key+r' $\pi$ 2-pt Log Sum-Ratio',fontsize=fontsize);
 ax.set_xlabel(r'$t$ slice');
 #ax.set_ylabel(r'$log[(-1)^{t+1} log[\frac{C_\pi(t+1a) C_\pi(t+2a)}{C_\pi(t) C_\pi(t+3a)}]]$');
 ax.set_ylabel('-log[ratio of sums]');
 if not tmax is None:
  ax.set_xlim(xlim);
 try:
  ax.set_ylim(ylim);
 except NameError:
  pass;
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize); # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white');
## ------

def axis_mods_sum(fig,key,tmax=None,sep=1,sgn=1,**kwargs):
 if sgn == 1:
  sgnstr='+';
 else:
  sgnstr='-';
 fontsize=20;
 plot_type="sum_even";
 if not tmax is None:
  xlim=[-1,tmax/2+1-sep];
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value;
   elif akey == "ylim":
    ylim = value;
   elif akey == "fontsize":
    fontsize = value;
   elif akey == "plot_type":
    plot_type = value;
 ##endif kwargs
 #
 ax   =fig.gca();
 rect =fig.patch;
 if plot_type is "sum_even":
  fig.suptitle(key+r' $\pi$ 2-pt Normalized Correlator Sum (Even)',fontsize=fontsize);
 else: 
  fig.suptitle(key+r' $\pi$ 2-pt Normalized Correlator Sum (Odd)',fontsize=fontsize);
 ax.set_xlabel(r'$t$ slice');
 ax.set_ylabel('Normalized Correlator Sum');
 if not tmax is None:
  ax.set_xlim(xlim);
 try:
  ax.set_ylim(ylim);
 except NameError:
  pass;
 ax.set_yscale('log');
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize); # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white');
## ------

def axis_mods_simple_sum(fig,key,tmax=None,sep=1,sgn=1,**kwargs):
 if sgn == 1:
  sgnstr='+';
 else:
  sgnstr='-';
 fontsize=20;
 plot_type="simple_sum_even";
 if not tmax is None:
  xlim=[-1,tmax/2+1-sep];
 if not(kwargs is None):
  for akey,value in kwargs.iteritems():
   if   akey == "xlim":
    xlim = value;
   elif akey == "ylim":
    ylim = value;
   elif akey == "fontsize":
    fontsize = value;
   elif akey == "plot_type":
    plot_type = value;
 ##endif kwargs
 #
 ax   =fig.gca();
 rect =fig.patch;
 if plot_type is "simple_sum_even":
  fig.suptitle(key+r' $\pi$ 2-pt Simple Correlator Sum (Even)',fontsize=fontsize);
 else: 
  fig.suptitle(key+r' $\pi$ 2-pt Simple Correlator Sum (Odd)',fontsize=fontsize);
 ax.set_xlabel(r'$t$ slice');
 if sep > 1:
  if plot_type is "simple_sum_even":
   ax.set_ylabel(r'$[C_\pi(t)'+sgnstr+r'C_\pi(t+'+str(sep)+r'a)e^{+E'+str(sep)+r'a}]e^{+Et}/2$');
  else:
   ax.set_ylabel(r'$[C_\pi(t)'+sgnstr+r'C_\pi(t+'+str(sep)+r'a)e^{+E'+str(sep)+r'a}]'\
    +r'(-1)^{t}e^{+Et}/(-e^{-(F-E)a}-1)$');
 else:
  if plot_type is "simple_sum_even":
   ax.set_ylabel(r'$[C_\pi(t)'+sgnstr+r'C_\pi(t+a)e^{+En a}]e^{+En t}/2$');
  else:
   ax.set_ylabel(r'$[C_\pi(t)'+sgnstr+r'C_\pi(t+a)e^{+En a}](-1)^{t}e^{+En t}\frac{1}'\
    +r'{(-e^{-(Eo-En)a}-1)}$');
 if not tmax is None:
  ax.set_xlim(xlim);
 try:
  ax.set_ylim(ylim);
 except NameError:
  pass;
 ax.set_yscale('log');
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(fontsize); # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white');
## ------

def create_fit_func(models,fit,tmax=0):
 ## -- get a/b key information from models[index].a, etc...
 #
 lparm=fit.transformed_p;
 #
 try: # vanilla
  a =gv.mean(ut.sqr_arr(lparm['a']));
  E =gv.mean(ut.sum_dE(lparm['E']));
  def new_func(t):
   return models[0].s*np.dot(a,[gv.exp(-E[i]*t)+gv.exp(-E[i]*(tmax-t)) for i in range(len(E))]);
  return new_func;
 #
 except KeyError:
  pass;
 #
 try: # even
  an =ut.sqr_arr(lparm['an']);
  En =ut.sum_dE(lparm['En']);
  #
  try: # even+odd
   ao =ut.sqr_arr(lparm['ao']);
   Eo =ut.sum_dE(lparm['Eo']);
   def new_func(t):
    return models[0].s[0]*\
           np.dot(an,[gv.exp(-En[i]*t)+gv.exp(-En[i]*(tmax-t)) for i in range(len(En))])\
         + models[0].s[1]* np.dot(ao,[gv.cos(t*np.pi)*\
          (gv.exp(-Eo[i]*t)+gv.exp(-Eo[i]*(tmax-t)))\
           for i in range(len(Eo))]);
   return new_func;
  #
  except KeyError: # even only
   def new_func(t):
    return models[0].s[0]*\
           np.dot(an,[gv.exp(-En[i]*t)+gv.exp(-En[i]*(tmax-t)) for i in range(len(En))]);
   return new_func;
 #
 except KeyError: # even did not work
  #
  try: # odd only
   ao =gv.mean(ut.sqr_arr(lparm['ao']));
   Eo =gv.mean(ut.sum_dE(lparm['Eo']));
   def new_func(t):
    return models[0].s*np.dot(ao,[gv.cos(t*np.pi)*\
          (gv.exp(-Eo[i]*t)+gv.exp(-Eo[i]*(tmax-t)))\
           for i in range(len(Eo))]);
   return new_func;
  #
  except KeyError: # nothing worked
   pass;
 print "No fit function generated";
 return None;
