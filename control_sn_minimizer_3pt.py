from corrfitter               import CorrFitter
from data_manipulations       import standard_load
from make_data                import make_data
from make_data_db             import make_data_db
from make_models              import make_models
#from make_models              import *
from make_prior               import make_prior
from make_bootstrap           import make_bootstrap
from print_results            import print_fit
from print_results            import print_error_budget
from save_data                import save_data
from save_prior               import save_prior_from_fit
from make_plot                import make_plot
from make_plot                import make_plot_corr_neg
from make_plot                import make_plot_1plus1
from plot_corr_double_log     import plot_corr_double_log
from plot_corr_effective_mass import plot_corr_effective_mass
from plot_corr_normalized     import plot_corr_normalized
from meta_data                import *
from util_files               import read_fit_file
import data_manipulations as dm
import defines           as df
import define_prior      as dfp
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np
import sn_minimizer      as snm
import argparse
import hashlib
import sys

parser = argparse.ArgumentParser(description='fit 3-point correlators') # description of what?
parser.add_argument('-r','--reset',dest='override_init',action='store_true')
parser.add_argument('-p','--plot',dest='override_plot',action='store_true')
parser.add_argument('-d','--dump',dest='dump_gvar',action='store_true')
parser.add_argument('-D','--dump-by-name',dest='dump_gvar_name',action='store_const',const=None)
parser.add_argument('-l','--load',dest='load_gvar',action='store_true')
parser.add_argument('-L','--load-by-name',dest='load_gvar_name',action='store_const',const=None)
argsin = parser.parse_known_args(sys.argv[1:]) ## in namespace
argsin = vars(argsin[0]) ## pull out of namespace
print argsin


if df.do_irrep == "8":
  irrepStr = '8p'
elif df.do_irrep == "8'":
  irrepStr = '8m'
elif df.do_irrep == "16":
  irrepStr = '16p'

taglist = list() # for gvar.dump hash key
filekey = 'a'  ## -- standard choice, no filters
#filekey = 'm'  ## -- munich filter
#print "Using munich filter"
#taglist.append(('l32v5.mes2pt','mes'))
taglist.append(('l32v5.bar2pt.'+irrepStr,'bar2pt'))
if not(df.do_irrep == "16"):
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7'))
else:
 ## -- both 16+ and 16-
 irrepStr = '16p'
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6','16p'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7','16p'))
 irrepStr = '16m'
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6','16m'))
 taglist.append(('l32v5.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7','16m'))

argsin['dump_gvar'] = False
argsin['load_gvar'] = True
dall =  standard_load(taglist,filekey,argsin)

inCurrent=['aiai']
inPostfix='t6'
outCurrent='aiai'
outPrefix='sn3an'
tsep=6

#cmat = list()
#if df.do_irrep == "8":
#  op_list = [1,2,3,5,6]
#  nameStr = "8p"
#elif df.do_irrep == "8'":
#  op_list = [4,7]
#  nameStr = "8m"
#elif df.do_irrep == "16":
#  op_list = [2,3,4,6]
#  nameStr = "16"
#for c in op_list:
#  #cmat.append([dall[inCurrent+'s'+str(c)+str(k)+inPostfix] for k in op_list])
#  datin = list()
#  for k in op_list:
#    datin.append(0)
#    for v in inCurrent:
#      datin[-1] += dall[v+'s'+str(c)+str(k)+inPostfix]
#  cmat.append(datin)
#print cmat
#cmat = np.array(cmat)
#cvec,kvec = snm.minimize_3pt(cmat,tsep)
cvec,kvec,cmat = dm.sn_minimize_postload_3pt(dall,tsep,'aiai')

diag3pt = np.array(snm.apply_matrices(cmat,snm.get_perp_list(cvec),snm.get_perp_list(kvec)))
print 'optimized 3pt'
for t in range(tsep+1):
  print t,diag3pt[:,:,t]

xgv = list()
for i in range(len(diag3pt)):
 for j in range(len(diag3pt)):
  xgv.append(diag3pt[i,j])

markList = ['o','s','p','h','*','v','^','D','+','x']
colorList = ['r','g','b','c','y','m','#115533','#552888','#ef5500','#218386','#404040']

fig = plt.figure(facecolor='white')
plt.subplots_adjust(bottom=0.12,left=0.12,right=0.85,top=0.97)
ax = fig.gca()
handles = []
labels = []
i=-1
for j in range(len(diag3pt)):
 i=i+1
 handles.append(
  ax.errorbar(
   #[x+2.*(i-len(diag3pt)*len(diag3pt)/2.)/(3.*len(diag3pt)*len(diag3pt)) for x in range(tsep+1)],
   [x+2.*(i-len(diag3pt)/2.)/(3.*len(diag3pt)) for x in range(tsep+1)],
   #[x.mean for x in xgv[:tsep+1]],
   [x.mean/xgv[j][tsep/2].mean for x in xgv[j][:tsep+1]],
  yerr=[x.sdev/xgv[j][tsep/2].mean for x in xgv[j][:tsep+1]],
  linestyle='',
  markersize=2,
  capsize=1,
  elinewidth=1,
  linewidth=0.3,
  mfc=colorList[i%len(colorList)],
  color=colorList[i%len(colorList)],
  marker=markList[i%len(markList)]#,
  #label=str(key[1])+str(key[2])+str(key[3])+'-'+key[4]
  )
 )
 #labels.append(str(key[1])+str(key[2])+str(key[3])+'-'+key[4])
 #labels.append('State '+str(j/len(diag3pt))+str(j%len(diag3pt))+' '+outPrefix)
 labels.append('Optimization '+str(j)+' '+outPrefix)
pass
ax.set_xlabel(r'$\tau$ ',fontsize=15)
plt.ylabel('y').set_rotation(0) # rotation of y axis label
ax.set_ylabel(r'$\frac{w^{T}\cdot C\cdot v(\tau,'+str(tsep)+')}{w^{T}\cdot C\cdot v('+str(tsep/2)+','+str(tsep)+')}$',fontsize=15)
ax.xaxis.labelpad = 10 # vertical alignment of x axis label
ax.yaxis.labelpad = 15 # horizontal alignment of y axis label
ax.set_xlim(-.5,tsep+.5)
ax.set_ylim(-3,3)
plt.legend(handles,labels,fontsize=4,numpoints=1,bbox_to_anchor=(1.001,1),loc=2,borderaxespad=0.,frameon=False)
plt.axhline(0,color='k')
plt.xticks(range(0,tsep+1),fontsize=10)
plt.yticks(range(-3,4),fontsize=10)
#plt.get_current_fig_manager().full_screen_toggle() ## full screen, not maximized
if True:
 plt.show()
else:
 mng = plt.get_current_fig_manager()
 mng.resize(*mng.window.maxsize())
 fig.set_size_inches(8,5)
 fig.savefig('/home/asm58/dump3pt/'+outPrefix+'_s'+nameStr+'_'+outCurrent+'.pdf',dpi=400)

