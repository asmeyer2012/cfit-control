import gvar as gv
import numpy as np
import defines as df

def make_prior(models=None,priorkey=None):
 prior = gv.BufferDict();
 
 if models is None:
  pass;
 else:
  if priorkey is None:
   skey=models[0].all_datatags[0];
  else:
   skey=priorkey; ## -- fix later

  for pkey in df.define_prior[skey]:
   prior[pkey]=df.define_prior[skey][pkey];

  for pkey in prior: # logarithmize the logarithmic coefficients
   if pkey[:3] == 'log':
    prior[pkey] = gv.log(prior[pkey]);

 return prior;
