import gvar       as gv
import util_funcs as utf

nkey = ('logEn','c1n','c2n','c3n','c5n','c6n')
okey = ('logEo','c1o','c2o','c3o','c5o','c6o')
define_prior={}
define_prior['nkey'] = nkey
define_prior['okey'] = okey
define_prior['logEn']=[]
define_prior['c1n']=[]
define_prior['c2n']=[]
define_prior['c3n']=[]
define_prior['c5n']=[]
define_prior['c6n']=[]
define_prior['logEo']=[]
define_prior['c1o']=[]
define_prior['c2o']=[]
define_prior['c3o']=[]
define_prior['c5o']=[]
define_prior['c6o']=[]

## -- even states
## -- 0
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.74,-0.6,1.1,-0.1,0.1,0.1],
[0.5,10.0,10.0,10.0,10.0,10.0]))
## -- 1
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.02,2.7,1.2,0.7,0.1,0.1],
[0.02,10.0,10.0,10.0,10.0,10.0]))
## -- 2
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.02,0.4,0.2,-0.1,0.3,-0.2],
[0.02,10.0,10.0,10.0,10.0,10.0]))
## -- 3
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.05,0.4,0.5,-0.4,0.0,0.2],
[0.05,10.0,10.0,10.0,10.0,10.0]))
## -- 4
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.1,-1.4,-0.5,0.4,0.4,0.3],
[0.05,10.0,10.0,10.0,10.0,10.0]))
## -- 5
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.05,-2.0,0.7,0.4,-0.1,-0.1],
[0.05,10.0,10.0,10.0,10.0,10.0]))
## -- 6
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[0.2,0.3,0.2,-0.4,0.3,-0.0],
[0.2,10.0,10.0,10.0,10.0,10.0]))
## -- 7
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[1.0,-1.1,-0.4,-0.9,0.1,0.4],
[1.0,10.0,10.0,10.0,10.0,10.0]))
## -- 8
utf.append_prior_state(define_prior,nkey,
gv.gvar(
[1.0,0.0,0.0,0.0,0.0,0.0],
[1.0,10.0,10.0,10.0,10.0,10.0]))
### -- 8
#utf.append_prior_state(define_prior,nkey,
#gv.gvar(
#[1.0,0.0,0.0,0.0,0.0,0.0],
#[1.0,10.0,10.0,10.0,10.0,10.0]))

## -- odd states
## -- 0
utf.append_prior_state(define_prior,okey,
gv.gvar(
[0.95,1.2,-0.2,0.5,0.1,-0.0],
[0.5,10.0,10.0,10.0,10.0,10.0]))
## -- 1
utf.append_prior_state(define_prior,okey,
gv.gvar(
[0.05,-0.8,-1.1,-0.2,-0.2,-0.2],
[0.05,10.0,10.0,10.0,10.0,10.0]))
## -- 2
utf.append_prior_state(define_prior,okey,
gv.gvar(
[0.05,-2.1,-0.3,-0.2,0.4,0.0],
[0.05,10.0,10.0,10.0,10.0,10.0]))
## -- 3
utf.append_prior_state(define_prior,okey,
gv.gvar(
[0.05,0.7,-0.5,0.0,0.1,0.4],
[0.05,10.0,10.0,10.0,10.0,10.0]))
## -- 4
utf.append_prior_state(define_prior,okey,
gv.gvar(
[0.05,-2.2,0.1,0.6,-0.2,0.1],
[0.05,10.0,10.0,10.0,10.0,10.0]))
## -- 5
utf.append_prior_state(define_prior,okey,
gv.gvar(
[0.35,0.3,-0.2,0.6,0.4,-0.1],
[0.3,10.0,10.0,10.0,10.0,10.0]))
## -- 6
utf.append_prior_state(define_prior,okey,
gv.gvar(
[3.0,16.4,-18.3,4.6,-2.9,0.2],
[3.0,20.0,20.0,20.0,10.0,10.0]))

define_prior['G11']=\
{'c1n':define_prior['c1n'], 'c1o':define_prior['c1o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G22']=\
{'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G33']=\
{'c3n':define_prior['c3n'], 'c3o':define_prior['c3o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G55']=\
{'c5n':define_prior['c5n'], 'c5o':define_prior['c5o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G66']=\
{'c6n':define_prior['c6n'], 'c6o':define_prior['c6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }

define_prior['G12']=\
{'c1n':define_prior['c1n'], 'c1o':define_prior['c1o'],
 'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G13']=\
{'c1n':define_prior['c1n'], 'c1o':define_prior['c1o'],
 'c3n':define_prior['c3n'], 'c3o':define_prior['c3o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G15']=\
{'c1n':define_prior['c1n'], 'c1o':define_prior['c1o'],
 'c5n':define_prior['c5n'], 'c5o':define_prior['c5o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G16']=\
{'c1n':define_prior['c1n'], 'c1o':define_prior['c1o'],
 'c6n':define_prior['c6n'], 'c6o':define_prior['c6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G23']=\
{'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'c3n':define_prior['c3n'], 'c3o':define_prior['c3o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G25']=\
{'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'c5n':define_prior['c5n'], 'c5o':define_prior['c5o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G26']=\
{'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'c6n':define_prior['c6n'], 'c6o':define_prior['c6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G35']=\
{'c3n':define_prior['c3n'], 'c3o':define_prior['c3o'],
 'c5n':define_prior['c5n'], 'c5o':define_prior['c5o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G36']=\
{'c3n':define_prior['c3n'], 'c3o':define_prior['c3o'],
 'c6n':define_prior['c6n'], 'c6o':define_prior['c6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G56']=\
{'c5n':define_prior['c5n'], 'c5o':define_prior['c5o'],
 'c6n':define_prior['c6n'], 'c6o':define_prior['c6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }

