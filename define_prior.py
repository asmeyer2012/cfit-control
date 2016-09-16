import gvar       as gv
import util_funcs as utf

## -- HISQ a=0.15 l3248 physical
## -- prior mass splittings

## -- PDG inputs
## -- S8'
ngrd_s8p=gv.gvar(0.94,0.1)  ## -- even ground state (PDG \Delta mass)
ogrd_s8p=gv.gvar(1.23,0.1)  ## -- odd ground state (PDG orbital state)
delr_s8p=gv.gvar(0.30,0.1)  ## -- radial splitting (PDG radial state)
## -- S8
ngrd_s8=gv.gvar(0.71,0.1)  ## -- even ground state (PDG Nucleon mass)
dels_s8=gv.gvar(0.23,0.1)  ## -- \Delta-N splitting (PDG mass splitting)
delp_s8=gv.gvar(0.38,0.1)  ## -- N-roper splitting (PDG excited state)

## -- other priors
## -- S8'
delt_s8p=gv.gvar(4.6e-2,8e-2)   ## -- taste splitting (HISQ \pi taste splittings)
delx_s8p=gv.gvar(5e-1,5e-1)       ## -- extra (hopefully unconstrained) states
## -- S8
## v5.2.0 (3+4,g2+3 fit)
delr_s8=gv.gvar(0.33,0.1)    ## -- radial splitting (8' fit)
delt_s8=gv.gvar(0.039,0.044) ## -- taste splitting (8' fit, actualx2s)
ovrs_s8=gv.gvar(0.984,0.042) ## -- for overriding prior for first delta state (8' \Delta[0]x2s)
#ovrs_s8=gv.gvar(1.023,0.042) ## -- for overriding prior for first delta state (8' \Delta[1]x2s)
odel_s8=gv.gvar(1.134,dels_s8.sdev)  ## -- odd delta state (8' fit (\Delta orbital))
ogrd_s8=gv.gvar(1.134-dels_s8.mean,dels_s8.sdev)  ## -- odd ground state (8' fit (\Delta orbital))
delu_s8=delr_s8              ## -- splitting for states with unknown continuum limit
delx_s8=delx_s8p             ## -- extra (hopefully unconstrained) states

### -- S8
### v5 (3+3,g2+2 fit)
#delr_s8=gv.gvar(0.30,0.1)    ## -- radial splitting (8' fit)
#delt_s8=gv.gvar(0.045,0.060) ## -- taste splitting (8' fit, actualx2s)
#ovrs_s8=gv.gvar(0.953,0.060) ## -- for overriding prior for first delta state (8' \Delta[0]x2s)
##ovrs_s8=gv.gvar(0.998,0.090) ## -- for overriding prior for first delta state (8' \Delta[1]x3s)
#odel_s8=gv.gvar(1.213,dels_s8.sdev)  ## -- odd delta state (8' fit (\Delta orbital))
#ogrd_s8=gv.gvar(1.213-dels_s8.mean,dels_s8.sdev)  ## -- odd ground state (8' fit (\Delta orbital))
#delu_s8=delr_s8              ## -- splitting for states with unknown continuum limit
#delx_s8=delx_s8p             ## -- extra (hopefully unconstrained) states

#v5old
#delt_s8=gv.gvar(0.038,0.082) ## -- taste splitting (8' fit, actual)
#ogrd_s8=gv.gvar(1.19-dels_s8.mean,dels_s8.sdev)  ## -- odd ground state (8' fit (\Delta orbital))
##ovrs_s8=gv.gvar(0.966,0.042) ## -- for overriding prior for first delta state (8' \Delta[0]x1s)
#ovrs_s8=gv.gvar(1.004,0.012) ## -- for overriding prior for first delta state (8' \Delta[1]x2s)

### v4
#delr_s8=gv.gvar(0.30,0.25)   ## -- radial splitting (8' fit)
##delt_s8=gv.gvar(0.128,0.074)   ## -- taste splitting (8' fit, actual)
##delt_s8=gv.gvar(0.043,0.074)   ## -- taste splitting (8' fit, actual/3)
#delt_s8=gv.gvar(0.064,0.074)   ## -- taste splitting (8' fit, actual/2)
#delu_s8=dels_s8              ## -- splitting for states with unknown continuum limit
#delx_s8=gv.gvar(1e0,5e-1)     ## -- extra (hopefully unconstrained) states
#ogrd_s8=gv.gvar(1.157-dels_s8.mean,dels_s8.sdev)  ## -- odd ground state (8' fit (\Delta orbital))
##ovrs_s8=gv.gvar(0.892,0.140) ## -- for overriding prior for first delta state (8' fit \Delta[0])
##ovrs_s8=gv.gvar(0.953,0.070) ## -- for overriding prior for first delta state (8' fit[1] - taste)
#ovrs_s8=gv.gvar(1.017,0.032) ## -- for overriding prior for first delta state (8' fit \Delta[1])
##ovrs_s8=gv.gvar(1.081,0.070) ## -- for overriding prior for first delta state (8' fit[1] + taste)
##delr_s8=gv.gvar(0.30,0.30)   ## -- radial splitting (UNMOTIVATED)
##delt_s8=delt_s8p             ## -- taste splitting (HISQ \pi taste splittings)
##ngrd_s8=gv.gvar(0.72,0.3)    ## -- even ground state (effective mass)
##ogrd_s8=gv.gvar(1.19-dels_s8.mean,dels_s8.sdev)  ## -- odd ground state (8' fit (\Delta orbital))
##ovrs_s8=gv.gvar(.94,0.3) ## -- for overriding prior for first delta state (PDG)

## -- S16
delr_s16=delr_s8  ## -- radial splitting (PDG value)
delu_s16=dels_s8  ## -- splitting for states with unknown continuum limit
delx_s16=delx_s8  ## -- extra (hopefully unconstrained) states
dels_s16=gv.gvar(0.254,0.036)   ## -- N-\Del splitting (8 fit, D0-N0, actualx1s)
delt_s16=gv.gvar(0.061,0.066)   ## -- taste splitting (8 fit x1s)
ngrd_s16=gv.gvar(0.731,0.1)     ## -- even ground state (8 fit, large error )
ogrd_s16=gv.gvar(0.932,0.036) ## -- odd ground state (8 fit N'0, actual x3s)
ovrs_s16=gv.gvar(0.985,0.036) ## -- overriding prior for first delta state (S8 fit, actual x1s)

## v5 old
#dels_s16=gv.gvar(0.280,0.028)   ## -- N-\Del splitting (8 fit, D0-N0, actual x3 error)
#delt_s16=gv.gvar(0.040,0.016)   ## -- taste splitting (8 fit)
#ngrd_s16=gv.gvar(0.749,0.1)     ## -- even ground state (8 fit, large error )
##ngrd_s16=gv.gvar(0.764,0.050) ## -- even ground state (8 fit + taste, actual x2 error)
##ogrd_s16=gv.gvar(0.955,0.030) ## -- odd ground state (8 fit, actual x3 error)
##ogrd_s16=gv.gvar(0.942,0.040) ## -- odd ground state (8 fit N'0, actual x3 error)
#ogrd_s16=gv.gvar(0.982,0.040) ## -- odd ground state (8 fit N'0+t, actual x3 error)
#ovrs_s16=gv.gvar(1.030,0.030) ## -- overriding prior for first delta state (S8 fit, actual x3 error)

## -- S16
### v4
#delr_s16=delr_s8  ## -- radial splitting (PDG value)
#dels_s16=gv.gvar(0.218,0.045)   ## -- N-\Del splitting (8 fit, actual x3 error)
#delt_s16=gv.gvar(0.044,0.020)## -- taste splitting (8 fit)
#delu_s16=dels_s16 ## -- splitting for states with unknown continuum limit
#delx_s16=delx_s8  ## -- extra (hopefully unconstrained) states
#ngrd_s16=gv.gvar(0.720,0.050) ## -- even ground state (8 fit, actual x2 error)
##ngrd_s16=gv.gvar(0.764,0.050) ## -- even ground state (8 fit + taste, actual x2 error)
##ogrd_s16=gv.gvar(0.955,0.030) ## -- odd ground state (8 fit, actual x3 error)
#ogrd_s16=gv.gvar(0.955,0.030) ## -- odd ground state (8 fit, actual x3 error)
#ovrs_s16=gv.gvar(0.938,0.030) ## -- overriding prior for first delta state (S8 fit, actual x2 error)

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
define_init_s8['logEn']=list(gv.exp([0.736,.039,.050,.140,.054,.376,.065,.083] + [1]*10))
define_init_s8['logEo']=list(gv.exp([0.892,.052,.052,.044,.419,.122,.1,.1] + [1]*10))
#define_init_s8['logEn']=list(gv.exp([0.780,.019,.037,.095,.035,.142,.1,.1] + [1]*10))
#define_init_s8['logEo']=list(gv.exp([0.932,.030,.081,.183,.030,.046,0.1,.1] + [1]*10))
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

## v5 old
#lAm  = 1e1 # log amplitude mean
#lAcs = 1e2 # log amplitude sdev (source)
#lAks = 1e1 # log amplitude sdev (sink)
#Am   = 0   # amplitude mean
#As   = 1e1 # amplitude sdev (source) (temporary)
#Acs  = 1e2 # amplitude sdev (source)
#Aks  = 1e1 # amplitude sdev (sink)

## v5.1
lAm  = 1e2 # log amplitude mean
lAcs = 1e3 # log amplitude sdev (source)
lAks = 1e1 # log amplitude sdev (sink)
Am   = 0   # amplitude mean
#As   = 1e0 # amplitude sdev (source) (temporary)
Acs  = 1e3 # amplitude sdev (source)
Aks  = 1e1 # amplitude sdev (sink)

## v5.2
#lAm  = 5e1 # log amplitude mean
#lAcs = 1e2 # log amplitude sdev (source)
#lAks = 1e1 # log amplitude sdev (sink)
#Am   = 0   # amplitude mean
#Acs  = 1e2 # amplitude sdev (source)
#Aks  = 1e1 # amplitude sdev (sink)

## -- S8
## -- even stacks
nstack_s8mean = [
[ngrd_s8.mean, ## N
 ngrd_s8.mean+  delt_s8.mean,
 ngrd_s8.mean+2*delt_s8.mean,
 ngrd_s8.mean+  delr_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+  delt_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+2*delt_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+3*delt_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+4*delt_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+  delx_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+2*delx_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+3*delx_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+4*delx_s8.mean,
 ngrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+5*delx_s8.mean],
[ovrs_s8.mean, ## \Delta
 ovrs_s8.mean+  delt_s8.mean,
 ovrs_s8.mean+  delr_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+  delt_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+2*delt_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+3*delt_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+4*delt_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+4*delt_s8.mean+  delx_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+4*delt_s8.mean+2*delx_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+4*delt_s8.mean+3*delx_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+4*delt_s8.mean+4*delx_s8.mean,
 ovrs_s8.mean+  delr_s8.mean+4*delt_s8.mean+5*delx_s8.mean] ]

nstack_s8sdev = [
[ngrd_s8.sdev, ## N
 delt_s8.sdev, delt_s8.sdev,
 delr_s8.sdev,
 delt_s8.sdev, delt_s8.sdev, delt_s8.sdev, delt_s8.sdev,
 delx_s8.sdev, delx_s8.sdev, delx_s8.sdev, delx_s8.sdev, delx_s8.sdev],
[ovrs_s8.sdev, ## \Delta
 delt_s8.sdev,
 delr_s8.sdev,
 delt_s8.sdev, delt_s8.sdev, delt_s8.sdev, delt_s8.sdev,
 delx_s8.sdev, delx_s8.sdev, delx_s8.sdev, delx_s8.sdev, delx_s8.sdev]
]

ostack_s8mean = [
[ogrd_s8.mean, ## N
 ogrd_s8.mean+  delt_s8.mean,
 ogrd_s8.mean+2*delt_s8.mean,
 ogrd_s8.mean+  delr_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+  delt_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+2*delt_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+3*delt_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+4*delt_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+  delx_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+2*delx_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+3*delx_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+4*delx_s8.mean,
 ogrd_s8.mean+  delr_s8.mean+4*delt_s8.mean+5*delx_s8.mean],
[odel_s8.mean, ## \Delta
 odel_s8.mean+  delt_s8.mean,
 odel_s8.mean+  delr_s8.mean,
 odel_s8.mean+  delr_s8.mean+  delt_s8.mean,
 odel_s8.mean+  delr_s8.mean+2*delt_s8.mean,
 odel_s8.mean+  delr_s8.mean+3*delt_s8.mean,
 odel_s8.mean+  delr_s8.mean+4*delt_s8.mean,
 odel_s8.mean+  delr_s8.mean+4*delt_s8.mean+  delx_s8.mean,
 odel_s8.mean+  delr_s8.mean+4*delt_s8.mean+2*delx_s8.mean,
 odel_s8.mean+  delr_s8.mean+4*delt_s8.mean+3*delx_s8.mean,
 odel_s8.mean+  delr_s8.mean+4*delt_s8.mean+4*delx_s8.mean,
 odel_s8.mean+  delr_s8.mean+4*delt_s8.mean+5*delx_s8.mean]
]

ostack_s8sdev = [
[ogrd_s8.sdev, ## N
 delt_s8.sdev, delt_s8.sdev, delt_s8.sdev,
 delr_s8.sdev,
 delt_s8.sdev, delt_s8.sdev, delt_s8.sdev, delt_s8.sdev,
 delx_s8.sdev, delx_s8.sdev, delx_s8.sdev, delx_s8.sdev, delx_s8.sdev],
[odel_s8.sdev, ## \Delta
 delt_s8.sdev,
 delr_s8.sdev,
 delt_s8.sdev, delt_s8.sdev, delt_s8.sdev, delt_s8.sdev,
 delx_s8.sdev, delx_s8.sdev, delx_s8.sdev, delx_s8.sdev, delx_s8.sdev]
]

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
[ovrs_s8.mean-ngrd_s8.mean-2*delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[ovrs_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 4 Del[0]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
#[ovrs_s8.mean-ngrd_s8.mean-delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delt_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 5 N[1] - this state gives issues when subtracting sufficiently small ovrs_s8
#utf.append_prior_state(define_prior_s8,nkey_s8,
#gv.gvar(
##[delr_s8.mean+ngrd_s8.mean-ovrs_s8.mean-delt_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
##[delr_s8.mean+ngrd_s8.mean-ovrs_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
#[delr_s8.mean+ngrd_s8.mean+delt_s8.mean-ovrs_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
#[delr_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delr_s8.mean-dels_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
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
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
## -- 9 \Delta[1]
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(nkey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(nkey_s8)-3)/2)+[Aks]*((len(nkey_s8)-1)/2)))
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
[delx_s8.mean-3*delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
#[dels_s8.mean-3*delt_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
#[dels_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 5
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
#[delu_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
#[delu_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
## -- 6
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
[delx_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
#[delr_s8.mean,lAm]+[Am]*(len(okey_s8)-2),
#[delr_s8.sdev,lAcs]+[Acs]*((len(okey_s8)-3)/2)+[Aks]*((len(okey_s8)-1)/2)))
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
## -- 1
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
#[2*delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
#[delt_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
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
[delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
#v4
#utf.append_prior_state(define_prior_s8p,nkey_s8p,
#gv.gvar(
#[delx_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
#[delx_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 4
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 5
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
## -- 6
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delt_s8p.mean,lAm]+[Am]*(len(nkey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(nkey_s8p)-3)/2)+[Aks]*((len(nkey_s8p)-1)/2)))
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
[delt_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
#v4
#utf.append_prior_state(define_prior_s8p,okey_s8p,
#gv.gvar(
#[delx_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
#[delx_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 3
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delt_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
## -- 4
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delt_s8p.mean,lAm]+[Am]*(len(okey_s8p)-2),
[delt_s8p.sdev,lAcs]+[Acs]*((len(okey_s8p)-3)/2)+[Aks]*((len(okey_s8p)-1)/2)))
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
## -- even stacks
nstack_s16mean = [
[ngrd_s16.mean, ## N
 ngrd_s16.mean+  delr_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+  delt_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+2*delt_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+3*delt_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+4*delt_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+  delx_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+2*delx_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+3*delx_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+4*delx_s16.mean,
 ngrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+5*delx_s16.mean],
[ovrs_s16.mean, ## \Delta
 ovrs_s16.mean+  delt_s16.mean,
 ovrs_s16.mean+2*delt_s16.mean,
 ovrs_s16.mean+  delr_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+  delt_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+2*delt_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+3*delt_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+4*delt_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+4*delt_s16.mean+  delx_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+4*delt_s16.mean+2*delx_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+4*delt_s16.mean+3*delx_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+4*delt_s16.mean+4*delx_s16.mean,
 ovrs_s16.mean+  delr_s16.mean+4*delt_s16.mean+5*delx_s16.mean]
 ]

nstack_s16sdev = [
[ngrd_s16.sdev, ## N
 delr_s16.sdev,
 delt_s16.sdev, delt_s16.sdev, delt_s16.sdev, delt_s16.sdev,
 delx_s16.sdev, delx_s16.sdev, delx_s16.sdev, delx_s16.sdev, delx_s16.sdev],
[ovrs_s16.sdev, ## \Delta
 delt_s16.sdev, delt_s16.sdev,
 delr_s16.sdev,
 delt_s16.sdev, delt_s16.sdev, delt_s16.sdev, delt_s16.sdev,
 delx_s16.sdev, delx_s16.sdev, delx_s16.sdev, delx_s16.sdev, delx_s16.sdev]
]

ostack_s16mean = [
[ogrd_s16.mean, ## N
 ogrd_s16.mean+  delt_s16.mean,
 ogrd_s16.mean+2*delt_s16.mean,
 ogrd_s16.mean+  delr_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+  delt_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+2*delt_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+3*delt_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+4*delt_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+  delx_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+2*delx_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+3*delx_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+4*delx_s16.mean,
 ogrd_s16.mean+  delr_s16.mean+4*delt_s16.mean+5*delx_s16.mean],
[ogrd_s16.mean+  dels_s16.mean, ## \Delta
 ogrd_s16.mean+  dels_s16.mean+  delt_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+  delt_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+2*delt_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+3*delt_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+4*delt_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+4*delt_s16.mean+  delx_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+4*delt_s16.mean+2*delx_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+4*delt_s16.mean+3*delx_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+4*delt_s16.mean+4*delx_s16.mean,
 ogrd_s16.mean+  dels_s16.mean+  delr_s16.mean+4*delt_s16.mean+5*delx_s16.mean]
]

ostack_s16sdev = [
[ogrd_s16.sdev, ## N
 delt_s16.sdev, delt_s16.sdev,
 delr_s16.sdev,
 delt_s16.sdev, delt_s16.sdev, delt_s16.sdev, delt_s16.sdev,
 delx_s16.sdev, delx_s16.sdev, delx_s16.sdev, delx_s16.sdev, delx_s16.sdev],
[ogrd_s16.sdev, ## \Delta
 delt_s16.sdev,
 delr_s16.sdev,
 delt_s16.sdev, delt_s16.sdev, delt_s16.sdev, delt_s16.sdev,
 delx_s16.sdev, delx_s16.sdev, delx_s16.sdev, delx_s16.sdev, delx_s16.sdev]
]
#utf.stack_prior_states(define_prior_s16,nkey_s16,nstack_s16mean,nstack_s16sdev)
#utf.stack_prior_states(define_prior_s16,okey_s16,ostack_s16mean,ostack_s16sdev)

## -- S16
## -- even states
## -- 0
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[ngrd_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[ngrd_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[ngrd_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 1 -> override with delta prior from S(3/2,16)_0 fit
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[ovrs_s16.mean-ngrd_s16.mean-1*delt_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[ovrs_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[ovrs_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 2
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delt_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delt_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 3
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delt_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delt_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 4
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delr_s16.mean-2*delt_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delr_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delr_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 5
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delt_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delt_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 6
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delt_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delt_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 7
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 8
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 9
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 10
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 11
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 12
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))
## -- 13
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(nkey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(nkey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(nkey_s16)-3)/2)+[Aks]*((len(nkey_s16)-1)/2)))

## -- odd states
## -- 0
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[ogrd_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
[ogrd_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 1
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
[delt_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 2
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
[delt_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 3
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[dels_s16.mean-2*delt_s16.mean,lAm]+[Am]*(len(okey_s16)-2), # 2tastes
#[dels_s16.mean,lAm]+[Am]*(len(okey_s16)-2), # 0tastes
[dels_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 4
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
[delt_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 5
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
[delt_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 6
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
[delt_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 7
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delr_s16.mean-3*delt_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
[delr_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 8
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 9
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 10
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 11
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))
## -- 12
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,lAm]+[Am]*(len(okey_s16)-2),
#[delx_s16.sdev,lAcs,lAcs]+[As]*(len(okey_s16)-3)))
[delx_s16.sdev,lAcs]+[Acs]*((len(okey_s16)-3)/2)+[Aks]*((len(okey_s16)-1)/2)))

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

