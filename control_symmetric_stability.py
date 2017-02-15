from corrfitter           import CorrFitter
from data_manipulations   import standard_load
from extract_3pt_info     import *
from make_data            import make_data,import_corfit_file
from make_data_db         import make_data_db
from make_init            import make_init_from_fit_file_3pt
from make_models          import make_models
from make_models_3pt      import make_models_3pt
from make_prior           import make_prior
from make_prior_3pt       import make_prior_3pt
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
import defines            as df
import define_prior       as dfp
import define_prior_3pt   as dfp3
import gvar               as gv
import gvar.dataset       as gvd
#import importlib          as impl ## -- import with variable name
import matplotlib.pyplot  as plt
import numpy              as np
#import shutil             as shil ## -- copy files
import util_funcs         as utf
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

### 8+ representation
#taglist = list() # for gvar.dump hash key
##filekey = 'an'  ## -- e4b56737
#filekey = 'a'  ## -- 4218b279
##taglist.append(('l32v6.mes2pt','mes'))
#taglist.append(('l32v6.bar2pt.'+irrepStr,'bar2pt'))
#taglist.append(('l32v6.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6'))
#taglist.append(('l32v6.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7'))
#taglist.append(('l32v6.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6'))
#taglist.append(('l32v6.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7'))
#taglist.append(('l32v6.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6'))
#taglist.append(('l32v6.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7'))

## 8+ representation
taglist = list() # for gvar.dump hash key
#filekey = 'n'  ## -- 
#filekey = 'mn' ## -- 
#print "Using -1^T factor"
#filekey = 'an'  ## -- 
#filekey = 'm'  ## -- munich filter
#print "Using Munich filter"
filekey = 'a'  ## -- standard choice, no filters
#taglist.append(('l32v6.mes2pt','mes'))
taglist.append(('l32v6.bar2pt.'+irrepStr,'bar2pt'))
if not(df.do_irrep == "16"):
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7'))
else:
 ## -- both 16+ and 16-
 irrepStr = '16p'
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6','16p'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7','16p'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6','16p'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7','16p'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6','16p'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7','16p'))
 irrepStr = '16m'
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6','16m'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7','16m'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6','16m'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7','16m'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6','16m'))
 taglist.append(('l32v6.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7','16m'))
## -- for later
if df.do_irrep == "16":
 irrepStr = '16'

## -- consolidated all loading into a single file:
dall = standard_load(taglist,filekey,argsin)

## -- symmetric 3pts require n3st == nst, o3st == ost
def doProcess(nst,ost,data=dall):
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
        eokey = utf.get_evenodd(key)
        if eokey == 'n':
         init[key] = df.define_init[key][:nst]
        elif eokey == 'o':
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
   models2 = make_models(data=dall,lkey=df.lkey)
   models3 = make_models_3pt(data=dall,lkey=df.lkey3)
   models = list()
   for model in models2:
    models.append(model)
   for model in models3:
    models.append(model)
   #print df.lkey+df.lkey3
   #for model in models:
   # model.all_datatags
   #raise ValueError("test")
   prior2 = make_prior(models2,prior_dict=pdict,nst=nst,ost=ost)
   prior3 = make_prior_3pt(models3,prior_dict=pdict3,nst=nst,ost=ost,n3st=nst,o3st=ost)
   priors = gv.BufferDict()
   for key in prior2:
    priors[key] = prior2[key]
   for key in prior3:
    priors[key] = prior3[key]
   fitter = CorrFitter(models=models,maxit=df.maxit)
   if df.do_init3:
     init={}
     if not(argsin['override_init']):
      init = make_init_from_fit_file_3pt(models,'fit_dict'+irrepStr+'_3pt',
       fresh_overlap=False,fresh_amplitude=True)
     else:
      for key in df.define_init_3pt:
       eokey = utf.get_evenodd(key)
       if eokey == 'nn':
        init[key] = np.resize(df.define_init_3pt[key],(df.num_nst_3pt,df.num_nst_3pt))
        if df.do_v_symmetric:
         init[key] = utf.truncate_upper_triangle(init[key],df.num_nst_3pt)
       elif eokey == 'oo':
        init[key] = np.resize(df.define_init_3pt[key],(df.num_ost_3pt,df.num_ost_3pt))
        if df.do_v_symmetric:
         init[key] = utf.truncate_upper_triangle(init[key],df.num_ost_3pt)
       elif eokey == 'no':
        init[key] = np.resize(df.define_init_3pt[key],(df.num_nst_3pt,df.num_ost_3pt))
       elif eokey == 'on':
        ## -- is this correct for symmetric v?
        #init[key] = np.resize(df.define_init_3pt[key],(df.num_ost_3pt,df.num_nst_3pt))
        pass
       elif eokey == 'n':
        init[key] = df.define_init_3pt[key][:df.num_nst]
       elif eokey == 'o':
        init[key] = df.define_init_3pt[key][:df.num_ost]
   else:
     init=None
  print init
  fit = fitter.lsqfit(data=dall,prior=priors,p0=init,svdcut=df.svdcut)
  ## --
  print_fit(fit,priors,do_v_symm=True)
  print_error_budget(fit)
  #save_data('fit-stability/fit_'+str(nst)+'_'+str(ost)+'.out',fit,dall)
  if df.do_2pt and not(df.do_3pt):
   save_init_from_fit(fit,'fit-stability/fit_'+str(nst)+'_'+str(ost)+'.py',do_v_symm=True)
  else:
   save_init_from_fit(fit,'fit-stability/fit_n'+str(nst)+'_o'+str(ost)\
    +'_ng'+str(nst)+'_og'+str(ost)+'.py',do_v_symm=True)

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
  #for n3st,o3st in df.nost_3pt:
  for ost in range(min_ost,max_ost):
   for nst in range(min_nst,max_nst):
    if nst+ost>df.stab_max_states:
     continue
    if nst<mid_nst and ost<mid_ost:
     continue
    #print "starting fit ",nst,",",ost
    pool.apply_async(doProcess,args=(nst,ost))
 pool.close()
 pool.join()
elif not(doParallel):
 #for n3st,o3st in df.nost_3pt:
 for ost in range(min_ost,max_ost):
  for nst in range(min_nst,max_nst):
   if nst+ost>df.stab_max_states:
    continue
   if nst<mid_nst and ost<mid_ost:
    continue
   doProcess(nst,ost)
