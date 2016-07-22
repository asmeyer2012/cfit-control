from corrfitter               import CorrFitter
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
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.ss.t06.p00','ss','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.ss.t-7.p00','ss','t7'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'v4v4.t06.p00','v4v4','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'v4v4.t-7.p00','v4v4','t7'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'axp.t06.p00','axp','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'axp.t-7.p00','axp','t7'))

## -- get just the first entry of array
filelist = list(np.transpose(np.array(taglist))[0])

if argsin['load_gvar']:
 gvarhash = hashlib.md5(''.join(filelist)+filekey).hexdigest()[:8]
 dall = gv.load('gvar.dump.'+gvarhash)
 print "loaded data from gvar file: gvar.dump."+gvarhash
else:
 for tag in taglist:
  td[tag[1:]] = import_corfit_file(tag[0]) ## -- import all of the files in taglist

 ## -- pre-consolidation manipulation
 pass
 
 for key in td:
  dset0[key] = consolidate_tags(td[key])
 for key in dset0:
  dset1[key] = consolidate_tags(dset0[key])
 
 ## -- post-consolidation manipulation
 for key in dset1:
  for xkey in dset1[key]:
   if 'v4v4' in xkey\
   or 'axax' in xkey\
   or 'ayay' in xkey\
   or 'azaz' in xkey:
    print "applying filter to key",key,xkey
    munich_filter(dset1[key],xkey)
 pass
 
 dnavg = gv.dataset.Dataset()
 for key in dset1:
  for xkey in dset1[key]:
   if 'm' in xkey:
    #print "skipping mixed symmetry key",key,xkey,"..."
    continue
   dnavg[xkey] = dset1[key][xkey]
 dall = gv.dataset.avg_data(dnavg)
 ## -- if requested, save to pickle file
 if argsin['dump_gvar']:
  gvarhash = hashlib.md5(''.join(filelist)+filekey).hexdigest()[:8]
  gv.dump(dall,'gvar.dump.'+gvarhash)
  print "dumped data to gvar file: gvar.dump."+gvarhash
pass # dataset
  
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
plot_corr_effective_mass      (models2,dall,None,**df.fitargs)
plot_corr_effective_mass_check(models2,dall,None,**df.fitargs)
if df.do_plot_terminal:
 plt.show()
