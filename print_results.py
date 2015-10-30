import gvar as gv
import numpy as np
import util_funcs as ut

def print_fit(fit, prior):
 ## -- print the fit parameters neatly
 ## -- give both summed and differential energies
 ## -- if variables fit as logs, give both log and linear
 ## --
 do_unicode=False
 do_sigdigit=True
 #
 print gv.fmt_chi2(fit)
 print
 print "Printing best fit parameters : "
 #
 for skey in fit.p:
  ## -- if variable was fit as a log, print log first
  if skey[:3] == 'log':
   print "------"
   efirst=0.
   lkey=skey[3:]
   for j in range(len(fit.transformed_p[lkey])):
    sigstr=get_sigma_str(lkey,fit,prior,j,do_unicode)
    if (lkey[len(lkey)-2:] == 'En' or \
        lkey[len(lkey)-2:] == 'Eo' or \
        lkey[len(lkey)-1 ] == 'E'):
     if j > 0:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)
    ##else j==0 for energy
     else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    ##else not energy
    else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)\
            +'  '+sigstr
  ##endif log
  elif skey[:4] == 'sqrt':
   print "------"
   efirst=0.
   lkey=skey[4:]
   for j in range(len(fit.transformed_p[lkey])):
    sigstr=get_sigma_str(lkey,fit,prior,j,do_unicode)
    if (lkey[len(lkey)-2:] == 'En' or \
        lkey[len(lkey)-2:] == 'Eo' or \
        lkey[len(lkey)-1 ] == 'E'):
     if j > 0:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)
    ##else j==0 for energy
     else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    ##else not energy
    else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)\
            +'  '+sigstr
  ##endif sqrt
  print "------"
  efirst=0.
  for j in range(len(fit.transformed_p[skey])):
   sigstr=get_sigma_str(skey,fit,prior,j,do_unicode)
   if (skey[len(skey)-2:] == 'En' or \
       skey[len(skey)-2:] == 'Eo' or \
       skey[len(skey)-1 ] == 'E'):
    if j > 0:
     print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']  :  '\
           +ut.fmt_num(sum(fit.transformed_p[skey][:j+1]),do_sigdigit,do_unicode)\
           +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
           +ut.fmt_num(fit.transformed_p[skey][j],do_sigdigit,do_unicode)
    ##else j==0 for energy
    else:
     print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']  :  '\
           +ut.fmt_num(sum(fit.transformed_p[skey][:j+1]),do_sigdigit,do_unicode)\
           +'  '+sigstr
   ##else not energy
   else:
    print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']  :  '\
          +ut.fmt_num(fit.transformed_p[skey][j],do_sigdigit,do_unicode)\
          +'  '+sigstr
 #
 print "------"
## ------
##

def print_error_budget(fit):
 ## -- sometimes fails, just ignore for now
 try:
  print fit.fmt_errorbudget(outputs,inputs)
 except:
  print
  print "Could not print error budget"
  print "(Error budget not implemented yet)"
  print
## ------
##
 

def get_sigma_str(key,fit,prior,j,do_unicode=True):
 ## -- list the sigma away from prior
 #
 try:
  ## -- requesting log, log prior
  ##    or requesting linear, linear prior
  sig=int(np.abs(np.trunc(\
      (fit.p[key][j].mean-prior[key][j].mean)\
       /(prior[key][j]).sdev)))
 except KeyError:
  ## -- requested linear, have log or sqrt prior
  try:
   sig=int(np.abs(np.trunc(\
       (gv.log(fit.transformed_p[key][j].mean)-prior['log'+key][j].mean)\
        /(prior['log'+key][j]).sdev)))
  except KeyError:
   sig=int(np.abs(np.trunc(\
       (gv.sqrt(fit.transformed_p[key][j].mean)-prior['sqrt'+key][j].mean)\
        /(prior['sqrt'+key][j]).sdev)))
 if do_unicode:
  if sig > 0:
   sigstr=str(sig)+u'\u03C3' # unicode for sigma (cannot be saved to string)
  else:
   sigstr='  '
 else:
  if sig > 0:
   sigstr=str(sig)+'sig'
  else:
   sigstr='    '
 return sigstr
## ------
##
