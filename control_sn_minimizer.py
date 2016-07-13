from corrfitter               import CorrFitter
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
import defines           as df
import define_prior      as dfp
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np
import sn_minimizer      as snm
import sys

makeData = df.do_makedata_3pt

## -- for raw correlator file input
data,dset = make_data(df.mdp,do_makedata=makeData,\
                      do_db=False,filename="./import-correlators-bar3pt")
## --

inPrefix='v4v4'
inPostfix='t6'
outPrefix='prod3'
tsep=6

cmat = list()
if df.do_irrep == "8":
  op_list = [1,2,3,5,6]
  nameStr = "8p"
elif df.do_irrep == "8'":
  op_list = [4,7]
  nameStr = "8m"
elif df.do_irrep == "16":
  op_list = [2,3,4,6]
  nameStr = "16"
for c in op_list:
  cmat.append([data[inPrefix+'s'+str(c)+str(k)+inPostfix] for k in op_list])
cmat = np.array(cmat)
cvec,kvec = snm.minimize_all(cmat,tsep)

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
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
fig.set_size_inches(8,5)
fig.savefig('/home/asm58/dump3pt/'+outPrefix+'.s'+nameStr+'.'+inPrefix+'.opt3pt.pdf',dpi=400)

