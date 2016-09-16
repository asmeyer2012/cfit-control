from corrfitter               import CorrFitter
from data_manipulations       import standard_load,sn_minimize_postload
from extract_3pt_info         import *
from make_data                import make_data,import_corfit_file
from make_data_db             import make_data_db
from make_models              import make_models
from make_models_3pt          import make_models_3pt
from make_prior               import make_prior
from make_prior_3pt           import make_prior_3pt
from make_bootstrap           import make_bootstrap
from manipulate_dataset       import *
from print_results            import print_fit
from print_results            import print_error_budget
from save_data                import save_data
from save_prior               import save_prior_from_fit
from sn_minimizer             import *
from make_plot                import make_plot
from make_plot                import make_plot_corr_neg
from make_plot                import make_plot_1plus1
from plot_corr_double_log     import plot_corr_double_log
from plot_corr_effective_mass import plot_corr_effective_mass
from plot_corr_effective_mass_check import plot_corr_effective_mass_check
from plot_corr_normalized     import plot_corr_normalized
from plot_corr_3pt            import plot_corr_3pt
from meta_data                import *
from util_files               import read_fit_file
import defines           as df
import define_prior      as dfp
import define_prior_3pt  as dfp3
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np
import argparse
import hashlib
import sys

parser = argparse.ArgumentParser(description='fit 3-point correlators') # description of what?
parser.add_argument('-d','--dump',dest='dump_gvar',action='store_true')
parser.add_argument('-D','--dump-by-name',dest='dump_gvar_name',action='store_const',const=None)
parser.add_argument('-l','--load',dest='load_gvar',action='store_true')
parser.add_argument('-L','--load-by-name',dest='load_gvar_name',action='store_const',const=None)
argsin = parser.parse_known_args(sys.argv[1:]) ## in namespace
argsin = vars(argsin[0]) ## pull out of namespace
print argsin

## -- assume that data has already been parsed into import files, complete with config tags
td = {}
dset0 = {}
dset1 = {}
davg  = {}

if df.do_irrep == "8":
  irrepStr = '8p'
elif df.do_irrep == "8'":
  irrepStr = '8m'
elif df.do_irrep == "8":
  irrepStr = '16p'

taglist = list() # for gvar.dump hash key
filekey = 'm'
taglist.append(('l32v4.bar2pt.'+irrepStr,'2pt'))

dall = standard_load(taglist,filekey,argsin)
if df.do_sn_minimize:
 defm = {}
 for key in dall:
  tlen = len(dall[key])
  #if dall[key][2]/dall[key][0] > 0.\
  #and dall[key][tlen-2]/dall[key][0] > 0.:
  # defm[key] = [-gv.log(dall[key][2]/dall[key][0])/2.+gv.log(dall[key][tlen-2]/dall[key][0])/2.]
  #else:
  # defm[key] = [gv.gvar(1e-8,1e-6)]
  defm[key] = [] ## -- skip the first
  for t in range(1,tlen/2-2):
   if dall[key][t+2]/dall[key][t] > 0.\
   and dall[key][tlen-t-2]/dall[key][tlen-t] > 0.:
    defm[key].append(-gv.log(dall[key][t+2]/dall[key][t])/4.
     -gv.log(dall[key][tlen-t-2]/dall[key][tlen-t])/4.)
   else:
    defm[key].append(gv.gvar(1e-8,1e-8)) ## -- add garbage value, > 0
  #defm[key].append(-gv.log(dall[key][tlen/2]/dall[key][tlen/2-2])/2.
  # -gv.log(dall[key][tlen/2]/dall[key][tlen/2+2])/2.)
  #print defm[key]
 #raise ValueError("test")
 cvec,kvec,_ = sn_minimize_postload(defm,df.rangeMax)
 clist = list()
 klist = list()
 for key in dall:
  ## -- deconstruct key based on current conventions
  k = int(key[-1])
  if not(k in klist):
   klist.append(k)
  c = int(key[-2])
  if not(c in clist):
   clist.append(c)
 call = list()
 for i,c in zip(range(len(clist)),sorted(clist)):
  call.append(list(np.zeros(len(klist))))
  for j,k in zip(range(len(klist)),sorted(klist)):
   call[i][j] = dall['s'+str(c)+str(k)]
 cdia = diagonalize_correlator(call,cvec,kvec)
 ddia = {}
 for i,c in zip(range(len(clist)),sorted(clist)):
  for j,k in zip(range(len(klist)),sorted(klist)):
   ddia['s'+str(c)+str(k)] = cdia[i][j]

else:
 ddia = dall
 
models2 = make_models    (data=dall,lkey=df.lkey)
models3 = make_models_3pt(data=dall,lkey=df.lkey3)
priors2 = make_prior    (models2)
priors3 = make_prior_3pt(models3)

models = list()
for model in models2:
 models.append(model)
for model in models3:
 models.append(model)
priors = gv.BufferDict()
for key in priors2:
 priors[key] = priors2[key]
for key in priors3:
 if key in priors2:
  continue
 priors[key] = priors3[key]
if df.do_init2:
  init2={}
  for key in df.define_init:
    if key[-1] == 'n':
     init2[key] = df.define_init[key][:df.num_nst]
    elif key[-1] == 'o':
     init2[key] = df.define_init[key][:df.num_ost]
else:
  init2=None
if df.do_init3:
  init3={}
  for key in df.define_init_3pt:
    if key[-2:] == 'nn':
     init3[key] = np.resize(df.define_init_3pt[key],(df.num_nst,df.num_nst))
    elif key[-2:] == 'no':
     init3[key] = np.resize(df.define_init_3pt[key],(df.num_nst,df.num_ost))
    elif key[-2:] == 'on':
     init3[key] = np.resize(df.define_init_3pt[key],(df.num_ost,df.num_nst))
    elif key[-2:] == 'oo':
     init3[key] = np.resize(df.define_init_3pt[key],(df.num_ost,df.num_ost))
    elif key[-1] == 'n':
     init3[key] = df.define_init_3pt[key][:df.num_nst]
    elif key[-1] == 'o':
     init3[key] = df.define_init_3pt[key][:df.num_ost]
else:
  init3=None
pass 

## -- plot
plot_corr_effective_mass      (models2,ddia,None,**df.fitargs)
plot_corr_effective_mass_check(models2,ddia,None,**df.fitargs)
#plot_corr_effective_mass      (models2,dall,None,**df.fitargs)
#plot_corr_effective_mass_check(models2,dall,None,**df.fitargs)
if df.do_plot_terminal:
 plt.show()
