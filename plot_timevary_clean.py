import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines      as df
import define_prior as dfp

## -- handle which input is being varied
fix_tmin = False # only a single value of tmin
fix_tmax = True # only a single value of tmin
fix_tmin_val = 0
fix_tmax_val = 9
assert fix_tmin != fix_tmax # xor

## -- number of states, for legend
fix_nst = df.num_nst
fix_ost = df.num_ost
max_nst = 4
max_ost = 4
print fix_nst
print fix_ost

## -- multiplicities of particles, controls plot symbols
num_symbols = 3
symbList = ['o','^','s']
numN = [1,3,0,4] #Ns, Ds, unknowns
numO = [3,4,0,6]
mark_nst = [([y+1>sum(numN[:x]) for x in range(len(numN))].count(True)-1)%num_symbols
 for y in range(fix_nst)]
mark_ost = [([y+1>sum(numO[:x]) for x in range(len(numO))].count(True)-1)%num_symbols
 for y in range(fix_ost)]

## -- print chi2/pvalue (not sure what to do with these)
do_chi2 = False # not implemented
do_pval = False # not implemented
cut_chi2 = False

## -- fine tuned plotting handles
parity_offset = 0.05 # change distance between even/odd states
do_vbar = False # vertical bars separating different tmin/tmax
plotLimit = [0.8,1.6]

def plot_timevary(fit_collector,**kwargs):
 """
 """
 fitCount  = 0
 hVal  = [] ## -- horizontal axis value, ~ fit
 hName = [] ## -- fit name, e.g. 1+1, 2+1...
 hChi2 = [] ## -- fit chi2, for color coding
 hValDatn  = [[] for x in range(num_symbols)]
 hValDato  = [[] for x in range(num_symbols)]
 enCentral = [[] for x in range(num_symbols)]
 eoCentral = [[] for x in range(num_symbols)]
 enError = [[] for x in range(num_symbols)]
 eoError = [[] for x in range(num_symbols)]
 #hValDatn  = [] ## -- mostly same as hVal, but match size of enCentral and offset
 #hValDato  = [] ## -- mostly same as hVal, but match size of eoCentral and offset
 #enCentral = []
 #eoCentral = []
 #enError = []
 #eoError = []
 nst = df.num_nst
 ost = df.num_ost
 ## -- tkey should be tuple: nst,ost, and 'fit' or 'prior' or other descriptor
 for tmax in df.tmvr_tmax:
  for tmin in range(2,tmax):
   tkey=(tmin,tmax,'fit')
   ## -- ignore fits with large chi2
   try:
    dof = float(fit_collector[tkey]['dof'])
    npr = float(len(df.define_prior['nkey']))
    if cut_chi2:
     if dof/(dof-npr*(nst+ost))*fit_collector[tkey]['chi2'] > df.max_chi2\
        or dof/(dof-npr*(nst+ost))*fit_collector[tkey]['chi2'] < df.min_chi2:
      print dof/(dof-npr*(nst+ost))*fit_collector[tkey]['chi2'] 
      continue 
     pass
   except KeyError:
    print "KeyError: ",tkey
    continue
   except ZeroDivisionError:
    print "ZeroDivisionError"
    continue
   ## -- collect only important info
   hVal.append(fitCount+0.5)
   if fix_tmin:
     name = str(tmax)
   elif fix_tmax:
     name = str(tmin)
   if do_chi2:
     name = name +'('+str(round(dof/(dof-npr*(nst+ost))*fit_collector[tkey]['chi2'],2))+')'
   hName.append(name)
   hChi2.append(fit_collector[tkey]['chi2'])
   for key in fit_collector[tkey]:
    sum=0
    it=0 #iterator, decides on nucleon vs delta vs unknown
    if key[:2] == 'En' and not(key[3:] == 'log'):
     for x in fit_collector[tkey][key]:
      if it > max_nst:
       break
       pass
      sum += x.mean
      hValDatn[mark_nst[it]].append(fitCount+0.5-parity_offset)
      enCentral[mark_nst[it]].append(sum)
      enError[mark_nst[it]].append(x.sdev)
      it+=1
      if it > max_nst-1:
       break
       pass
    elif key[:2] == 'Eo' and not(key[3:] == 'log'):
     for x in fit_collector[tkey][key]:
      sum += x.mean
      hValDato[mark_ost[it]].append(fitCount+0.5+parity_offset)
      eoCentral[mark_ost[it]].append(sum)
      eoError[mark_ost[it]].append(x.sdev)
      it+=1
      if it > max_ost-1:
       break
       pass
   fitCount += 1
 fig = plt.figure(facecolor='white')
 plt.subplots_adjust(bottom=0.15,left=0.15,right=0.97,top=0.95)
 ax = fig.add_subplot(111)
 plt.xticks(hVal,hName,rotation=0)
 #plt.xticks(hVal,hName,rotation='vertical')
 ax.set_xlabel(r'$t_{\rm min}$',fontsize=30)
 plt.ylabel('y').set_rotation(0)
 #ax.set_ylabel(r'$a\cdot E_{fit}$',fontsize=40)
 ax.set_ylabel(r'$M_{\rm fit}$',fontsize=30)
 ax.xaxis.labelpad = 0
 ax.yaxis.labelpad = 30
 ax.set_xlim([0,fitCount])
 ax.set_ylim(plotLimit)
 plt.xticks(plt.xticks()[0],fontsize=20)
 plt.yticks(plt.yticks()[0],fontsize=20)
 for x in range(num_symbols):
  ax.errorbar(hValDatn[x],enCentral[x],enError[x],
   color='r',marker=symbList[x],linestyle='')
  ax.errorbar(hValDato[x],eoCentral[x],eoError[x],
   color='b',marker=symbList[x],linestyle='')
  pass
 #ax.errorbar(hValDatn,enCentral,enError,
 # color='r',marker='o',linestyle='')
 #ax.errorbar(hValDato,eoCentral,eoError,
 # color='b',marker='o',linestyle='')
 if fix_tmax:
  boxLabel  = r'$t_{\rm max}='+str(fix_tmax_val)+'$'
 elif fix_tmin:
  boxLabel  = r'$t_{\rm min}='+str(fix_tmin_val)+'$'
 boxLabel += '\n'
 boxLabel += r'$N_{\rm even}='+str(fix_nst)+'$'
 boxLabel += '\n'
 boxLabel += r'$N_{\rm odd}='+str(fix_ost)+'$'
 ax.text(.75*fitCount,1.45,boxLabel,fontsize=20,
  bbox={'facecolor':'white', 'alpha':0.8, 'pad':10})
 if do_vbar:
  for x in range(1,fitCount):
   ax.axvline(x,color='k')
 plt.show()
