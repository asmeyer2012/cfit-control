import gvar as gv
import numpy as np

def fn_apply_tags(dset,fn,prea,preb=None,newtag=None,copytags=False):
  """
  -- applies a function fn to a pair of prefixes for all matching suffixes
  -- pre(fix)a may be a list of prefixes,
     in which case the function is applied to all with the same pre(fix)b
  -- if newtag is provided, saves the result with the prefix newtag, otherwise with prea
  -- if preb==None, calculates fn([prea])
     otherwise calculates fn([prea],[preb])
  ==
  -- use before consolidate_tags
  """
  dout = gv.dataset.Dataset()
  if not(newtag is None):
   pout=newtag
  else: 
   pout=prea
  if isinstance(prea,str):
   ## -- apply just to a single prea
   for tag in dset:
    pfix = '_'.join(tag.split('_')[:-1])
    if pfix == prea:
     sfix = '_'+tag.split('_')[-1]
     if not(preb is None):
      ## -- 2-tag function
      try: 
       dout[pout+sfix] = fn(dset[prea+sfix],dset[preb+sfix])
      except KeyError:
       print "key",preb+sfix,"missing from dataset"
       continue
     else:
      ## -- 1-tag function
      dout[pout+sfix] = fn(dset[prea+sfix])
  else:
   ## -- apply to the entire list of prea
   for tag in dset:
    pfix = '_'.join(tag.split('_')[:-1])
    if pfix in prea:
      pos = [i for i,x in enumerate(prea) if x==pfix][0]
      sfix = '_'+tag.split('_')[-1]
      if not(preb is None):
       ## -- 2-tag function
       try: 
        dout[pout[pos]+sfix] = fn(dset[pfix+sfix],dset[preb+sfix])
       except KeyError:
        print "key",preb+sfix,"missing from dataset"
        continue
      else:
       ## -- 1-tag function
       dout[pout[pos]+sfix] = fn(dset[pfix+sfix])
  if copytags: ## -- copy over unused tags
   if isinstance(pout,str):
    for tag in dset:
     pfix = '_'.join(tag.split('_')[:-1])
     if pfix != pout:
      dout[tag] = dset[tag]
   else:
    for tag in dset:
     pfix = '_'.join(tag.split('_')[:-1])
     if not(pfix in pout):
      dout[tag] = dset[tag]
  return dout

def fn_apply_tags2(dseta,dsetb,fn,prea,preb=None,newtag=None,copytags=False):
  """
  -- same as fn_apply_tags, but when prea and preb are in different data sets
  ==
  -- use before consolidate_tags
  """
  dout = gv.dataset.Dataset()
  if not(newtag is None):
   pout=newtag
  else: 
   pout=prea
  if isinstance(prea,str):
   ## -- apply just to a single prea
   for tag in dseta:
    pfix = '_'.join(tag.split('_')[:-1])
    if pfix == prea:
     sfix = '_'+tag.split('_')[-1]
     if not(preb is None):
      ## -- 2-tag function
      try: 
       dout[pout+sfix] = fn(dseta[prea+sfix],dsetb[preb+sfix])
      except KeyError:
       print "key",preb+sfix,"missing from dataset"
       continue
     else:
      ## -- 1-tag function
      dout[pout+sfix] = fn(dseta[prea+sfix])
  else:
   ## -- apply to the entire list of prea
   for tag in dseta:
    pfix = '_'.join(tag.split('_')[:-1])
    if pfix in prea:
      pos = [i for i,x in enumerate(prea) if x==pfix][0]
      sfix = '_'+tag.split('_')[-1]
      if not(preb is None):
       ## -- 2-tag function
       try: 
        dout[pout[pos]+sfix] = fn(dseta[pfix+sfix],dsetb[preb+sfix])
       except KeyError:
        print "key",preb+sfix,"missing from dataset"
        continue
      else:
       ## -- 1-tag function
       dout[pout[pos]+sfix] = fn(dseta[pfix+sfix])
  if copytags: ## -- copy over unused tags
   if isinstance(pout,str):
    for tag in dseta:
     pfix = '_'.join(tag.split('_')[:-1])
     if pfix != pout:
      dout[tag] = dseta[tag]
   else:
    for tag in dseta:
     pfix = '_'.join(tag.split('_')[:-1])
     if not(pfix in pout):
      dout[tag] = dseta[tag]
  return dout

def average_tag_fn(cor):
  """
  -- average all correlators in a list
  ==
  -- function called by fn_apply_tags
  """
  sum=np.zeros(len(cor[0]))
  for c in cor:
   sum=np.add(sum,c)
  return [sum/len(cor)]

def plateau_tag_fn(cor):
  """
  -- (dumb) average of correlator for all values of t
  ==
  -- function called by fn_apply_tags
  """
  sum=0
  for c in cor:
   sum+=np.sum(c)
  return sum/(len(cor)*len(cor[0]))

def project_t_fn(cor,t):
  """
  -- remove all but specified values of t
  ==
  -- prototype function
     must define a new function with t fixed to use with fn_apply_tags
  """
  cnew=list()
  for c in cor:
   cnew.append(np.array([c[tp] for tp in t]))
  return cnew

def apply_t_fn(cor,fn,t=None):
  """
  -- apply a function fn(cor,t)
  ==
  -- prototype function
     must define a new function with fn fixed to use with fn_apply_tags
  """
  cnew=list()
  if t is None:
   tval=range(len(cor[0]))
  else:
   tval=t
  for c in cor:
   cnew.append(np.array([fn(c,tp) for tp in tval]))
  return cnew

# -- not sure if this is what I want, averages before ratio

def correlator_pion_ratio_fn(cora,corb,t,T,expm,fac):
  """
  -- average corb*expm^t for a range of t,
     then divide all of cora by fac*sqrt(avg)
  ==
  -- prototype function
     must define a new function with t,T,expm,fac fixed to use with fn_apply_tags
  """
  def fexp(cor,tp):
    if tp<T/2:
     return np.abs(cor[tp])*np.power(expm,float(tp))
    else:
     return np.abs(cor[tp])*np.power(expm,float(T-tp))
  cor2=average_tag_fn(corb)
  cor1=apply_t_fn(cor2,fexp,t)
  cor0=plateau_tag_fn(cor1)
  cor0=gv.mean(np.sqrt(cor0)*fac)
  cnew=list()
  for c in cora:
   cnew.append(c*cor0)
  return cnew

def correlator_timeshift_ratio(cor,tshf):
  """
  -- shifts a correlator by tshf, then takes the ratio with the original
  ==
  -- prototype function
     must define a new function with tshf fixed to use with fn_apply_tags
  """
  cnew = list()
  for c in cor:
   cshf = c[tshf:]
   corg = c[:len(cor)-tshf]
   cnew.append(list(np.array(cshf)/np.array(corg)))
  return cnew

def correlator_power(cor,pwr):
  """
  -- takes all timeslices of correlator to some power
  ==
  -- prototype function
     must define a new function with tshf fixed to use with fn_apply_tags
  """
  cnew = list()
  for c in cor:
   cnew.append(list())
   for t in range(len(c)):
    cnew[-1].append(np.power(c[t],pwr))
    if np.isnan(cnew[-1][-1]):
     cnew[-1][-1] = 0.
  return cnew

def correlator_plateau_avg(cor):
  """
  -- calculate dumb average of entire correlator
  ==
  -- use before consolidate tags
  """
  cnew = list()
  for c in cor:
   cnew.append(np.sum(c)/len(c))
  return cnew

def separate_tags(dset,tag):
  """
  -- return a dataset whose suffix tags are only in the list of tags provided
  ==
  """
  dout = gv.dataset.Dataset()
  for key in dset:
   sfix=key.split('_')[-1]
   try:
    if not(sfix in tag):
     continue
   except KeyError:
    if sfix != tag:
     continue
   if not(key in dout):
    dout[key] = list()
   for cor in dset[key]:
    dout[key].append(cor)
  return dout

def consolidate_tags(dset):
  """
  -- remove suffix part of all tags and collects data based on prefix
  -- can have multiple suffixes, all separated by '_', only removes last suffix
  ==
  """
  dout = gv.dataset.Dataset()
  for key in dset:
   pfix='_'.join(key.split('_')[:-1])
   #print pfix
   try:
    ## -- test if entry already exists
    for cor in dset[key]:
     dout[pfix].append(cor)
   except KeyError:
    #dset[pfix] = list()
    dout[pfix] = list()
    for cor in dset[key]:
     dout[pfix].append(cor)
  return dout

def average_tags(dset):
  """
  -- same as consolidate_tags, except averages configurations rather than appending
  -- removes last suffix during process
  ==
  """
  dout = gv.dataset.Dataset()
  maxn = 0
  dowarn = False
  for key in dset:
   pfix='_'.join(key.split('_')[:-1])
   #print pfix
   try:
    ## -- test if entry already exists
    for cor in dset[key]:
     if any([all(x in cor for x in corout) for corout in dout[pfix]]):
      if dowarn:
       print "warning: repeat entry for key",pfix
      continue
     dout[pfix].append(cor)
    maxn = max(len(dout[pfix]),maxn) ## -- keep track of lengths
   except KeyError:
    #dset[pfix] = list()
    dout[pfix] = list()
    for cor in dset[key]:
     if any([all(x in cor for x in corout) for corout in dout[pfix]]):
      if dowarn:
       print "warning: repeat entry for key",pfix
      continue
     dout[pfix].append(cor)
  for key in dout:
   ## -- if length is shorter, delete data from dictionary and warn
   if len(dout[key]) < maxn:
    if dowarn:
     print "warning: key",key,"has",len(dout[key]),"of",maxn,\
      "required entries to be averaged, ignoring"
    dout.pop(key,None)
  for key in dout:
   dout[key] = average_tag_fn(dout[key])
  return dout

def average_prefix(dset,pfixin,pfixout):
  """
  -- averages all leading prefixes in list pfixin
  -- returns dataset with averaged prefixes replaced by pfixout
  -- all other prefixes are returned unchanged
  ==
  """
  dout = gv.dataset.Dataset()
  print "averaging keys for prefix in ",pfixin
  for key in dset:
   pfix=key.split('_')[0]
   if pfix in pfixin:
    sfix='_'.join(key.split('_')[1:])
    try:
     ## -- test if entry already exists
     for cor in dset[key]:
      dout[pfixout+'_'+sfix].append(cor)
    except KeyError:
     dout[pfixout+'_'+sfix] = list()
     for cor in dset[key]:
      dout[pfixout+'_'+sfix].append(cor)
   else:
    dout[key] = dset[key]
  for key in dout:
   if key.split('_')[0] == pfixout:
    dout[key] = average_tag_fn(dout[key])
  return dout

def scale_tag(dset,tag,fac):
  """
  -- scales all correlators of a specific tag or list of tags by fac
  ==
  -- use after consolidate_tags
  -- argument dset is altered by this function
  """
  if isinstance(tag,str):
    ## -- single tag given
    cnew = list()
    for cor in dset[tag]:
     cnew.append(cor*fac)
    dset[tag] = cnew
  else:
    ## -- assuming list of tags given
    for key in tag:
      cnew = list()
      for cor in dset[key]:
       cnew.append(cor*fac)
      dset[key] = cnew
  return dset

def munich_filter(dset,tag):
  """
  -- multiplies correlators of tag or list of tags by -1^t
  -- name supplied by Andreas Kronfeld
  ==
  -- use after consolidate_tags
  -- argument dset is altered by this function
  """
  if isinstance(tag,str):
    ## -- single tag given
    cnew = list()
    tfac = np.array(np.cos(np.pi*np.arange(len(dset[tag][0]))))
    for cor in dset[tag]:
     #cnew.append(list(np.array(cor)*tfac))
     cnew.append(cor*tfac)
    dset[tag] = cnew
  else:
    ## -- assuming list of tags given
    for key in tag:
      cnew = list()
      tfac = np.array(np.cos(np.pi*np.arange(len(dset[key][0]))))
      for cor in dset[key]:
       #cnew.append(list(np.array(cor)*tfac))
       cnew.append(cor*tfac)
      dset[key] = cnew
  return dset

#def average_tag(dset,tag=None):
#  """
#  -- (dumb) average of all data which share a tag
#  -- if no tag provided, averages all tags
#  ==
#  -- use after consolidate_tags
#  """
#  if not(tag is None):
#   if isinstance(tag,str):
#    ## -- single tag provided, use that one
#    klen = len(dset[tag])
#    if klen > 1:
#     sum=np.zeros(len(dset[tag][0]))
#     for cor in dset[tag]:
#      sum=np.add(sum,cor)
#     dset[tag]=[sum/klen]
#    else:
#     dset[tag]=dset[tag]
#   else:
#    ## -- multiple tags in a list, do over all
#    for key in tag:
#     klen = len(dset[key])
#     if klen > 1:
#      sum=np.zeros(len(dset[key][0]))
#      for cor in dset[key]:
#       sum=np.add(sum,cor)
#      dset[key]=[sum/klen]
#     else:
#      dset[key]=dset[key]
#     #dset[key]=average_tag(dset,key)[key]
#  else:
#   ## -- no tag, loop over all keys
#   for key in dset:
#    dset[key]=average_tag(dset,key)[key]
#  pass
#  return dset

def project_t_tag(dset,tag,t,newtag=None):
  """
  -- return only values of t from the list provided for correlator tags
  ==
  -- use after consolidate_tags
  -- argument dset is altered by this function
  """
  if not(newtag is None):
    otag = newtag
  else:
    otag = tag
  cnew = list()
  if isinstance(tag,str):
   for cor in dset[tag]:
    cnew.append(np.array([cor[tp] for tp in t]))
   dset[otag] = cnew
  else:
   for key,okey in zip(tag,otag):
    dset[okey]=project_t_tag(dset,key,t,okey)[okey]
  return dset

def cat_dataset(dset1,dset2):
  """
  -- combines all tags in the two datasets into a third
  -- if tags are shared between the two datasets, they are combined
  """
  dout = gv.dataset.Dataset()
  for key in dset1:
   dout[key] = dset1[key]
  for key in dset2:
   if key in dset1:
    for cor in dset2[key]:
     dout[key].append(cor)
    pass
   else:
    dout[key] = dset2[key]
  return dout

## test routines
#dset = gv.dataset.Dataset('testdata')
#print 'dset',dset
#def testfn(cora,corb):
#  return correlator_ratio_fn(cora,corb,range(len(cora[0]))[1:],0.2,1.0)
#dtest3 = fn_apply_tags(dset,testfn,'H','H',newtag='J')
#print 'dtest3',dtest3
#dtest3 = fn_apply_tags(dset,testfn,'H','H',newtag='J',copytags=True)
#print 'dtest3',dtest3
#dtest3 = fn_apply_tags(dset,average_tag_fn,['H','I'],newtag=['J','K'])
#print 'dtest3',dtest3
#dtest1 = average_tag(dset)
#print 'dtest1',dtest1
#print 'dtest1',dset
#dtest2 = average_tag(dset,'I_1')
#print 'dtest2',dtest2
#print 'dtest3',dset
#dtest3 = average_tag(dset,'H_1')
#print 'dtest3',dtest3
#dtest4 = average_tag(dset,['H_1','I_1'])
#print 'dtest4',dtest4
#dtest5 = consolidate_tags(dtest4)
#print 'dtest5',dtest5
#dtest6 = scale_tag(dtest5,'H',2)
#print 'dtest6',dtest6
#dtest6 = project_t_tag(dtest5,'H',[2,3,4])
#print 'dtest6',dtest6
