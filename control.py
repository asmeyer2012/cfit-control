from corrfitter               import CorrFitter
from extract_3pt_info         import *
from make_data                import make_data
from make_data_db             import make_data_db
from make_models              import make_models
#from make_models              import *
from make_prior               import make_prior
from make_bootstrap           import make_bootstrap
from print_results            import print_fit
from print_results            import print_error_budget
from save_data                import save_data
from save_prior               import save_prior_from_fit
from make_plot                import make_plot
from make_plot                import make_plot_corr_neg
from make_plot                import make_plot_1plus1
from plot_corr_double_log     import plot_corr_double_log
from plot_corr_effective_mass import plot_corr_effective_mass
from plot_corr_normalized     import plot_corr_normalized
from meta_data                import *
from util_files               import read_fit_file
import defines           as df
import define_prior      as dfp
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np
import sys

if df.do_db:
 ## -- for database input
 ##    - (database file name defined in make_data_db.py)
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,do_db=True)
 models = make_models(data=data,lkey=df.lkey)
 prior = make_prior(models)
else:
 ## -- for raw correlator file input
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,\
                       do_db=False,filename="./import-correlators-bar2pt")
 data3,dset3 = make_data(df.mdp,do_makedata=df.do_makedata_3pt,\
                         do_db=False,filename="./import-correlators-bar3pt")
 models = make_models(data=data,lkey=df.lkey)
 prior = make_prior(models)
## --

## -- DEPRICATED
#if df.do_uncorr:
# ## -- remove the correlations from the data
# dataCorr = data
# datlen = len(gv.evalcov(data)['Gaa','Gaa'])
# fakecov = np.zeros((datlen,datlen))
# for i in range(datlen):
#  fakecov[i,i] = np.diag(gv.evalcov(data)['Gaa','Gaa'])[i]
# data['Gaa'] = gv.gvar([data['Gaa'][i].mean for i in range(datlen)],np.array(fakecov))
## --

fitter = CorrFitter(models=models,maxit=df.maxit)
#fit = fitter.chained_lsqfit(data=data, prior=prior)
#fit = fitter.lsqfit(data=data, prior=fit.p)
#fit = fitter.lsqfit(data=data,prior=prior,p0="test.init.out",svdcut=df.svdcut)
if df.do_2pt:
  if df.do_initial:
   try:
    p0={}
    for key in df.define_init:
     eokey = utf.get_evenodd(key)
     if eokey == 'o':
      p0[key] = df.define_init[key][:df.num_ost]
     else:
      p0[key] = df.define_init[key][:df.num_nst]
    fit = fitter.lsqfit(data=data,prior=prior,p0=p0,svdcut=df.svdcut)
   except KeyError:
    print "Could not use initial point definitions"
    fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
  else:
   fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
  #bs_avg = make_bootstrap(fitter,dset,df.mdp.n_bs)
  print_fit(fit,prior)
  print_error_budget(fit)
  #save_data(mdp.output_path +'/'+ mdp.fit_fname,fit,data)
  save_data('./test.fit.out',fit,data)
  save_prior_from_fit(df.define_prior,df.define_model,fit,"test.prior.out",
    round_e=2,round_a=1,preserve_e_widths=True,preserve_a_widths=True)
  
  if df.do_plot:
   if df.do_default_plot:
    fitter.display_plots()
   plot_corr_double_log(models,data,fit,**df.fitargs)
   plot_corr_normalized(models,data,fit,**df.fitargs)
   plt.show()
pass #do_2pt

if df.do_3pt:
  ## -- test routines
  if df.do_symm == "s":
    if df.do_irrep == "8":
     classList = [1,2,3,5,6]
    elif df.do_irrep == "8'":
     classList = [4,7]
    elif df.do_irrep == "16":
     classList = [2,3,4,6]
  elif df.do_sym == "m":
    print "not set up for mixed symmetry yet!"
    raise ValueError # set up class list for mixed symmetry
    if df.do_irrep == "8":
     classList = [1,2,3,5,6]
    elif df.do_irrep == "8'":
     classList = [4,7]
    elif df.do_irrep == "16":
     classList = [2,3,4,6]
  
  testpre = 's'
  testpost= ''
  #testdat = np.array(
  # [[data[testpre+'44'+testpost],data[testpre+'47'+testpost]],
  #  [data[testpre+'74'+testpost],data[testpre+'77'+testpost]]])
  #testdenom = np.array(
  # [[extract_2pt_val(data,'G44',8),extract_2pt_val(data,'G47',8)],
  #  [extract_2pt_val(data,'G74',8),extract_2pt_val(data,'G77',8)]])
  testdat = list()
  for c in classList:
   testdat.append([data[testpre+str(c)+str(k)+testpost] for k in classList])
  testdat = np.array(testdat)
  [cmat,kmat] = extract_3pt_cov(fit)
  diagdat = diagonalize_correlator(testdat,cmat,kmat)
  
  testpre3 = 'v4v4'
  #testpre3 = 'azaz'
  testpost3= 't6'
  #testdat3 = np.array(
  # [[data[testpre3+'44'+testpost3],data[testpre3+'47'+testpost3]],
  #  [data[testpre3+'74'+testpost3],data[testpre3+'77'+testpost3]]])
  testdat3 = list()
  for c in classList:
   testdat3.append([data[testpre3+str(c)+str(k)+testpost3] for k in classList])
  testdat3 = np.array(testdat3)
  diag3pt = diagonalize_correlator(testdat3,cmat,kmat)
  
  markList = ['o','s','p','h','*','v','^','D','+','x']
  colorList = ['r','g','b','c','y','m','#115533','#552888','#ef5500','#218386','#404040']
  tsep = 6
  nameTagPre = 'test'
  
  xgv = list()
  for j in range(len(diag3pt)):
   xgv.append(diag3pt[j,j])
  #xgv = diag3pt
  
  ## -- plot diagonal
  fig = plt.figure(facecolor='white')
  plt.subplots_adjust(bottom=0.12,left=0.12,right=0.85,top=0.97)
  ax = fig.gca()
  handles = []
  labels = []
  i=-1
  for j in range(len(diag3pt)):
   #if key[4] != STIdx:
   # continue
   #print key,len(rdat[key]),STsum[key[4]]
   i=i+1
   handles.append(
    ax.errorbar(
    [x+2.*(i-len(diag3pt)/2.)/(3.*len(diag3pt)) for x in range(tsep+1)],
     #[x.mean for x in xgv[:tsep+1]],
     [x.mean/xgv[j][tsep/2].mean for x in xgv[j][:tsep+1]],
    yerr=[x.sdev/xgv[j][tsep/2].mean for x in xgv[j][:tsep+1]],
    linestyle='',
    markersize=2,
    capsize=1,
    elinewidth=1,
    linewidth=0.3,
    mfc=colorList[i%len(colorList)],
    color=colorList[i%len(colorList)],
    marker=markList[i%len(markList)]#,
    #label=str(key[1])+str(key[2])+str(key[3])+'-'+key[4]
    )
   )
   #labels.append(str(key[1])+str(key[2])+str(key[3])+'-'+key[4])
   labels.append('State '+str(j)+' '+testpre3)
  pass
  ax.set_xlabel(r'$\tau$ ',fontsize=15)
  plt.ylabel('y').set_rotation(0) # rotation of y axis label
  ax.set_ylabel(r'$\frac{Cij(\tau,'+str(tsep)+')}{Cij('+str(tsep/2)+','+str(tsep)+')}$',fontsize=15)
  ax.xaxis.labelpad = 10 # vertical alignment of x axis label
  ax.yaxis.labelpad = 15 # horizontal alignment of y axis label
  ax.set_xlim(-.5,tsep+.5)
  ax.set_ylim(-3,3)
  plt.legend(handles,labels,fontsize=4,numpoints=1,bbox_to_anchor=(1.001,1),loc=2,borderaxespad=0.,frameon=False)
  plt.axhline(0,color='k')
  plt.xticks(range(0,tsep+1),fontsize=10)
  plt.yticks(range(-3,4),fontsize=10)
  #plt.get_current_fig_manager().full_screen_toggle() ## full screen, not maximized
  mng = plt.get_current_fig_manager()
  mng.resize(*mng.window.maxsize())
  fig.set_size_inches(8,5)
  fig.savefig('/home/asm58/dump3pt/'+nameTagPre+'.s'+df.do_irrep+'.'+testpre3+'.diag3pt.pdf',dpi=400)
pass #do_3pt
