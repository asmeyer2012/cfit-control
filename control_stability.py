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
import gvar              as gv
import gvar.dataset      as gvd
import importlib         as impl ## -- import with variable name
import matplotlib.pyplot as plt
import numpy             as np
import shutil            as shil ## -- copy files

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

def new_state_n(emean,esdev):
 return 'utf.append_prior_state(define_prior,nkey,\ngv.gvar(\n[' +\
   str(emean) + ',0,0,0,0,0],\n[' + str(esdev) + ',10,10,10,10,10]))\n'

def new_state_o(emean,esdev): 
 return 'utf.append_prior_state(define_prior,okey,\ngv.gvar(\n[' +\
   str(emean) + ',0,0,0,0,0],\n[' + str(esdev) + ',10,10,10,10,10]))\n'

max_nst=10
max_ost=10
fit_collector = {}
for ost in range(1,max_ost):
 for nst in range(1,max_nst):
  dfp = impl.import_module('prior_'+str(nst)+'_'+str(ost))
  pdict0 = dfp.define_prior
  prior = make_prior(models,prior_dict=pdict0)
  fitter = CorrFitter(models=models,maxit=2000)
  try:
   fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
  except ValueError:
   if ost < nst:
    break ## -- go to next ost
   elif nst < ost:
    ## -- generate next prior file and continue
    if nst < max_nst-1:
     fread = open('prior_'+str(nst)+'_'+str(ost)+'.py','r')
     sread = fread.read()
     fread.close()
     sspln = sread.split('## -- end even states')
     ## -- lastEn carried over from previous iteration
     sspln.insert(1,new_state_n(round(1.1*max(lastEn.mean,0.1),2),round(0.1*np.exp(nst*.3),2)))
     sspln.insert(2,'## -- end even states')
     fwrite = open('prior_'+str(nst+1)+'_'+str(ost)+'.py','w')
     fwrite.write('\n'.join(sspln))
     fwrite.close()
    continue
   else:
    ## -- ost == nst, something wrong
    raise ValueError('Value error in fitting')
  print_fit(fit,prior)
  print_error_budget(fit)
  save_data('fit/fit_'+str(nst)+'_'+str(ost)+'.out',fit,data)
  save_prior_from_fit(pdict0,df.define_model,fit,'prior/prior_'+str(nst)+'_'+str(ost)+'.out',
    round_e=2,round_a=1,preserve_e_widths=True,preserve_a_widths=True)
  fit_collector[nst,ost,'fit'] = fit
  fit_collector[nst,ost,'prior'] = prior
  ## -- read and add states
  fread = open('prior/prior_'+str(nst)+'_'+str(ost)+'.out','r')
  sread = fread.read()
  fread.close()
  if nst < max_nst-1:
   ## -- split file where state needs to be added
   sspln = sread.split('## -- end even states')
   ## -- add state
   lastEn = fit.transformed_p['logEn'][-1]
   ## -- 30 -> 0.1*exp = 2.0 at nst=10
   sspln.insert(1,new_state_n(round(1.1*max(lastEn.mean,0.1),2),round(0.1*np.exp(nst*.3),2)))
   sspln.insert(2,'## -- end even states')
   ## -- write new files
   fwrite = open('prior_'+str(nst+1)+'_'+str(ost)+'.py','w')
   fwrite.write('\n'.join(sspln))
   fwrite.close()
  if ost < max_ost-1:
   ssplo = sread.split('## -- end odd states')
   lastEo = fit.transformed_p['logEo'][-1]
   ssplo.insert(1,new_state_o(round(1.1*max(lastEo.mean,0.1),2),round(0.1*np.exp(ost*.3),2)))
   ssplo.insert(2,'## -- end odd states')
   fwrite = open('prior_'+str(nst)+'_'+str(ost+1)+'.py','w')
   fwrite.write('\n'.join(ssplo))
   fwrite.close()

