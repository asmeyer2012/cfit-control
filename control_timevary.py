from corrfitter           import CorrFitter
from make_data            import make_data
from make_data_db         import make_data_db
from make_models          import make_models
from make_prior           import make_prior
from make_bootstrap       import make_bootstrap
from multiprocessing      import Pool
from print_results        import print_fit
from print_results        import print_error_budget
from save_data            import save_data
from save_prior           import save_prior_from_fit
from plot_corr_double_log import plot_corr_double_log
from plot_corr_normalized import plot_corr_normalized
from meta_data            import *
import defines           as df
import define_prior      as dfp
import gvar              as gv
import gvar.dataset      as gvd
#import importlib         as impl ## -- import with variable name
import matplotlib.pyplot as plt
import numpy             as np
#import shutil            as shil ## -- copy files
import util_funcs        as utf

doParallel=True
maxProcesses=6

if df.do_db:
 ## -- for database input
 ##    - (database file name defined in make_data_db.py)
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,do_db=True)
 #models = make_models(data=data,lkey=df.lkey) ## -- make models in loop
else:
 ## -- for raw correlator file input
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,\
                       do_db=False,filename="./import-correlators")
## --
mdef = df.define_model

def doProcess(tmin,tmax,data=data,mdef=mdef):
  ## -- do a single fit ... set up for parallelizing
  for key in data:
    mdef[key]['tfit'] = range(tmin,tmax)
  models = make_models(data=data,lkey=df.lkey,mdef=mdef)
  pdict0 = utf.get_prior_dict(df.define_prior,
   df.define_prior['nkey'],df.define_prior['okey'],df.num_nst,df.num_ost)
  prior = make_prior(models,prior_dict=pdict0,nst=df.num_nst,ost=df.num_ost)
  fitter = CorrFitter(models=models,maxit=df.maxit)
  #try: ## -- if catching value error, just exit
  ## -- p0 = initial values (dictionary)
  if df.do_initial:
   try:
    p0={}
    for key in df.define_init:
     if key[-1] == 'o':
      p0[key] = df.define_init[key][:df.num_ost]
     else:
      p0[key] = df.define_init[key][:df.num_nst]
    fit = fitter.lsqfit(data=data,prior=prior,p0=p0,svdcut=df.svdcut)
   except KeyError:
    print "Could not use initial point definitions"
    fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
  else:
   fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
  ## --
  print_fit(fit,prior)
  print_error_budget(fit)
  save_data('fittmvr/fit_'+str(tmin)+'_'+str(tmax)+'.out',fit,data)
  #save_prior_from_fit(pdict0,df.define_model,fit,'prior/prior_'+str(nst)+'_'+str(ost)+'.out',
  #  round_e=2,round_a=1,preserve_e_widths=True,preserve_a_widths=True)
  #except ValueError:
  # print "Caught value error for ",nst," ",ost

if __name__ == '__main__' and doParallel:
 pool= Pool(processes=maxProcesses)
 for tmax in df.tmvr_tmax:
  for tmin in range(1,tmax):
   pool.apply_async(doProcess,args=(tmin,tmax))
 pool.close()
 pool.join()
elif not(doParallel):
 for tmax in df.tmvr_tmax:
  for tmin in range(1,tmax):
   doProcess(nst,ost)
