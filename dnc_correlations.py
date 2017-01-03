import numpy as np
import gvar as gv
import manipulate_dataset as md

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
 for key in dset:
  skey = key.split('_')
  if skey[0] == pfix1:
   tdat0[key] = md.average_tag_fn(dset[key]) ## keep suffix
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
