import numpy as np
import gvar as gv
import lsqfit as lsf
import util_funcs as utf

def get_option(key,default,**kwargs):
 try:
  return kwargs[key]
 except KeyError:
  return default

def create_fit_func(model,fit):
 try:
  tfp = fit.transformed_p
 except AttributeError:
  ## -- prior was input instead
  tfp = fit
 pass
 tfk = tfp.keys()
 tps = ( 1 if model.tp > 0 else -1) ## -- symmetry or antisymmetry factor
 tpa = abs(model.tp)
 ## -- find keys and ensure they are tuples
 akey = model.a
 bkey = model.b
 Ekey = model.dE
 try:
  akey[0]
 except IndexError:
  akey = (akey,)
 try:
  bkey[0]
 except IndexError:
  bkey = (bkey,)
 try:
  Ekey[0]
 except IndexError:
  Ekey = (Ekey,)
 la = {}
 lb = {}
 lE = {}
 ## -- save data to dictionaries
 for key in akey:
  if key[:3] == 'log':
   la[key[3:]] = gv.exp(tfp[key])
  elif key[:4] == 'sqrt':
   la[key[4:]] = [x*x for x in tfp[key]]
  else:
   la[key] = tfp[key]
 for key in bkey:
  if key[:3] == 'log':
   lb[key[3:]] = gv.exp(tfp[key])
  elif key[:4] == 'sqrt':
   lb[key[4:]] = [x*x for x in tfp[key]]
  else:
   lb[key] = tfp[key]
 for key in Ekey:
  if key[:3] == 'log':
   lE[key[3:]] = gv.exp(tfp[key])
  elif key[:4] == 'sqrt':
   lE[key[4:]] = [x*x for x in tfp[key]]
  else:
   lE[key] = tfp[key]
 ## -- sort out odd/even function to create
 try:
  do_evn = abs(model.s[0]) > 0
 except TypeError:
  do_evn = True
 try:
  do_odd = abs(model.s[1]) > 0
 except TypeError:
  do_odd = False
 if do_odd and do_evn:
  ## -- assume the first key is the even state and the second is the odd
  if len(la[akey[0]]) == 0:
   #print "even priors not available"
   do_evn = False
  if len(la[akey[1]]) == 0:
   #print "odd priors not available"
   do_odd = False
 pass
 ## -- finish constructing functions
 if bool(do_odd) ^ bool(do_evn): # xor
  lc = la[akey[0]]*lb[bkey[0]]
  for key in Ekey:
   lE[key] = ut.sum_dE(lE[key])
  if do_odd: ## -- odd only
   def new_func(t):
    return list(model.s[1]*gv.cos([np.pi*x for x in t])*(
     np.array([np.dot(lco,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lEo))]) +\
     np.array([np.dot(lco,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lEo))]) ) )
  else:
   try: ## -- even only, make sure to deal with s correctly
    def new_func(t):
     return list(model.s[0]*(
          np.array([np.dot(lc,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lE))]) +\
      tps*np.array([np.dot(lc,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lE))]) ))
   except TypeError:
    def new_func(t):
     return list(model.s*(
          np.array([np.dot(lc,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lE))]) +\
      tps*np.array([np.dot(lc,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lE))]) ))
  return new_func
 else:
  lcn = la[akey[0]]*lb[bkey[0]]
  lco = la[akey[1]]*lb[bkey[1]]
  lEn = utf.sum_dE(lE[Ekey[0]])
  lEo = utf.sum_dE(lE[Ekey[1]])
  def new_func(t):
   ## -- even and odd
   return list(model.s[0]*(
        np.array([np.dot(lcn,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lEn))]) +\
    tps*np.array([np.dot(lcn,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lEn))]) )+\
    model.s[1]*gv.cos([np.pi*x for x in t])*(
        np.array([np.dot(lco,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lEo))]) +\
    tps*np.array([np.dot(lco,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lEo))]) ) )
  return new_func
pass
