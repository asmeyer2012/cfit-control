import gvar as gv
import gvar.dataset as gvd
#import multiprocessing ## -- parallelization

def make_bootstrap(fitter,dset,n_bs):
 bs_datalist = (gvd.avg_data(d) for d in gvd.bootstrap_iter(dset,n_bs));
 bs = gvd.Dataset();
 for bs_fit in fitter.bootstrap_iter(bs_datalist):
  p = bs_fit.pmean;
  for key in p:
   if key[:3] == 'log':
    bs.append(key[3:],gv.exp(p[key]));
   else:
    bs.append(key,p[key]);
 bs_avg = gvd.avg_data(bs,bstrap=True);
 return bs_avg;
