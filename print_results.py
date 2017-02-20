import gvar as gv
import numpy as np
import defines as df
import util_funcs as ut
#from lsqfit._utilities import gammaQ
from lsqfit import gammaQ

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
    skey = key.split('_')
    bkey = ut.get_basekey(skey[0])
    if bkey[0] is None:
     if   'gn' in bkey[1]:
      n3 += len(fit.p[key])
     elif 'go' in bkey[1]:
      o3 += len(fit.p[key])
  else:
   if do_v_symm:
    ## -- use 'no' instead, faster
    n3 = len(fit.p[df.current_key[0]+'no'])
    o3 = len(fit.p[df.current_key[0]+'no'][0])
   else:
    n3 = len(fit.p[df.current_key[0]+'nn'])
    o3 = len(fit.p[df.current_key[0]+'oo'])
 except KeyError:
  ## -- 2pt fit
  #print "2 point reduced dof"
  pass
 #if do_adv:
 klen = len(df.define_prior['nkey'])
 n2 = 0
 o2 = 0
 for key in fit.p:
  skey = key.split('_')
  bkey = ut.get_basekey(skey[0])
  if   (bkey[1][-2:] == 'En') and (bkey[0] is None):
   n2 += len(fit.p[key])
  elif (bkey[1][-2:] == 'Eo') and (bkey[0] is None):
   o2 += len(fit.p[key])
 #else:
 # klen = len(df.define_prior['nkey'])
 # n2 = len(fit.transformed_p['En'])
 # o2 = len(fit.transformed_p['Eo'])
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
  spkey = skey.split('_')
  keylen = len(spkey)
  if keylen == 1:
   ikey = -1
   jkey = -1
   ksuf = ''
  elif keylen == 2:
   ikey = int(spkey[1])
   jkey = -1
   ksuf = '_'+str(ikey)
  elif keylen == 3:
   ikey = int(spkey[1])
   jkey = int(spkey[2])
   ksuf = '_'+str(ikey)+'_'+str(jkey)
  else:
   raise KeyError("too many underscores in key name")
  bkey = ut.get_basekey(skey.split('_')[0])
  ## -- if variable was fit as a log, print log first
  if bkey[0] == 'log':
   efirst=0.
   lkey=bkey[1]
   for j in range(len(fit.p[lkey+ksuf])):
    sigstr=get_sigma_str(lkey+ksuf,fit,prior,j,do_unicode)
    if (lkey[-2:] == 'En' or \
        lkey[-2:] == 'Eo' or \
        lkey[-1 ] == 'E') and keylen == 1:
     if j > 0:
      print '{:>10}'.format(bkey[0]+lkey+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)
     ##else j==0 for energy
     else:
      print '{:>10}'.format(bkey[0]+lkey+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    elif(lkey[-2:] == 'En' or \
         lkey[-2:] == 'Eo' or \
         lkey[-1 ] == 'E') and keylen > 1:
     efst = 0
     for i in range(ikey):
      efst += fit.p[skey][0]
      #print i,efst,lkey.split('_')[0]+'_'+str(i)
     if j > 0:
      print '{:>10}'.format(bkey[0]+lkey+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(efst+sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)
     ##else j==0 for energy
     else:
      print '{:>10}'.format(bkey[0]+lkey+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(efst+sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    ##else not energy
    else:
      print '{:>10}'.format(bkey[0]+lkey+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)\
            +'  '+sigstr
  ##endif log
  elif bkey[0] == 'sqrt':
   #print "------"
   efirst=0.
   lkey=bkey[1]
   for j in range(len(fit.p[skey])):
    sigstr=get_sigma_str(lkey+ksuf,fit,prior,j,do_unicode)
    if (lkey[-2:] == 'En' or \
        lkey[-2:] == 'Eo' or \
        lkey[-1 ] == 'E'):
     if j > 0:
      print '{:>10}'.format(bkey[0]+lkey+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)
     ##else j==0 for energy
     else:
      print '{:>10}'.format(bkey[0]+lkey+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    ##else not energy
    else:
      print '{:>10}'.format(bkey[0]+lkey+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)\
            +'  '+sigstr
   ##endif sqrt
  else: ## not log, sqrt
   efirst=0.
   for j in range(len(fit.p[skey])):
    if bkey[1][-2:] == 'nn' or bkey[1][-2:] == 'no' or\
       bkey[1][-2:] == 'on' or bkey[1][-2:] == 'oo':
      pass
    else:
      sigstr=get_sigma_str(bkey[1]+ksuf,fit,prior,j,do_unicode)
    if (bkey[1][-2:] == 'En' or \
        bkey[1][-2:] == 'Eo' or \
        bkey[1][-1 ] == 'E'):
     if j > 0:
      print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)
     ##else j==0 for energy
     else:
      print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    elif(bkey[1][-2:] == 'En' or \
         bkey[1][-2:] == 'Eo' or \
         bkey[1][-1 ] == 'E'):
     if j > 0:
      print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delE'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)
     ##else j==0 for energy
     else:
      print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(sum(fit.p[skey][:j+1]),do_sigdigit,do_unicode)\
            +'  '+sigstr
    elif(bkey[1][-2:] == 'gn' or \
         bkey[1][-2:] == 'go'):
     if j > 0:
      print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(fit.p[skey][0]+fit.p[skey][j],\
             do_sigdigit,do_unicode)\
            +'  '+sigstr+' |    delg'+'['+'{:>2}'.format(j)+']  :  '\
            +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)
     ##else j==0 for energy
     else:
      print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
            +ut.fmt_num(fit.p[skey][0],do_sigdigit,do_unicode)\
            +'  '+sigstr
    ##else not energy
    else:
     if bkey[1][-2:] == 'nn' or bkey[1][-2:] == 'no' or\
        bkey[1][-2:] == 'on' or bkey[1][-2:] == 'oo':
       if df.do_v_symmetric and\
        ((bkey[1][-2:] == 'nn' or bkey[1][-2:] == 'oo') and\
         (ikey == jkey) ):
        if (keylen > 1):
         xi = 1
        else:
         xi = 0
        ## -- upper triangle matrix 3-point factors
        vlen = int(np.sqrt(8*len(fit.p[skey])+1)-1)/2
        ui = np.triu_indices(vlen)
        i = ui[0][j]+xi
        k = ui[1][j]+xi
        sigstr=get_sigma_str(bkey[1]+ksuf,fit,prior,j,do_unicode)
        print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(i)+']'\
              +'['+'{:>2}'.format(k)+']  :  '\
              +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)\
              +'  '+sigstr
       else:
        ## -- print 3-point factors
        for k in range(len(fit.p[skey][0])):
          sigstr=get_sigma_str(bkey[1]+ksuf,fit,prior,(j,k),do_unicode)
          print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(j)+']'\
                +'['+'{:>2}'.format(k)+']  :  '\
                +ut.fmt_num(fit.p[skey][j][k],do_sigdigit,do_unicode)\
                +'  '+sigstr
     else:
       print '{:>10}'.format(bkey[1]+ksuf)+'['+'{:>2}'.format(j)+']      :  '\
             +ut.fmt_num(fit.p[skey][j],do_sigdigit,do_unicode)\
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
       (gv.log(fit.p[key][j].mean)-prior['log('+key+')'][j].mean)\
        /(prior['log('+key+')'][j]).sdev)))
  except KeyError:
   sig=int(np.abs(np.trunc(\
       (gv.sqrt(fit.p[key][j].mean)-prior['sqrt('+key+')'][j].mean)\
        /(prior['sqrt('+key+')'][j]).sdev)))
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
