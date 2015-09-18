import gvar as gv
import numpy as np
import sys

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
   dpp_sdev = [ dsdev[i] if dmean[i]+dsdev[i] > 0 else 1e-20 for i in range(len(dsdev))]
   dpm_sdev = [ dsdev[i] if (dmean[i]-dsdev[i] > 0 and dmean[i] > 0) else 
    (max(dmean[i]-1e-20,1e-20) if dmean[i] > 0 else -1e-20)
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
   dmm_sdev = [ dsdev[i] if dmean[i]-dsdev[i] < 0 else 1e-20 for i in range(len(dsdev))]
   dmp_sdev = [ dsdev[i] if (dmean[i]+dsdev[i] < 0 and dmean[i] < 0) else 
    (max(-dmean[i]-1e-20,1e-20) if dmean[i] < 0 else -1e-20)
    for i in range(len(dsdev))]
   return [dmp_sdev,dmm_sdev]
 else:
   dmm_sdev = [ dsdev[i] if dmean[i]-dsdev[i] < 0 else val for i in range(len(dsdev))]
   dmp_sdev = [ dsdev[i] if (dmean[i]+dsdev[i] < 0 and dmean[i] < 0) else 
    (max(-dmean[i]-val,val) if dmean[i] < 0 else -val)
    for i in range(len(dsdev))]
   return [dmp_sdev,dmm_sdev]

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

def append_prior_state(prior,lkey,lgvar):
 """
 Fill a prior array with a state
 State is appended to end of prior dictionary
 All keys provided in lkey are also updated with their corresponding gvar
 """
 if len(lkey) != len(lgvar):
  print "Key list is not the same size as prior value list"
  sys.exit()
 for key,val in zip(lkey,lgvar):
  prior[key].append(val)
 pass

