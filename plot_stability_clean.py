import matplotlib.pyplot as plt
import defines      as df
import define_prior as dfp
import gvar         as gv
import make_init    as mi
import numpy        as np
import util_funcs   as utf
import util_plots   as utp
import os

nst = 6
ost = 4
n3st = 5
o3st = 5
max_nst = 10
max_ost = 10
fix_even = True
fix_odd = not(fix_even)

## -- multiplicities of particles, controls plot symbols
num_symbols = 3
symbList = ['o','^','s']
numN = [3,2,0,4] #Ns, Ds, unknowns
numO = [4,1,1,6]
#numN = [1,3,0,4] #Ns, Ds, unknowns
#numO = [3,4,0,6]
mark_nst = [([y+1>sum(numN[:x]) for x in range(len(numN))].count(True)-1)%num_symbols
 for y in range(max_nst)]
mark_ost = [([y+1>sum(numO[:x]) for x in range(len(numO))].count(True)-1)%num_symbols
 for y in range(max_ost)]

## -- print chi2/pvalue (not sure what to do with these)
do_chi2 = False # not implemented
do_pval = False # not implemented
cut_chi2 = False

## -- fine tuned plotting handles
parity_offset = 0.05 # change distance between even/odd states
do_vbar = False # vertical bars separating different tmin/tmax
plotLimit = [0.6,1.6,0.2]

def plot_stability(fit_collector,**kwargs):
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
 ## -- tkey should be tuple: nst,ost, and 'fit' or 'prior' or other descriptor
 for stin in range(1,10):
   if fix_even:
    tkey=(nst,stin,n3st,o3st)
   else:
    tkey=(stin,ost,n3st,o3st)
   nin = tkey[0]
   oin = tkey[1]
   ## -- ignore fits with large chi2
   try:
    fit_collector[tkey]
   except KeyError:
    continue
   ## -- collect only important info
   hVal.append(fitCount+0.5)
   name = str(nin)+'N+'+str(oin)+'O'
   hName.append(name)
   #hChi2.append(fit_collector[tkey]['chi2'])
   for key in fit_collector[tkey]:
    sum=0
    it=0 #iterator, decides on nucleon vs delta vs unknown
    if key[:2] == 'En' and not(key[3:] == 'log'):
     for x in fit_collector[tkey][key]:
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
 #ax.set_xlabel(r'$\# states$',fontsize=30)
 plt.ylabel('y').set_rotation(0)
 #ax.set_ylabel(r'$a\cdot E_{fit}$',fontsize=40)
 ax.set_ylabel(r'$a M_{\rm fit}$',fontsize=30)
 ax.xaxis.labelpad = 0
 #ax.yaxis.labelpad = 30
 plt.xticks(plt.xticks()[0],fontsize=16,rotation='vertical')
 #plt.yticks(plt.yticks()[0],fontsize=20)
 plt.yticks(list(np.arange(plotLimit[0],plotLimit[1]+1e-8,plotLimit[2])),
  fontsize=20)
 ax.set_xlim([0,fitCount])
 ax.set_ylim(plotLimit[:2])
 for x in range(num_symbols):
  ax.errorbar(hValDatn[x],enCentral[x],enError[x],
   color='r',marker=symbList[x],linestyle='')
  ax.errorbar(hValDato[x],eoCentral[x],eoError[x],
   color='b',marker=symbList[x],linestyle='')
  pass
 ax.yaxis.set_label_coords(-0.1,0.45)
 #ax.errorbar(hValDatn,enCentral,enError,
 # color='r',marker='o',linestyle='')
 #ax.errorbar(hValDato,eoCentral,eoError,
 # color='b',marker='o',linestyle='')
 #boxLabel  = r'$t_{\rm min}='+str(df.rangeMin)+'$'
 #boxLabel += '\n'
 #boxLabel += r'$t_{\rm max}='+str(df.rangeMax)+'$'
 boxLabel  = r'$t\in ['+str(df.rangeMin)+','+str(df.rangeMax)+']$'
 boxLabel += '\n'
 boxLabel += r'$N^{(3)}_{\rm even}='+str(n3st)+'$'
 boxLabel += '\n'
 boxLabel += r'$N^{(3)}_{\rm odd}='+str(o3st)+'$'
 #ax.text(.80*fitCount,1.15,boxLabel,fontsize=20,
 ax.text(.80*fitCount,1.30,boxLabel,fontsize=20,
  bbox={'facecolor':'white', 'alpha':0.8, 'pad':10})
 #ax.text(.75*fitCount,1.45,boxLabel,fontsize=20,
 # bbox={'facecolor':'white', 'alpha':0.8, 'pad':10})
 if do_vbar:
  for x in range(1,fitCount):
   ax.axvline(x,color='k')
 plt.show()

if __name__ == "__main__":
 fit_collector = {}
 for xfile in os.walk('./fit-stability/'):
  for file in xfile[2]:
   if '.pyc' in file:
    continue ## only want non-compiled versions
   if int(file.split('_')[3][2:]) != n3st:
    continue
   if int(file.split('_')[4].split('.')[0][2:]) != o3st:
    continue
   try:
    nin = int(file.split('_')[1][1:])
    oin = int(file.split('_')[2][1:])
    fit_collector[nin,oin,n3st,o3st] = mi.load_dict_from_fit_file_3pt('./fit-stability/',file.split('.')[0])
   except IOError:
    print "IOError"
    continue
   except IndexError:
    continue
 plot_stability(fit_collector)
