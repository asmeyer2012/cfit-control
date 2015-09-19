import gvar as gv
import numpy as np
import defines as df

def make_prior(models,prior_dict=None):
 prior = gv.BufferDict()
 
 for model in models:
  skey=model.all_datatags[0]

  if prior_dict is None: ## -- take default from defines
   for pkey in df.define_prior[skey]:
    prior[pkey]=df.define_prior[skey][pkey]

   ## -- logarithmize the logarithmic coefficients
   for pkey in prior:
    ## -- don't do logs unless they are in the current model, else double counting
    if not(pkey[3:] in model.a+model.b+model.dE):
     continue
    if pkey[:3] == 'log':
     prior[pkey] = gv.log(prior[pkey])
  else: ## -- allow passing of new prior, for chained operations
   for pkey in prior_dict[skey]:
    prior[pkey]=prior_dict[skey][pkey]

   for pkey in prior:
    if not(pkey[3:] in model.a+model.b+model.dE):
     continue
    if pkey[:3] == 'log':
     prior[pkey] = gv.log(prior[pkey])

 return prior
