from corrfitter           import CorrFitter
from make_data            import make_data
from make_data_db         import make_data_db
from make_models          import make_models
#from make_models          import *
from make_prior           import make_prior
from make_bootstrap       import make_bootstrap
from print_results        import print_fit
from print_results        import print_error_budget
from save_data            import save_data
from save_prior           import save_prior_from_fit
from make_plot            import make_plot
from make_plot            import make_plot_corr_neg
from make_plot            import make_plot_1plus1
from plot_corr_double_log import plot_corr_double_log
from plot_corr_normalized import plot_corr_normalized
from meta_data            import *
from util_files           import read_fit_file
import defines           as df
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np

if df.do_db:
 ## -- for database input
 ##    - (database file name defined in make_data_db.py)
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,do_db=True)
 models = make_models(data=data,lkey=df.lkey)
 prior = make_prior(models)
else:
 ## -- for raw correlator file input
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,\
                       do_db=False,filename="./import-correlators")
 #models = make_models(mdp=df.mdp)
 models = make_models(data=data,lkey=df.lkey)
 prior = make_prior(models)
## --

if df.do_uncorr:
 ## -- remove the correlations from the data
 dataCorr = data
 datlen = len(gv.evalcov(data)['Gaa','Gaa'])
 fakecov = np.zeros((datlen,datlen))
 for i in range(datlen):
  fakecov[i,i] = np.diag(gv.evalcov(data)['Gaa','Gaa'])[i]
 data['Gaa'] = gv.gvar([data['Gaa'][i].mean for i in range(datlen)],np.array(fakecov))
## --

fitter = CorrFitter(models=models,maxit=df.maxit)
#fit = fitter.chained_lsqfit(data=data, prior=prior)
#fit = fitter.lsqfit(data=data, prior=fit.p)
fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
#bs_avg = make_bootstrap(fitter,dset,df.mdp.n_bs)
print_fit(fit,prior)
print_error_budget(fit)
#save_data(mdp.output_path +'/'+ mdp.fit_fname,fit,data)
save_data('./test.fit.out',fit,data)
save_prior_from_fit(df.define_prior,df.define_model,fit,"test.prior.out",
  round_e=2,round_a=1,preserve_e_widths=True,preserve_a_widths=True)

if df.do_plot:
 if df.do_default_plot:
  fitter.display_plots()
 #plot_corr_double_log(models,data,fit,**df.fitargs)
 plot_corr_normalized(models,data,fit,**df.fitargs)
 plt.show()
 #make_plot_corr_neg(models,data,fit,prior)
 #make_plot(models,data,fit)
 if df.do_effmass:
  make_plot_1plus1(models,data,fit)

