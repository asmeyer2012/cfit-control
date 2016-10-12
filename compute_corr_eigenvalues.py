from data_manipulations import standard_load
import gvar as gv
import gvar.linalg as gvl
import defines as df
import define_prior as dfp
import define_prior_3pt as dfp3
import numpy as np
import argparse
import sys
import time
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='fit 3-point correlators') # description of what?
#parser.add_argument('-r','--reset',dest='override_init',action='store_true')
#parser.add_argument('-p','--plot',dest='override_plot',action='store_true')
#parser.add_argument('-d','--dump',dest='dump_gvar',action='store_true')
#parser.add_argument('-D','--dump-by-name',dest='dump_gvar_name',action='store_const',const=None)
parser.add_argument('-l','--load',dest='load_gvar',action='store_false')
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

taglist = list()
filekey = 'a'
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

## -- consolidated all loading into a single file:
start = time.time()
print "loading gvar data: start ",start
dall = standard_load(taglist,filekey,argsin)
print "end ",(time.time() - start)

## -- get entire correlation matrix
start = time.time()
print "making correlation: start ",start
#corall = gv.evalcorr(dall) ## -- super slow
corall = gv.evalcorr(dall.buf) ## -- uses precomputed data, need to slice data manually
print "end ",(time.time() - start)

## -- defines
tmin2 = df.rangeMin
tmax2 = df.rangeMax
## -- dictionaries
covd = {}
cord = {}
covm = np.array([])
corm = np.array([])
for key1 in df.lkey:
 cord[key1] = np.array([])
 for key2 in df.lkey:
  print key1,key2
  cord[key1,key2] = corall[dall.slice(key1),dall.slice(key2)][tmin2:tmax2+1,tmin2:tmax2+1]
  #covd[key1,key2] = gv.evalcov (dall)[key1,key2][tmin2:tmax2+1,tmin2:tmax2+1]
  if len(cord[key1]) > 0:
   cord[key1] = np.vstack((cord[key1],cord[key1,key2]))
   #covd[key1] = np.vstack((covd[key1],covd[key1,key2]))
  else:
   cord[key1] = cord[key1,key2]
   #covd[key1] = covd[key1,key2]
 if len(corm) > 0:
  corm = np.vstack((corm,np.transpose(cord[key1])))
  #covm = np.vstack((covm,np.transpose(covd[key1])))
 else:
  corm = np.transpose(cord[key1])
  #covm = np.transpose(covd[key1])

#if False:
# corm3 = np.array([])
# for key1 in df.lkey3:
#  cord[key1] = np.array([])
#  for key2 in df.lkey3:
#   print key1,key2
#   cord[key1,key2] = corall[key1,key2][tmin2:tmax2+1,tmin2:tmax2+1]
#   #covd[key1,key2] = gv.evalcov (dall)[key1,key2][tmin2:tmax2+1,tmin2:tmax2+1]
#   if len(cord[key1]) > 0:
#    cord[key1] = np.vstack((cord[key1],cord[key1,key2]))
#    #covd[key1] = np.vstack((covd[key1],covd[key1,key2]))
#   else:
#    cord[key1] = cord[key1,key2]
#    #covd[key1] = covd[key1,key2]
#  if len(covm) > 0:
#   corm3 = np.vstack((corm3,np.transpose(cord[key1])))
#   #covm = np.vstack((covm,np.transpose(covd[key1])))
#  else:
#   corm3 = np.transpose(cord[key1])
#   #covm = np.transpose(covd[key1])
#

eval = gvl.eigvalsh(corm)
pval = []
for i,v in enumerate(eval[::-1]):
 pval.append([i,v])
pval = np.transpose(pval)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.scatter(pval[0],pval[1])
ax.set_yscale('log')
ax.set_ylim([1e-3,1e2])
plt.show()

