import gvar as gv
import numpy as np
import defines as df
import define_prior as dfp
import define_prior_3pt as dfp3
import util_funcs as utf

def add_first_blocks(keylistn,keylisto,keylistv,numstn,numsto,En,Eo,dEn,dEo,
  g0n=gv.gvar(0,1e1),g0o=gv.gvar(0,1e1), gxn=gv.gvar(0,1e0),gxo=gv.gvar(0,1e0),
  #lAn=gv.gvar(1,1e2),lAo=gv.gvar(1,1e2), An=gv.gvar(0,1e2),Ao=gv.gvar(0,1e2),
  #lAn=gv.gvar(1,3e1),lAo=gv.gvar(1,3e1), An=gv.gvar(0,3e1),Ao=gv.gvar(0,3e1),
  #lAn=gv.gvar(1,2e1),lAo=gv.gvar(1,2e1), An=gv.gvar(0,2e1),Ao=gv.gvar(0,2e1),
  lAn=gv.gvar(1,1e1),lAo=gv.gvar(1,1e1), An=gv.gvar(0,1e1),Ao=gv.gvar(0,1e1),
  vdn=gv.gvar(0,1e0),vdo=gv.gvar(0,1e0), vxs=gv.gvar(0,1e0),
  symmetric_V=True, explicit_priors={}):
 prior = gv.BufferDict()
 ## -- add first even and odd block to a set of priors, return that set of priors when done
 tag0 = '_0'
 for key in keylistn:
  if key in explicit_priors:
   prior[key+tag0] = explicit_priors[key][:numstn]
  else:
   bkey = utf.get_basekey(key)
   if   bkey[1][-2:] == 'En':
    prior[key+tag0] = gv.gvar([En.mean]+[dEn.mean]*(numstn-1),[En.sdev]+[dEn.sdev]*(numstn-1))
   elif bkey[1][-2:] == 'gn':
    prior[key+tag0] = gv.gvar([g0n.mean]+[gxn.mean]*(numstn-1),[g0n.sdev]+[gxn.sdev]*(numstn-1))
   else:
    #if   bkey[0] == 'log' or bkey[0] == 'sqrt':
    if not(bkey[0] is None):
     prior[key+tag0] = gv.gvar([lAn.mean]*numstn,[lAn.sdev]*numstn)
    else:
     prior[key+tag0] = gv.gvar([An.mean]*numstn,[An.sdev]*numstn)
 for key in keylisto:
  if key in explicit_priors:
   prior[key+tag0] = explicit_priors[key][:numsto]
  else:
   bkey = utf.get_basekey(key)
   if   bkey[1][-2:] == 'Eo':
    prior[key+tag0] = gv.gvar([Eo.mean]+[dEo.mean]*(numsto-1),[Eo.sdev]+[dEo.sdev]*(numsto-1))
   elif bkey[1][-2:] == 'go':
    prior[key+tag0] = gv.gvar([g0o.mean]+[gxo.mean]*(numsto-1),[g0o.sdev]+[gxo.sdev]*(numsto-1))
   else:
    #if   key[:3] == 'log' or key[:4] == 'sqrt':
    if not(bkey[0] is None):
     prior[key+tag0] = gv.gvar([lAo.mean]*numsto,[lAo.sdev]*numsto)
    else:
     prior[key+tag0] = gv.gvar([Ao.mean]*numsto,[Ao.sdev]*numsto)
 tag0 = '_0_0'
 for key in keylistv:
  if key in explicit_priors:
   ## -- assume it is already properly truncated
   prior[key+tag0] = explicit_priors[key]
  else:
   eokey = utf.get_evenodd(key)
   if   eokey == 'nn':
    if symmetric_V:
     prior[key+tag0] = gv.gvar([vdn.mean]*(numstn*(numstn-1)/2),[vdn.sdev]*(numstn*(numstn-1)/2))
    else:
     prior[key+tag0] = gv.gvar([[vdn.mean]*numstn]*numstn,[[vdn.sdev]*numstn]*numstn)
   elif eokey == 'oo':
    if symmetric_V:
     prior[key+tag0] = gv.gvar([vdo.mean]*(numsto*(numsto-1)/2),[vdo.sdev]*(numsto*(numsto-1)/2))
    else:
     prior[key+tag0] = gv.gvar([[vdo.mean]*numsto]*numsto,[[vdo.sdev]*numsto]*numsto)
   elif eokey == 'no':
    prior[key+tag0] = gv.gvar([[vxs.mean]*numsto]*numstn,[[vxs.sdev]*numsto]*numstn)
   elif eokey == 'on':
    if symmetric_V:
     continue
    prior[key+tag0] = gv.gvar([[vxs.mean]*numstn]*numsto,[[vxs.sdev]*numstn]*numsto)
 ## -- return
 #print 'first prior',prior
 return prior

def add_next_block(prior,newEven,numst,E0,dE, g0s=gv.gvar(0,1e1), gxs=gv.gvar(0,3e-1),
  #lAs=gv.gvar(1,1e2), As=gv.gvar(0,1e2), vds=gv.gvar(0,1e0), vxs=gv.gvar(0,1e1),
  #lAs=gv.gvar(1,3e1), As=gv.gvar(0,3e1), vds=gv.gvar(0,1e0), vxs=gv.gvar(0,1e1),
  #lAs=gv.gvar(1,2e1), As=gv.gvar(0,2e1), vds=gv.gvar(0,1e0), vxs=gv.gvar(0,1e1),
  lAs=gv.gvar(1,1e1), As=gv.gvar(0,1e1), vds=gv.gvar(0,1e0), vxs=gv.gvar(0,1e1),
  symmetric_V=True,explicit_priors={}):
 ## -- sort to find out how many blocks of even, odd; key prefixes
 #print 'in prior',prior
 kpre = []
 nn = 0
 no = 0
 for key in prior:
  sp = key.split('_')
  if not(sp[0] in kpre):
   kpre.append(sp[0])
  if len(sp) < 3:
   continue
  eokey = utf.get_evenodd(key)
  if eokey == 'on':
   no = max(int(sp[1]),no)
   nn = max(int(sp[2]),nn)
  if eokey != 'no':
   continue
  else:
   nn = max(int(sp[1]),nn)
   no = max(int(sp[2]),no)
 #print "block: ",newEven
 #print numst,nn,no

 ## -- add a set of priors for each prefix
 for key in kpre:
  if newEven: ## -- add even state block
   bkey = utf.get_basekey(key)
   eokey = utf.get_evenodd(key)
   if   eokey == 'nn': ## -- vnn
    for k in range(nn+1):   ## -- off diagonals
      lnn = len(prior[key+'_'+str(k)+'_'+str(k)])
      lnn = (1+int(np.round(np.sqrt(1+8*lnn))))/2
      nkey = key+'_'+str(k)+'_'+str(nn+1)
      #print 'nn',nkey,lnn,k,nn
      if key in explicit_priors:
       prior[nkey] = explicit_priors[key] 
      else:
       prior[nkey] = gv.gvar([[vxs.mean]*numst]*lnn,[[vxs.sdev]*numst]*lnn)
      if not(symmetric_V):
       nkey = key+'_'+str(nn+1)+'_'+str(k)
       #print 'nn',nkey,lnn,nn,k
       if key in explicit_priors:
        prior[nkey] = explicit_priors[key] 
       else:
        prior[nkey] = gv.gvar([[vxs.mean]*lnn]*numst,[[vxs.sdev]*lnn]*numst)
    nkey = key+'_'+str(nn+1)+'_'+str(nn+1)
    if key in explicit_priors:
     prior[nkey] = explicit_priors[key]
    else:
     if symmetric_V: ## -- diagonal
       #print "prior nn",numst,(numst*(numst-1))/2
       prior[nkey] = gv.gvar([vxs.mean]*(numst*(numst-1)/2),[vds.sdev]*(numst*(numst-1)/2))
     else:
       prior[nkey] = gv.gvar([[vxs.mean]*numst]*numst,[[vds.sdev]*numst]*numst)
   elif eokey == 'no':
    prekey = utf.get_fnkey(bkey[1][:-2]+'oo',bkey[0])
    for k in range(no+1):
      loo = len(prior[prekey+'_'+str(k)+'_'+str(k)])
      loo = (1+int(np.round(np.sqrt(1+8*loo))))/2
      #print key,'no',loo,numst
      nkey = key+'_'+str(nn+1)+'_'+str(k)
      if not(key in explicit_priors):
       prior[nkey] = gv.gvar([[vxs.mean]*loo]*numst,[[vxs.sdev]*loo]*numst)
      else:
       prior[nkey] = explicit_priors[key] 
   elif eokey == 'on':
    if symmetric_V:
     continue
    prekey = utf.get_fnkey(bkey[1][:-2]+'oo',bkey[0])
    for k in range(no+1):
      loo = len(prior[prekey+'_'+str(k)+'_'+str(k)])
      loo = (1+int(np.round(np.sqrt(1+8*loo))))/2
      #print 'on',loo
      nkey = key+'_'+str(k)+'_'+str(nn+1)
      if not(key in explicit_priors):
       prior[nkey] = gv.gvar([[vxs.mean]*numst]*loo,[[vxs.sdev]*numst]*loo)
      else:
       prior[nkey] = explicit_priors[key] 
   elif eokey == 'n': ## -- different behavior for gn, En, an, bn
    nkey = key+'_'+str(nn+1)
    if key in explicit_priors:
     prior[nkey] = explicit_priors[key][:numst]
    else:
     if   bkey[1][-2:] == 'En':
      Ex = sum([prior[key+'_'+str(t)][0].mean for t in range(nn+1)])
      prior[nkey] = gv.gvar([E0.mean-Ex]+[dE.mean]*(numst-1), [E0.sdev]+[dE.sdev]*(numst-1))
      #prior[nkey] = gv.gvar([E0.mean-prior[key+'_'+str(nn)][0].mean]
      # +[dE.mean]*(numst-1),[E0.sdev]+[dE.sdev]*(numst-1))
      assert prior[nkey][0] > 0,"Even energy for block "+str(nn+1)+" not monotonically increasing"
     elif bkey[1][-2:] == 'gn':
      prior[nkey] = gv.gvar([g0s.mean]+[gxs.mean]*(numst-1),[g0s.sdev]+[gxs.sdev]*(numst-1))
     else: ## -- an, bn
      #if key[:3] == 'log' or key[:4] == 'sqrt':
      if not(bkey[0] is None):
       prior[nkey] = gv.gvar([lAs.mean]*numst,[lAs.sdev]*numst)
      else:
       prior[nkey] = gv.gvar([As.mean]*numst,[As.sdev]*numst)

  else: ## -- add odd state block
   bkey = utf.get_basekey(key)
   eokey = utf.get_evenodd(key)
   if   eokey == 'oo':
    for k in range(no+1):   ## -- off diagonals
      loo = len(prior[key+'_'+str(k)+'_'+str(k)])
      loo = (1+int(np.round(np.sqrt(1+8*loo))))/2
      #print 'oo',loo
      nkey = key+'_'+str(k)+'_'+str(no+1)
      if key in explicit_priors:
       prior[nkey] = explicit_priors[key] 
      else:
       prior[nkey] = gv.gvar([[vxs.mean]*numst]*loo,[[vxs.sdev]*numst]*loo)
      if not(symmetric_V):
       nkey = key+'_'+str(no+1)+'_'+str(k)
       if key in explicit_priors:
        prior[nkey] = explicit_priors[key] 
       else:
        prior[nkey] = gv.gvar([[vxs.mean]*loo]*numst,[[vxs.sdev]*loo]*numst)
    nkey = key+'_'+str(no+1)+'_'+str(no+1)
    if symmetric_V: ## -- diagonal
      prior[nkey] = gv.gvar([vxs.mean]*(numst*(numst-1)/2),[vds.sdev]*(numst*(numst-1)/2))
    else:
      prior[nkey] = gv.gvar([[vxs.mean]*numst]*numst,[[vds.sdev]*numst]*numst)
   elif eokey == 'no':
    prekey = utf.get_fnkey(bkey[1][:-2]+'nn',bkey[0])
    for k in range(nn+1):
      lnn = len(prior[prekey+'_'+str(k)+'_'+str(k)])
      lnn = (1+int(np.round(np.sqrt(1+8*lnn))))/2
      #print 'no',lnn
      nkey = key+'_'+str(k)+'_'+str(no+1)
      if not(key in explicit_priors):
       prior[nkey] = gv.gvar([[vxs.mean]*numst]*lnn,[[vxs.sdev]*numst]*lnn)
      else:
       prior[nkey] = explicit_priors[key] 
   elif eokey == 'on':
    if symmetric_V:
     continue
    prekey = utf.get_fnkey(bkey[1][:-2]+'nn',bkey[0])
    for k in range(nn+1):
      lnn = len(prior[prekey+'_'+str(k)+'_'+str(k)])
      lnn = (1+int(np.round(np.sqrt(1+8*lnn))))/2
      #print 'on',lnn
      nkey = key+'_'+str(no+1)+'_'+str(k)
      if not(key in explicit_priors):
       prior[nkey] = gv.gvar([[vxs.mean]*numst]*lnn,[[vxs.sdev]*numst]*lnn)
      else:
       prior[nkey] = explicit_priors[key] 
   elif eokey == 'o':
    nkey = key+'_'+str(no+1)
    if key in explicit_priors:
     prior[nkey] = explicit_priors[key][:numst]
    else:
     if   bkey[1][-2:] == 'Eo':
      Ex = sum([prior[key+'_'+str(t)][0].mean for t in range(no+1)])
      prior[nkey] = gv.gvar([E0.mean-Ex]+[dE.mean]*(numst-1), [E0.sdev]+[dE.sdev]*(numst-1))
      #prior[nkey] = gv.gvar([E0.mean-prior[key+'_'+str(no)][0].mean]
      # +[dE.mean]*(numst-1),[E0.sdev]+[dE.sdev]*(numst-1))
      assert prior[nkey][0] > 0,"Odd energy for block "+str(no+1)+" not monotonically increasing"
     elif bkey[1][-2:] == 'go':
      prior[nkey] = gv.gvar([g0s.mean]+[gxs.mean]*(numst-1),[g0s.sdev]+[gxs.sdev]*(numst-1))
     else: ## -- ao, bo
      #if key[:3] == 'log' or key[:4] == 'sqrt':
      if not(bkey[0] is None):
       prior[nkey] = gv.gvar([lAs.mean]*numst,[lAs.sdev]*numst)
      else:
       prior[nkey] = gv.gvar([As.mean]*numst,[As.sdev]*numst)
 ## -- return
 #print 'out prior',prior
 return prior

def truncate_prior_states_2pt(prior,nn,no):
 ## -- reduce to nn even and no odd states
 ##    highest energy states are removed before lower-energy states
 nst = []
 ost = []
 ## -- tabulate energies/blocks
 for key in prior:
  skey = key.split('_')
  bkey = utf.get_basekey(skey[0])
  if bkey[1][-2:] == 'En' or bkey[1][-2:] == 'Eo':
   i = int(skey[1])
   if   bkey[0] == 'log':
    en = gv.exp(prior[key])
   elif bkey[0] == 'sqrt':
    en = prior[key]*prior[key]
   else:
    en = prior[key]
   for e in en:
    if   bkey[1][-2:] == 'En':
      nst.append([e,i])
    elif bkey[1][-2:] == 'Eo':
      ost.append([e,i])
 nstx = []
 ostx = []
 for x,y in [(nst,nstx),(ost,ostx)]:
  e0 = 0
  i = -1
  for ste,sti in x:
   if sti > i:
    i = sti
    e0 += ste
    e   = e0
    y.append([e0,sti])
   else:
    e += ste
    y.append([e,sti])
 nst = nstx
 ost = ostx

 ## -- order states and determine how many to cut from each 
 nst = np.array(sorted(nst)[nn:])
 ost = np.array(sorted(ost)[no:])
 if len(nst) > 0:
  nst = sorted(np.transpose(nst)[1])
 if len(ost) > 0:
  ost = sorted(np.transpose(ost)[1])
 ## -- build new prior dictionary
 newprior = gv.BufferDict()
 for key in prior:
  skey = key.split('_')
  bkey = utf.get_basekey(skey[0])
  eokey = utf.get_evenodd(skey[0])
  k = int(skey[1])
  kp = len(prior[key])
  ## -- everything else
  if (eokey != 'nn') and (eokey != 'oo') and (bkey[1][-2] != 'g'):
   for v, x1 in [('n',list(nst)),('o',list(ost))]:
    if eokey == v:
     c1 = list(x1).count(k)
    else:
     continue
    if c1 == 0:
     newprior[key] = prior[key]
    elif c1 >= kp:
      continue
    else:
     newprior[key] = prior[key][slice(None,kp-c1)]
 return newprior

def truncate_prior_states(prior,nn,no,nn3=-1,no3=-1):
 ## -- reduce to nn even and no odd states
 ##    highest energy states are removed before lower-energy states
 nst = []
 ost = []
 ## -- tabulate energies/blocks
 for key in prior:
  skey = key.split('_')
  bkey = utf.get_basekey(skey[0])
  if bkey[1][-2:] == 'En' or bkey[1][-2:] == 'Eo':
   i = int(skey[1])
   if   bkey[0] == 'log':
    en = gv.exp(prior[key])
   elif bkey[0] == 'sqrt':
    en = prior[key]*prior[key]
   else:
    en = prior[key]
   for e in en:
    if   bkey[1][-2:] == 'En':
      nst.append([e,i])
    elif bkey[1][-2:] == 'Eo':
      ost.append([e,i])
 nstx = []
 ostx = []
 for x,y in [(nst,nstx),(ost,ostx)]:
  e0 = 0
  i = -1
  for ste,sti in x:
   if sti > i:
    i = sti
    e0 += ste
    e   = e0
    y.append([e0,sti])
   else:
    e += ste
    y.append([e,sti])
 nst = nstx
 ost = ostx
 nn3x = nn
 no3x = no
 if nn3 > -1:
   nn3x = min(nn3,nn)
 if no3 > -1:
   no3x = min(no3,no)
 ## -- order states and determine how many to cut from each 
 nst3 = np.array(sorted(nst)[nn3x:])
 ost3 = np.array(sorted(ost)[no3x:])
 nst = np.array(sorted(nst)[nn:])
 ost = np.array(sorted(ost)[no:])
 if len(nst) > 0:
  nst = sorted(np.transpose(nst)[1])
 if len(ost) > 0:
  ost = sorted(np.transpose(ost)[1])
 if len(nst3) > 0:
  nst3 = sorted(np.transpose(nst3)[1])
 if len(ost3) > 0:
  ost3 = sorted(np.transpose(ost3)[1])
 ## -- build new prior dictionary
 newprior = gv.BufferDict()
 for key in prior:
  skey = key.split('_')
  bkey = utf.get_basekey(skey[0])
  eokey = utf.get_evenodd(skey[0])
  k = int(skey[1])
  kp = len(prior[key])
  try:
   ## -- only works if prior is a matrix; 3-point currents for non-symmetric or off-diagonal
   l = int(skey[2])
   lp = len(prior[key][0])
   for v, x1, x2 in [('nn',nst3,nst3),('no',nst3,ost3),('on',ost3,nst3),('oo',ost3,ost3)]:
    if eokey == v:
     c1 = list(x1).count(k)
     c2 = list(x2).count(l)
     if c1 == 0 and c2 == 0:
      newprior[key] = prior[key]
     else:
      if c1 >= kp or c2 >= lp:
       continue
       #newprior[key] = np.array([])
      else:
       newprior[key] = prior[key][slice(None,kp-c1),slice(None,lp-c2)]
  except (IndexError,TypeError):
   ## -- 3-point matrix diagonals for symmetric
   for v, x1 in [('nn',nst3),('oo',ost3)]:
    if eokey == v:
     c1 = list(x1).count(k)
     if c1 == 0:
      newprior[key] = prior[key]
     else:
      kpt = int(np.round(np.sqrt(1+8*kp))-1)/2
      if c1 >= kpt or kpt == 0:
       #continue
       newprior[key] = np.array([])
      else:
       ## -- reconstruct and truncate to new size
       tmp = np.array(utf.reconstruct_upper_triangle(prior[key],kpt))
       newprior[key] = utf.truncate_upper_triangle(tmp,kpt-c1)
   ## -- everything else
   if (eokey != 'nn') and (eokey != 'oo'):
    for v, x1, x2 in [('n',list(nst),list(nst3)),('o',list(ost),list(ost3))]:
     if bkey[1][-2:] == 'g'+v:
      c1 = list(x2).count(k)
     elif eokey == v:
      c1 = list(x1).count(k)
     else:
      continue
     if c1 == 0:
      newprior[key] = prior[key]
     elif c1 >= kp:
       continue
     else:
      newprior[key] = prior[key][slice(None,kp-c1)]
 return newprior

def transform_prior(prior):
 ## -- if log/sqrt priors are present, apply log/sqrt to values
 ##    should be applied after all priors have been added
 for key in prior:
  bkey = utf.get_basekey(key)
  if bkey[0] == 'log':
   prior[key] = gv.log(prior[key])
  elif bkey[0] == 'sqrt':
   prior[key] = gv.sqrt(prior[key])
  pass
 ## -- return
 #print 'xform',prior
 return prior

def retrieve_linear_prior(prior):
 ## -- if log/sqrt priors are present, apply inverse to values
 ##    should be applied after all priors have been added
 for key in prior:
  skey = key.split('_')
  bkey = utf.get_basekey(skey[0])
  if len(skey) == 1:
   nkey = skey[0]
  else:
   nkey = bkey[1] + '_' + '_'.join(skey[1:])
  if bkey[0] == 'log':
   prior[nkey] = gv.exp(prior[key])
  elif bkey[0] == 'sqrt':
   prior[nkey] = prior[key]*prior[key]
  pass
 ## -- return
 #print 'xform',prior
 return prior
