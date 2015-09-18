import gvar       as gv
import util_funcs as utf

## -- append so it is easier to rearrange states
nkey = ('logEn','c2n','c3n','c4n','c6n','k2n','k3n','k4n','k6n')
okey = ('logEo','c2o','c3o','c4o','c6o','k2o','k3o','k4o','k6o')
define_prior = utf.create_prior_dict(nkey,okey)
define_prior['nkey'] = nkey
define_prior['okey'] = okey

## -- even states
## -- 1
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[1.20,-1.8,0.0,1.6,1.0,-1.4,1.1,0.5,1.0],
[0.5,10,10,10,10,10,10,10,10]
))
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.10,3.1,0.4,-0.2,1.0,-0.5,2.5,0.1,1.0],
[0.1,10,10,10,10,10,10,10,10]
))
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.10,2.9,-0.1,0.0,1.0,0.7,-2.6,0.2,1.0],
[0.1,10,10,10,10,10,10,10,10]
))
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[1.0,-1.3,0.2,-9.2,1.0,2.7,-5.1,0.1,1.0],
[0.5,10,10,20,10,10,10,10,10]
))

## -- odd states
## -- 1
utf.append_prior_state(define_prior,okey,
gv.gvar(
[1.55,-0.2,-0.1,-5.8,1.0,-2.9,-5.8,-0.1,1.0],
[0.5,10,10,10,10,10,10,10,10]
))
## -- 2
utf.append_prior_state(define_prior,okey,
gv.gvar(
[0.2,-1.6,0.4,-1.4,1.0,-1.3,2.5,0.0,1.0],
[0.1,10,10,10,10,10,10,10,10]
))
## -- 3
utf.append_prior_state(define_prior,okey,
gv.gvar(
[0.5,1.9,-0.3,-2.5,1.0,-2.0,3.7,0.1,1.0],
[0.4,10,10,10,10,10,10,10,10]
))
