import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import lsqfit as ls
import util_funcs as ut
import defines as df

def make_plot(models,data,fit):
 #key='G00';
 key=models[0].datatag;
 fig1 = plt.figure();
 plot_correlator(models,data,fit,fig1,key,"correlator");
 #fig2 = plt.figure();
 #plot_correlator(models,data,fit,fig2,key,"log_ratio");
 fig3 = plt.figure();
 plot_correlator(models,data,fit,fig3,key,"fit_normalized");
 plt.show();

def plot_correlator(models,data,fit,fig,key,plot_type):
 ## -- use data to make plots
 ## -- all data points shown with error bars
 ## -- points used in fit are filled in, others are not
 #

 ## -- determine index of models to use
 curr_mod=models[models[0].all_datatags.index(key)];

 ## -- use models to determine fit ranges, etc
 tslc = curr_mod.tdata;
 tfit = curr_mod.tfit;

 ## -- set up figure objects
 ax  = fig.gca()
 rect= fig.patch;

 ## -- options used in all fits
 ms=6.0; # marker size

 ## -- set up fit 
 fit_func = create_fit_func(models,fit,len(tslc));
 #
 if plot_type is "correlator":
  ## -- fix tfit
  tfit = range(tfit[0],tfit[0]+len(tfit)*2-1);
  ## -- fit
  t_all = np.linspace(0.,len(tslc),49);
  gvfit_all = models[0].s[0]*fit_func(t_all);
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all);
  ax.plot(t_all,fit_mean,color='b');
  #ax.plot(t_all,fit_mean+fit_sdev,color='b',ls='--');
  #ax.plot(t_all,fit_mean-fit_sdev,color='b',ls='--');
  #
  ## -- data
  dmean = models[0].s[0]*gv.mean(data[key]);
  dsdev = gv.sdev(data[key]);
  ax.errorbar(tslc,dmean,yerr=dsdev,ls='None',mfc='None',mec='k',color='r',marker='o',ms=ms);
  ax.scatter(tfit,dmean[tfit[0:len(tfit)]],color='r',marker='o',s=ms*ms);
  #
  ## -- axis modifications
  axis_mods_correlator(fig,key,len(tslc));
  #
 elif plot_type is "log_ratio":
  #df.sep=1; # timeslice separation between correlators in ratio
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-0.5-df.sep,100);
  try:
   gvfit_all = fit.transformed_p['E'][0]*np.ones(len(t_all));
  except KeyError:
   gvfit_all = fit.transformed_p['En'][0]*np.ones(len(t_all));
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all);
  ax.plot(t_all,fit_mean,color='b');
  ax.plot(t_all,fit_mean+fit_sdev,color='b',ls='--');
  ax.plot(t_all,fit_mean-fit_sdev,color='b',ls='--');
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [ls.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]));
  #rdat = gv.log([avdat[i]/avdat[i+1] for i in range(len(avdat)-1)]);
  rdat = gv.log([avdat[i]/avdat[i+df.sep] for i in range(len(avdat)-df.sep)])/df.sep;
  #
  dmean = gv.mean(rdat);
  dsdev = gv.sdev(rdat);
  #
  ax.errorbar(tslc[0:len(tslc)/2+1-df.sep],dmean,yerr=dsdev,ls='None',mfc='None',\
   mec='k',color='r',marker='o',ms=ms);
  ax.scatter(tfit[0:len(tfit)-df.sep],dmean[tfit[0:len(tfit)-df.sep]],color='r',marker='o',s=ms*ms);
  #
  ## -- axis modifications
  axis_mods_log_ratio(fig,key,len(tslc),sep=df.sep);
  #
 elif plot_type is "fit_normalized":
  ## -- fit
  t_all = np.linspace(0.5,len(tslc)/2-0.5,100);
  gvfit_all = fit_func(t_all);
  fit_norm = np.ones(len(t_all));
  fit_mean = gv.mean(gvfit_all);
  fit_sdev = gv.sdev(gvfit_all)/fit_mean;
  ax.plot(t_all,fit_norm,color='b');
  ax.plot(t_all,fit_norm+fit_sdev,color='b',ls='--');
  ax.plot(t_all,fit_norm-fit_sdev,color='b',ls='--');
  #
  ## -- data
  avdat = np.concatenate(([data[key][0]],\
   [ls.wavg([data[key][i],data[key][len(data[key])-i]])\
   for i in range(1,len(data[key])/2)],[data[key][len(data[key])/2]]));
  tav =np.array(range(len(avdat)));
  ndat=avdat/gv.mean(fit_func(tav));
  #
  dmean = gv.mean(ndat);
  dsdev = gv.sdev(ndat);
  #
  ax.errorbar(tslc[0:len(tslc)/2+1],dmean,yerr=dsdev,ls='None',mfc='None',\
   mec='k',color='r',marker='o',ms=ms);
  ax.scatter(tfit,dmean[tfit],color='r',marker='o',s=ms*ms);
  #
  ### -- axis modifications
  axis_mods_fit_normalized(fig,key,len(tslc));
  #
 else:
  print "Not a valid plot type";
  return;
## ------

def axis_mods_correlator(fig,key,tmax=None):
 ax   =fig.gca();
 rect =fig.patch;
 fig.suptitle(key+r' $\pi$ 2-pt Function',fontsize=20);
 ax.set_xlabel(r'$t$ slice');
 ax.set_ylabel(r'$C_\pi(t)$');
 if not tmax is None:
  ax.set_xlim([-1,tmax+1]);
 #ax.set_ylim([1e-4,1e-1]);
 ax.set_yscale('log');
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(20); # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white');
## ------

def axis_mods_log_ratio(fig,key,tmax=None,sep=1):
 ax   =fig.gca();
 rect =fig.patch;
 fig.suptitle(key+r' $\pi$ 2-pt Log Ratio',fontsize=20);
 ax.set_xlabel(r'$t$ slice');
 if sep > 1:
  ax.set_ylabel(r'$-log(C_\pi(t+'+str(sep)+r'a) / C_\pi(t))$');
 else:
  ax.set_ylabel(r'$-log(C_\pi(t+a) / C_\pi(t))$');
 if not tmax is None:
  ax.set_xlim([-1,tmax/2+1-sep]);
 #ax.set_ylim([1e-4,1e-1]);
 ax.set_ylim([-1,1]);
 #ax.set_yscale('log');
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(20); # must be after setting label content (LaTeX ruins it)
 rect.set_facecolor('white');
## ------

def axis_mods_fit_normalized(fig,key,tmax=None):
 ax   =fig.gca();
 rect =fig.patch;
 fig.suptitle(key+r' $\pi$ 2-pt Fit-Normalized',fontsize=20);
 ax.set_xlabel(r'$t$ slice');
 ax.set_ylabel(r'$C_\pi(t)/$'+key+' fit');
 if not tmax is None:
  ax.set_xlim([-1,tmax/2+1]);
 #ax.set_ylim([0.95,1.05]);
 #ax.set_ylim([0.7,1.3]);
 ax.set_ylim([0,2]);
 #ax.set_ylim([-2,4]);
 #ax.set_yscale('log');
 for item in ([ax.xaxis.label,ax.yaxis.label]):
  item.set_fontsize(20); # must be after setting label content (LaTeX ruins it)
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
