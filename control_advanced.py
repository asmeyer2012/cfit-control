from corrfitter               import CorrFitter
from data_manipulations       import standard_load,sn_minimize_postload_3pt
from extract_3pt_info         import *
from make_data                import make_data,import_corfit_file
from make_data_db             import make_data_db
#from make_init                import make_init_from_fit_file_3pt
from make_init                import make_adv_init_from_fit_file_3pt
from make_models              import make_models
from make_models_3pt          import make_models_3pt,make_models_advanced
from make_prior               import make_prior
from make_prior_3pt           import make_prior_3pt
#from make_prior_advanced      import make_prior_advanced
from make_prior_advanced      import truncate_prior_states
from make_bootstrap           import make_bootstrap
from manipulate_dataset       import *
from print_results            import fmt_reduced_chi2
from print_results            import print_fit
from print_results            import print_error_budget
from save_data                import save_data
from save_fit                 import save_init_from_fit
from save_prior               import save_prior_from_fit
from make_plot                import make_plot
from make_plot                import make_plot_corr_neg
from make_plot                import make_plot_1plus1
#from plot_corr_double_log_folded import plot_corr_double_log_folded
from plot_corr_adv_dl_folded  import plot_corr_adv_dl_folded
#from plot_corr_effective_mass import plot_corr_effective_mass
from plot_corr_effective_mass_check import plot_corr_effective_mass_check
from plot_corr_normalized     import plot_corr_normalized
#from plot_corr_3pt            import plot_corr_3pt
from plot_corr_stacked_3pt    import plot_corr_3pt
#from plot_corr_stacked_3pt_clean    import plot_corr_3pt
from meta_data                import *
from util_files               import read_fit_file
import defines               as df
import define_prior          as dfp
import define_prior_3pt      as dfp3
import define_prior_advanced as dfpa
import gvar                  as gv
import gvar.dataset          as gvd
import matplotlib.pyplot     as plt
import numpy                 as np
import util_funcs            as utf
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
#filekey = 'n'  ## -- standard choice, no filters
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

## -- consolidated all loading into a single file:
dall = standard_load(taglist,filekey,argsin)
  
models2 = make_models    (data=dall,lkey=df.lkey,use_advanced=True)
#models3 = make_models_3pt(data=dall,lkey=df.lkey3)
models3 = make_models_advanced(data=dall,lkey=df.lkey3)
priors2 = make_prior    (models2)
priors3 = make_prior_3pt(models3)
priorsa = df.define_prior_adv
np.set_printoptions(precision=4,linewidth=100)
d1 = {}
d1['en0'] = list()
d1['enc'] = list() 
d1['enb'] = list()
d1['ens'] = list()
d1['enr'] = list()
d1['eo0'] = list()
d1['eoc'] = list() 
d1['eob'] = list()
d1['eos'] = list()
d1['eor'] = list()
for i in range(6):
 try:
  d1['en0'].append(gv.mean(gv.exp(priorsa['logEn_'+str(i)][0])))
  d1['enc'].append(gv.mean(gv.exp(priorsa['logEn_'+str(i)])))
  d1['enc'][-1][0] = 0
  d1['enb'].append(gv.mean(gv.exp(priorsa['logEn_'+str(i)])))
  d1['ens'].append(gv.sdev(gv.exp(priorsa['logEn_'+str(i)])))
  d1['enr'].append(gv.sdev(gv.exp(priorsa['logEn_'+str(i)]))\
   /gv.mean(gv.exp(priorsa['logEn_'+str(i)])))
 except KeyError:
  pass
 try:
  d1['eo0'].append(gv.mean(gv.exp(priorsa['logEo_'+str(i)][0])))
  d1['eoc'].append(gv.mean(gv.exp(priorsa['logEo_'+str(i)])))
  d1['eoc'][-1][0] = 0
  d1['eob'].append(gv.mean(gv.exp(priorsa['logEo_'+str(i)])))
  d1['eos'].append(gv.sdev(gv.exp(priorsa['logEo_'+str(i)])))
  d1['eor'].append(gv.sdev(gv.exp(priorsa['logEo_'+str(i)]))\
   /gv.mean(gv.exp(priorsa['logEo_'+str(i)])))
 except KeyError:
  continue

conv = .197/.15
f = open('s'+irrepStr+'.aprior','w')
#for i,x,y in enumerate(zip(np.array(d1).T,np.array(d2).T)):
f.write('#i block taste sumE dE sigE sumE[GeV] dE[GeV] sigE[GeV] sigE/dE \n')
f.write('#even\n')
k = 0
for i,(e0,ec,eb,es,er) in enumerate(zip(np.cumsum(d1['en0']),\
  d1['enc'],d1['enb'],d1['ens'],d1['enr'])):
 for j,(ecx,ebx,esx,erx) in enumerate(zip(e0+np.cumsum(ec),eb,es,er)):
  #f.write( str(i)+' '+str(j)+' '+str(ecx)+' '+str(ebx)+' '+str(esx)+' '+str(erx)+'\n' )
  #f.write('%d %d %d %1.3f %1.3f %1.3f %1.3f \n' % (k, i, j, ecx, ebx, esx, erx))
  f.write('%d %d %d %1.3f %1.3f %1.3f %1.3f %1.3f %1.3f %1.3f\n' %\
   (k, i, j, ecx, ebx, esx, conv*ecx, conv*ebx, conv*esx, erx))
  k+=1
f.write('#odd\n')
k = 0
for i,(e0,ec,eb,es,er) in enumerate(zip(np.cumsum(d1['eo0']),\
  d1['eoc'],d1['eob'],d1['eos'],d1['eor'])):
 for j,(ecx,ebx,esx,erx) in enumerate(zip(e0+np.cumsum(ec),eb,es,er)):
  #f.write( str(i)+' '+str(j)+' '+str(ecx)+' '+str(ebx)+' '+str(esx)+' '+str(erx)+'\n' )
  f.write('%d %d %d %1.3f %1.3f %1.3f %1.3f %1.3f %1.3f %1.3f \n' %\
   (k, i, j, ecx, ebx, esx, conv*ecx, conv*ebx, conv*esx, erx))
  k+=1
f.close()

raise ValueError('test')
priorsa = truncate_prior_states(df.define_prior_adv,
 df.num_nst,df.num_ost,df.num_nst_3pt,df.num_ost_3pt)
#raise ValueError('test')

models = list()
for model in models2:
 models.append(model)
for model in models3:
 models.append(model)
priors = gv.BufferDict()
for key in priors2:
 priors[key] = priors2[key]
#for key in priors3:
# if key in priors2:
#  continue
# priors[key] = priors3[key]
priors = priorsa

#if df.do_init2:
#  init2={}
#  if argsin['override_init']:
#   init2 = make_init_from_fit_file_3pt(models2,'fit_dict')
#  else:
#   for key in df.define_init:
#     if key[-1] == 'n':
#      init2[key] = df.define_init[key][:df.num_nst]
#     elif key[-1] == 'o':
#      init2[key] = df.define_init[key][:df.num_ost]
#else:
#  init2=None

## -- temporary fix
if df.do_init3:
  #init3={}
  #if argsin['override_init']:
  init3 = make_adv_init_from_fit_file_3pt(models3,'fit_adv_'+irrepStr+'_3pt',\
   fresh_overlap=True,fresh_amplitude=True)
else:
  init3=None
pass 

## -- temporary
init2=None
#init3=None
print init3


fitter2 = CorrFitter(models=models2,maxit=df.maxit)
fitter3 = CorrFitter(models=models,maxit=df.maxit)
#print models
#raise ValueError('test')
print
print 'prior: '
for key in sorted(priors):
 print key,priors[key]
#print
#print 'init : ',init3
#for key in init3:
# print key,init3[key]
print
if df.do_2pt:
 print "starting 2pt fit..."
 fit2 = fitter2.lsqfit(data=dall,prior=priors2,p0=init2,svdcut=df.svdcut)
 ## -- fits take a long time, so print prematurely
 print_fit(fit2,priors2)
if df.do_3pt:
 print "starting 3pt fit..."
 #print 'init',init3
 #print 'prior',priors
 fit3 = fitter3.lsqfit(data=dall,prior=priors,p0=init3,svdcut=df.svdcut)
else:
 print "Ignoring 3pt fit!"
 fit3=None

#print 'transformed ',fit3.transformed_p
#print
#print 'params      ',fit3.p
#print
#print 'fit0 ',models[0].datatag,models[0].fitfcn(fit3.p)
#print
#print 'fit44 ',models[0].datatag
#test = models[0].testfitfcn(fit3.transformed_p)
#print "final:"
#print list(np.transpose([-fit3.p['logc4o_0']*fit3.p['k4o_0']*((-1)**t)*gv.exp(-(48-t)*fit3.p['logEo_0']) for t in range(2,10)])[0])
#print 
#print list(np.transpose([gv.exp(fit3.p['logc4n_0'])*fit3.p['k4n_0']*gv.exp(-t*gv.exp(fit3.p['logEn_0']))+gv.exp(fit3.p['logc4o_0'])*fit3.p['k4o_0']*((-1)**t)*gv.exp(-t*gv.exp(fit3.p['logEo_0'])) for t in range(2,10)])[0])
#print
#print list(np.transpose([-fit3.p['logc4n_0']*fit3.p['k4n_0']*gv.exp(-t*fit3.p['logEn_0'])+fit3.p['logc4o_0']*fit3.p['k4o_0']*((-1)**t)*gv.exp(-t*fit3.p['logEo_0']) for t in range(2,10)])[0])

#print
#print 'fit44 ',models[4].datatag
#print models[4].fitfcn(fit3.p)
#print 
#print [gv.exp(fit3.p['logc4n_0'])*fit3.p['k4n_0']*gv.exp(-t*fit3.p['logEn_0'])+gv.exp(fit3.p['logc4o_0'])*fit3.p['k4o_0']*((-1)**t)*gv.exp(-t*fit3.p['logEo_0']) for t in range(2,10)]

## -- save fit as an initial value dictionary
if df.do_irrep == "16":
 irrepStr = '16'
if df.do_2pt:
 save_init_from_fit(fit2,'fit_adv_'+irrepStr+'_2pt.py')
if df.do_3pt:
 save_init_from_fit(fit3,'fit_adv_'+irrepStr+'_3pt.py',df.do_v_symmetric)

#fit3 = fitter3.lsqfit(data=dall,prior=priors,svdcut=df.svdcut)
print fmt_reduced_chi2(fit3)
#save_data('./test.fit.out',fit,dall)

## -- print
#if df.do_2pt:
# print_fit(fit2,priors2)
print_fit(fit3,priors,df.do_v_symmetric)

### -- save fit as an initial value dictionary
#if df.do_irrep == "16":
# irrepStr = '16'
#if df.do_2pt:
# save_init_from_fit(fit2,'fit_dict'+irrepStr+'_2pt.py')
#if df.do_3pt:
# save_init_from_fit(fit3,'fit_dict'+irrepStr+'_3pt.py',df.do_v_symmetric)

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

## -- plot
if df.do_plot or argsin['override_plot']:
 #plot_corr_effective_mass_check(models2,dall,None,**df.fitargs)
 #plot_corr_effective_mass(models2,dall,None,**df.fitargs)
 #plot_corr_double_log(models2,dall,fit3,**df.fitargs)
 #plot_corr_adv_dl_folded(models2,dall,fit3,req=None,**df.fitargs)
 #plot_corr_adv_dl_folded(models2,dall,fit3,req=[[0],list()],**df.fitargs)
 #plot_corr_adv_dl_folded(models2,dall,fit3,req=[[1],list()],**df.fitargs)
 #plot_corr_adv_dl_folded(models2,dall,fit3,req=[list(),[0]],**df.fitargs)
 #plot_corr_adv_dl_folded(models2,dall,fit3,req=[list(),[1]],**df.fitargs)
 #plot_corr_adv_dl_folded(models2,dall,fit3,req=[list(),[0,1]],**df.fitargs)
 #plot_corr_normalized(models2,dall,fit3,**df.fitargs)
 if df.do_3pt:
  #plot_corr_3pt(models3,dall,fit3,**df.fitargs)
  pass
 if df.do_plot_terminal:
  plt.show()

#if df.do_sn_minimize:
# ## -- shortcut
# cvec6,kvec6,_ = sn_minimize_postload_3pt(dall,6,'aiai')
# cvec7,kvec7,_ = sn_minimize_postload_3pt(dall,7,'aiai')
# print "source vectors:"
# print cvec6
# print cvec7
# print "sink vectors:"
# print kvec6
# print kvec7
# clist = list()
# klist = list()
# for key in dall:
#  ## -- deconstruct key based on current conventions
#  tkey = 't'.join(key.split('t')[:-1])
#  if len(tkey) == 0:
#   continue
#  k = int(tkey[-1])
#  if not(k in klist):
#   klist.append(k)
#  c = int(tkey[-2])
#  if not(c in clist):
#   clist.append(c)
# call6 = list()
# call7 = list()
# for i,c in zip(range(len(clist)),sorted(clist)):
#  call6.append(list(np.zeros(len(klist))))
#  call7.append(list(np.zeros(len(klist))))
#  for j,k in zip(range(len(klist)),sorted(klist)):
#   call6[i][j] = dall['aiais'+str(c)+str(k)+'t6']
#   call7[i][j] = dall['aiais'+str(c)+str(k)+'t7']
# cdia6 = diagonalize_correlator(call6,cvec6,kvec6)
# cdia7 = diagonalize_correlator(call7,cvec6,kvec6)
# #ddia = {}
# for i,c in zip(range(len(clist)),sorted(clist)):
#  for j,k in zip(range(len(klist)),sorted(klist)):
#   dall['aiais'+str(c)+str(k)+'t6'] = cdia6[i][j]
#   dall['aiais'+str(c)+str(k)+'t7'] = cdia7[i][j]
# #kwargs = df.fitargs
# for key in dall:
#  tkey = 't'.join(key.split('t')[:-1]) 
#  if len(tkey) > 0:
#   df.fitargs[tkey]["p3_save_name"] = \
#    "s3-s8p-l3248-coul-"+tkey+".pdf"
#   df.fitargs[tkey]["y_scale"] = [-.2,.6]
#   df.fitargs[tkey]["yaxistitle"] = r"$\beta v_{i}^{T}C_{ij}w_{j}(t,T)$"
# plot_corr_3pt(models3,dall,fit3,**df.fitargs)
# plt.show()
