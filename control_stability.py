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
 models = make_models(data=data,lkey=df.lkey)
else:
 ## -- for raw correlator file input
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,\
                       do_db=False,filename="./import-correlators")
 models = make_models(data=data,lkey=df.lkey)
## --

def doProcess(nst,ost,data=data,models=models):
  ## -- do a single fit ... set up for parallelizing
  pdict0 = utf.get_prior_dict(dfp.define_prior,
   dfp.define_prior['nkey'],dfp.define_prior['okey'],nst,ost)
  prior = make_prior(models,prior_dict=pdict0,nst=nst,ost=ost)
  fitter = CorrFitter(models=models,maxit=df.maxit)
  #try: ## -- if catching value error, just exit
  ## -- p0 = initial values (dictionary)
  if df.do_initial:
   try:
    p0={}
    for key in dfp.define_init:
     if key[-1] == 'o':
      p0[key] = dfp.define_init[key][:df.num_ost]
     else:
      p0[key] = dfp.define_init[key][:df.num_nst]
    fit = fitter.lsqfit(data=data,prior=prior,p0=p0,svdcut=df.svdcut)
   except KeyError:
    print "Could not use initial point definitions"
    fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
  else:
   fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
  ## --
  print_fit(fit,prior)
  print_error_budget(fit)
  save_data('fit/fit_'+str(nst)+'_'+str(ost)+'.out',fit,data)
  #save_prior_from_fit(pdict0,df.define_model,fit,'prior/prior_'+str(nst)+'_'+str(ost)+'.out',
  #  round_e=2,round_a=1,preserve_e_widths=True,preserve_a_widths=True)
  #except ValueError:
  # print "Caught value error for ",nst," ",ost

min_nst=df.stab_min_nst
mid_nst=df.stab_mid_nst
max_nst=df.stab_max_nst
min_ost=df.stab_min_ost
mid_ost=df.stab_mid_ost
max_ost=df.stab_max_ost

if __name__ == '__main__' and doParallel:
 pool= Pool(processes=maxProcesses)
 for ost in range(min_ost,max_ost):
  for nst in range(min_nst,max_nst):
   if nst+ost>df.stab_max_states:
    continue
   if nst<mid_nst and ost<mid_ost:
    continue
   pool.apply_async(doProcess,args=(nst,ost))
 pool.close()
 pool.join()
elif not(doParallel):
 for ost in range(min_ost,max_ost):
  for nst in range(min_nst,max_nst):
   if nst+ost>df.stab_max_states:
    continue
   if nst<mid_nst and ost<mid_ost:
    continue
   doProcess(nst,ost)
