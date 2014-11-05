from corrfitter     import CorrFitter
from make_data      import make_data
from make_data_db   import make_data_db
from make_models    import make_models
from make_models    import *
from make_prior     import make_prior
from make_bootstrap import make_bootstrap
from print_results  import print_fit
from print_results  import print_error_budget
from save_data      import save_data
from make_plot      import make_plot
from meta_data      import *
import defines      as df
import gvar         as gv
import gvar.dataset as gvd

if df.do_db:
 ## -- for database input
 ##    - (database file name defined in make_data_db.py)
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,do_db=True);
 models = make_models(data=data,lkey=df.lkey);
 prior = make_prior(models);
else:
 ## -- for raw correlator file input
 data,dset = make_data(df.mdp,do_makedata=df.do_makedata,\
                       do_db=False,filename="./import-correlators");
 models = make_models(mdp=df.mdp);
 prior = make_prior(models);
## --

fitter = CorrFitter(models=models,maxit=df.maxit);
#fit = fitter.chained_lsqfit(data=data, prior=prior);
#fit = fitter.lsqfit(data=data, prior=fit.p);
fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut);
#bs_avg = make_bootstrap(fitter,dset,df.mdp.n_bs);
print_fit(fit,prior);
print_error_budget(fit);
#save_data(mdp.output_path +'/'+ mdp.fit_fname,fit,data);

if df.do_plot:
 if df.do_default_plot:
  fitter.display_plots();
 make_plot(models,data,fit);

