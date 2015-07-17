import gvar as gv
import numpy as np

def sig_digits(gval,do_unicode=False):
 ## -- print either a gv.gvar or float with leading 0s replaced by os
 ## -- print both mean and sdev if gvar
 ## -- pad with spaces so printout is always same length
 try: ## -- gvars
  smean = sig_digits(gval.mean);
  ssdev = sig_digits(gval.sdev);
  if do_unicode:
   return smean +' '+ u'\u00B1' +' '+ ssdev;
  else:
   return smean + ' +-' + ssdev;
 except AttributeError:
  ## -- floats
  sval = str(gval);
  if gval > 0:
   sval = ' '+sval;
  if sval[1] == '0':
   sval = sval[0]+'o'+sval[2:];
   for i in range(3,len(sval)):
    if sval[i] == '0':
     sval=sval[:i]+'o'+sval[i+1:];
    else:
     break;
  return str('{:<10.10}'.format(sval));
## ------
##

def fmt_num(num,do_sigdigit=True,do_unicode=True):
 if do_sigdigit:
  return sig_digits(num,do_unicode);
 else:
  try:
   smean = fmt_num(num.mean,do_sigdigit,do_unicode);
   ssdev = fmt_num(num.sdev,do_sigdigit,do_unicode);
   ## -- pad with space
   if do_unicode:
    return smean+' '+u'\u00B1'+ssdev;
   else:
    return smean+' +-'+ssdev;
  except AttributeError:
   if num > 0:
    sval = ' '+str(num);
   else:
    sval = str(num);
   return '{:<10.10}'.format(sval);
## ------
##

def sqr_arr(arr):
 ## -- square all elements of the array
 return [arr[i]*arr[i] for i in range(len(arr))];

def sum_dE(arr):
 try:
  return [sum(arr[:i+1]) for i in range(len(arr))];
 except:
  return [arr]

def pos_arr(arr,val=None):
 if val is None:
  return [  arr[i] if arr[i] > 0 else 1e-20 for i in range(len(arr)) ];
 else:
  return [  arr[i] if arr[i] > 0 else val   for i in range(len(arr)) ];

def neg_arr(arr,val=None):
 if val is None:
  return [ -arr[i] if arr[i] < 0 else 1e-20 for i in range(len(arr)) ];
 else:
  return [ -arr[i] if arr[i] < 0 else val   for i in range(len(arr)) ];

