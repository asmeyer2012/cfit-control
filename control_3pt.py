from corrfitter               import CorrFitter
from data_manipulations       import standard_load,sn_minimize_postload_3pt
from extract_3pt_info         import *
from make_data                import make_data,import_corfit_file
from make_data_db             import make_data_db
from make_init                import make_init_from_fit_file_3pt
from make_models              import make_models
from make_models_3pt          import make_models_3pt
from make_prior               import make_prior
from make_prior_3pt           import make_prior_3pt
from make_bootstrap           import make_bootstrap
from manipulate_dataset       import *
from mock_data_generator      import generate_mock_data
from print_results            import fmt_reduced_chi2
from print_results            import print_fit
from print_results            import print_error_budget
from save_data                import save_data
from save_fit                 import save_init_from_fit
from save_prior               import save_prior_from_fit
from make_plot                import make_plot
from make_plot                import make_plot_corr_neg
from make_plot                import make_plot_1plus1
from plot_corr_double_log_folded import plot_corr_double_log_folded
#from plot_corr_effective_mass import plot_corr_effective_mass
#from plot_corr_effective_mass_check import plot_corr_effective_mass_check
from plot_corr_adv_effm_clean import plot_corr_effective_mass
from plot_corr_normalized     import plot_corr_normalized
#from plot_corr_3pt            import plot_corr_3pt
#from plot_splitting           import plot_splitting
from plot_corr_stacked_3pt    import plot_corr_3pt
#from plot_corr_stacked_3pt_clean    import plot_corr_3pt
from plot_corr_adv_stacked_3pt import plot_corr_adv_stacked_3pt
from meta_data                import *
from util_files               import read_fit_file
import defines           as df
import define_prior      as dfp
import define_prior_3pt  as dfp3
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np
import util_funcs        as utf
import argparse
import hashlib
import sys

import matplotlib as mpl
mpl.use('TkAgg')

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

if df.do_irrep == "8":
  irrepStr = '8p'
elif df.do_irrep == "8'":
  irrepStr = '8m'
elif df.do_irrep == "16":
  irrepStr = '16p'

## 8+ representation
taglist = list() # for gvar.dump hash key
filekey = 'a'  ## -- standard choice, no filters
#filekey = 'm'  ## -- munich filter
#filekey = 'n'  ## -- munich filter
#print "Using munich filter"
#print "*** USING -1^t FILTER ***"
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
if df.do_mock:
 dall,truth = generate_mock_data('mock8m.0')
else:
 dall = standard_load(taglist,filekey,argsin)
  
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
  if argsin['override_init']:
   try:
    init2 = make_init_from_fit_file_3pt(models2,'fit_dict'+irrepStr+'_2pt.py')
    print "loaded initial values from file: ",'fit_dict'+irrepStr+'_2pt.py'
   except:
    init2 = None
    print "could not load 2-point function initial values"
  else:
   for key in df.define_init:
     eokey = utf.get_evenodd(key)
     #if key[-1] == 'n':
     if eokey == 'n':
      init2[key] = df.define_init[key][:df.num_nst]
     elif eokey == 'o':
      init2[key] = df.define_init[key][:df.num_ost]
else:
  init2=None
if df.do_init3:
  init3={}
  if not(argsin['override_init']):
#   try:
    init3 = make_init_from_fit_file_3pt(models,'fit_dict'+irrepStr+'_3pt')
    print "loaded initial values from file: ",'fit_dict'+irrepStr+'_3pt.py'
#   except:
#    init3 = None
#    print "could not load 3-point function initial values"
  else:
   for key in df.define_init_3pt:
     eokey = utf.get_evenodd(key)
     #if key[-2:] == 'nn':
     if eokey == 'nn':
      init3[key] = np.resize(df.define_init_3pt[key],(df.num_nst_3pt,df.num_nst_3pt))
      if df.do_v_symmetric:
       init3[key] = utf.truncate_upper_triangle(init3[key],df.num_nst_3pt)
      #elif key[-2:] == 'oo':
     elif eokey == 'oo':
      init3[key] = np.resize(df.define_init_3pt[key],(df.num_ost_3pt,df.num_ost_3pt))
      if df.do_v_symmetric:
       init3[key] = utf.truncate_upper_triangle(init3[key],df.num_ost_3pt)
      #elif key[-2:] == 'no':
     elif eokey == 'no':
      init3[key] = np.resize(df.define_init_3pt[key],(df.num_nst_3pt,df.num_ost_3pt))
      #elif key[-2:] == 'on':
     elif eokey == 'on':
      ## -- is this correct for symmetric v?
      #init3[key] = np.resize(df.define_init_3pt[key],(df.num_ost_3pt,df.num_nst_3pt))
      pass
      #elif key[-1] == 'n':
     elif eokey == 'n':
      init3[key] = df.define_init_3pt[key][:df.num_nst]
      #elif key[-1] == 'o':
     elif eokey == 'o':
      init3[key] = df.define_init_3pt[key][:df.num_ost]
else:
  init3=None
pass 
#print 'init: ',init3
#init3 = None ## -- test

fitter2 = CorrFitter(models=models2,maxit=df.maxit)
fitter3 = CorrFitter(models=models,maxit=df.maxit)

#np.set_printoptions(precision=4,linewidth=100)
#d1 = list()
#d2 = list()
#conv = .197/.15
#d1.append(np.cumsum(gv.mean(gv.exp(priors['logEn']))))
#d1.append(gv.mean(gv.exp(priors['logEn'])))
#d1.append(gv.sdev(gv.exp(priors['logEn'])))
#d1.append(conv*np.cumsum(gv.mean(gv.exp(priors['logEn']))))
#d1.append(conv*gv.mean(gv.exp(priors['logEn'])))
#d1.append(conv*gv.sdev(gv.exp(priors['logEn'])))
#d1.append(gv.sdev(gv.exp(priors['logEn']))/gv.mean(gv.exp(priors['logEn'])))
#d2.append(np.cumsum(gv.mean(gv.exp(priors['logEo']))))
#d2.append(gv.mean(gv.exp(priors['logEo'])))
#d2.append(gv.sdev(gv.exp(priors['logEo'])))
#d2.append(conv*np.cumsum(gv.mean(gv.exp(priors['logEo']))))
#d2.append(conv*gv.mean(gv.exp(priors['logEo'])))
#d2.append(conv*gv.sdev(gv.exp(priors['logEo'])))
#d2.append(gv.sdev(gv.exp(priors['logEo']))/gv.mean(gv.exp(priors['logEo'])))
#print np.array(d1).T
#
#f = open('s'+irrepStr+'.prior','w')
#f.write('#i sumE dE sigE sumE[GeV] dE[GeV] sigE[GeV] sigE/dE \n')
#f.write('#even\n')
#for i,x in enumerate(np.array(d1).T):
# #f.write( str(i)+' '+str(x)+'\n' )
# #f.write( '%d %1.3f %1.3f %1.3f %1.3f \n' % (i,)+tuple(x))
# outdat = (i,)+tuple(x)
# f.write( '%d %1.3f %1.3f %1.3f %1.3f %1.3f %1.3f %1.3f \n' % outdat)
#f.write('#odd\n')
#for i,x in enumerate(np.array(d2).T):
# #f.write( str(i)+' '+str(x)+'\n' )
# outdat = (i,)+tuple(x)
# f.write( '%d %1.3f %1.3f %1.3f %1.3f %1.3f %1.3f %1.3f \n' % outdat)
#f.close()
#
#raise ValueError("test")

if df.do_2pt:
 print "starting 2pt fit..."
 fit2 = fitter2.lsqfit(data=dall,prior=priors2,p0=init2,svdcut=df.svdcut)
 ## -- fits take a long time, so print prematurely
 print_fit(fit2,priors2)
if df.do_3pt:
 print "starting 3pt fit..."
 #print priors
 fit3 = fitter3.lsqfit(data=dall,prior=priors,p0=init3,svdcut=df.svdcut)
else:
 print "Ignoring 3pt fit!"
 fit3=None

#fit3 = fitter3.lsqfit(data=dall,prior=priors,svdcut=df.svdcut)
print fmt_reduced_chi2(fit3,df.do_v_symmetric)
#save_data('./test.fit.out',fit,dall)

## -- print
#if df.do_2pt:
# print_fit(fit2,priors2)
print_fit(fit3,priors,df.do_v_symmetric)

## -- save fit as an initial value dictionary
if df.do_2pt:
 save_init_from_fit(fit2,'fit_dict'+irrepStr+'_2pt.py')
if df.do_3pt:
 save_init_from_fit(fit3,'fit_dict'+irrepStr+'_3pt.py',df.do_v_symmetric)

## -- test routines
#import util_plots as utp
#for model in models:
# try:
#  fn = utp.create_fit_func_3pt(model,fit3)
#  test1 = model.fitfcn(fit3.transformed_p)
#  test2 = fn(model.tfit)
#  print model.datatag
#  print test1
#  print test2
# except AttributeError:
#  ## -- 2pt
#  pass

np.set_printoptions(precision=3,linewidth=100)
elst = []
for key in sorted(fit3.p):
 #if key[:2] == 'En' or key[:2] == 'Eo':
 tkey = utf.get_basekey(key)
 if (tkey[0] is None) and (tkey[1][-2:] == 'En' or tkey[1][-2:] == 'Eo'):
  for e in fit3.p[key]:
   elst.append(e)
cor = gv.evalcorr(elst)
evl,evc = gv.linalg.eigvalsh(cor,True)
chol = np.linalg.cholesky(cor).T
print 'correlation E:'
print gv.evalcorr(elst)
print 'eigenvalues:'
print evl
print 'eigenvectors:'
print evc
print 'cholesky:'
print chol

## -- plot
if df.do_plot or argsin['override_plot']:
 ##plot_corr_effective_mass_check(models2,dall,None,**df.fitargs)
 ##plot_corr_effective_mass(models2,dall,None,**df.fitargs)
 #plot_corr_effective_mass(models2,dall,fit3,**df.fitargs)
 #plot_corr_effective_mass(models2,dall,fit3,req=[[0],list()],**df.fitargs)
 #plot_corr_effective_mass(models2,dall,fit3,req=[[0,1],list()],**df.fitargs)
 #plot_corr_effective_mass(models2,dall,fit3,req=[list(),[0]],**df.fitargs)
 #plot_corr_effective_mass(models2,dall,fit3,req=[list(),[1]],**df.fitargs)
 #plot_corr_effective_mass(models2,dall,fit3,req=[list(),[2]],**df.fitargs)
 #plot_corr_effective_mass(models2,dall,fit3,req=[list(),[0,1,2]],**df.fitargs)
 ##plot_corr_effective_mass(models2,dall,fit3,req=[[2],list()],**df.fitargs)
 #plot_corr_effective_mass(models2,dall,fit3,req=[list(),[0]],**df.fitargs)
 ##plot_corr_double_log(models2,dall,fit3,**df.fitargs)
 ##plot_corr_double_log_folded(models2,dall,fit3,**df.fitargs)
 #plot_corr_double_log_folded(models2,dall,fit3,**df.fitargs)
 #plot_corr_double_log_folded(models2,dall,fit3,req=[[0],list()],**df.fitargs)
 #plot_corr_double_log_folded(models2,dall,fit3,req=[[0,1],list()],**df.fitargs)
 #plot_corr_double_log_folded(models2,dall,fit3,req=[list(),[0]],**df.fitargs)
 #plot_corr_double_log_folded(models2,dall,fit3,req=[list(),[1]],**df.fitargs)
 #plot_corr_double_log_folded(models2,dall,fit3,req=[list(),[2]],**df.fitargs)
 #plot_corr_double_log_folded(models2,dall,fit3,req=[list(),[0,1,2]],**df.fitargs)
 ##plot_corr_double_log_folded(models2,dall,fit3,req=[[2],list()],**df.fitargs)
 #plot_corr_double_log_folded(models2,dall,fit3,req=[list(),[0]],**df.fitargs)
 ###plot_corr_double_log_folded(models2,dall,fit3,req=[list(),[1]],**df.fitargs)
 ##plot_corr_normalized(models2,dall,fit3,**df.fitargs)
 ##if df.do_3pt:
 ## plot_corr_3pt(models3,dall,fit3,**df.fitargs)
 plot_corr_adv_stacked_3pt(models3,dall,fit3,**df.fitargs)
 #plot_corr_adv_stacked_3pt(models3,dall,fit3,req=[[0],list()],**df.fitargs)
 #plot_corr_adv_stacked_3pt(models3,dall,fit3,req=[[1],list()],**df.fitargs)
 #plot_corr_adv_stacked_3pt(models3,dall,fit3,req=[list(),[0,1]],**df.fitargs)
 if df.do_plot_terminal:
  plt.show()

if df.do_sn_minimize:
 ## -- shortcut
 cvec6,kvec6,_ = sn_minimize_postload_3pt(dall,6,'aiai')
 cvec7,kvec7,_ = sn_minimize_postload_3pt(dall,7,'aiai')
 print "source vectors:"
 print cvec6
 print cvec7
 print "sink vectors:"
 print kvec6
 print kvec7
 clist = list()
 klist = list()
 for key in dall:
  ## -- deconstruct key based on current conventions
  tkey = 't'.join(key.split('t')[:-1])
  if len(tkey) == 0:
   continue
  k = int(tkey[-1])
  if not(k in klist):
   klist.append(k)
  c = int(tkey[-2])
  if not(c in clist):
   clist.append(c)
 call6 = list()
 call7 = list()
 for i,c in zip(range(len(clist)),sorted(clist)):
  call6.append(list(np.zeros(len(klist))))
  call7.append(list(np.zeros(len(klist))))
  for j,k in zip(range(len(klist)),sorted(klist)):
   call6[i][j] = dall['aiais'+str(c)+str(k)+'t6']
   call7[i][j] = dall['aiais'+str(c)+str(k)+'t7']
 cdia6 = diagonalize_correlator(call6,cvec6,kvec6)
 cdia7 = diagonalize_correlator(call7,cvec6,kvec6)
 #ddia = {}
 for i,c in zip(range(len(clist)),sorted(clist)):
  for j,k in zip(range(len(klist)),sorted(klist)):
   dall['aiais'+str(c)+str(k)+'t6'] = cdia6[i][j]
   dall['aiais'+str(c)+str(k)+'t7'] = cdia7[i][j]
 #kwargs = df.fitargs
 for key in dall:
  tkey = 't'.join(key.split('t')[:-1]) 
  if len(tkey) > 0:
   df.fitargs[tkey]["p3_save_name"] = \
    "s3-s8p-l3248-coul-"+tkey+".pdf"
   df.fitargs[tkey]["y_scale"] = [-.2,.6]
   df.fitargs[tkey]["yaxistitle"] = r"$\beta v_{i}^{T}C_{ij}w_{j}(t,T)$"
 plot_corr_3pt(models3,dall,fit3,**df.fitargs)
 plt.show()
