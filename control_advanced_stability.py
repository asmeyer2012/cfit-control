from corrfitter           import CorrFitter
from data_manipulations   import standard_load
from extract_3pt_info     import *
from make_data            import make_data,import_corfit_file
from make_data_db         import make_data_db
from make_init            import make_adv_init_from_fit_file_3pt
from make_models          import make_models
from make_models_3pt      import make_models_3pt,make_models_advanced
from make_prior           import make_prior
from make_prior_3pt       import make_prior_3pt
from make_prior_advanced  import truncate_prior_states
from make_bootstrap       import make_bootstrap
from manipulate_dataset   import *
from multiprocessing      import Pool
from print_results        import print_fit
from print_results        import print_error_budget
from save_data            import save_data
from save_fit             import save_init_from_fit
from save_prior           import save_prior_from_fit
from plot_corr_double_log import plot_corr_double_log
from plot_corr_normalized import plot_corr_normalized
from meta_data            import *
import defines               as df
import define_prior          as dfp
import define_prior_3pt      as dfp3
import define_prior_advanced as dfpa
import gvar                  as gv
import gvar.dataset          as gvd
#import importlib             as impl ## -- import with variable name
import matplotlib.pyplot     as plt
import numpy                 as np
#import shutil                as shil ## -- copy files
import util_funcs            as utf
import argparse
import hashlib
import sys

parser = argparse.ArgumentParser(description='fit 3-point correlators') # description of what?
parser.add_argument('-r','--reset',dest='override_init',action='store_true')
parser.add_argument('-p','--plot',dest='override_plot',action='store_true')
parser.add_argument('-d','--dump',dest='dump_gvar',action='store_true')
parser.add_argument('-D','--dump-by-name',dest='dump_gvar_name',action='store_const',const=None)
parser.add_argument('-l','--load',dest='load_gvar',action='store_true')
parser.add_argument('-L','--load-by-name',dest='load_gvar_name',action='store_const',const=None)
argsin = parser.parse_known_args(sys.argv[1:]) ## in namespace
argsin = vars(argsin[0]) ## pull out of namespace
print argsin

doParallel=True
maxProcesses=8

if df.do_irrep == "8":
  irrepStr = '8p'
elif df.do_irrep == "8'":
  irrepStr = '8m'
elif df.do_irrep == "16":
  irrepStr = '16p'

## 8+ representation
taglist = list() # for gvar.dump hash key
#filekey = 'a'  ## -- standard choice, no filters
#filekey = 'm'  ## -- munich filter
filekey = 'n'  ## -- -1^t filter
#filekey = 'mn'  ## -- munich + -1^t filter
#print "*** USING MUNICH FILTER ***"
taglist.append(('l32v5.bar2pt.'+irrepStr,'bar2pt'))
if not(df.do_irrep == "16"):
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7'))
else:
 ## -- both 16+ and 16-
 irrepStr = '16p'
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7','16p'))
 irrepStr = '16m'
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7','16m'))

## -- consolidated all loading into a single file:
dall = standard_load(taglist,filekey,argsin)

def doProcess(nst,ost,n3st=1,o3st=1,data=dall):
  ## -- do a single fit ... set up for parallelizing
  if df.do_2pt and not(df.do_3pt):
   pdict3 = utf.get_prior_dict(df.define_prior,
    df.define_prior['nkey'],df.define_prior['okey'],nst,ost,do_v_symm=True)
   models = make_models(data=dall,lkey=df.lkey)
   prior  = make_prior(models,prior_dict=pdict3,nst=nst,ost=ost)
   fitter = CorrFitter(models=models,maxit=df.maxit)
   if df.do_init2:
     init={}
     if argsin['override_init']:
      init = make_init_from_fit_file_3pt(models,'fit_dict')
     else:
      for key in df.define_init:
        if key[-1] == 'n':
         init[key] = df.define_init[key][:nst]
        elif key[-1] == 'o':
         init[key] = df.define_init[key][:ost]
   else:
     init=None
  else:
   pdict = utf.get_prior_dict(df.define_prior,
    df.define_prior['nkey'],df.define_prior['okey'],
    nst,ost,do_v_symm=True)
   pdict3 = utf.get_prior_dict(df.define_prior_3pt,
    df.define_prior_3pt['nkey'],df.define_prior_3pt['okey'],
    nst,ost,df.define_prior_3pt['vkey'],nst,ost,do_v_symm=True)
   for key in pdict:
    pdict3[key] = pdict[key]
   models2 = make_models(data=dall,lkey=df.lkey,use_advanced=True)
   #models3 = make_models_3pt(data=dall,lkey=df.lkey3)
   models3 = make_models_advanced(data=dall,lkey=df.lkey3)
   models = list()
   for model in models2:
    models.append(model)
   for model in models3:
    models.append(model)
   #prior2 = make_prior(models2,prior_dict=pdict,nst=nst,ost=ost)
   #prior3 = make_prior_3pt(models3,prior_dict=pdict3,nst=nst,ost=ost,n3st=nst,o3st=ost)
   #priors = gv.BufferDict()
   #for key in prior2:
   # priors[key] = prior2[key]
   #for key in prior3:
   # priors[key] = prior3[key]
   priorsa = truncate_prior_states(df.define_prior_adv,
    nst,ost,n3st,o3st)
   fitter = CorrFitter(models=models,maxit=df.maxit)
   if df.do_init3:
     #init3={}
     #if argsin['override_init']:
     init = make_adv_init_from_fit_file_3pt(models3,'fit_adv_'+irrepStr+'_3pt',\
      fresh_overlap=True,fresh_amplitude=True)
   else:
     init=None
   pass 
  #fit = fitter.lsqfit(data=dall,prior=priors,p0=init,svdcut=df.svdcut)
  #print priorsa
  #print init
  fit = fitter.lsqfit(data=dall,prior=priorsa,p0=init,svdcut=df.svdcut)
  ## --
  print_fit(fit,priorsa,do_v_symm=True)
  print_error_budget(fit)
  #save_data('fit-stability/fit_'+str(nst)+'_'+str(ost)+'.out',fit,dall)
  if df.do_2pt and not(df.do_3pt):
   save_init_from_fit(fit,'fit-adv/fit_'+str(nst)+'_'+str(ost)+'.py',do_v_symm=True)
  else:
   save_init_from_fit(fit,'fit-adv/fit_n'+str(nst)+'_o'+str(ost)\
    +'_ng'+str(n3st)+'_og'+str(o3st)+'.py',do_v_symm=True)

min_nst=df.stab_min_nst
mid_nst=df.stab_mid_nst
max_nst=df.stab_max_nst
min_ost=df.stab_min_ost
mid_ost=df.stab_mid_ost
max_ost=df.stab_max_ost

if __name__ == '__main__' and doParallel:
 pool= Pool(processes=maxProcesses)
 if df.do_2pt and not(df.do_3pt):
  for ost in range(min_ost,max_ost):
   for nst in range(min_nst,max_nst):
    if nst+ost>df.stab_max_states:
     continue
    if nst<mid_nst and ost<mid_ost:
     continue
    pool.apply_async(doProcess,args=(nst,ost))
 else:
  for n3st,o3st in df.nost_3pt:
   for ost in range(min_ost,max_ost):
    for nst in range(min_nst,max_nst):
     if nst+ost>df.stab_max_states:
      continue
     if nst<mid_nst and ost<mid_ost:
      continue
     #print "starting fit ",nst,",",ost,",",n3st,",",o3st
     #pool.apply_async(doProcess,args=(nst,ost))
     pool.apply_async(doProcess,args=(nst,ost,n3st,o3st))
 pool.close()
 pool.join()
elif not(doParallel):
 for n3st,o3st in df.nost_3pt:
  for ost in range(min_ost,max_ost):
   for nst in range(min_nst,max_nst):
    if nst+ost>df.stab_max_states:
     continue
    if nst<mid_nst and ost<mid_ost:
     continue
    print "starting fit ",nst,",",ost,",",n3st,",",o3st
    doProcess(nst,ost,n3st,o3st)
