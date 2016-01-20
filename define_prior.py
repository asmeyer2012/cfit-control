import gvar       as gv
import util_funcs as utf

## -- prior mass splittings
## -- S8
ngrd_s8=gv.gvar(1.08,0.04) ## -- even ground state (effective mass)
ogrd_s8=gv.gvar(1.58-0.23,0.20) ## -- odd ground state (8' fit (\Delta orbital))
#ogrd_s8=gv.gvar(ngrd_s8.mean+0.26,0.25) ## -- odd ground state (8' fit (\Delta orbital))
ovrs_s8=gv.gvar(1.32,0.02) ## -- for overriding prior for first delta state (8' fit)
delp_s8=gv.gvar(0.38,0.30) ## -- N-roper splitting (PDG)
delr_s8=gv.gvar(0.26,0.25) ## -- radial splitting (8' fit)
dels_s8=gv.gvar(0.23,0.20) ## -- \Delta-N splitting (PDG)
delt_s8=gv.gvar(0.02,0.04) ## -- taste splitting (8' fit)
delu_s8=dels_s8            ## -- splitting for states with unknown continuum limit
delx_s8=gv.gvar(1e0,5e-1)   ## -- extra (hopefully unconstrained) states

## -- S8'
ngrd_s8p=gv.gvar(1.39,0.1) ## -- even ground state
ogrd_s8p=gv.gvar(ngrd_s8p.mean+0.3,0.2) ## -- odd ground state (grd + radial)
delr_s8p=gv.gvar(0.30,0.30) ## -- radial splitting
#dels_s8p=gv.gvar() ## -- \Delta-N splitting
delt_s8p=gv.gvar(4e-2,8e-2) ## -- taste splitting (HISQ \pi taste splittings)
delx_s8p=delx_s8            ## -- extra (hopefully unconstrained) states

## -- S16
ngrd_s16=gv.gvar(1.112,0.05) ## -- even ground state (effective mass)
ogrd_s16=gv.gvar(1.444,0.03) ## -- odd ground state (8 fit)
ovrs_s16=ogrd_s8  ## -- for overriding prior for first delta state (S8' fit)
delr_s16=delr_s8  ## -- radial splitting (8' fit)
dels_s16=gv.gvar(0.16,0.02)   ## -- N-\Del splitting (8 fit)
delt_s16=delt_s8  ## -- taste splitting (8' fit)
delu_s16=dels_s16 ## -- splitting for states with unknown continuum limit
delx_s16=delx_s8  ## -- extra (hopefully unconstrained) states

## -- used if do_init is defined in defines.py
define_init_s8={}
define_init_s8p={}
define_init_s16={}
num_nreal_s8=5 #3N+2D +1radial
num_oreal_s8=3 #4N+1D+1?
num_nreal_s8p=2 #0N+2D +1radial
num_oreal_s8p=1 #0N+1D+0?
num_nreal_s16=4 #1N+3D
num_oreal_s16=5 #3N+4D+1?
Alog  = 2     # amplitude guess for actual log states
xAlog = 1e-2  # amplitude guess for possibly unconstrained log states
Anom  = 1     # amplitude guess for actual states (unknown sign)
xAnom = 1e-3  # amplitude guess for possibly unconstrained states

## -- S8
define_init_s8['logEn']=list(gv.exp([1.084,.035,.029,.201,.025,.364,.027,.028] + [1]*10))
define_init_s8['logEo']=list(gv.exp([1.427,.045,.041,.026,.147,.172,.260,.367] + [1]*10))
define_init_s8['logc1n']=list(gv.exp([Alog]*num_nreal_s8 + [xAlog]*10))
define_init_s8['logc1o']=list(gv.exp([Alog]*num_oreal_s8 + [xAlog]*10))
#define_init_s8['logk1n']=list(gv.exp([Alog]*num_nreal_s8 + [xAlog]*10))
#define_init_s8['logk1o']=list(gv.exp([Alog]*num_oreal_s8 + [xAlog]*10))
define_init_s8['c2n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['c3n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['c5n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['c6n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['c2o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['c3o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['c5o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['c6o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['k1n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['k2n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['k3n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['k5n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['k6n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['k1o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['k2o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['k3o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['k5o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['k6o']=[Anom]*num_oreal_s8 + [xAnom]*10
#
define_init_s8['ks1n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['ks2n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['ks3n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['ks5n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['ks6n']=[Anom]*num_nreal_s8 + [xAnom]*10
define_init_s8['ks1o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['ks2o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['ks3o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['ks5o']=[Anom]*num_oreal_s8 + [xAnom]*10
define_init_s8['ks6o']=[Anom]*num_oreal_s8 + [xAnom]*10

## -- S8'
#define_init_s8p['logEn']=list(gv.exp([1.28,.025,.29] + [1]*10))
#define_init_s8p['logEo']=list(gv.exp([1.54,.03] + [1]*10))
define_init_s8p['logEn']=list(gv.exp([1.326,.018,.176,.422] + [1]*10))
define_init_s8p['logEo']=list(gv.exp([1.433,.072,.348,.672] + [1]*10))
define_init_s8p['logc4n']=list(gv.exp([Alog]*num_nreal_s8p + [xAlog]*10))
define_init_s8p['logc4o']=list(gv.exp([Alog]*num_oreal_s8p + [xAlog]*10))
define_init_s8p['c7n']=[Anom]*num_nreal_s8p + [xAnom]*10
define_init_s8p['c7o']=[Anom]*num_oreal_s8p + [xAnom]*10
define_init_s8p['k4n']=[Anom]*num_nreal_s8p + [xAnom]*10
define_init_s8p['k4o']=[Anom]*num_oreal_s8p + [xAnom]*10
define_init_s8p['k7n']=[Anom]*num_nreal_s8p + [xAnom]*10
define_init_s8p['k7o']=[Anom]*num_oreal_s8p + [xAnom]*10
define_init_s8p['ks4n']=[Anom]*num_nreal_s8p + [xAnom]*10
define_init_s8p['ks4o']=[Anom]*num_oreal_s8p + [xAnom]*10
define_init_s8p['ks7n']=[Anom]*num_nreal_s8p + [xAnom]*10
define_init_s8p['ks7o']=[Anom]*num_oreal_s8p + [xAnom]*10

## -- S16
define_init_s16['logEn']=list(gv.exp([1.111,.23,.018,.02] + [1]*10))
define_init_s16['logEo']=list(gv.exp([1.478,.06,.01,.1,1.805] + [1]*10))
define_init_s16['logc2n']=list(gv.exp([Alog]*num_nreal_s16 + [xAlog]*10))
define_init_s16['logc2o']=list(gv.exp([Alog]*num_oreal_s16 + [xAlog]*10))
define_init_s16['c3n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['c4n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['c6n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['c3o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['c4o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['c6o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['k2n']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['k3n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['k4n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['k6n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['k2o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['k3o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['k4o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['k6o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['ks2n']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['ks3n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['ks4n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['ks6n']=[Anom]*num_nreal_s16 + [xAnom]*10
define_init_s16['ks2o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['ks3o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['ks4o']=[Anom]*num_oreal_s16 + [xAnom]*10
define_init_s16['ks6o']=[Anom]*num_oreal_s16 + [xAnom]*10

## -- define prior objects to pass to defines.py if requested
define_prior_s8={}
define_prior_s8p={}
define_prior_s16={}

nkey_s8 = ('logEn' ,'logc1n','c2n','c3n','c5n','c6n','k1n','k2n','k3n','k5n','k6n',
 'ks1n','ks2n','ks3n','ks5n','ks6n')
okey_s8 = ('logEo' ,'logc1o','c2o','c3o','c5o','c6o','k1o','k2o','k3o','k5o','k6o',
 'ks1o','ks2o','ks3o','ks5o','ks6o')
nkey_s8p = ('logEn','logc4n','c7n','k4n','k7n','ks4n','ks7n')
okey_s8p = ('logEo','logc4o','c7o','k4o','k7o','ks4o','ks7o')
nkey_s16 = ('logEn','logc2n','c3n','c4n','c6n','k2n','k3n','k4n','k6n','ks2n','ks3n','ks4n','ks6n')
okey_s16 = ('logEo','logc2o','c3o','c4o','c6o','k2o','k3o','k4o','k6o','ks2o','ks3o','ks4o','ks6o')
#nkey_s16 = ('logEn','logc2n','logk2n','c3n','c4n','c6n','k3n','k4n','k6n')
#okey_s16 = ('logEo','logc2o','logk2o','c3o','c4o','c6o','k3o','k4o','k6o')

## -- S8
define_prior_s8['nkey'] = nkey_s8
define_prior_s8['okey'] = okey_s8
define_prior_s8p['nkey'] = nkey_s8p
define_prior_s8p['okey'] = okey_s8p
define_prior_s16['nkey'] = nkey_s16
define_prior_s16['okey'] = okey_s16
for key in nkey_s8 + okey_s8:
  define_prior_s8[key]=[]
for key in nkey_s8p + okey_s8p:
  define_prior_s8p[key]=[]
for key in nkey_s16 + okey_s16:
  define_prior_s16[key]=[]

lAm = 1  # log amplitude mean
lAs = 10 # log amplitude sdev
Am  = 0  # amplitude mean
As  = 10 # amplitude sdev

## -- S8
## -- even states
## -- 0 N
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[ngrd_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[ngrd_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
#[ngrd_s8.mean,lAm,lAm]+[Am]*(len(nkey_s8)-2),
#[ngrd_s8.sdev,lAs,lAs]+[As]*(len(nkey_s8)-2)))
## -- 1 N
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 2 N
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 3 \Delta -> override with delta prior from S(3/2,16)_0 fit
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[ovrs_s8.mean-ngrd_s8.mean-2*delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[ovrs_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 4 \Delta
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 5 N(roper)
#print "value ngrd: ",ngrd_s8.mean
#print "value ovrs: ",ovrs_s8.mean
#print "value delr: ",delr_s8.mean
#print "value delt: ",delt_s8.mean
#print "prior set to: ",delr_s8.mean+ngrd_s8.mean-ovrs_s8.mean-3*delt_s8.mean
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
#[delr_s8.mean+ngrd_s8.mean-ovrs_s8.mean-3*delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delr_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delr_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
#[delr_s8.mean-1*delt_s8.mean,lAm,lAm]+[Am]*(len(nkey_s8)-2), ##old, doesn't make sense
#[delr_s8.sdev,lAs,lAs]+[As]*(len(nkey_s8)-2)))
## -- 6 N[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
#[delr_s8.mean,lAm,lAm]+[Am]*(len(nkey_s8)-2), ##old, wrong splitting
#[delr_s8.sdev,lAs,lAs]+[As]*(len(nkey_s8)-2)))
## -- 7 N[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 8 N[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 9 \Delta[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[dels_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[dels_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 10 N[2]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 11
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 12
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))
## -- 13
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(nkey_s8)-2)))

## -- odd states
## -- 0
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[ogrd_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[ogrd_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 1
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 2
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 3
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 4
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[dels_s8.mean-3*delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[dels_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 5
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delu_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delu_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 6
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delr_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delr_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 7
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delt_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 8
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 9
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 10
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 11
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))
## -- 12
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAs]+[As]*(len(okey_s8)-2)))

## -- S8'
## -- even states S8'
## -- 0
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[ngrd_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[ngrd_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))
## -- 1
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delt_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))
## -- 2
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delr_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delr_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))
## -- 3
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))
## -- 4
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))
## -- 5
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))
## -- 6
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))
## -- 7
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))
## -- 8
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(nkey_s8p)-2)))

## -- odd states S8'
## -- 0
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[ogrd_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[ogrd_s8p.sdev,lAs]+[As]*(len(okey_s8p)-2)))
## -- 1
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delr_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delr_s8p.sdev,lAs]+[As]*(len(okey_s8p)-2)))
## -- 2
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(okey_s8p)-2)))
## -- 3
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(okey_s8p)-2)))
## -- 4
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(okey_s8p)-2)))
## -- 5
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(okey_s8p)-2)))
## -- 6
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(okey_s8p)-2)))
## -- 7
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAs]+[As]*(len(okey_s8p)-2)))

## -- S16
## -- even states
## -- 0
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[ngrd_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[ngrd_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 1 -> override with delta prior from S(3/2,16)_0 fit
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[ovrs_s16.mean-ngrd_s16.mean-0*delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[ovrs_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 2
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 3
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 4
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delr_s16.mean-2*delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delr_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 5
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 6
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 7
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 8
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 9
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 10
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 11
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 12
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))
## -- 13
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(nkey_s16)-3)))

## -- odd states
## -- 0
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[ogrd_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[ogrd_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 1
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 2
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 3
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[dels_s16.mean-2*delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[dels_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 4
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 5
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 6
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 7
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delr_s16.mean-3*delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delr_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 8
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 9
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 10
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 11
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))
## -- 12
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAs,lAs]+[As]*(len(okey_s16)-3)))

## -- construct models quickly using loops
key_list_s8 = list()
key_list_s8p = list()
key_list_s16 = list()
log_s8='1'
log_s8p='4'
log_s16='2'
for sc in ['1','2','3','5','6']:
 for sk in ['1','2','3','5','6']:
  key_list_s8.append(('G'+sc+sk,sc,sk))
  key_list_s8.append(('G'+sc+sk+'s',sc,'s'+sk))
pass
for sc in ['4','7']:
 for sk in ['4','7']:
  key_list_s8p.append(('G'+sc+sk,sc,sk))
  key_list_s8p.append(('G'+sc+sk+'s',sc,'s'+sk))
pass
for sc in ['2','3','4','6']:
 for sk in ['2','3','4','6']:
  key_list_s16.append(('G'+sc+sk,sc,sk))
  key_list_s16.append(('G'+sc+sk+'s',sc,'s'+sk))
pass

for key in key_list_s8:
  if key[1] == log_s8:
    logstr1='log'
  else:
    logstr1=''
  try:
    define_prior_s8[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior_s8[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior_s8[logstr1+'c'+key[1]+'o'],
      'k'+key[2]+'n':define_prior_s8['k'+key[2]+'n'],
      'k'+key[2]+'o':define_prior_s8['k'+key[2]+'o'],
      'logEn':define_prior_s8['logEn'],
      'logEo':define_prior_s8['logEo'] }
  except KeyError:
    continue ## -- key is not defined, don't worry about it
pass
for key in key_list_s8p:
  if key[1] == log_s8p:
    logstr1='log'
  else:
    logstr1=''
  try:
    define_prior_s8p[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior_s8p[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior_s8p[logstr1+'c'+key[1]+'o'],
      'k'+key[2]+'n':define_prior_s8p['k'+key[2]+'n'],
      'k'+key[2]+'o':define_prior_s8p['k'+key[2]+'o'],
      'logEn':define_prior_s8p['logEn'],
      'logEo':define_prior_s8p['logEo'] }
  except KeyError:
    continue ## -- key is not defined, don't worry about it
pass
for key in key_list_s16:
  if key[1] == log_s16:
    logstr1='log'
  else:
    logstr1=''
  try:
    define_prior_s16[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior_s16[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior_s16[logstr1+'c'+key[1]+'o'],
      'k'+key[2]+'n':define_prior_s16['k'+key[2]+'n'],
      'k'+key[2]+'o':define_prior_s16['k'+key[2]+'o'],
      'logEn':define_prior_s16['logEn'],
      'logEo':define_prior_s16['logEo'] }
  except KeyError:
    continue ## -- key is not defined, don't worry about it
pass

## -- end

