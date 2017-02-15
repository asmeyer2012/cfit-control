import gvar       as gv
import util_funcs as utf
import make_prior_advanced as mpa

## -- HISQ a=0.15 l3248 physical
## -- prior mass splittings

## -- PDG inputs
#nn0938=gv.gvar(0.71,0.1)
#nd1232=gv.gvar(0.94,0.1)
#nn1440=gv.gvar(1.10,0.1)    ## -- even radial state (PDG Nucleon(1440) state)
#nn1680=gv.gvar(1.28,0.03)   ## -- even radial state (PDG Nucleon(1680) state)
#nd1600=gv.gvar(1.22,0.03)   ## -- even delta state  (PDG delta(1600) state)
#nd1620=gv.gvar(1.23,0.03)   ## -- even delta state  (PDG delta(1600) state)
#nd1680=gv.gvar(1.28,0.03)   ## -- even delta state  (PDG delta(1680) state)
#on1520=gv.gvar(1.16,0.1)    ## -- odd nucleon state (PDG nucleon(1520) state)
#on1535=gv.gvar(1.17,0.1)    ## -- odd nucleon state (PDG nucleon(1535) state)
#on1650=gv.gvar(1.26,0.03)   ## -- odd nucleon state (PDG delta(1675) state)
#on1675=gv.gvar(1.28,0.03)   ## -- odd nucleon state (PDG delta(1675) state)
#on1700=gv.gvar(1.29,0.03)   ## -- odd nucleon state (PDG delta(1675) state)
#od1620=gv.gvar(1.23,0.03)   ## -- odd delta state   (PDG delta(1620) state)
#od1700=gv.gvar(1.29,0.03)   ## -- odd delta state   (PDG delta(1700) state)
#onpi100 =gv.gvar(0.97,0.1)  ## -- odd ground state (N+pi, 1 momentum unit)
#onpi100t=gv.gvar(1.03,0.03) ## -- odd ground state (N+pi, 1 momentum unit+taste)
#onpi110 =gv.gvar(1.07,0.03) ## -- odd ground state (N+pi, 2 momentum unit)

nn0938=gv.gvar(0.71,0.1)
nd1232=gv.gvar(0.94,0.1)
nn1440=gv.gvar(1.10,0.1)    ## -- even radial state (PDG Nucleon(1440) state)
nn1680=gv.gvar(1.28,0.1)   ## -- even radial state (PDG Nucleon(1680) state)
nd1600=gv.gvar(1.22,0.1)   ## -- even delta state  (PDG delta(1600) state)
nd1620=gv.gvar(1.23,0.1)   ## -- even delta state  (PDG delta(1600) state)
nd1680=gv.gvar(1.28,0.1)   ## -- even delta state  (PDG delta(1680) state)
on1520=gv.gvar(1.16,0.1)    ## -- odd nucleon state (PDG nucleon(1520) state)
#on1535=gv.gvar(1.17,0.1)    ## -- odd nucleon state (PDG nucleon(1535) state)
## --  corrected to prevent super small splitting
on1535=gv.gvar(1.20,0.1)    ## -- odd nucleon state (PDG nucleon(1535) state)
on1650=gv.gvar(1.26,0.1)   ## -- odd nucleon state (PDG delta(1675) state)
on1675=gv.gvar(1.28,0.1)   ## -- odd nucleon state (PDG delta(1675) state)
on1700=gv.gvar(1.29,0.1)   ## -- odd nucleon state (PDG delta(1675) state)
od1620=gv.gvar(1.23,0.1)   ## -- odd delta state   (PDG delta(1620) state)
od1700=gv.gvar(1.29,0.1)   ## -- odd delta state   (PDG delta(1700) state)
onpi100 =gv.gvar(0.97,0.1)  ## -- odd ground state (N+pi, 1 momentum unit)
onpi100t=gv.gvar(1.03,0.1) ## -- odd ground state (N+pi, 1 momentum unit+taste)
onpi110 =gv.gvar(1.07,0.1) ## -- odd ground state (N+pi, 2 momentum unit)

xnpi=10. ## -- N pi state suppression factor (EFT gives 1/30.)
## -- from fitting
## -- S8'
## -- S8
#ngrd_s8=gv.gvar(0.71,0.1)  ## -- even ground state  (PDG Nucleon mass)
#ogrd_s8=gv.gvar(0.97,0.1)  ## -- odd ground state   (N+pi, 1 momentum unit)
#dels_s8=gv.gvar(0.23,0.1)  ## -- \Delta-N splitting (PDG mass splitting)
#delp_s8=gv.gvar(0.38,0.1)  ## -- N-roper splitting  (PDG excited state)
## -- S16

## -- other priors
## -- S8'
delt_s8p=gv.gvar(4.6e-2,8e-2)   ## -- taste splitting (HISQ \pi taste splittings)
delx_s8p=gv.gvar(5e-1,5e-1)       ## -- extra (hopefully unconstrained) states
## -- S8
#delr_s8=gv.gvar(0.278,0.1)    ## -- radial splitting (8' fit, actualx1s)
ovrn_s8=gv.gvar(1.005,0.020) ## -- (0.006 actual error)
ovro_s8=gv.gvar(1.169,0.100) ## -- (0.038 actual error)
delt_s8=gv.gvar(0.028,0.025) ## -- (0.0075 actual error)
#ovrs_s8=gv.gvar(0.927,0.060) ## -- for overriding prior for first delta state (8' \Delta[0]x2s)
#odel_s8=gv.gvar(1.166,0.086)  ## -- odd delta state (8' fit (\Delta orbital, actualx1s))
#delu_s8=delr_s8              ## -- splitting for states with unknown continuum limit
delx_s8=delx_s8p             ## -- extra (hopefully unconstrained) states
## -- S16
#delu_s16=dels_s8  ## -- splitting for states with unknown continuum limit
delx_s16=delx_s8  ## -- extra (hopefully unconstrained) states
delt_s16=gv.gvar(0.042,0.076) ## -- taste splitting (8 fit x1s)
ngrd_s16=gv.gvar(0.7493,0.1)  ## -- even ground state (8 fit, large error )
ogrd_s16=gv.gvar(0.942,0.1)   ## -- odd ground state (8 fit N'0, large error)
ovrs_s16=gv.gvar(0.944,0.030) ## -- overriding prior for first delta state (S8 fit, actual x1s)

## -- used if do_init is defined in defines.py
define_init_s8={}
define_init_s8p={}
define_init_s16={}
#num_nreal_s8=5 #3N+2D +1radial
#num_oreal_s8=5 #4N+1D+1?
#num_nreal_s8p=2 #0N+2D +1radial
#num_oreal_s8p=1 #0N+1D+0?
#num_nreal_s16=4 #1N+3D
#num_oreal_s16=5 #3N+4D+1?
#Alog  = 1.2   # amplitude guess for actual log states
#xAlog = 1e-2  # amplitude guess for possibly unconstrained log states
#Anom  = 1     # amplitude guess for actual states (unknown sign)
#xAnom = 1e-3  # amplitude guess for possibly unconstrained states

## -- list of keys
nkey_s8  = ('log(En)','log(c1n)','c2n','c3n','c5n','c6n','k1n','k2n','k3n','k5n','k6n')
okey_s8  = ('log(Eo)','log(c1o)','c2o','c3o','c5o','c6o','k1o','k2o','k3o','k5o','k6o')
nkey_s8p = ('log(En)','log(c4n)','c7n','k4n','k7n')
okey_s8p = ('log(Eo)','log(c4o)','c7o','k4o','k7o')
nkey_s16 = ('log(En)','log(c2n)','c3n','c4n','c6n','k2n','k3n','k4n','k6n')
okey_s16 = ('log(Eo)','log(c2o)','c3o','c4o','c6o','k2o','k3o','k4o','k6o')

def curkey(key):
  return (key+'nn',key+'no',key+'on',key+'oo')
current_list = ['axax','ayay','azaz']
current_key  = ['aiai','aiai','aiai']
tsep_list = [6,7]

vkey_s8 = tuple()
for cur in current_key:
 if not(cur in vkey_s8):
  vkey_s8 += curkey(cur)
  nkey_s8  = nkey_s8 + (cur+'gn',)
  okey_s8  = okey_s8 + (cur+'go',)
  nkey_s8p = nkey_s8p + (cur+'gn',)
  okey_s8p = okey_s8p + (cur+'go',)
  nkey_s16 = nkey_s16 + (cur+'gn',)
  okey_s16 = okey_s16 + (cur+'go',)
vkey_s8p = vkey_s8
vkey_s16 = vkey_s8

### -- add blocks of states
### -- S8
explicit_priors_s8 = {}
for key in ['log(c1n)','log(c1o)']:
 explicit_priors_s8[key] = gv.gvar([1e1]*10,[1e2]*10)
for key in ['c2n','c2o','c3n','c3o','c5n','c5o','c6n','c6o']:
 explicit_priors_s8[key] = gv.gvar([0]*10,[1e2]*10)
define_prior_s8 = mpa.add_first_blocks(nkey_s8,okey_s8,vkey_s8,3,1, nn0938,ovro_s8,delt_s8,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
#define_prior_s8 = mpa.add_first_blocks(nkey_s8,okey_s8,vkey_s8,3,1, nn0938,on1520,delt_s8,delt_s8,
# symmetric_V=True, explicit_priors=explicit_priors_s8)
## even states
mpa.add_next_block(define_prior_s8,True,2, ovrn_s8,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
#mpa.add_next_block(define_prior_s8,True,2, nd1232,delt_s8,
# symmetric_V=True, explicit_priors=explicit_priors_s8)
mpa.add_next_block(define_prior_s8,True,3, nn1440,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
mpa.add_next_block(define_prior_s8,True,2, nd1600,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
mpa.add_next_block(define_prior_s8,True,1, nn1680,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
## odd states
mpa.add_next_block(define_prior_s8,False,3, on1535,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
mpa.add_next_block(define_prior_s8,False,1, od1620,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
mpa.add_next_block(define_prior_s8,False,1, on1675,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
mpa.add_next_block(define_prior_s8,False,2, od1700,delt_s8,
 symmetric_V=True, explicit_priors=explicit_priors_s8)
### N+pi scattering states
#mpa.add_next_block(define_prior_s8,False,1, onpi100,delt_s8,
# symmetric_V=True, explicit_priors=explicit_priors_s8)
#mpa.add_next_block(define_prior_s8,False,1, onpi100t,delt_s8,
# symmetric_V=True, explicit_priors=explicit_priors_s8)
#mpa.add_next_block(define_prior_s8,False,1, onpi110,delt_s8,
# symmetric_V=True, explicit_priors=explicit_priors_s8)

## -- S8'
## -- actual
explicit_priors_s8p = {}
explicit_priors_s8p['log(c4n)'] = gv.gvar([1e1]*5,[1e2]*5)
explicit_priors_s8p['log(c4o)'] = gv.gvar([1e1]*5,[1e2]*5)
explicit_priors_s8p['c7n'] = gv.gvar([0]*5,[1e2]*5)
explicit_priors_s8p['c7o'] = gv.gvar([0]*5,[1e2]*5)
define_prior_s8p=\
 mpa.add_first_blocks(nkey_s8p,okey_s8p,vkey_s8p,2,1, nd1232,on1520,delt_s8p,delt_s8p,
 symmetric_V=True, explicit_priors=explicit_priors_s8p)
## even states
mpa.add_next_block(define_prior_s8p,True,2, nd1600,delt_s8p,
 symmetric_V=True, explicit_priors=explicit_priors_s8p)
#mpa.add_next_block(define_prior_s8p,True,4, nd1680,delt_s8p,
# symmetric_V=True, explicit_priors=explicit_priors_s8p)
mpa.add_next_block(define_prior_s8p,True,4, gv.gvar(1.8,0.6),delt_s8p,
 symmetric_V=True, explicit_priors=explicit_priors_s8p)
## odd states
#mpa.add_next_block(define_prior_s8p,False,4, on1675,delt_s8p,
mpa.add_next_block(define_prior_s8p,False,4, on1675,delt_s8p,
 symmetric_V=True, explicit_priors=explicit_priors_s8p)
#mpa.add_next_block(define_prior_s8p,False,2, on1700,delt_s8p,
# symmetric_V=True, explicit_priors=explicit_priors_s8p)
mpa.add_next_block(define_prior_s8p,False,4, gv.gvar(1.8,0.6),delt_s8p,
 symmetric_V=True, explicit_priors=explicit_priors_s8p)

### -- S16
define_prior_s16={}
explicit_priors_s16 = {}
define_prior_s16=\
 mpa.add_first_blocks(nkey_s16,okey_s16,vkey_s16,1,4, nn0938,on1520,delt_s16,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
## even states
mpa.add_next_block(define_prior_s16,True,3, nd1232,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
mpa.add_next_block(define_prior_s16,True,1, nn1440,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
mpa.add_next_block(define_prior_s16,True,3, nd1600,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
mpa.add_next_block(define_prior_s16,True,5, nn1680,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
## odd states
mpa.add_next_block(define_prior_s16,False,1, on1535,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
mpa.add_next_block(define_prior_s16,False,2, od1620,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
mpa.add_next_block(define_prior_s16,False,1, on1650,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
mpa.add_next_block(define_prior_s16,False,5, on1675,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)
mpa.add_next_block(define_prior_s16,False,4, od1700,delt_s16,
 symmetric_V=True, explicit_priors=explicit_priors_s16)

## -- do log/sqrt conversions
mpa.transform_prior(define_prior_s8)
mpa.transform_prior(define_prior_s8p)
mpa.transform_prior(define_prior_s16)

## -- pass along keys too
#define_prior_s8['nkey'] = nkey_s8
#define_prior_s8['okey'] = okey_s8
#define_prior_s8['vkey'] = vkey_s8
#define_prior_s8p['nkey'] = nkey_s8p
#define_prior_s8p['okey'] = okey_s8p
#define_prior_s8p['vkey'] = vkey_s8p
#define_prior_s16['nkey'] = nkey_s16
#define_prior_s16['okey'] = okey_s16
#define_prior_s16['vkey'] = vkey_s16

## -- construct models quickly using loops
key_list_s8 = list()
key_list_s8p = list()
key_list_s16 = list()
log_s8='1'
log_s8p='4'
log_s16='2'
for sc in ['1','2','3','5','6']:
 for sk in ['1','2','3','5','6']:
  key_list_s8.append(('s'+sc+sk,sc,sk))
pass
for sc in ['4','7']:
 for sk in ['4','7']:
  key_list_s8p.append(('s'+sc+sk,sc,sk))
pass
for sc in ['2','3','4','6']:
 for sk in ['2','3','4','6']:
  key_list_s16.append(('s'+sc+sk,sc,sk))
pass

#for key in key_list_s8:
#  if key[1] == log_s8:
#    logstr1='log'
#  else:
#    logstr1=''
#  try:
#    define_prior_s8[key[0]]=\
#     {logstr1+'c'+key[1]+'n':define_prior_s8[logstr1+'c'+key[1]+'n'],
#      logstr1+'c'+key[1]+'o':define_prior_s8[logstr1+'c'+key[1]+'o'],
#      'k'+key[2]+'n':define_prior_s8['k'+key[2]+'n'],
#      'k'+key[2]+'o':define_prior_s8['k'+key[2]+'o'],
#      'logEn':define_prior_s8['logEn'],
#      'logEo':define_prior_s8['logEo'] }
#  except KeyError:
#    continue ## -- key is not defined, don't worry about it
#pass
#for key in key_list_s8p:
#  if key[1] == log_s8p:
#    logstr1='log'
#  else:
#    logstr1=''
#  try:
#    define_prior_s8p[key[0]]=\
#     {logstr1+'c'+key[1]+'n':define_prior_s8p[logstr1+'c'+key[1]+'n'],
#      logstr1+'c'+key[1]+'o':define_prior_s8p[logstr1+'c'+key[1]+'o'],
#      'k'+key[2]+'n':define_prior_s8p['k'+key[2]+'n'],
#      'k'+key[2]+'o':define_prior_s8p['k'+key[2]+'o'],
#      'logEn':define_prior_s8p['logEn'],
#      'logEo':define_prior_s8p['logEo'] }
#  except KeyError:
#    continue ## -- key is not defined, don't worry about it
#pass
#for key in key_list_s16:
#  if key[1] == log_s16:
#    logstr1='log'
#  else:
#    logstr1=''
#  try:
#    define_prior_s16[key[0]]=\
#     {logstr1+'c'+key[1]+'n':define_prior_s16[logstr1+'c'+key[1]+'n'],
#      logstr1+'c'+key[1]+'o':define_prior_s16[logstr1+'c'+key[1]+'o'],
#      'k'+key[2]+'n':define_prior_s16['k'+key[2]+'n'],
#      'k'+key[2]+'o':define_prior_s16['k'+key[2]+'o'],
#      'logEn':define_prior_s16['logEn'],
#      'logEo':define_prior_s16['logEo'] }
#  except KeyError:
#    continue ## -- key is not defined, don't worry about it
#pass

### -- construct models quickly using loops
#key_list3_s8 = list()
#key_list3_s8p = list()
#key_list3_s16 = list()
#log_s8='1'
#log_s8p='4'
#log_s16='2'
#for cur,ckey in zip(current_list,current_key):
# for tsep in tsep_list:
#  for sc in ['1','2','3','5','6']:
#   for sk in ['1','2','3','5','6']:
#    #key_list3_s8.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
#    key_list3_s8.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
#  pass
#  for sc in ['4','7']:
#   for sk in ['4','7']:
#    #key_list3_s8p.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
#    key_list3_s8p.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
#  pass
#  for sc in ['2','3','4','6']:
#   for sk in ['2','3','4','6']:
#    #key_list3_s16.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
#    key_list3_s16.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
#  pass

#for key in key_list3_s8:
#  if key[1] == log_s8:
#    logstr1='log'
#  else:
#    logstr1=''
#  try:
#    define_prior3_s8[key[0]]=\
#     {logstr1+'c'+key[1]+'n':define_prior3_s8[logstr1+'c'+key[1]+'n'],
#      logstr1+'c'+key[1]+'o':define_prior3_s8[logstr1+'c'+key[1]+'o'],
#      'k'+key[2]+'n':define_prior3_s8['k'+key[2]+'n'],
#      'k'+key[2]+'o':define_prior3_s8['k'+key[2]+'o'],
#      'logEn':define_prior3_s8['logEn'],
#      'logEo':define_prior3_s8['logEo'] }
#    for cur in current_list:
#     for tsep in tsep_list:
#      define_prior3_s8[key[0]][key[5]+'nn']=define_prior3_s8[key[5]+'nn']
#      define_prior3_s8[key[0]][key[5]+'no']=define_prior3_s8[key[5]+'no']
#      define_prior3_s8[key[0]][key[5]+'on']=define_prior3_s8[key[5]+'on']
#      define_prior3_s8[key[0]][key[5]+'oo']=define_prior3_s8[key[5]+'oo']
#  except KeyError:
#    continue ## -- key is not defined, don't worry about it
#pass
#for key in key_list3_s8p:
#  if key[1] == log_s8p:
#    logstr1='log'
#  else:
#    logstr1=''
#  try:
#    define_prior3_s8p[key[0]]=\
#     {logstr1+'c'+key[1]+'n':define_prior3_s8p[logstr1+'c'+key[1]+'n'],
#      logstr1+'c'+key[1]+'o':define_prior3_s8p[logstr1+'c'+key[1]+'o'],
#      'k'+key[2]+'n':define_prior3_s8p['k'+key[2]+'n'],
#      'k'+key[2]+'o':define_prior3_s8p['k'+key[2]+'o'],
#      'logEn':define_prior3_s8p['logEn'],
#      'logEo':define_prior3_s8p['logEo'] }
#    define_prior3_s8p[key[0]][key[5]+'nn']=define_prior3_s8p[key[5]+'nn']
#    define_prior3_s8p[key[0]][key[5]+'no']=define_prior3_s8p[key[5]+'no']
#    define_prior3_s8p[key[0]][key[5]+'on']=define_prior3_s8p[key[5]+'on']
#    define_prior3_s8p[key[0]][key[5]+'oo']=define_prior3_s8p[key[5]+'oo']
#  except KeyError:
#    continue ## -- key is not defined, don't worry about it
#pass
#for key in key_list3_s16:
#  if key[1] == log_s16:
#    logstr1='log'
#  else:
#    logstr1=''
#  try:
#    define_prior3_s16[key[0]]=\
#     {logstr1+'c'+key[1]+'n':define_prior3_s16[logstr1+'c'+key[1]+'n'],
#      logstr1+'c'+key[1]+'o':define_prior3_s16[logstr1+'c'+key[1]+'o'],
#      'k'+key[2]+'n':define_prior3_s16['k'+key[2]+'n'],
#      'k'+key[2]+'o':define_prior3_s16['k'+key[2]+'o'],
#      'logEn':define_prior3_s16['logEn'],
#      'logEo':define_prior3_s16['logEo'] }
#    for cur in current_list:
#     for tsep in tsep_list:
#      define_prior3_s16[key[0]][key[5]+'nn']=define_prior3_s16[key[5]+'nn']
#      define_prior3_s16[key[0]][key[5]+'no']=define_prior3_s16[key[5]+'no']
#      define_prior3_s16[key[0]][key[5]+'on']=define_prior3_s16[key[5]+'on']
#      define_prior3_s16[key[0]][key[5]+'oo']=define_prior3_s16[key[5]+'oo']
#  except KeyError:
#    continue ## -- key is not defined, don't worry about it
#pass

## -- end

