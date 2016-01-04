import gvar       as gv
import util_funcs as utf

## -- prior mass splittings
## -- S8
ngrd_s8=gv.gvar(1.0,0.5) ## -- even ground state
ogrd_s8=gv.gvar(ngrd_s8.mean+0.3,0.5) ## -- odd ground state
ovrs_s8=gv.gvar(1.25,0.2)  ## -- for overriding prior for first delta state
delr_s8=gv.gvar(0.45,0.45) ## -- radial splitting
dels_s8=gv.gvar(0.22,0.22) ## -- \Delta-N splitting
delt_s8=gv.gvar(4e-2,8e-2) ## -- taste splitting
delu_s8=dels_s8            ## -- splitting for states with unknown continuum limit
delx_s8=gv.gvar(1e0,1e0)   ## -- extra (hopefully unconstrained) states
## -- S8'
ngrd_s8p=gv.gvar(0.85,0.5) ## -- even ground state
ogrd_s8p=gv.gvar(ngrd_s8p.mean+0.3,0.5) ## -- odd ground state
delr_s8p=gv.gvar(0.30,0.30) ## -- radial splitting
#dels_s8p=gv.gvar() ## -- \Delta-N splitting
delt_s8p=gv.gvar(4e-2,8e-2) ## -- taste splitting
delx_s8p=gv.gvar(1e0,1e0)  ## -- extra (hopefully unconstrained) states
## -- S16
ngrd_s16=gv.gvar(0.989,0.5) ## -- even ground state (effective mass)
ogrd_s16=gv.gvar(ngrd_s16.mean+0.45,0.45) ## -- odd ground state (N-N*(1535) mass splitting, PDG)
ovrs_s16=gv.gvar(1.299,0.1) ## -- for overriding prior for first delta state (S8' fit)
delr_s16=gv.gvar(0.6,0.6)   ## -- radial splitting (N-N*(1710) mass splitting, PDG)
dels_s16=gv.gvar(0.22,0.22) ## -- N-\Del splitting (PDG)
delt_s16=gv.gvar(4e-2,8e-2) ## -- taste splitting (HISQ \pi taste splittings)
delu_s16=dels_s16           ## -- splitting for states with unknown continuum limit
delx_s16=gv.gvar(1e0,1e0)   ## -- extra (hopefully unconstrained) states

## -- used if do_init is defined in defines.py
define_init_s8={}
define_init_s8p={}
define_init_s16={}
num_nreal_s8=8 #3N+2D +1radial
num_oreal_s8=6 #4N+1D+1?
num_nreal_s8p=3 #0N+2D +1radial
num_oreal_s8p=1 #0N+1D+0?
num_nreal_s16=4 #1N+3D
num_oreal_s16=5 #3N+4D+1?

## -- S8
define_init_s8['logEn']=list(gv.exp([1.13,.006,.03,.128,.005,1.48,.20,.07] + [1]*10))
define_init_s8['logEo']=list(gv.exp([1.42,.036,.015,.141,.054,2.2,.20] + [1]*10))
define_init_s8['logc1n']=list(gv.exp([2]*num_nreal_s8 + [1e-6]*10))
define_init_s8['logc1o']=list(gv.exp([2]*num_oreal_s8 + [1e-6]*10))
define_init_s8['logk1n']=list(gv.exp([2]*num_nreal_s8 + [1e-6]*10))
define_init_s8['logk1o']=list(gv.exp([2]*num_oreal_s8 + [1e-6]*10))
define_init_s8['c2n']=[1]*num_nreal_s8 + [1e-6]*10
define_init_s8['c3n']=[1]*num_nreal_s8 + [1e-6]*10
define_init_s8['c5n']=[1]*num_nreal_s8 + [1e-6]*10
define_init_s8['c6n']=[1]*num_nreal_s8 + [1e-6]*10
define_init_s8['c2o']=[1]*num_oreal_s8 + [1e-6]*10
define_init_s8['c3o']=[1]*num_oreal_s8 + [1e-6]*10
define_init_s8['c5o']=[1]*num_oreal_s8 + [1e-6]*10
define_init_s8['c6o']=[1]*num_oreal_s8 + [1e-6]*10
define_init_s8['k2n']=[1]*num_nreal_s8 + [1e-6]*10
define_init_s8['k3n']=[1]*num_nreal_s8 + [1e-6]*10
define_init_s8['k5n']=[1]*num_nreal_s8 + [1e-6]*10
define_init_s8['k6n']=[1]*num_nreal_s8 + [1e-6]*10
define_init_s8['k2o']=[1]*num_oreal_s8 + [1e-6]*10
define_init_s8['k3o']=[1]*num_oreal_s8 + [1e-6]*10
define_init_s8['k5o']=[1]*num_oreal_s8 + [1e-6]*10
define_init_s8['k6o']=[1]*num_oreal_s8 + [1e-6]*10
## -- S8'
define_init_s8p['logEn']=list(gv.exp([1.30,.01,.50] + [1]*10))
define_init_s8p['logEo']=list(gv.exp([1.50] + [1]*10))
define_init_s8p['logc4n']=list(gv.exp([2]*num_nreal_s8p + [1e-6]*10))
define_init_s8p['logk4n']=list(gv.exp([2]*num_nreal_s8p + [1e-6]*10))
define_init_s8p['logc4o']=list(gv.exp([2]*num_oreal_s8p + [1e-6]*10))
define_init_s8p['logk4o']=list(gv.exp([2]*num_oreal_s8p + [1e-6]*10))
define_init_s8p['c7n']=[1]*num_nreal_s8p + [1e-6]*10
define_init_s8p['k7n']=[1]*num_nreal_s8p + [1e-6]*10
define_init_s8p['c7o']=[1]*num_oreal_s8p + [1e-6]*10
define_init_s8p['k7o']=[1]*num_oreal_s8p + [1e-6]*10
## -- S16
define_init_s16['logEn']=list(gv.exp([1.143,.135,.001,.002] + [1]*10))
define_init_s16['logEo']=list(gv.exp([1.478,.025,.078,.035,1.805] + [1]*10))
define_init_s16['logc2n']=list(gv.exp([2]*num_nreal_s16 + [1e-6]*10))
define_init_s16['logk2n']=list(gv.exp([2]*num_nreal_s16 + [1e-6]*10))
define_init_s16['logc2o']=list(gv.exp([2]*num_oreal_s16 + [1e-6]*10))
define_init_s16['logk2o']=list(gv.exp([2]*num_oreal_s16 + [1e-6]*10))
define_init_s16['c3n']=[1]*num_nreal_s16 + [1e-6]*10
define_init_s16['c4n']=[1]*num_nreal_s16 + [1e-6]*10
define_init_s16['c6n']=[1]*num_nreal_s16 + [1e-6]*10
define_init_s16['k3n']=[1]*num_nreal_s16 + [1e-6]*10
define_init_s16['k4n']=[1]*num_nreal_s16 + [1e-6]*10
define_init_s16['k6n']=[1]*num_nreal_s16 + [1e-6]*10
define_init_s16['c3o']=[1]*num_oreal_s16 + [1e-6]*10
define_init_s16['c4o']=[1]*num_oreal_s16 + [1e-6]*10
define_init_s16['c6o']=[1]*num_oreal_s16 + [1e-6]*10
define_init_s16['k3o']=[1]*num_oreal_s16 + [1e-6]*10
define_init_s16['k4o']=[1]*num_oreal_s16 + [1e-6]*10
define_init_s16['k6o']=[1]*num_oreal_s16 + [1e-6]*10

## -- define prior objects to pass to defines.py if requested
define_prior_s8={}
define_prior_s8p={}
define_prior_s16={}

nkey_s8 = ('logEn','logc1n','logk1n','c2n','c3n','c5n','c6n','k2n','k3n','k5n','k6n')
okey_s8 = ('logEo','logc1o','logk1o','c2o','c3o','c5o','c6o','k2o','k3o','k5o','k6o')
nkey_s8p = ('logEn','logc4n','logk4n','c7n','k7n')
okey_s8p = ('logEo','logc4o','logk4o','c7o','k7o')
nkey_s16 = ('logEn','logc2n','logk2n','c3n','c4n','c6n','k3n','k4n','k6n')
okey_s16 = ('logEo','logc2o','logk2o','c3o','c4o','c6o','k3o','k4o','k6o')

## -- S8
define_prior_s8['nkey'] = nkey_s8
define_prior_s8['okey'] = okey_s8
define_prior_s8['logEn']=[]
define_prior_s8['logEo']=[]
define_prior_s8['logc1n']=[]
define_prior_s8['logc1o']=[]
define_prior_s8['logk1n']=[]
define_prior_s8['logk1o']=[]
define_prior_s8['c2n']=[]
define_prior_s8['c3n']=[]
define_prior_s8['c5n']=[]
define_prior_s8['c6n']=[]
define_prior_s8['c2o']=[]
define_prior_s8['c3o']=[]
define_prior_s8['c5o']=[]
define_prior_s8['c6o']=[]
define_prior_s8['k2n']=[]
define_prior_s8['k3n']=[]
define_prior_s8['k5n']=[]
define_prior_s8['k6n']=[]
define_prior_s8['k2o']=[]
define_prior_s8['k3o']=[]
define_prior_s8['k5o']=[]
define_prior_s8['k6o']=[]
## -- S8'
define_prior_s8p['nkey'] = nkey_s8p
define_prior_s8p['okey'] = okey_s8p
define_prior_s8p['logEn']=[]
define_prior_s8p['logc4n']=[]
define_prior_s8p['logk4n']=[]
define_prior_s8p['c7n']=[]
define_prior_s8p['k7n']=[]
define_prior_s8p['logEo']=[]
define_prior_s8p['logc4o']=[]
define_prior_s8p['logk4o']=[]
define_prior_s8p['c7o']=[]
define_prior_s8p['k7o']=[]
## -- S16
define_prior_s16['nkey'] = nkey_s16
define_prior_s16['okey'] = okey_s16
define_prior_s16['logEn']=[]
define_prior_s16['logEo']=[]
define_prior_s16['logc2n']=[]
define_prior_s16['logk2n']=[]
define_prior_s16['logc2o']=[]
define_prior_s16['logk2o']=[]
define_prior_s16['c3n']=[]
define_prior_s16['c4n']=[]
define_prior_s16['c6n']=[]
define_prior_s16['k3n']=[]
define_prior_s16['k4n']=[]
define_prior_s16['k6n']=[]
define_prior_s16['c3o']=[]
define_prior_s16['c4o']=[]
define_prior_s16['c6o']=[]
define_prior_s16['k3o']=[]
define_prior_s16['k4o']=[]
define_prior_s16['k6o']=[]

## -- S16
## -- even states
## -- 0
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[ngrd_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[ngrd_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 1 -> override with delta prior from S(3/2,16)_0 fit
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[ovrs_s16.mean-ngrd_s16.mean-0*delt_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[ovrs_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 2
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 3
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 4
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delr_s16.mean-2*delt_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delr_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 5
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 6
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 7
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 8
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 9
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 10
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 11
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 12
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))
## -- 13
utf.append_prior_state(define_prior_s16,nkey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(nkey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(nkey_s16)-3)))

## -- odd states
## -- 0
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[ogrd_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[ogrd_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 1
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 2
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 3
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[dels_s16.mean-2*delt_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[dels_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 4
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 5
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 6
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delt_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delt_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 7
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delr_s16.mean-3*delt_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delr_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 8
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 9
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 10
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 11
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))
## -- 12
utf.append_prior_state(define_prior_s16,okey_s16,
gv.gvar(
[delx_s16.mean,1,1]+[0]*(len(okey_s16)-3),
[delx_s16.sdev,10,10]+[10]*(len(okey_s16)-3)))

## -- S8
## -- even states
## -- 0
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[ngrd_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[ngrd_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 1
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delt_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 2
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delt_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 3 -> override with delta prior from S(3/2,16)_0 fit
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[ovrs_s8.mean-ngrd_s8.mean-2*delt_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[ovrs_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 4
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delt_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 5
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delr_s8.mean-1*delt_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delr_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 6
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delr_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delr_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 7
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delt_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delt_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 8
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 9
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 10
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 11
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 12
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))
## -- 13
utf.append_prior_state(define_prior_s8,nkey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(nkey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(nkey_s8)-3)))

## -- odd states
## -- 0
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[ogrd_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[ogrd_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 1
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delt_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 2
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delt_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 3
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delt_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 4
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[dels_s8.mean-3*delt_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[dels_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 5
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delu_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delu_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 6
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delr_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delr_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 7
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delt_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delt_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 8
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 9
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 10
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 11
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))
## -- 12
utf.append_prior_state(define_prior_s8,okey_s8,
gv.gvar(
[delx_s8.mean,1,1]+[0]*(len(okey_s8)-3),
[delx_s8.sdev,10,10]+[10]*(len(okey_s8)-3)))

## -- S8'
## -- even states S8'
## -- 0
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[ngrd_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[ngrd_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))
## -- 1
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delt_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[delt_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))
## -- 2
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delr_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[delr_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))
## -- 3
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))
## -- 4
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))
## -- 5
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))
## -- 6
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))
## -- 7
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))
## -- 8
utf.append_prior_state(define_prior_s8p,nkey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(nkey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(nkey_s8p)-3)))

## -- odd states S8'
## -- 0
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[ogrd_s8p.mean,1,1]+[0]*(len(okey_s8p)-3),
[ogrd_s8p.sdev,10,10]+[10]*(len(okey_s8p)-3)))
## -- 1
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delr_s8p.mean,1,1]+[0]*(len(okey_s8p)-3),
[delr_s8p.sdev,10,10]+[10]*(len(okey_s8p)-3)))
## -- 2
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(okey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(okey_s8p)-3)))
## -- 3
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(okey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(okey_s8p)-3)))
## -- 4
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(okey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(okey_s8p)-3)))
## -- 5
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(okey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(okey_s8p)-3)))
## -- 6
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(okey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(okey_s8p)-3)))
## -- 7
utf.append_prior_state(define_prior_s8p,okey_s8p,
gv.gvar(
[delx_s8p.mean,1,1]+[0]*(len(okey_s8p)-3),
[delx_s8p.sdev,10,10]+[10]*(len(okey_s8p)-3)))

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
  if key[2] == log_s8 or key[2] == 's'+log_s8:
    logstr2='log'
  else:
    logstr2=''
  try:
    define_prior_s8[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior_s8[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior_s8[logstr1+'c'+key[1]+'o'],
      logstr2+'k'+key[2]+'n':define_prior_s8[logstr2+'k'+key[2]+'n'],
      logstr2+'k'+key[2]+'o':define_prior_s8[logstr2+'k'+key[2]+'o'],
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
  if key[2] == log_s8p or key[2] == 's'+log_s8p:
    logstr2='log'
  else:
    logstr2=''
  try:
    define_prior_s8p[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior_s8p[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior_s8p[logstr1+'c'+key[1]+'o'],
      logstr2+'k'+key[2]+'n':define_prior_s8p[logstr2+'k'+key[2]+'n'],
      logstr2+'k'+key[2]+'o':define_prior_s8p[logstr2+'k'+key[2]+'o'],
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
  if key[2] == log_s16 or key[2] == 's'+log_s16:
    logstr2='log'
  else:
    logstr2=''
  try:
    define_prior_s8[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior_s16[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior_s16[logstr1+'c'+key[1]+'o'],
      logstr2+'k'+key[2]+'n':define_prior_s16[logstr2+'k'+key[2]+'n'],
      logstr2+'k'+key[2]+'o':define_prior_s16[logstr2+'k'+key[2]+'o'],
      'logEn':define_prior_s16['logEn'],
      'logEo':define_prior_s16['logEo'] }
  except KeyError:
    continue ## -- key is not defined, don't worry about it
pass

### -- Construct prior objects with their prior values
### -- S8
#define_prior_s8['G11']=\
#{'logc1n':define_prior_s8['logc1n'],
# 'logc1o':define_prior_s8['logc1o'],
# 'logk1n':define_prior_s8['logk1n'],
# 'logk1o':define_prior_s8['logk1o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G12']=\
#{'logc1n':define_prior_s8['logc1n'],
# 'logc1o':define_prior_s8['logc1o'],
# 'k2n':define_prior_s8['k2n'],
# 'k2o':define_prior_s8['k2o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G13']=\
#{'logc1n':define_prior_s8['logc1n'],
# 'logc1o':define_prior_s8['logc1o'],
# 'k3n':define_prior_s8['k3n'],
# 'k3o':define_prior_s8['k3o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G15']=\
#{'logc1n':define_prior_s8['logc1n'],
# 'logc1o':define_prior_s8['logc1o'],
# 'k5n':define_prior_s8['k5n'],
# 'k5o':define_prior_s8['k5o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G16']=\
#{'logc1n':define_prior_s8['logc1n'],
# 'logc1o':define_prior_s8['logc1o'],
# 'k6n':define_prior_s8['k6n'],
# 'k6o':define_prior_s8['k6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G21']=\
#{'logk1n':define_prior_s8['logk1n'],
# 'logk1o':define_prior_s8['logk1o'],
# 'c2n':define_prior_s8['c2n'],
# 'c2o':define_prior_s8['c2o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G22']=\
#{'c2n':define_prior_s8['c2n'],
# 'c2o':define_prior_s8['c2o'],
# 'k2n':define_prior_s8['k2n'],
# 'k2o':define_prior_s8['k2o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G23']=\
#{'c2n':define_prior_s8['c2n'],
# 'c2o':define_prior_s8['c2o'],
# 'k3n':define_prior_s8['k3n'],
# 'k3o':define_prior_s8['k3o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G25']=\
#{'c2n':define_prior_s8['c2n'],
# 'c2o':define_prior_s8['c2o'],
# 'k5n':define_prior_s8['k5n'],
# 'k5o':define_prior_s8['k5o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G26']=\
#{'c2n':define_prior_s8['c2n'],
# 'c2o':define_prior_s8['c2o'],
# 'k6n':define_prior_s8['k6n'],
# 'k6o':define_prior_s8['k6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G31']=\
#{'logk1n':define_prior_s8['logk1n'],
# 'logk1o':define_prior_s8['logk1o'],
# 'c3n':define_prior_s8['c3n'],
# 'c3o':define_prior_s8['c3o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G32']=\
#{'k2n':define_prior_s8['k2n'],
# 'k2o':define_prior_s8['k2o'],
# 'c3n':define_prior_s8['c3n'],
# 'c3o':define_prior_s8['c3o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G33']=\
#{'c3n':define_prior_s8['c3n'],
# 'c3o':define_prior_s8['c3o'],
# 'k3n':define_prior_s8['k3n'],
# 'k3o':define_prior_s8['k3o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G35']=\
#{'c3n':define_prior_s8['c3n'],
# 'c3o':define_prior_s8['c3o'],
# 'k5n':define_prior_s8['k5n'],
# 'k5o':define_prior_s8['k5o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G36']=\
#{'c3n':define_prior_s8['c3n'],
# 'c3o':define_prior_s8['c3o'],
# 'k6n':define_prior_s8['k6n'],
# 'k6o':define_prior_s8['k6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G51']=\
#{'logk1n':define_prior_s8['logk1n'],
# 'logk1o':define_prior_s8['logk1o'],
# 'c5n':define_prior_s8['c5n'],
# 'c5o':define_prior_s8['c5o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G52']=\
#{'k2n':define_prior_s8['k2n'],
# 'k2o':define_prior_s8['k2o'],
# 'c5n':define_prior_s8['c5n'],
# 'c5o':define_prior_s8['c5o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G53']=\
#{'k3n':define_prior_s8['k3n'],
# 'k3o':define_prior_s8['k3o'],
# 'c5n':define_prior_s8['c5n'],
# 'c5o':define_prior_s8['c5o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G55']=\
#{'c5n':define_prior_s8['c5n'],
# 'c5o':define_prior_s8['c5o'],
# 'k5n':define_prior_s8['k5n'],
# 'k5o':define_prior_s8['k5o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G56']=\
#{'c5n':define_prior_s8['c5n'],
# 'c5o':define_prior_s8['c5o'],
# 'k6n':define_prior_s8['k6n'],
# 'k6o':define_prior_s8['k6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G61']=\
#{'logk1n':define_prior_s8['logk1n'],
# 'logk1o':define_prior_s8['logk1o'],
# 'c6n':define_prior_s8['c6n'],
# 'c6o':define_prior_s8['c6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G62']=\
#{'k2n':define_prior_s8['k2n'],
# 'k2o':define_prior_s8['k2o'],
# 'c6n':define_prior_s8['c6n'],
# 'c6o':define_prior_s8['c6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G63']=\
#{'k3n':define_prior_s8['k3n'],
# 'k3o':define_prior_s8['k3o'],
# 'c6n':define_prior_s8['c6n'],
# 'c6o':define_prior_s8['c6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G65']=\
#{'k5n':define_prior_s8['k5n'],
# 'k5o':define_prior_s8['k5o'],
# 'c6n':define_prior_s8['c6n'],
# 'c6o':define_prior_s8['c6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
#define_prior_s8['G66']=\
#{'c6n':define_prior_s8['c6n'],
# 'c6o':define_prior_s8['c6o'],
# 'k6n':define_prior_s8['k6n'],
# 'k6o':define_prior_s8['k6o'],
# 'logEn':define_prior_s8['logEn'],
# 'logEo':define_prior_s8['logEo'] }
### -- S8'
#define_prior_s8p['G44']=\
#{'logc4n':define_prior_s8p['logc4n'],
# 'logc4o':define_prior_s8p['logc4o'],
# 'logk4n':define_prior_s8p['logk4n'],
# 'logk4o':define_prior_s8p['logk4o'],
# 'logEn':define_prior_s8p['logEn'],
# 'logEo':define_prior_s8p['logEo'] }
#define_prior_s8p['G47']=\
#{'k7n':define_prior_s8p['k7n'],
# 'k7o':define_prior_s8p['k7o'],
# 'logc4n':define_prior_s8p['logc4n'],
# 'logc4o':define_prior_s8p['logc4o'],
# 'logEn':define_prior_s8p['logEn'],
# 'logEo':define_prior_s8p['logEo'] }
#define_prior_s8p['G74']=\
#{'logk4n':define_prior_s8p['logk4n'],
# 'logk4o':define_prior_s8p['logk4o'],
# 'c7n':define_prior_s8p['c7n'],
# 'c7o':define_prior_s8p['c7o'],
# 'logEn':define_prior_s8p['logEn'],
# 'logEo':define_prior_s8p['logEo'] }
#define_prior_s8p['G77']=\
#{'c7n':define_prior_s8p['c7n'],
# 'c7o':define_prior_s8p['c7o'],
# 'k7n':define_prior_s8p['k7n'],
# 'k7o':define_prior_s8p['k7o'],
# 'logEn':define_prior_s8p['logEn'],
# 'logEo':define_prior_s8p['logEo'] }
### -- S16
#define_prior_s16['G22']=\
#{'logc2n':define_prior_s16['logc2n'],
# 'logc2o':define_prior_s16['logc2o'],
# 'logk2n':define_prior_s16['logk2n'],
# 'logk2o':define_prior_s16['logk2o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G23']=\
#{'logc2n':define_prior_s16['logc2n'],
# 'logc2o':define_prior_s16['logc2o'],
# 'k3n':define_prior_s16['k3n'],
# 'k3o':define_prior_s16['k3o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G24']=\
#{'logc2n':define_prior_s16['logc2n'],
# 'logc2o':define_prior_s16['logc2o'],
# 'k4n':define_prior_s16['k4n'],
# 'k4o':define_prior_s16['k4o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G26']=\
#{'logc2n':define_prior_s16['logc2n'],
# 'logc2o':define_prior_s16['logc2o'],
# 'k6n':define_prior_s16['k6n'],
# 'k6o':define_prior_s16['k6o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G32']=\
#{'logk2n':define_prior_s16['logk2n'],
# 'logk2o':define_prior_s16['logk2o'],
# 'c3n':define_prior_s16['c3n'],
# 'c3o':define_prior_s16['c3o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G33']=\
#{'c3n':define_prior_s16['c3n'],
# 'c3o':define_prior_s16['c3o'],
# 'k3n':define_prior_s16['k3n'],
# 'k3o':define_prior_s16['k3o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G34']=\
#{'c3n':define_prior_s16['c3n'],
# 'c3o':define_prior_s16['c3o'],
# 'k4n':define_prior_s16['k4n'],
# 'k4o':define_prior_s16['k4o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G36']=\
#{'c3n':define_prior_s16['c3n'],
# 'c3o':define_prior_s16['c3o'],
# 'k6n':define_prior_s16['k6n'],
# 'k6o':define_prior_s16['k6o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G42']=\
#{'logk2n':define_prior_s16['logk2n'],
# 'logk2o':define_prior_s16['logk2o'],
# 'c4n':define_prior_s16['c4n'],
# 'c4o':define_prior_s16['c4o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G43']=\
#{'k3n':define_prior_s16['k3n'],
# 'k3o':define_prior_s16['k3o'],
# 'c4n':define_prior_s16['c4n'],
# 'c4o':define_prior_s16['c4o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G44']=\
#{'c4n':define_prior_s16['c4n'],
# 'c4o':define_prior_s16['c4o'],
# 'k4n':define_prior_s16['k4n'],
# 'k4o':define_prior_s16['k4o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G46']=\
#{'c4n':define_prior_s16['c4n'],
# 'c4o':define_prior_s16['c4o'],
# 'k6n':define_prior_s16['k6n'],
# 'k6o':define_prior_s16['k6o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G62']=\
#{'logk2n':define_prior_s16['logk2n'],
# 'logk2o':define_prior_s16['logk2o'],
# 'c6n':define_prior_s16['c6n'],
# 'c6o':define_prior_s16['c6o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G63']=\
#{'k3n':define_prior_s16['k3n'],
# 'k3o':define_prior_s16['k3o'],
# 'c6n':define_prior_s16['c6n'],
# 'c6o':define_prior_s16['c6o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G64']=\
#{'k4n':define_prior_s16['k4n'],
# 'k4o':define_prior_s16['k4o'],
# 'c6n':define_prior_s16['c6n'],
# 'c6o':define_prior_s16['c6o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }
#define_prior_s16['G66']=\
#{'c6n':define_prior_s16['c6n'],
# 'c6o':define_prior_s16['c6o'],
# 'k6n':define_prior_s16['k6n'],
# 'k6o':define_prior_s16['k6o'],
# 'logEn':define_prior_s16['logEn'],
# 'logEo':define_prior_s16['logEo'] }

## -- end

