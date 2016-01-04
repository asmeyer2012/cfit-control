import gvar as gv
import numpy as np
import defines as df
import define_prior as dfp
import util_funcs as utf

def make_prior(models,prior_dict=None,nst=-1,ost=-1):
 prior = gv.BufferDict()
 
 for model in models:
  skey=model.all_datatags[0]

  if prior_dict is None: ## -- take default from defines
   if (nst > -1 and ost > -1):
    dprior = utf.get_prior_dict(df.define_prior,
     df.define_prior['nkey'],df.define_prior['okey'],nst,ost)
   else:
    dprior = utf.get_prior_dict(df.define_prior,
     df.define_prior['nkey'],df.define_prior['okey'],df.num_nst,df.num_ost)
   for pkey in dprior[skey]:
    prior[pkey]=dprior[skey][pkey]

   ## -- logarithmize the logarithmic coefficients
   for pkey in prior:
    ## -- don't do logs unless they are in the current model, else double counting
    if not(pkey[3:] in model.a+model.b+model.dE) and\
       not(pkey[4:] in model.a+model.b+model.dE):
     continue
    if pkey[:3] == 'log':
     prior[pkey] = gv.log(prior[pkey])
    elif pkey[:4] == 'sqrt':
     prior[pkey] = gv.sqrt(prior[pkey])
  else: ## -- allow passing of new prior, for chained operations
   if (nst > -1 and ost > -1):
    dprior = utf.get_prior_dict(prior_dict,
     prior_dict['nkey'],prior_dict['okey'],nst,ost)
   else:
    dprior = utf.get_prior_dict(prior_dict,
     prior_dict['nkey'],prior_dict['okey'],df.num_nst,df.num_ost)
   for pkey in dprior[skey]:
    prior[pkey]=dprior[skey][pkey]

   for pkey in prior:
    if not(pkey[3:] in model.a+model.b+model.dE) and\
       not(pkey[4:] in model.a+model.b+model.dE):
     continue
    if pkey[:3] == 'log':
     prior[pkey] = gv.log(prior[pkey])
    elif pkey[:4] == 'sqrt':
     prior[pkey] = gv.sqrt(prior[pkey])

 return prior
