import copy
import itertools
import numpy as np
import gvar as gv
import manipulate_dataset as md
from multiprocessing import Pool

#pi0:~simone/python/minFit/Zvqq/new-Zvqq.py
# # intersection of config id
# self.commonConfigId = set(configId[0]).intersection(*configId[1:]) # intersection set of configId
# self.all = list()
# for cl in configId:
#     al = list()
#     for id, j in zip(cl,range(len(cl))):
#         if id in self.commonConfigId:
#             al.append(j)
#             pass
#         pass
#     self.all.append(al)
#     pass
# print 'count configs in db vs the intersection'
# for j in range(len(configId)):
#     print 'npt:', j, 'db:', len(configId[j]), 'all:', len(self.all[j])
#     pass
# self.nconf = len(self.all[0])
# return

def get_intersect(dset,pfix1,pfix2):
 ## -- computes the list of tags which contains the common configurations between the datasets
 ##    returns the common list as a set
 klst1 = []
 klst2 = []
 for key in dset:
  skey = key.split('_')
  if pfix1 == skey[0]:
   klst1.append('_'.join(skey[1:]))
  if pfix2 == skey[0]:
   klst2.append('_'.join(skey[1:]))
 return set(klst1).intersection(klst2)
 
def compute_correlation_pair(dset,pfix1,pfix2):
 ## -- compute correlations for data, only using common configurations
 ##    a pair of prefixes is used, output averaged dataset is returned
 isect = get_intersect(dset,pfix1,pfix2)
 tdat0 = gv.dataset.Dataset()
 print "starting correlations ",pfix1,pfix2
 for key in dset:
  skey = key.split('_')
  if skey[0] == pfix1:
   tdat0[key] = md.average_tag_fn(dset[key]) ## keep suffix
   #print key
   #print tdat0[key]
 if pfix1 != pfix2:
  for key in dset:
   skey = key.split('_')
   if skey[0] == pfix2:
    tdat0[key] = md.average_tag_fn(dset[key])
 tdat1 = gv.dataset.Dataset(keys=[pfix1,pfix2])
 if pfix1 == pfix2:
  for key in isect:
   tdat1.append(pfix1,tdat0[pfix1+'_'+key][0]) # arrays of len 1
 else:
  for key in isect:
   tdat1.append(pfix1,tdat0[pfix1+'_'+key][0])
   tdat1.append(pfix2,tdat0[pfix2+'_'+key][0])
 #print tdat1.keys()
 #print len(tdat1[pfix1])
 #raise ValueError("test")
 #print "starting avg_data"
 #testout = gv.dataset.avg_data(tdat1)
 #print "ending   avg_data"
 #return testout
 return gv.dataset.avg_data(tdat1)

 #tdat1[pfix1] = []
 #tdat1[pfix2] = []
 #for key in isect:
 # tdat1[pfix1].append(tdat0[pfix1+'_'+key])
 #if pfix1 != pfix2:
 # for key in isect:
 #  tdat1[pfix2].append(tdat0[pfix2+'_'+key])
 #return gv.dataset.avg_data(tdat1)

def divide_and_conquer_correlations(dset):
 ## -- split up correlations into multiple small datasets and average each small set
 ##    take correlations of small sets and stitch them together
 ##    computations of small sets done in parallel
 ##    assumes all keys in dset take form '<correlator key>_<series configuration>'
 pflst = []
 ## -- create a list of prefixes
 for key in dset:
  skey = key.split('_')
  if not(skey[0] in pflst):
   pflst.append(skey[0])
 
 rdat = gv.BufferDict()
 call = {}
 ## -- compute diagonals first to construct full dataset
 for key1 in pflst:
  ## -- handled separately because there may be more configurations in full sample
  tdat = compute_correlation_pair(dset,key1,key1)
  rdat[key1] = tdat[key1]
  call[key1,key1] = gv.evalcorr(tdat)[key1,key1]

 for i,key1 in enumerate(pflst):
  for j,key2 in enumerate(pflst):
   if i <= j:
    continue ## -- degenerate with i > j, i == j
   tdat = compute_correlation_pair(dset,key1,key2)
   cdat = gv.evalcorr(tdat)
   call[key1,key2] = cdat[key1,key2]
   call[key2,key1] = cdat[key2,key1]
 ## -- add correlations and return
 rdat = gv.correlate(rdat,call)
 return rdat

## map_async will only take single argument functions, so inputs must be provided as tuples
def compute_diagonal((dset,key)):
 print "diagonal key ",key
 tdat = compute_correlation_pair(dset,key,key)
 return (key,gv.mean(tdat[key]),gv.sdev(tdat[key]),gv.evalcorr(tdat)[key,key])

def compute_offdiagonal((dset,key1,key2)):
 print "off-diagonal key ",(key1,key2)
 tdat = compute_correlation_pair(dset,key1,key2)
 return (key1,key2,gv.evalcorr(tdat)[key1,key2])

maxProcesses=6
def divide_and_conquer_parallel(dset):
 ## -- split up correlations into multiple small datasets and average each small set
 ##    take correlations of small sets and stitch them together
 ##    computations of small sets done in parallel
 ##    assumes all keys in dset take form '<correlator key>_<series configuration>'
 pflst = []
 pool = Pool(processes=maxProcesses)
 ## -- create a list of prefixes
 for key in dset:
  skey = key.split('_')
  if not(skey[0] in pflst):
   pflst.append(skey[0])
  #if len(pflst) > 1:
  # break
 
 rdat = gv.BufferDict()
 call = {}
 # ## -- handled separately because there may be more configurations in full sample
 print "computing diagonal"
 mapout = pool.map(compute_diagonal,zip([dset for x in pflst],pflst))
 print "done computing diagonal"
 for val in mapout:
  rdat[val[0]] = gv.gvar(val[1],val[2])
  call[val[0],val[0]] = val[3]

 idx = np.triu_indices(len(pflst),1)
 print "computing off-diagonal"
 mapout = pool.map(compute_offdiagonal,
  zip([dset for x in idx[0]],[pflst[t] for t in idx[0]],[pflst[t] for t in idx[1]]))
 print "done computing off-diagonal"
 pool.close()
 pool.join()
 for val in mapout:
  call[val[0],val[1]] = val[2]
  call[val[1],val[0]] = np.transpose(val[2])
 ## -- add correlations and return
 rdat = gv.correlate(rdat,call)
 return rdat
 #return gv.BufferDict()
