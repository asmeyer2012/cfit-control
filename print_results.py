import gvar as gv
import numpy as np
import defines as df
import util_funcs as ut
from lsqfit._utilities import gammaQ

def reduced_dof(fit,do_v_symm=False):
 for key in fit.p:
  do_adv = False
  if 'gn' in key:
   do_adv = True
   break
 try:
  n3 = 0
  o3 = 0
  if do_adv:
   for key in fit.p:
    if   'gn' in key:
     n3 += len(fit.transformed_p[key])
    elif 'go' in key:
     o3 += len(fit.transformed_p[key])
  else:
   if do_v_symm:
    ## -- use 'no' instead, faster
    n3 = len(fit.transformed_p[df.current_key[0]+'no'])
    o3 = len(fit.transformed_p[df.current_key[0]+'no'][0])
   else:
    n3 = len(fit.transformed_p[df.current_key[0]+'nn'])
    o3 = len(fit.transformed_p[df.current_key[0]+'oo'])
 except KeyError:
  ## -- 2pt fit
  #print "2 point reduced dof"
  pass
 if do_adv:
  klen = len(df.define_prior['nkey']) ## -- still same?
  n2 = 0
  o2 = 0
  for key in fit.p:
   if   key.split('_')[0][-2:] == 'En':
    n2 += len(fit.transformed_p[key])
   elif key.split('_')[0][-2:] == 'Eo':
    o2 += len(fit.transformed_p[key])
 else:
  klen = len(df.define_prior['nkey'])
  n2 = len(fit.transformed_p['En'])
  o2 = len(fit.transformed_p['Eo'])
 #print klen,n2,o2,n3,o3
 if df.do_v_symmetric:
  return fit.dof - ( klen*(n2+o2) + (n3+o3)*(n3+o3+1)/2 )
 else:
  return fit.dof - ( klen*(n2+o2) + (n3+o3)*(n3+o3) )

def fmt_reduced_chi2(fit,do_v_symm=False):
 rstr = 'reduced chi2/dof = '
 #try:
 # n3 = len(fit.transformed_p[df.current_key[0]+'nn'])
 # o3 = len(fit.transformed_p[df.current_key[0]+'oo'])
 #except KeyError:
 # ## -- 2pt fit
 # n3 = 0
 # o3 = 0
 #klen = len(df.define_prior['nkey'])
 #n2 = len(fit.transformed_p['En'])
 #o2 = len(fit.transformed_p['Eo'])
 #newdof = fit.dof - ( klen*(n2+o2) + (n3+o3)*(n3+o3) )
 newdof = reduced_dof(fit,do_v_symm)
 if newdof < 1:
  newchi2 = np.nan
  rstr = rstr + 'nan [' + str(newdof) + ']    Q = ?'
 else:
  newchi2 = fit.chi2/newdof
  rstr = rstr + str(ut.round_to_n_sigdig(newchi2,len(str(newdof)))) + ' [' + str(newdof)\
    + ']    Q = %.2g' % gammaQ(newdof/2.,fit.chi2/2.)
 return rstr

def print_fit(fit, prior,do_v_symm=False):
 ## -- print the fit parameters neatly
 ## -- give both summed and differential energies
 ## -- if variables fit as logs, give both log and linear
 ## --
 do_unicode=False
 do_sigdigit=True
 #
 print '        '+gv.fmt_chi2(fit)
 print fmt_reduced_chi2(fit,do_v_symm)
 print
 print "Printing best fit parameters : "
 #
 for skey in sorted(fit.p):
  ## -- if variable was fit as a log, print log first
  if skey[:3] == 'log':
   #print "------"
   efirst=0.
   lkey=skey[3:]
   for j in range(len(fit.transformed_p[lkey])):
    sigstr=get_sigma_str(lkey,fit,prior,j,do_unicode)
    if (lkey[-2:] == 'En' or \
        lkey[-2:] == 'Eo' or \
        lkey[-1 ] == 'E'):
     if j > 0:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)
     ##else j==0 for energy
     else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    elif(lkey.split('_')[0][-2:] == 'En' or \
         lkey.split('_')[0][-2:] == 'Eo' or \
         lkey.split('_')[0][-1 ] == 'E'):
     efst = 0
     for i in range(int(skey.split('_')[1])):
      efst += fit.transformed_p[lkey.split('_')[0]+'_'+str(i)][0]
      #print i,efst,lkey.split('_')[0]+'_'+str(i)
     if j > 0:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(efst+sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)
     ##else j==0 for energy
     else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(efst+sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    ##else not energy
    else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)\
            +'  '+sigstr
  ##endif log
  elif skey[:4] == 'sqrt':
   #print "------"
   efirst=0.
   lkey=skey[4:]
   for j in range(len(fit.transformed_p[lkey])):
    sigstr=get_sigma_str(lkey,fit,prior,j,do_unicode)
    if (lkey[len(lkey)-2:] == 'En' or \
        lkey[len(lkey)-2:] == 'Eo' or \
        lkey[len(lkey)-1 ] == 'E'):
     if j > 0:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)
    ##else j==0 for energy
     else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.transformed_p[lkey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    ##else not energy
    else:
      print '{:>10}'.format(lkey)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(fit.transformed_p[lkey][j],do_sigdigit,do_unicode)\
            +'  '+sigstr
  ##endif sqrt
  #print "------"
  efirst=0.
  for j in range(len(fit.transformed_p[skey])):
   if skey[-2:] == 'nn' or skey[-2:] == 'no' or\
      skey[-2:] == 'on' or skey[-2:] == 'oo' or\
      skey.split('_')[0][-2:] == 'nn' or skey.split('_')[0][-2:] == 'no' or\
      skey.split('_')[0][-2:] == 'on' or skey.split('_')[0][-2:] == 'oo':
     #for k in range(len(fit.transformed_p[skey][0])):
     #  sigstr=get_sigma_str(skey,fit,prior,(j,k),do_unicode)
     pass
   else:
     sigstr=get_sigma_str(skey,fit,prior,j,do_unicode)
   if (skey[-2:] == 'En' or \
       skey[-2:] == 'Eo' or \
       skey[-1 ] == 'E'):
    if j > 0:
     print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']      :  '\
           +ut.fmt_num(sum(fit.transformed_p[skey][:j+1]),do_sigdigit,do_unicode)\
           +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
           +ut.fmt_num(fit.transformed_p[skey][j],do_sigdigit,do_unicode)
    ##else j==0 for energy
    else:
     print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']      :  '\
           +ut.fmt_num(sum(fit.transformed_p[skey][:j+1]),do_sigdigit,do_unicode)\
           +'  '+sigstr
   elif(skey.split('_')[0][-2:] == 'En' or \
        skey.split('_')[0][-2:] == 'Eo' or \
        skey.split('_')[0][-1 ] == 'E'):
    if j > 0:
     print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']      :  '\
           +ut.fmt_num(sum(fit.transformed_p[skey][:j+1]),do_sigdigit,do_unicode)\
           +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
           +ut.fmt_num(fit.transformed_p[skey][j],do_sigdigit,do_unicode)
    ##else j==0 for energy
    else:
     print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']      :  '\
           +ut.fmt_num(sum(fit.transformed_p[skey][:j+1]),do_sigdigit,do_unicode)\
           +'  '+sigstr
   elif(skey.split('_')[0][-2:] == 'gn' or \
        skey.split('_')[0][-2:] == 'go'):
    if j > 0:
     print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']      :  '\
           +ut.fmt_num(fit.transformed_p[skey][0]+fit.transformed_p[skey][j],\
            do_sigdigit,do_unicode)\
           +'  '+sigstr+' |    delg'+'['+'{:>2}'.format(j)+']  :  '\
           +ut.fmt_num(fit.transformed_p[skey][j],do_sigdigit,do_unicode)
    ##else j==0 for energy
    else:
     print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']      :  '\
           +ut.fmt_num(fit.transformed_p[skey][0],do_sigdigit,do_unicode)\
           +'  '+sigstr
   ##else not energy
   else:
    if skey[-2:] == 'nn' or skey[-2:] == 'no' or\
       skey[-2:] == 'on' or skey[-2:] == 'oo' or\
       skey.split('_')[0][-2:] == 'nn' or skey.split('_')[0][-2:] == 'no' or\
       skey.split('_')[0][-2:] == 'on' or skey.split('_')[0][-2:] == 'oo':
      if df.do_v_symmetric and\
       ((skey[-2:] == 'nn' or skey[-2:] == 'oo') or\
       ((skey.split('_')[0][-2:] == 'nn' or skey.split('_')[0][-2:] == 'oo') and\
        (int(skey.split('_')[1]) == int(skey.split('_')[2])) )):
       if (len(skey.split('_')) > 1):
        xi = 1
       else:
        xi = 0
       ## -- upper triangle matrix 3-point factors
       vlen = int(np.sqrt(8*len(fit.transformed_p[skey])+1)-1)/2
       ui = np.triu_indices(vlen)
       i = ui[0][j]+xi
       k = ui[1][j]+xi
       sigstr=get_sigma_str(skey,fit,prior,j,do_unicode)
       print '{:>10}'.format(skey)+'['+'{:>2}'.format(i)+']'+'['+'{:>2}'.format(k)+']  :  '\
             +ut.fmt_num(fit.transformed_p[skey][j],do_sigdigit,do_unicode)\
             +'  '+sigstr
      else:
       ## -- print 3-point factors
       for k in range(len(fit.transformed_p[skey][0])):
         sigstr=get_sigma_str(skey,fit,prior,(j,k),do_unicode)
         print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']'+'['+'{:>2}'.format(k)+']  :  '\
               +ut.fmt_num(fit.transformed_p[skey][j][k],do_sigdigit,do_unicode)\
               +'  '+sigstr
    else:
      print '{:>10}'.format(skey)+'['+'{:>2}'.format(j)+']      :  '\
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
 except TypeError:
  ## -- Vnn, Vno, etc...
  #print key,j
  sig=int(np.abs(np.trunc(\
      (fit.p[key][j[0]][j[1]].mean-prior[key][j[0]][j[1]].mean)\
       /(prior[key][j[0]][j[1]]).sdev)))
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
