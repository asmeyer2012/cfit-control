import gvar as gv
import numpy as np
import sys
from math import log10, floor

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
 ## -- was this ever used?

 #for key in nkey:
 # rprior[key] = prior[key][:nn]
 # if len(rprior[key]) < nn:
 #  raise ValueError("Not enough prior states to fill prior dictionary")
 #for key in okey:
 # rprior[key] = prior[key][:no]
 # if len(rprior[key]) < no:
 #  raise ValueError("Not enough prior states to fill prior dictionary")
 #try:
 # for key in prior['vkey']:
 #  if key[-2] == 'n':
 #   n1=nn
 #  elif key[-2] == 'o':
 #   n1=no
 #  else:
 #   raise ValueError("Unparseable key:",key)
 #  if key[-1] == 'n':
 #   n2=nn
 #  elif key[-1] == 'o':
 #   n2=no
 #  else:
 #   raise ValueError("Unparseable key:",key)
 #  rprior[key] = prior[key][:n1][:n2]
 #  if len(rprior[key]) < n1 or len(rprior[key][0]) < n2:
 #   raise ValueError("Not enough prior states to fill prior dictionary")
 #except KeyError:
 # pass # probably 2-point function
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
     if xkey[-2] == 'n':
      n1=nn3
     elif xkey[-2] == 'o':
      n1=no3
     else:
      raise ValueError("Unparseable key:",key)
     if xkey[-1] == 'n':
      n2=nn3
     elif xkey[-1] == 'o':
      n2=no3
     else:
      raise ValueError("Unparseable key:",key)
     #rprior[key][xkey] = np.resize(prior[key][xkey],(n1,n2))
     if do_v_symm and (xkey[-2:] == 'nn' or xkey[-2:] == 'oo'):
      #rprior[key][xkey] = prior[key][xkey][:(n1*(n1+1)/2)] ## -- outdated
      try:
       rprior[key][xkey] = truncate_upper_triangle(prior[key][xkey],n1)
      except:
       rprior[key][xkey] = prior[key][xkey]
     elif do_v_symm and (xkey[-2:] == 'on'):
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
  #print "stack ",i," mass : ",ms
  #print "stack ",i," error: ",es
  #print "stack ",i," split: ",gstack[i]

 ## -- sorting of states
 lsort = np.transpose(sorted(lorder,key=lambda x: x[0])) ## -- sorted list of masses vs stacks
 ncount = [len(x) for x in mstk] ## -- number of states in stacks
 ## -- positions of elements in stacks
 npos = [[i for i,y in enumerate(lsort[1]) if x==y] for x in range(len(mstk))]
 niter = [0 for i in range(len(mstk))]
 lasti = -1
 #print "sorted : ",lsort
 #print "niter  : ",niter

 ## -- construct the gvars for the spectrum
 gstate = np.array([])
 for i,x in zip(range(len(lsort[1])),lsort[1]):
  #print gstate
  #if i==0:
  # lasti = int(x)
  # gstack['de'] = [gstack[x][0]] ## -- get lowest energy state
  #else:
  if lasti == int(x):
   ## -- correlated with most recent, just add next splitting
   #print "append"
   #print np.append(gstate,gstack[int(x)][niter[int(x)]])
   gstate = np.append(gstate,gstack[int(x)][niter[int(x)]])
  else:
   ## -- find out if this stack has been used yet
   if niter[int(x)] == 0:
    ## -- if not, decorrelate with all previous states
    #print "decorrelate"
    #print np.append(gstate,gstack[int(x)][0] - np.sum(gstate))
    gstate = np.append(gstate,gstack[int(x)][0] - np.sum(gstate))
   else:
    ## -- else, decorrelate with all states between last occurrence
    lastpos = [j for j,y in enumerate(lsort[1][:i]) if x==int(y)][-1]
    #print "decorrelate between"
    #print lastpos,"  ",np.sum(gstate[lastpos+1:])
    gstate = np.append(gstate,gstack[int(x)][niter[int(x)]] - np.sum(gstate[lastpos+1:]))
   lasti = int(x)
  niter[lasti] += 1

 ## -- pull prior values from defines
 #lAm = df.lAm
 #Am  = df.Am
 #lAcs= df.lAcs
 #lAks= df.lAks
 #Acs = df.Acs
 #Aks = df.Aks

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

