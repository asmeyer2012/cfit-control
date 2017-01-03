from corrfitter               import CorrFitter
from data_manipulations       import standard_load
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
parser.add_argument('-D','--dump-by-name',dest='dump_gvar_name',action='store_const',const=None)
argsin = parser.parse_known_args(sys.argv[1:]) ## in namespace
argsin = vars(argsin[0]) ## pull out of namespace
print argsin

## -- this is completely independent of defines, just set here so we
##    can do simultaneous processing elsewhere
do_irrep = "8"
#do_irrep = "8'"
#do_irrep = "16"
if do_irrep == "8":
  irrepStr = '8p'
elif do_irrep == "8'":
  irrepStr = '8m'
elif do_irrep == "16":
  irrepStr = '16p'

taglist = list() # for gvar.dump hash key
#taglist.append(('l32v3.mes2pt','mes2pt'))
#filekey='a'
#filekey='m'
#filekey='mn'
filekey='n'
#print "applying munich filter"
print "applying -1^t filter"

taglist.append(('l32v5.bar2pt.'+irrepStr,'bar2pt'))
if not(do_irrep == "16"):
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

argsin['load_gvar'] = False
argsin['dump_gvar'] = True
#standard_load(taglist,filekey,argsin)
dnavg = standard_load(taglist,filekey,argsin)
