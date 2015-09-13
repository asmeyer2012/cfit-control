import gvar as gv
import numpy as np
import defines as df

def make_prior(models=None,priorkey=None):
 prior = gv.BufferDict()
 
 if models is None:
  pass
 else:
  for model in models:
   if priorkey is None:
    skey=model.all_datatags[0]
   else:
    skey=priorkey ## -- fix later

   for pkey in df.define_prior[skey]:
    prior[pkey]=df.define_prior[skey][pkey]

   for pkey in prior: # logarithmize the logarithmic coefficients
    if not(pkey[3:] in model.a+model.b+model.dE): # don't do logs unless they are in the model
     continue
    if pkey[:3] == 'log':
     prior[pkey] = gv.log(prior[pkey])

 return prior
