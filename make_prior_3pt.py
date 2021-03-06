import gvar as gv
import numpy as np
import defines as df
import define_prior as dfp
import define_prior_3pt as dfp3
import util_funcs as utf

def make_prior_stacked_3pt(models,prior_dict=None,nst=-1,ost=-1,n3st=-1,o3st=-1):
 prior = gv.BufferDict()
 
 for model in models:
  skey=model.all_datatags[0]

  if prior_dict is None: ## -- take default from defines
   if (nst > -1 and ost > -1):
    dprior = utf.get_prior_dict(df.define_prior_3pt,
     df.define_prior_3pt['nkey'],df.define_prior_3pt['okey'],nst,ost,
     df.define_prior_3pt['vkey'],n3st,o3st)
   else:
    dprior = utf.get_prior_dict(df.define_prior_3pt,
     df.define_prior_3pt['nkey'],df.define_prior_3pt['okey'],df.num_nst,df.num_ost,
     df.define_prior_3pt['vkey'],df.num_nst_3pt,df.num_ost_3pt)
   for pkey in dprior[skey]:
    prior[pkey]=dprior[skey][pkey]

   ## -- logarithmize the logarithmic coefficients
   for pkey in prior:
    ## -- don't do logs unless they are in the current model, else double counting
    bkey = utf.get_basekey(pkey)
    if not(bkey[1] in model.a+model.b+model.dEa+model.dEb):
     continue
    if bkey[0] == 'log':
     prior[pkey] = gv.log(prior[pkey])
    elif bkey[0] == 'sqrt':
     prior[pkey] = gv.sqrt(prior[pkey])
  else: ## -- allow passing of new prior, for chained operations
   if (nst > -1 and ost > -1):
    dprior = utf.get_prior_dict(prior_dict,
     prior_dict['nkey'],prior_dict['okey'],nst,ost,prior_dict['vkey'],n3st,o3st)
   else:
    dprior = utf.get_prior_dict(prior_dict,
     prior_dict['nkey'],prior_dict['okey'],df.num_nst,df.num_ost,
     prior_dict['vkey'],df.num_nst_3pt,df.num_ost_3pt)
   for pkey in dprior[skey]:
    prior[pkey]=dprior[skey][pkey]

   for pkey in prior:
    bkey = utf.get_basekey(pkey)
    if not(bkey[1] in model.a+model.b+model.dEa+model.dEb):
     continue
    if bkey[0] == 'log':
     prior[pkey] = gv.log(prior[pkey])
    elif bkey[0] == 'sqrt':
     prior[pkey] = gv.sqrt(prior[pkey])

 return prior

def make_prior_3pt(models,prior_dict=None,nst=-1,ost=-1,n3st=-1,o3st=-1,do_amp_prior=True):
 prior = gv.BufferDict()
 
 for model in models:
  skey=model.all_datatags[0]

  if prior_dict is None: ## -- take default from defines
   if (nst > -1 and ost > -1):
    dprior = utf.get_prior_dict(df.define_prior_3pt,
     df.define_prior_3pt['nkey'],df.define_prior_3pt['okey'],nst,ost,
     df.define_prior_3pt['vkey'],n3st,o3st,
     do_v_symm=df.do_v_symmetric,do_amp_prior=df.do_amp_prior)
   else:
    dprior = utf.get_prior_dict(df.define_prior_3pt,
     df.define_prior_3pt['nkey'],df.define_prior_3pt['okey'],df.num_nst,df.num_ost,
     df.define_prior_3pt['vkey'],df.num_nst_3pt,df.num_ost_3pt,
     do_v_symm=df.do_v_symmetric,do_amp_prior=df.do_amp_prior)
   for pkey in dprior[skey]:
    prior[pkey]=dprior[skey][pkey]

   ## -- logarithmize the logarithmic coefficients
   for pkey in prior:
    ## -- don't do logs unless they are in the current model, else double counting
    bkey = utf.get_basekey(pkey)
    if not(bkey[1] in model.a+model.b+model.dEa+model.dEb):
     continue
    if bkey[0] == 'log':
     #print pkey,prior[pkey]
     prior[pkey] = gv.log(prior[pkey])
    elif bkey[0] == 'sqrt':
     prior[pkey] = gv.sqrt(prior[pkey])
  else: ## -- allow passing of new prior, for chained operations
   if (nst > -1 and ost > -1):
    dprior = utf.get_prior_dict(prior_dict,
     prior_dict['nkey'],prior_dict['okey'],nst,ost,prior_dict['vkey'],n3st,o3st,df.do_v_symmetric)
   else:
    dprior = utf.get_prior_dict(prior_dict,
     prior_dict['nkey'],prior_dict['okey'],df.num_nst,df.num_ost,
     prior_dict['vkey'],df.num_nst_3pt,df.num_ost_3pt,df.do_v_symmetric)
   for pkey in dprior[skey]:
    prior[pkey]=dprior[skey][pkey]

   for pkey in prior:
    bkey = utf.get_basekey(pkey)
    if not(bkey[1] in model.a+model.b+model.dEa+model.dEb):
     continue
    if bkey[0] == 'log':
     prior[pkey] = gv.log(prior[pkey])
    elif bkey[0] == 'sqrt':
     prior[pkey] = gv.sqrt(prior[pkey])

 return prior
