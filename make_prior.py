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
    bkey = utf.get_basekey(pkey)
    #if not(pkey[3:] in model.a+model.b+model.dE) and\
    #   not(pkey[4:] in model.a+model.b+model.dE):
    if not(bkey[1] in model.a+model.b+model.dE):
     continue
    if bkey[0] == 'log':
     negcheck = filter(lambda x: x[1].mean < 0,enumerate(prior[pkey]))
     if len(negcheck) > 0:
      raise ValueError("Prior indices ",list(np.array(negcheck)[:,0]),
       " have negative values, key ",pkey)
     prior[pkey] = gv.log(prior[pkey])
    elif bkey[0] == 'sqrt':
     negcheck = filter(lambda x: x[1].mean < 0,enumerate(prior[pkey]))
     if len(negcheck) > 0:
      raise ValueError("Prior indices ",list(np.array(negcheck)[:,0]),
       " have negative values, key ",pkey)
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
    bkey = utf.get_basekey(pkey)
    #if not(pkey[3:] in model.a+model.b+model.dE) and\
    #   not(pkey[4:] in model.a+model.b+model.dE):
    if not(bkey[1] in model.a+model.b+model.dE):
     continue
    if bkey[0] == 'log':
     prior[pkey] = gv.log(prior[pkey])
    elif bkey[0] == 'sqrt':
     prior[pkey] = gv.sqrt(prior[pkey])

 return prior

def truncate_prior_states(prior,nn,no,nn3=-1,no3=-1,do_symm=False):
 ## -- reduce to nn even and no odd states
 ##    highest energy states are removed before lower-energy states
 nn3x = nn
 no3x = no
 if nn3 > -1:
   nn3x = min(nn3,nn)
 if no3 > -1:
   no3x = min(no3,no)

 ## -- build new prior dictionary
 newprior = gv.BufferDict()
 for key in prior:
  kp = len(prior[key])
  bkey = utf.get_basekey(key)
  try:
   ## -- only works if prior is a matrix; 3-point currents
   lp = len(prior[key][0])
   for v, x1, x2 in [('nn',nn3x,nn3x),('no',nn3x,no3x),('on',no3x,nn3x),('oo',no3x,no3x)]:
    if bkey[1][-2:] == v:
     #print v,x1,x2,key,len(prior[key]),len(prior[key][0])
     if x1 == 0 and x2 == 0:
      continue
     elif len(prior[key]) < x1 and len(prior[key][0]) < x2:
      tmp = prior[key]
      tmp = np.pad(tmp,((0,x1-len(prior[key])),(0,x2-len(prior[key]))),'constant',
       constant_values=((.1,.1),(.1,.1)))
     else:
      tmp = prior[key][slice(None,x1),slice(None,x2)]
     ## -- flatten matrix to upper triangle only if that is needed
     if (v == 'nn' or v == 'oo') and do_symm:
      tmp = utf.truncate_upper_triangle(tmp,x1)
     newprior[key] = tmp
  except (IndexError,TypeError):
   ## -- 3-point matrix diagonals for symmetric
   for v, x1 in [('nn',nn3x),('oo',no3x)]:
    if bkey[1][-2:] == v:
     pass
     #print 'test',key
     #if x1 == 0:
     # newprior[key] = prior[key]
     #else:
     # kpt = int(np.round(np.sqrt(1+8*kp))-1)/2
     # ## -- reconstruct and truncate to new size
     # tmp = np.array(utf.reconstruct_upper_triangle(prior[key],kpt))
     # newprior[key] = utf.truncate_upper_triangle(tmp,x1)
   ## -- everything else
   if (bkey[1][-2:] != 'nn') and (bkey[1][-2:] != 'oo'):
    for v, x1 in [('n',nn),('o',no)]:
     if bkey[1][-1] != v:
      continue
     if x1 == 0:
      continue
     elif x1 >= kp:
      newprior[key] = prior[key]
     else:
      newprior[key] = prior[key][slice(None,x1)]
 return newprior
