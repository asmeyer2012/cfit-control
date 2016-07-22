import gvar       as gv
import util_funcs as utf

## -- HISQ a=0.15 l3248 physical
## -- prior mass splittings

## -- PDG inputs
# S8'
#ntst_s8p=gv.gvar(0.82,0.3)  ## -- even ground state (PDG \Delta mass)
ngrd_s8p=gv.gvar(0.94,0.3)  ## -- even ground state (PDG \Delta mass) ## -- HERE: prior was too wide
ogrd_s8p=gv.gvar(1.23,0.3)  ## -- odd ground state (PDG orbital state)
delr_s8p=gv.gvar(0.30,0.3)  ## -- radial splitting (PDG radial state)
# S8
ngrd_s8=gv.gvar(0.71,0.3)  ## -- even ground state (PDG Nucleon mass)
dels_s8=gv.gvar(0.23,0.3)  ## -- \Delta-N splitting (PDG mass splitting)
delp_s8=gv.gvar(0.38,0.3)  ## -- N-roper splitting (PDG excited state)

## -- other priors
# S8'
#delt_s8p=gv.gvar(4.6e-2,4.6e-2) ## -- taste splitting (HISQ \pi taste splittings)
delt_s8p=gv.gvar(4.6e-2,8e-2)   ## -- taste splitting (HISQ \pi taste splittings)
#delt_s8p=gv.gvar(5e-2,8e-2) ## -- taste splitting (HISQ \pi taste splittings)
delx_s8p=gv.gvar(1e0,2e0)   ## -- extra (hopefully unconstrained) states
# S8
delr_s8=gv.gvar(0.43,0.6)   ## -- radial splitting (8' fit)
#delr_s8=gv.gvar(0.30,0.30)   ## -- radial splitting (UNMOTIVATED)
#delt_s8=gv.gvar(0.12,0.9) ## -- taste splitting (8' fit, actual)
delt_s8=gv.gvar(0.062,0.062) ## -- taste splitting (8' fit, half actual)
#delt_s8=delt_s8p             ## -- taste splitting (HISQ \pi taste splittings)
delu_s8=dels_s8              ## -- splitting for states with unknown continuum limit
delx_s8=gv.gvar(1e0,2e0)     ## -- extra (hopefully unconstrained) states
#ngrd_s8=gv.gvar(0.72,0.3)    ## -- even ground state (effective mass)
ogrd_s8=gv.gvar(1.23-dels_s8.mean,dels_s8.sdev)  ## -- odd ground state (8' fit (\Delta orbital))
#ogrd_s8=gv.gvar(1.19-dels_s8.mean,dels_s8.sdev)  ## -- odd ground state (8' fit (\Delta orbital))
ovrs_s8=gv.gvar(0.88,0.18) ## -- for overriding prior for first delta state (8' fit + taste)
#ovrs_s8=gv.gvar(.94,0.3) ## -- for overriding prior for first delta state (PDG)
# S16
delr_s16=delr_s8  ## -- radial splitting (8' fit)
dels_s16=gv.gvar(0.230,0.095)   ## -- N-\Del splitting (8 fit)
delt_s16=gv.gvar(0.040,0.045)## -- taste splitting (8 fit)
delu_s16=dels_s16 ## -- splitting for states with unknown continuum limit
delx_s16=delx_s8  ## -- extra (hopefully unconstrained) states
ngrd_s16=gv.gvar(0.884,0.046) ## -- even ground state (8 fit + taste)
ogrd_s16=gv.gvar(1.138,0.055) ## -- odd ground state (8 fit + taste)
ovrs_s16=gv.gvar(1.182,0.098)-2*delt_s16 ## -- for overriding prior for first delta state (S8 fit)

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
Alog  = 1.2   # amplitude guess for actual log states
xAlog = 1e-2  # amplitude guess for possibly unconstrained log states
Anom  = 1     # amplitude guess for actual states (unknown sign)
xAnom = 1e-3  # amplitude guess for possibly unconstrained states

## -- list of keys
nkey_s8 = ('logEn' ,'logc1n','c2n','c3n','c5n','c6n','k1n','k2n','k3n','k5n','k6n')
okey_s8 = ('logEo' ,'logc1o','c2o','c3o','c5o','c6o','k1o','k2o','k3o','k5o','k6o')
nkey_s8p = ('logEn','logc4n','c7n','k4n','k7n')
okey_s8p = ('logEo','logc4o','c7o','k4o','k7o')
#nkey_s8p = ('logEn','c4n','c7n','k4n','k7n')
#okey_s8p = ('logEo','c4o','c7o','k4o','k7o')
nkey_s16 = ('logEn','logc2n','c3n','c4n','c6n','k2n','k3n','k4n','k6n')
okey_s16 = ('logEo','logc2o','c3o','c4o','c6o','k2o','k3o','k4o','k6o')

## -- HISQ a=0.15 l3248 physical
# S8
define_init_s8['logEn']=list(gv.exp([0.681,.066,.146,.412,.023,.078,.079,.117] + [1]*10))
define_init_s8['logEo']=list(gv.exp([0.917,.093,.079,.124,.055,.171,1.011,.100] + [1]*10))
define_init_s8['logc1n']=list(gv.exp([Alog]*num_nreal_s8 + [xAlog]*10))
define_init_s8['logc1o']=list(gv.exp([Alog]*num_oreal_s8 + [xAlog]*10))
for key in nkey_s8[2:]+okey_s8[2:]:
  define_init_s8[key]=[Anom]*num_nreal_s8 + [xAnom]*10

# S8'
define_init_s8p['logEn']=list(gv.exp([0.9401,.0854,.1212,.2111,.4103] + [1]*10))
#define_init_s8p['logEn']=list(gv.exp([0.8520,.2293,.0753,.1132] + [1]*10))
#define_init_s8p['logEn']=list(gv.exp([0.8520,.1426,.2754] + [1]*10))
#define_init_s8p['logEn']=list(gv.exp([0.9701,.0825,.2754] + [1]*10))
#define_init_s8p['logEn']=list(gv.exp([.955,0.045,.35,.84] + [1]*10))
define_init_s8p['logEo']=list(gv.exp([1.2124,0.1966,0.7216,.32] + [1]*10))
#define_init_s8p['logEo']=list(gv.exp([1.2205,0.0765,0.1924,.32] + [1]*10))
#define_init_s8p['logEo']=list(gv.exp([1.2138,0.1924,.32] + [1]*10))
define_init_s8p['logc4n']=list(gv.exp([Alog]*num_nreal_s8p + [xAlog]*10))
define_init_s8p['logc4o']=list(gv.exp([Alog]*num_oreal_s8p + [xAlog]*10))
#define_init_s8p['c4n']=list(gv.exp([Anom]*num_nreal_s8p + [xAnom]*10))
#define_init_s8p['c4o']=list(gv.exp([Anom]*num_oreal_s8p + [xAnom]*10))
for key in nkey_s8p[2:]+okey_s8p[2:]:
  define_init_s8p[key]=[Anom]*num_nreal_s8p + [xAnom]*10

# S16
define_init_s16['logEn']=list(gv.exp([0.852,.237,.026,.040,.186,.079,.117] + [1]*10))
define_init_s16['logEo']=list(gv.exp([1.008,.076,.054,.095,.055,.171,1.011,.100] + [1]*10))
define_init_s16['logc2n']=list(gv.exp([Alog]*num_nreal_s16 + [xAlog]*10))
define_init_s16['logc2o']=list(gv.exp([Alog]*num_oreal_s16 + [xAlog]*10))
for key in nkey_s16[2:]+okey_s16[2:]:
  define_init_s16[key]=[Anom]*num_nreal_s16 + [xAnom]*10

## -- define prior objects to pass to defines.py if requested
define_prior_s8={}
define_prior_s8p={}
define_prior_s16={}

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

lAm  = 10  # log amplitude mean
lAcs = 10  # log amplitude sdev (source)
lAks = 10  # log amplitude sdev (sink)
Am   = 0   # amplitude mean
As   = 10  # amplitude sdev (source) (temporary)
Acs  = 1e2 # amplitude sdev (source)
Aks  = 10  # amplitude sdev (sink)

## -- S8
## -- even states
## -- 0 N
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[ngrd_s8.mean,lAm] +[Am]*(len(nkey_s8)-2),
[ngrd_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 1 N[0]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
#[delr_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
#[delr_s8.sdev,lAcs]+[As]*(len(nkey_s8)-2)))
#[ovrs_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
#[ovrs_s8.sdev,lAcs]+[As]*(len(nkey_s8)-2)))
## -- 2 N[0]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 3 Del[0]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[ovrs_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[ovrs_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 4 Del[0]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 5 N(roper?)
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delr_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delr_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 6 N[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 7 N[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 8 N[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 9 \Delta[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[dels_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[dels_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 10 N[2]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 11
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 12
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 13
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))

## -- odd states
## -- 0
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[ogrd_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[ogrd_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 1
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
#[delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delr_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delr_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 2
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 3
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 4
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[dels_s8.mean-3*delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[dels_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 5
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delu_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delu_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 6
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delr_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delr_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 7
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 8
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 9
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 10
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 11
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 12
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))

## -- S8'
## -- even states S8'
## -- test state
#utf.append_prior_state(define_prior_s8p,nkey_s8p,
#gv.gvar(
#[ntst_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
#[ntst_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 0
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[ngrd_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[ngrd_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
#[ngrd_s8p.mean-ntst_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
#[ngrd_s8p.sdev,lAcs]+[As]*(len(nkey_s8p)-2)))
## -- 1
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
#[delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
#[delt_s8p.sdev,lAcs]+[As]*(len(nkey_s8p)-2)))
## -- 2
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delr_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delr_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
#[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
#[delx_s8p.sdev,lAcs]+[As]*(len(nkey_s8p)-2)))
## -- 3
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 4
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 5
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 6
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 7
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 8
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))

## -- odd states S8'
## -- 0
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[ogrd_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[ogrd_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 1
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delr_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delr_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 2
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 3
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 4
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 5
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 6
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 7
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delx_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))

## -- S16
## -- even states
## -- 0
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[ngrd_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[ngrd_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 1 -> override with delta prior from S(3/2,16)_0 fit
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[ovrs_s16.mean-ngrd_s16.mean-0*delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[ovrs_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 2
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 3
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 4
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delr_s16.mean-2*delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delr_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 5
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 6
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 7
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 8
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 9
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 10
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 11
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 12
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
## -- 13
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(nkey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))

## -- odd states
## -- 0
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[ogrd_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[ogrd_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 1
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 2
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 3
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[dels_s16.mean-2*delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[dels_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 4
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 5
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 6
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delt_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 7
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delr_s16.mean-3*delt_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delr_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 8
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 9
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 10
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 11
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
## -- 12
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm,lAm]+[Am]*(len(okey_s16)-3),
[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))

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
  #key_list_s8.append(('G'+sc+sk+'s',sc,'s'+sk))
pass
for sc in ['4','7']:
 for sk in ['4','7']:
  key_list_s8p.append(('s'+sc+sk,sc,sk))
  #key_list_s8p.append(('G'+sc+sk+'s',sc,'s'+sk))
pass
for sc in ['2','3','4','6']:
 for sk in ['2','3','4','6']:
  key_list_s16.append(('s'+sc+sk,sc,sk))
  #key_list_s16.append(('G'+sc+sk+'s',sc,'s'+sk))
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

