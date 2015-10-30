import gvar       as gv
import util_funcs as utf

nkey = ('logEn','logc1n','logk1n','c2n','c3n','c5n','c6n','k2n','k3n','k5n','k6n')
okey = ('logEo','logc1o','logk1o','c2o','c3o','c5o','c6o','k2o','k3o','k5o','k6o')
define_prior={}
define_prior['nkey'] = nkey
define_prior['okey'] = okey
define_prior['logEn']=[]
define_prior['logEo']=[]
define_prior['logc1n']=[]
define_prior['logc1o']=[]
define_prior['logk1n']=[]
define_prior['logk1o']=[]
define_prior['c2n']=[]
define_prior['c3n']=[]
define_prior['c5n']=[]
define_prior['c6n']=[]
define_prior['c2o']=[]
define_prior['c3o']=[]
define_prior['c5o']=[]
define_prior['c6o']=[]
define_prior['k2n']=[]
define_prior['k3n']=[]
define_prior['k5n']=[]
define_prior['k6n']=[]
define_prior['k2o']=[]
define_prior['k3o']=[]
define_prior['k5o']=[]
define_prior['k6o']=[]

## -- prior mass splittings
ngrd=gv.gvar(1.0,0.5) ## -- even ground state
ogrd=gv.gvar(ngrd.mean+0.3,0.5) ## -- odd ground state
ovrs=gv.gvar(1.25,0.2)  ## -- for overriding prior for first delta state
delr=gv.gvar(0.45,0.45) ## -- radial splitting
dels=gv.gvar(0.22,0.22) ## -- \Delta-N splitting
delt=gv.gvar(4e-2,8e-2) ## -- taste splitting
delu=dels               ## -- splitting for states with unknown continuum limit
delx=gv.gvar(1e0,1e0)   ## -- extra (hopefully unconstrained) states

## -- used if do_init is defined in defines.py
define_init={}
num_nreal=8 #3N+2D +1radial
num_oreal=6 #4N+1D+1?
define_init['logEn']=list(gv.exp([1.13,.006,.03,.128,.005,1.48,.20,.07] + [1]*10))
define_init['logEo']=list(gv.exp([1.42,.036,.015,.141,.054,2.2,.20] + [1]*10))
define_init['logc1n']=list(gv.exp([2]*num_nreal + [1e-6]*10))
define_init['logc1o']=list(gv.exp([2]*num_oreal + [1e-6]*10))
define_init['logk1n']=list(gv.exp([2]*num_nreal + [1e-6]*10))
define_init['logk1o']=list(gv.exp([2]*num_oreal + [1e-6]*10))
define_init['c2n']=[1]*num_nreal + [1e-6]*10
define_init['c3n']=[1]*num_nreal + [1e-6]*10
define_init['c5n']=[1]*num_nreal + [1e-6]*10
define_init['c6n']=[1]*num_nreal + [1e-6]*10
define_init['c2o']=[1]*num_oreal + [1e-6]*10
define_init['c3o']=[1]*num_oreal + [1e-6]*10
define_init['c5o']=[1]*num_oreal + [1e-6]*10
define_init['c6o']=[1]*num_oreal + [1e-6]*10
define_init['k2n']=[1]*num_nreal + [1e-6]*10
define_init['k3n']=[1]*num_nreal + [1e-6]*10
define_init['k5n']=[1]*num_nreal + [1e-6]*10
define_init['k6n']=[1]*num_nreal + [1e-6]*10
define_init['k2o']=[1]*num_oreal + [1e-6]*10
define_init['k3o']=[1]*num_oreal + [1e-6]*10
define_init['k5o']=[1]*num_oreal + [1e-6]*10
define_init['k6o']=[1]*num_oreal + [1e-6]*10

## -- even states
## -- 0
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[ngrd.mean,1,1]+[0]*(len(nkey)-3),
[ngrd.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 1
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delt.mean,1,1]+[0]*(len(nkey)-3),
[delt.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 2
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delt.mean,1,1]+[0]*(len(nkey)-3),
[delt.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 3 -> override with delta prior from S(3/2,16)_0 fit
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[ovrs.mean-ngrd.mean-2*delt.mean,1,1]+[0]*(len(nkey)-3),
[ovrs.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 4
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delt.mean,1,1]+[0]*(len(nkey)-3),
[delt.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 5
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delr.mean-1*delt.mean,1,1]+[0]*(len(nkey)-3),
[delr.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 6
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delr.mean,1,1]+[0]*(len(nkey)-3),
[delr.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 7
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delt.mean,1,1]+[0]*(len(nkey)-3),
[delt.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 8
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(nkey)-3),
[delx.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 9
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(nkey)-3),
[delx.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 10
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(nkey)-3),
[delx.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 11
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(nkey)-3),
[delx.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 12
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(nkey)-3),
[delx.sdev,10,10]+[10]*(len(nkey)-3)))
## -- 13
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(nkey)-3),
[delx.sdev,10,10]+[10]*(len(nkey)-3)))

## -- odd states
## -- 0
utf.append_prior_state(define_prior,okey,
gv.gvar(
[ogrd.mean,1,1]+[0]*(len(okey)-3),
[ogrd.sdev,10,10]+[10]*(len(okey)-3)))
## -- 1
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delt.mean,1,1]+[0]*(len(okey)-3),
[delt.sdev,10,10]+[10]*(len(okey)-3)))
## -- 2
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delt.mean,1,1]+[0]*(len(okey)-3),
[delt.sdev,10,10]+[10]*(len(okey)-3)))
## -- 3
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delt.mean,1,1]+[0]*(len(okey)-3),
[delt.sdev,10,10]+[10]*(len(okey)-3)))
## -- 4
utf.append_prior_state(define_prior,okey,
gv.gvar(
[dels.mean-3*delt.mean,1,1]+[0]*(len(okey)-3),
[dels.sdev,10,10]+[10]*(len(okey)-3)))
## -- 5
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delu.mean,1,1]+[0]*(len(okey)-3),
[delu.sdev,10,10]+[10]*(len(okey)-3)))
## -- 6
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delr.mean,1,1]+[0]*(len(okey)-3),
[delr.sdev,10,10]+[10]*(len(okey)-3)))
## -- 7
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delt.mean,1,1]+[0]*(len(okey)-3),
[delt.sdev,10,10]+[10]*(len(okey)-3)))
## -- 8
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(okey)-3),
[delx.sdev,10,10]+[10]*(len(okey)-3)))
## -- 9
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(okey)-3),
[delx.sdev,10,10]+[10]*(len(okey)-3)))
## -- 10
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(okey)-3),
[delx.sdev,10,10]+[10]*(len(okey)-3)))
## -- 11
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(okey)-3),
[delx.sdev,10,10]+[10]*(len(okey)-3)))
## -- 12
utf.append_prior_state(define_prior,okey,
gv.gvar(
[delx.mean,1,1]+[0]*(len(okey)-3),
[delx.sdev,10,10]+[10]*(len(okey)-3)))

define_prior['G11']=\
{'logc1n':define_prior['logc1n'],
 'logc1o':define_prior['logc1o'],
 'logk1n':define_prior['logk1n'],
 'logk1o':define_prior['logk1o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G12']=\
{'logc1n':define_prior['logc1n'],
 'logc1o':define_prior['logc1o'],
 'k2n':define_prior['k2n'],
 'k2o':define_prior['k2o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G13']=\
{'logc1n':define_prior['logc1n'],
 'logc1o':define_prior['logc1o'],
 'k3n':define_prior['k3n'],
 'k3o':define_prior['k3o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G15']=\
{'logc1n':define_prior['logc1n'],
 'logc1o':define_prior['logc1o'],
 'k5n':define_prior['k5n'],
 'k5o':define_prior['k5o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G16']=\
{'logc1n':define_prior['logc1n'],
 'logc1o':define_prior['logc1o'],
 'k6n':define_prior['k6n'],
 'k6o':define_prior['k6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G21']=\
{'logk1n':define_prior['logk1n'],
 'logk1o':define_prior['logk1o'],
 'c2n':define_prior['c2n'],
 'c2o':define_prior['c2o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G22']=\
{'c2n':define_prior['c2n'],
 'c2o':define_prior['c2o'],
 'k2n':define_prior['k2n'],
 'k2o':define_prior['k2o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G23']=\
{'c2n':define_prior['c2n'],
 'c2o':define_prior['c2o'],
 'k3n':define_prior['k3n'],
 'k3o':define_prior['k3o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G25']=\
{'c2n':define_prior['c2n'],
 'c2o':define_prior['c2o'],
 'k5n':define_prior['k5n'],
 'k5o':define_prior['k5o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G26']=\
{'c2n':define_prior['c2n'],
 'c2o':define_prior['c2o'],
 'k6n':define_prior['k6n'],
 'k6o':define_prior['k6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G31']=\
{'logk1n':define_prior['logk1n'],
 'logk1o':define_prior['logk1o'],
 'c3n':define_prior['c3n'],
 'c3o':define_prior['c3o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G32']=\
{'k2n':define_prior['k2n'],
 'k2o':define_prior['k2o'],
 'c3n':define_prior['c3n'],
 'c3o':define_prior['c3o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G33']=\
{'c3n':define_prior['c3n'],
 'c3o':define_prior['c3o'],
 'k3n':define_prior['k3n'],
 'k3o':define_prior['k3o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G35']=\
{'c3n':define_prior['c3n'],
 'c3o':define_prior['c3o'],
 'k5n':define_prior['k5n'],
 'k5o':define_prior['k5o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G36']=\
{'c3n':define_prior['c3n'],
 'c3o':define_prior['c3o'],
 'k6n':define_prior['k6n'],
 'k6o':define_prior['k6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G51']=\
{'logk1n':define_prior['logk1n'],
 'logk1o':define_prior['logk1o'],
 'c5n':define_prior['c5n'],
 'c5o':define_prior['c5o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G52']=\
{'k2n':define_prior['k2n'],
 'k2o':define_prior['k2o'],
 'c5n':define_prior['c5n'],
 'c5o':define_prior['c5o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G53']=\
{'k3n':define_prior['k3n'],
 'k3o':define_prior['k3o'],
 'c5n':define_prior['c5n'],
 'c5o':define_prior['c5o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G55']=\
{'c5n':define_prior['c5n'],
 'c5o':define_prior['c5o'],
 'k5n':define_prior['k5n'],
 'k5o':define_prior['k5o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G56']=\
{'c5n':define_prior['c5n'],
 'c5o':define_prior['c5o'],
 'k6n':define_prior['k6n'],
 'k6o':define_prior['k6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G61']=\
{'logk1n':define_prior['logk1n'],
 'logk1o':define_prior['logk1o'],
 'c6n':define_prior['c6n'],
 'c6o':define_prior['c6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G62']=\
{'k2n':define_prior['k2n'],
 'k2o':define_prior['k2o'],
 'c6n':define_prior['c6n'],
 'c6o':define_prior['c6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G63']=\
{'k3n':define_prior['k3n'],
 'k3o':define_prior['k3o'],
 'c6n':define_prior['c6n'],
 'c6o':define_prior['c6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G65']=\
{'k5n':define_prior['k5n'],
 'k5o':define_prior['k5o'],
 'c6n':define_prior['c6n'],
 'c6o':define_prior['c6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
define_prior['G66']=\
{'c6n':define_prior['c6n'],
 'c6o':define_prior['c6o'],
 'k6n':define_prior['k6n'],
 'k6o':define_prior['k6o'],
 'logEn':define_prior['logEn'],
 'logEo':define_prior['logEo'] }
