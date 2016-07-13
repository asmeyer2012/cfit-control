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
from plot_corr_normalized     import plot_corr_normalized
from meta_data                import *
from util_files               import read_fit_file
import defines           as df
import define_prior      as dfp
import define_prior_3pt  as dfp3
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np
import sys

## -- assume that data has already been parsed into import files, complete with config tags
td = {}
dset = {}
davg = {}

td['2pt'] = import_corfit_file('l32.bar2pt.8m')
td['v4v4','t6'] = import_corfit_file('l32.bar3pt.8m.v4v4.t06.p00')
td['v4v4','t7'] = import_corfit_file('l32.bar3pt.8m.v4v4.t-7.p00')

## -- pre-consolidation manipulation
pass

for key in td:
 dset[key] = consolidate_tags(td[key])

## -- post-consolidation manipulation
pass

dnavg = gv.dataset.Dataset()
for key in dset:
 for xkey in dset[key]:
  dnavg[xkey] = dset[key][xkey]
dall = gv.dataset.avg_data(dnavg)
  
#for key in dset:
# davg[key] = gv.dataset.avg_data(dset[key])
#dall = gv.dataset.Dataset()
#for key in dset:
# dall = cat_dataavg(dall,davg[key])

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

fitter2 = CorrFitter(models=models2,maxit=df.maxit)
fitter3 = CorrFitter(models=models,maxit=df.maxit)
fit2 = fitter2.lsqfit(data=dall,prior=priors2,svdcut=df.svdcut)
fit3 = fitter3.lsqfit(data=dall,prior=priors,svdcut=df.svdcut)
#save_data('./test.fit.out',fit,dall)
print_fit(fit2,priors2)
print_fit(fit3,priors)

#fit = fitter.chained_lsqfit(data=data, prior=prior)
#fit = fitter.lsqfit(data=data, prior=fit.p)
#fit = fitter.lsqfit(data=data,prior=prior,p0="test.init.out",svdcut=df.svdcut)
#if df.do_2pt:
#  if df.do_initial:
#   try:
#    p0={}
#    for key in df.define_init:
#     if key[-1] == 'o':
#      p0[key] = df.define_init[key][:df.num_ost]
#     else:
#      p0[key] = df.define_init[key][:df.num_nst]
#    fit = fitter.lsqfit(data=data,prior=prior,p0=p0,svdcut=df.svdcut)
#   except KeyError:
#    print "Could not use initial point definitions"
#    fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
#  else:
#   fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
#  #bs_avg = make_bootstrap(fitter,dset,df.mdp.n_bs)
#  print_fit(fit,prior)
#  print_error_budget(fit)
#  #save_data(mdp.output_path +'/'+ mdp.fit_fname,fit,data)
#  save_data('./test.fit.out',fit,data)
#  save_prior_from_fit(df.define_prior,df.define_model,fit,"test.prior.out",
#    round_e=2,round_a=1,preserve_e_widths=True,preserve_a_widths=True)
#  
#  if df.do_plot:
#   if df.do_default_plot:
#    fitter.display_plots()
#   plot_corr_double_log(models,data,fit,**df.fitargs)
#   plot_corr_normalized(models,data,fit,**df.fitargs)
#   plt.show()
#pass #do_2pt
