from corrfitter           import CorrFitter
from make_data            import make_data
from make_data_db         import make_data_db
from make_models          import make_models
from make_prior           import make_prior
from make_bootstrap       import make_bootstrap
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

min_nst=3
max_nst=10
min_ost=3
max_ost=10
fit_collector = {}
for ost in range(min_ost,max_ost):
 for nst in range(min_nst,max_nst):
  #dfp = impl.import_module('prior_'+str(nst)+'_'+str(ost))
  pdict0 = utf.get_prior_dict(dfp.define_prior,
   dfp.define_prior['nkey'],dfp.define_prior['okey'],nst,ost)
  prior = make_prior(models,prior_dict=pdict0,nst=nst,ost=ost)
  fitter = CorrFitter(models=models,maxit=df.maxit)
  try:
   fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut) #p0 = initial values (dictionary)
  except ValueError:
   if ost < nst:
    break ## -- go to next ost
   else:
    continue
  print_fit(fit,prior)
  print_error_budget(fit)
  save_data('fit/fit_'+str(nst)+'_'+str(ost)+'.out',fit,data)
  #save_prior_from_fit(pdict0,df.define_model,fit,'prior/prior_'+str(nst)+'_'+str(ost)+'.out',
  #  round_e=2,round_a=1,preserve_e_widths=True,preserve_a_widths=True)
  fit_collector[nst,ost,'fit'] = fit
  fit_collector[nst,ost,'prior'] = prior

