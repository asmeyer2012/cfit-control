import gvar as gv
import numpy as np
import re
import sys
from math import log10, floor

## -- pull key name out of log() or sqrt()
##    returns both function name and contained key
##    if no function used, replaces function name with None
##    fails on error if old-style key used
def get_basekey(key):
 regrp = re.match('(\w+)\((\w+)\)',key)
 if regrp is None:
  if key[:3] == 'log' or key[:4] == 'sqrt':
   raise KeyError("Error: old-style key",key)
  else:
   return (None,key)
 else:
  return regrp.groups()

## -- parse key for even/odd, or raise exception if not
def get_evenodd(key):
 skey = key.split('_')
 suffix = get_basekey(skey[0])[1][-2:]
 if suffix[0] == 'n' or suffix[0] == 'o':
  return suffix
 else:
  if suffix[1] == 'n' or suffix[1] == 'o':
   return suffix[1]
  else:
   raise KeyError("Key parity not specified",key)
 
## -- returns key as an argument to function name
def get_fnkey(key,fn=None):
 if fn is None:
  return key
 else:
  return fn+'('+key+')'

## -- applies the function specified within key name
def apply_fn_op(key,val):
 bkey = get_basekey(key)
 if bkey[0] is None:
  return val
 else:
  if bkey[0] == 'log':
   return gv.log(val)
  elif bkey[0] == 'sqrt':
   return gv.sqrt(val)
  else:
   raise KeyError("Unknown function operation:",bkey[0])

## -- applies the inverse of function specified within key name
def apply_invfn_op(key,val):
 bkey = get_basekey(key)
 if bkey[0] is None:
  return val
 else:
  if bkey[0] == 'log':
   return gv.exp(val)
  elif bkey[0] == 'sqrt':
   return val*val
  else:
   raise KeyError("Unknown function operation:",bkey[0])


def round_to_n_sigdig(x,n):
  return round(x, n-1-int(floor(log10(abs(x)))))

def sig_digits(gval,do_unicode=False):
 ## -- print either a gv.gvar or float with leading 0s replaced by os
 ## -- print both mean and sdev if gvar
 ## -- pad with spaces so printout is always same length
 try: ## -- gvars
  smean = sig_digits(gval.mean)
  ssdev = sig_digits(gval.sdev)
  if do_unicode:
   return smean +' '+ u'\u00B1' +' '+ ssdev
  else:
   return smean + ' +-' + ssdev
 except AttributeError:
  ## -- floats
  sval = str(gval)
  if gval > 0:
   sval = ' '+sval
  if sval[1] == '0':
   sval = sval[0]+'o'+sval[2:]
   for i in range(3,len(sval)):
    if sval[i] == '0':
     sval=sval[:i]+'o'+sval[i+1:]
    else:
     break
  if any(c == 'e' for c in sval):
   sval=sval[:6]+sval[-4:]
  return str('{:<10.10}'.format(sval))
## ------
##

def fmt_num(num,do_sigdigit=True,do_unicode=True):
 if do_sigdigit:
  return sig_digits(num,do_unicode)
 else:
  try:
   smean = fmt_num(num.mean,do_sigdigit,do_unicode)
   ssdev = fmt_num(num.sdev,do_sigdigit,do_unicode)
   ## -- pad with space
   if do_unicode:
    return smean+' '+u'\u00B1'+ssdev
   else:
    return smean+' +-'+ssdev
  except AttributeError:
   if num > 0:
    sval = ' '+str(num)
   else:
    sval = str(num)
   return '{:<10.10}'.format(sval)
## ------
##

def sqr_arr(arr):
 ## -- square all elements of the array
 return [arr[i]*arr[i] for i in range(len(arr))]

def sum_dE(arr):
 try:
  return [sum(arr[:i+1]) for i in range(len(arr))]
 except:
  return [arr]

def pos_arr(arr,val=None):
 if val is None:
  return [  arr[i] if arr[i] > 0 else 1e-20 for i in range(len(arr)) ]
 else:
  return [  arr[i] if arr[i] > 0 else val   for i in range(len(arr)) ]

def neg_arr(arr,val=None):
 if val is None:
  return [ -arr[i] if arr[i] < 0 else 1e-20 for i in range(len(arr)) ]
 else:
  return [ -arr[i] if arr[i] < 0 else val   for i in range(len(arr)) ]

def pos_err(dmean,dsdev,val=None):
 if val is None:
   dpp_sdev = [ dsdev[i] if dmean[i]+dsdev[i] > 0 else 1e-6 for i in range(len(dsdev))]
   dpm_sdev = [ dsdev[i] if (dmean[i]-dsdev[i] > 0 and dmean[i] > 0) else 
    (max(dmean[i]-1e-6,1e-6) if dmean[i] > 0 else -1e-6)
    for i in range(len(dsdev))]
   return [dpm_sdev,dpp_sdev]
 else:
   dpp_sdev = [ dsdev[i] if dmean[i]+dsdev[i] > 0 else val for i in range(len(dsdev))]
   dpm_sdev = [ dsdev[i] if (dmean[i]-dsdev[i] > 0 and dmean[i] > 0) else 
    (max(dmean[i]-val,val) if dmean[i] > 0 else -val)
    for i in range(len(dsdev))]
   return [dpm_sdev,dpp_sdev]

def neg_err(dmean,dsdev,val=None):
 if val is None:
   dmm_sdev = [ dsdev[i] if dmean[i]-dsdev[i] < 0 else 1e-6 for i in range(len(dsdev))]
   dmp_sdev = [ dsdev[i] if (dmean[i]+dsdev[i] < 0 and dmean[i] < 0) else 
    (max(-dmean[i]-1e-6,1e-6) if dmean[i] < 0 else -1e-6)
    for i in range(len(dsdev))]
   return [dmp_sdev,dmm_sdev]
 else:
   dmm_sdev = [ dsdev[i] if dmean[i]-dsdev[i] < 0 else val for i in range(len(dsdev))]
   dmp_sdev = [ dsdev[i] if (dmean[i]+dsdev[i] < 0 and dmean[i] < 0) else 
    (max(-dmean[i]-val,val) if dmean[i] < 0 else -val)
    for i in range(len(dsdev))]
   return [dmp_sdev,dmm_sdev]

def truncate_upper_triangle(mat,n):
 """
 Turn a matrix of size n*n into an array of just the upper-triangular elements
 Will truncate matrix if larger than n*n
 Convienient numpy indexing routine for just this purpose
 """
 iu1 = np.triu_indices(n)
 return mat[iu1]

def reconstruct_upper_triangle(fmat,n):
 """
 The inverse of truncate_upper_triangle
 Turns a flat matrix of size n*(n+1)/2 into a square matrix
 """
 iu1 = np.triu_indices(n)
 tmp = np.array(n*[n*[gv.gvar(0,1)]])
 for i,x in zip(range(len(iu1[0])),np.transpose(iu1)):
  tmp[tuple(x)]       = fmat[i] ## upper triangle
  tmp[tuple(x)[::-1]] = fmat[i] ## lower triangle
 return tmp

def create_prior_dict(nkey,okey):
 """
 Create an empty prior dictionary for use
 Even and odd keys are given in two separate lists/tuples
 """
 rprior = {} ## -- return value = prior dictionary
 for key in nkey:
  rprior[key] = []
 for key in okey:
  rprior[key] = []
 return rprior

def get_prior_dict(prior,nkey,okey,nn,no,vkey=tuple(),nn3=1,no3=1,do_v_symm=False):
 """
 Get a prior dictionary which has many states in it and extract only
 the first nn+no states
 """
 rprior = {} ## -- return value = prior dictionary
 rprior['nkey'] = prior['nkey']
 rprior['okey'] = prior['okey']
 try:
  rprior['vkey'] = prior['vkey']
 except KeyError:
  pass

 for key in prior:
  if key in nkey+okey+vkey+('nkey','okey','vkey'):
   continue
  rprior[key] = {}
  for xkey in prior[key]:
   if (xkey in nkey):
    rprior[key][xkey] = prior[key][xkey][:nn]
   elif (xkey in okey):
    rprior[key][xkey] = prior[key][xkey][:no]
   elif (xkey in vkey):
    try:
     #for key in prior['vkey']:
     eokey = get_evenodd(xkey)
     if eokey[0] == 'n':
      n1=nn3
     elif eokey[0] == 'o':
      n1=no3
     else:
      raise ValueError("Unparseable key:",key)
     if eokey[1] == 'n':
      n2=nn3
     elif eokey[1] == 'o':
      n2=no3
     else:
      raise ValueError("Unparseable key:",key)
     #rprior[key][xkey] = np.resize(prior[key][xkey],(n1,n2))
     if do_v_symm and (eokey == 'nn' or eokey == 'oo'):
      #rprior[key][xkey] = prior[key][xkey][:(n1*(n1+1)/2)] ## -- outdated
      try:
       rprior[key][xkey] = truncate_upper_triangle(prior[key][xkey],n1)
      except:
       rprior[key][xkey] = prior[key][xkey]
     elif do_v_symm and (eokey == 'on'):
      continue ## -- use priors for 'no' instead
      #rprior[key][xkey] = prior[key][xkey][:(n1*(n1+1)/2)]
     else:
      rprior[key][xkey] = prior[key][xkey][:n1,:n2]
      if (len(rprior[key][xkey]) < n1 or len(rprior[key][xkey][0]) < n2):
       raise ValueError("Not enough prior states to fill prior dictionary")
    except KeyError:
     pass # probably 2-point function
 return rprior

def append_prior_state(prior,lkey,lgvar):
 """
 Fill a prior array with a state
 State is appended to end of prior dictionary
 All keys provided in lkey are also updated with their corresponding gvar
 """
 if len(lkey) != len(lgvar):
  raise TypeError("Key list is not the same size as prior value list")
 for key,val in zip(lkey,lgvar):
  prior[key].append(val)
 pass

def stack_prior_states(prior,lkey,mstk,estk):
 """
 Fill a prior dictionary with states which are determined from a set of stacks
 Prior energies within stacks are correlated, stacks are uncorrelated
 Other priors are chosen from some generic defaults
 """
 gstack = gv.BufferDict()
 lorder = []
 ## -- create independent gvars for each stack
 for i,ms,es in zip(range(len(mstk)),mstk,estk):
  mde = np.array(ms[1:])-np.array(ms[:-1])
  mde = np.insert(mde,0,ms[0])
  gstack[i] = gv.gvar(mde,es)
  for m in ms:
   lorder.append([m,i])

 ## -- sorting of states
 lsort = np.transpose(sorted(lorder,key=lambda x: x[0])) ## -- sorted list of masses vs stacks
 ncount = [len(x) for x in mstk] ## -- number of states in stacks
 ## -- positions of elements in stacks
 npos = [[i for i,y in enumerate(lsort[1]) if x==y] for x in range(len(mstk))]
 niter = [0 for i in range(len(mstk))]
 lasti = -1

 ## -- construct the gvars for the spectrum
 gstate = np.array([])
 for i,x in zip(range(len(lsort[1])),lsort[1]):
  if lasti == int(x):
   ## -- correlated with most recent, just add next splitting
   gstate = np.append(gstate,gstack[int(x)][niter[int(x)]])
  else:
   ## -- find out if this stack has been used yet
   if niter[int(x)] == 0:
    ## -- if not, decorrelate with all previous states
    gstate = np.append(gstate,gstack[int(x)][0] - np.sum(gstate))
   else:
    ## -- else, decorrelate with all states between last occurrence
    lastpos = [j for j,y in enumerate(lsort[1][:i]) if x==int(y)][-1]
    gstate = np.append(gstate,gstack[int(x)][niter[int(x)]] - np.sum(gstate[lastpos+1:]))
   lasti = int(x)
  niter[lasti] += 1

 ## -- defined again in DEFINES
 lAm  = 1e2 # log amplitude mean
 lAcs = 1e3 # log amplitude sdev (source)
 lAks = 1e1 # log amplitude sdev (sink)
 Am   = 0   # amplitude mean
 Acs  = 1e3 # amplitude sdev (source)
 Aks  = 1e1 # amplitude sdev (sink)

 ## -- append the prior states for this spectrum
 for p in gstate:
  pAmp = gv.gvar( [lAm]+[Am]*(len(lkey)-2), [lAcs]+[Acs]*((len(lkey)-3)/2)+[Aks]*((len(lkey)-1)/2) )
  append_prior_state(prior,lkey,np.insert(pAmp,0,p))
 pass

## -- keys have underscores and numbers appended to indicate blocks
##    pull all keys which start with a specific string, group them
def retrieve_block_keys(prior, key):
    keyList = []
    for pkey in prior:
      #print key,pkey
      if key in pkey:
        keyList.append(get_basekey(key)[1])
        #xkey = get_basekey(key)
        #if   xkey[0] == 'log':
        #  #print "appending key ",pkey
        #  keyList.append(xkey[1])
        #elif xkey[0] == 'sqrt':
        #  keyList.append(xkey[1])
        #else:
        #  #print "appending key ",pkey
        #  keyList.append(pkey)
    return sorted(keyList)

## -- reconstruct spectrum from advanced dictionary
##    returns a new dictionary with the summed spectrum
##    keys in new dictionary are prefixes of old keys
##    other keys and log/sqrt are ignored
def retrieve_spectrum_advanced(dict):
 klst = {}
 rval = {}
 for key in dict:
  skey = key.split('_')
  bkey = get_basekey(skey[0])
  if not(bkey[0] is None):
   continue
  if skey[0][-2:] == 'En' or skey[0][-2:] == 'Eo':
   ## -- keep a dictionary of prefixes and blocks for energies
   if skey[0] in klst:
    klst[skey[0]].append(skey[1])
   else: 
    klst[skey[0]] = [skey[1]]
 ## -- iterate over prefixes
 for pkey in klst:
  E0 = 0
  ## -- iterate over blocks
  for i in sorted(klst[pkey]):
   key = pkey +'_'+str(i)
   tmp = dict[key]
   ## -- correct the first energy
   E0 += tmp[0]
   tmp[0] = E0
   if not(pkey in rval):
    rval[pkey] = np.array([])
   ## -- add all of the energies
   for e in np.cumsum(tmp):
    rval[pkey] = np.append(rval[pkey],e)
  ## -- sort the states in increasing order
  rval[pkey] = sorted(rval[pkey])
 return rval

## -- fold data together, leaving first and middle points alone
def fold_data(dat,antisym=False):
 sg = (-1 if antisym else 1)
 lt = len(dat)
 rval = np.array((np.array(dat[1:lt/2]) + sg*np.array(dat[lt-1:lt/2:-1]))/2.)
 rval = np.append(rval,dat[lt/2])
 rval = np.insert(list(rval),0,dat[0])
 return rval
 #return np.insert(np.append(rval,dat[lt/2]),0,dat[0])

