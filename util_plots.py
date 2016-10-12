import numpy as np
import gvar as gv
import lsqfit as lsf
import util_funcs as utf

do_v_symm = True

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
  ## -- sloppy... I think this is handled incorrectly
  lc = la[akey[0]]*lb[bkey[0]]
  #for key in Ekey:
  # lE[key] = ut.sum_dE(lE[key])
  if do_evn:
    lE = ut.sum_dE(lE[Ekey[0]])
  else:
    lE = ut.sum_dE(lE[Ekey[1]])
  if do_odd: ## -- odd only
   def new_func(t):
    return list(model.s[1]*gv.cos([np.pi*x for x in t])*(
     np.array([np.dot(lco,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lE))]) +\
     np.array([np.dot(lco,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lE))]) ) )
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

def create_fit_func_3pt(model,fit):
 try:
  tfp = fit.transformed_p
 except AttributeError:
  ## -- prior was input instead
  tfp = fit
 pass
 tfk = tfp.keys()
 tpsa = ( 1 if model.tpa > 0 else -1) ## -- symmetry or antisymmetry factor
 tpsb = ( 1 if model.tpb > 0 else -1) ## -- symmetry or antisymmetry factor
 tpa = abs(model.tpa)
 tpb = abs(model.tpb)
 ## -- find keys and ensure they are tuples
 akey = model.a
 bkey = model.b
 Eakey = model.dEa
 Ebkey = model.dEb
 ## -- just assume that everything is odd+even
 #try:
 # akey[0]
 #except IndexError:
 # akey = (akey,)
 #try:
 # bkey[0]
 #except IndexError:
 # bkey = (bkey,)
 #try:
 # Eakey[0]
 #except IndexError:
 # Eakey = (Eakey,)
 #try:
 # Ebkey[0]
 #except IndexError:
 # Ebkey = (Ebkey,)
 la = {}
 lb = {}
 lEa = {}
 lEb = {}
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
 for key in Eakey:
  if key[:3] == 'log':
   lEa[key[3:]] = gv.exp(tfp[key])
  elif key[:4] == 'sqrt':
   lEa[key[4:]] = [x*x for x in tfp[key]]
  else:
   lEa[key] = tfp[key]
 for key in Ebkey:
  if key[:3] == 'log':
   lEb[key[3:]] = gv.exp(tfp[key])
  elif key[:4] == 'sqrt':
   lEb[key[4:]] = [x*x for x in tfp[key]]
  else:
   lEb[key] = tfp[key]
 ## -- sort out odd/even function to create
 ## -- same result for sb
 #try:
 # do_evn = abs(model.sa[0]) > 0
 #except TypeError:
 # do_evn = True
 #try:
 # do_odd = abs(model.sa[1]) > 0
 #except TypeError:
 # do_odd = False
 #if do_odd and do_evn:
 # ## -- assume the first key is the even state and the second is the odd
 # if len(la[akey[0]]) == 0:
 #  #print "even priors not available"
 #  do_evn = False
 # if len(la[akey[1]]) == 0:
 #  #print "odd priors not available"
 #  do_odd = False
 #pass
 ## -- define prototype functions
 def fn_evn(a,e,t,ts):
  return np.array([x*y for x,y in zip(a,gv.exp(-np.outer(e,t)))]) +\
    np.sign(ts)*np.array([x*y for x,y in zip(a,gv.exp(-np.outer(e,np.abs(ts)-np.array(t))))])
 def fn_odd(a,e,t,ts):
  return np.cos(np.pi*np.array(t))*fn_evn(a,e,t,ts)
 ## -- finish constructing functions
 ## -- assuming only even+odd
 #if bool(do_odd) ^ bool(do_evn): # xor
 # #
 # lc = la[akey[0]]*lb[bkey[0]]
 # for key in Eakey:
 #  lEa[key] = ut.sum_dE(lEa[key])
 # for key in Ebkey:
 #  lEb[key] = ut.sum_dE(lEb[key])
 # #
 # if do_evn:
 #  for key in model.Vnn:
 #    lv[key] = tfp[key]
 # elif do_odd:
 #  for key in model.Voo:
 #    lv[key] = tfp[key]
 # if do_odd: ## -- odd only
 #  def new_func(t,T,tsa,tsb):
 #   return list(model.sa[1]*model.sb[1]*np.array([np.sum(x) for x in\
 #    np.transpose(np.dot(lv,fn_odd(la,lEa,t,tsa))*fn_odd(lb,lEb,T-np.array(t),tsb))]))
 #   #return list(model.s[1]*gv.cos([np.pi*x for x in t])*(
 #   # np.array([np.dot(lco,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lEo))]) +\
 #   # np.array([np.dot(lco,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lEo))]) ) )
 # else:
 #  try: ## -- even only, make sure to deal with s correctly
 #   def new_func(t,ts):
 #    return list(model.s[0]*(
 #         np.array([np.dot(lc,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lE))]) +\
 #     tps*np.array([np.dot(lc,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lE))]) ))
 #  except TypeError:
 #   def new_func(t,ts):
 #    return list(model.s*(
 #         np.array([np.dot(lc,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lE))]) +\
 #     tps*np.array([np.dot(lc,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lE))]) ))
 # return new_func
 #else:
 lan = la[akey[0]]
 lao = la[akey[1]]
 lbn = lb[bkey[0]]
 lbo = lb[bkey[1]]
 lEan = utf.sum_dE(lEa[Eakey[0]])
 lEao = utf.sum_dE(lEa[Eakey[1]])
 lEbn = utf.sum_dE(lEb[Ebkey[0]])
 lEbo = utf.sum_dE(lEb[Ebkey[1]])
 tsa = model.tpa
 tsb = model.tpb
 T = model.T
 ## -- of course the new one is different, typical
 #if df.do_v_symmetric:
 if do_v_symm:
  lvnn = utf.reconstruct_upper_triangle(tfp[model.V[0][0]],
   int(np.sqrt(8*len(tfp[model.V[0][0]])+1)-1)/2)
  lvoo = utf.reconstruct_upper_triangle(tfp[model.V[1][1]],
   int(np.sqrt(8*len(tfp[model.V[1][1]])+1)-1)/2)
  lvno = tfp[model.V[0][1]]
  lvon = np.transpose(tfp[model.V[0][1]])
 else:
  lvnn = tfp[model.V[0][0]]
  lvoo = tfp[model.V[1][1]]
  lvno = tfp[model.V[0][1]]
  lvon = tfp[model.V[1][0]]
 nn = len(lvnn)
 no = len(lvoo)
 ## need to resize arrays if matrix is not same size as parameter list length
 nt = np.abs(model.tpa)
 def new_func(t):
  #print no,len(t)
  #print np.shape(np.transpose(lvon)),np.transpose(lvon)
  #print np.shape(np.resize(fn_odd(lao,lEao,t,tsa),(no,len(t)))),
  # np.resize(fn_odd(lao,lEao,t,tsa),(no,len(t)))
  #print np.dot(np.transpose(lvon),np.resize(fn_odd(lao,lEao,t,tsa),(no,len(t))))
  #print np.resize(fn_evn(lbn,lEbn,T-np.array(t),tsb),(nn,len(t)))
  #print np.transpose(np.dot(np.transpose(lvon),np.resize(fn_odd(lao,lEao,t,tsa),(no,len(t))))*\
  # np.resize(fn_evn(lbn,lEbn,T-np.array(t),tsb),(nn,len(t))))
  #print model.sa[1]*model.sb[0]*np.array([np.sum(x) for x in\
  # np.transpose(np.dot(np.transpose(lvon),np.resize(fn_odd(lao,lEao,t,tsa),(no,len(t))))*\
  # np.resize(fn_evn(lbn,lEbn,T-np.array(t),tsb),(nn,len(t))))])
  return list(
     model.sa[0]*model.sb[0]*np.array([np.sum(x) for x in\
     np.transpose(np.dot(np.transpose(lvnn),np.resize(fn_evn(lan,lEan,t,tsa),(nn,len(t))))*\
     np.resize(fn_evn(lbn,lEbn,T-np.array(t),tsb),(nn,len(t))))])\
   + model.sa[1]*model.sb[0]*np.array([np.sum(x) for x in\
     np.transpose(np.dot(np.transpose(lvon),np.resize(fn_odd(lao,lEao,t,tsa),(no,len(t))))*\
     np.resize(fn_evn(lbn,lEbn,T-np.array(t),tsb),(nn,len(t))))])\
   + model.sa[0]*model.sb[1]*np.array([np.sum(x) for x in\
     np.transpose(np.dot(np.transpose(lvno),np.resize(fn_evn(lan,lEan,t,tsa),(nn,len(t))))*\
     np.resize(fn_odd(lbo,lEbo,T-np.array(t),tsb),(no,len(t))))])\
   + model.sa[1]*model.sb[1]*np.array([np.sum(x) for x in\
     np.transpose(np.dot(np.transpose(lvoo),np.resize(fn_odd(lao,lEao,t,tsa),(no,len(t))))*\
     np.resize(fn_odd(lbo,lEbo,T-np.array(t),tsb),(no,len(t))))])\
   )
 #def new_func(t,ts):
 # ## -- even and odd
 # return list(model.s[0]*(
 #      np.array([np.dot(lcn,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lEn))]) +\
 #  tps*np.array([np.dot(lcn,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lEn))]) )+\
 #  model.s[1]*gv.cos([np.pi*x for x in t])*(
 #      np.array([np.dot(lco,gv.exp(x)) for x in np.outer(np.array(t),    -np.array(lEo))]) +\
 #  tps*np.array([np.dot(lco,gv.exp(x)) for x in np.outer(tpa-np.array(t),-np.array(lEo))]) ) )
 return new_func
pass
