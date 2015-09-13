from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
import meta_data
import gvar as gv

## ------
## FROM CONTROL.PY
## ------
## -- define some parameters as False
##    - if want to turn on, uncomment in switches
do_makedata=False
do_db=False
do_default_plot=False
do_plot=False
do_effmass=False
do_baryon=False
do_uncorr=False

## -- switches
#do_makedata=True
#do_db=True
#do_default_plot=True
do_plot=True
#do_effmass=True
do_baryon=True
#do_uncorr=True

## -- other parameters
#lkey=['G12'] # keys to process
lkey=['G11','G12'] # keys to process
#lkey=['G11','G12','G22'] # keys to process
maxit      =10000   # maximum iterations
svdcut     =None
#svdcut     =3e-3
#svdcut     =3e-2
#svdcut     =1e-1  # svd cut
## -- tolerance check does not work if lots of variation from + to -
## -- need to fix
ctol       =None # tolerance for consecutive correlator points
#ctol       =1e2 

## ------
## FROM MAKE_DATA_RAW.PY
## ------
## -- create meta_data, initial setup
## -- trying to eliminate need for meta_data
mdp = meta_data.md_params()
mdp.corr_len=-64 #only for make_data_raw
mdp.t_min   = 2 #unused
mdp.t_max   = 23 #unused
mdp.n_nfit = 1 #unused 
mdp.n_ofit = 1 #unused 
mdp.n_bs   = 1 #disabled
mdp.output_path="/project/axial/data/dbfile/"
mdp.output_fname="gb2pt_l2064f21b676m010m050_db"

## ------
## FROM MAKE_DATA_DB.PY
## ------
## -- database defines
dbpath   ='/project/axial/data/dbfile/'
config   ='l2064f21b676m010m050'
campaign ='gb2pt_l2064f21b676m010m050'
DBEngine = create_engine('sqlite:///'+dbpath+config+campaign+'.sqlite')
Session  = sessionmaker(bind=DBEngine)
session  = Session()
#
## -- output defines
out_path ='/project/axial/data/fit-in/'
out_fname='gb2pt_l2064f21b676m010m050_db'

## ------
## FROM MAKE_MODELS.PY
## ------
cor_len=64
define_model={}
## --
define_model['G11']=\
{
 'tdata':range(cor_len), 'tfit':range(2,16), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G12']=\
{
 'tdata':range(cor_len), 'tfit':range(2,18), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('c2n','c2o'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
define_model['G22']=\
{
 'tdata':range(cor_len), 'tfit':range(2,16), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
## --
#define_model['pion5RWRW']=\
#{#'n_nfit':1, 'n_ofit':0,\
# 'tdata':range(cor_len), 'tfit':range(tmin,cor_len-tmin+1), 'tp':cor_len,\
# 'akey':'an', 'bkey':'an', 'ekey':'En', 'skey':1. }
## 'akey':('an','ao'), 'bkey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
### --
#define_model['pion05RWRW']=\
#{#'n_nfit':1, 'n_ofit':1,\
# 'tdata':range(cor_len), 'tfit':range(tmin,cor_len-tmin+1), 'tp':cor_len,\
# 'akey':('an','ao'), 'bkey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
#define_model['pioni0RWRW']=define_model['pion05RWRW']
#define_model['pioniRWRW' ]=define_model['pion05RWRW']
#define_model['pion0RWRW' ]=define_model['pion05RWRW']
#define_model['pionsRWRW' ]=define_model['pion05RWRW']
#define_model['rhoiRWRW'  ]=define_model['pion05RWRW']
#define_model['rhoi0RWRW' ]=define_model['pion05RWRW']
#define_model['rho0RWRW'  ]=define_model['pion05RWRW']
#define_model['rhoisRWRW' ]=define_model['pion05RWRW']
#define_model['pioni5RWRW']=define_model['pion5RWRW' ]
#define_model['pionijRWRW']=define_model['pion5RWRW' ]
## -- more specific assignments
#tmin=20 #1+1
#define_model['pion05RWRW']['tfit']=range(tmin,cor_len-tmin+1)

## ------
## FROM MAKE_PRIOR.PY
## ------
#do_plot=True
define_prior={}

#define_prior['logEo']=gv.gvar([0.75,0.3],[100,100])
#define_prior['logc1o']=gv.gvar([0.01,3.3],[100,100])
#define_prior['logc2o']=gv.gvar([0.1,3.3],[100,100])
define_prior['logEo']=gv.gvar([0.9,0.2],[10,10])
define_prior['logc1o']=gv.gvar([0.8,3.3],[10,10])
define_prior['logc2o']=gv.gvar([0.6,0.01],[10,10])

#define_prior['logEn']=gv.gvar([0.5],[10])
#define_prior['logc1n']=gv.gvar([3.6],[10])
#define_prior['logc2n']=gv.gvar([3.6],[10])
define_prior['logEn']=gv.gvar([0.7,0.2],[10,10])
define_prior['logc1n']=gv.gvar([2.4,2.8],[10,10])
define_prior['logc2n']=gv.gvar([1.0,0.01],[10,10])

define_prior['G11']=\
{'logc1n':define_prior['logc1n'], 'logc1o':define_prior['logc1o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] } # s8 c1_1
define_prior['G22']=\
{'logc2n':define_prior['logc2n'], 'logc2o':define_prior['logc2o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] } # s8 c2_2
define_prior['G12']=\
{'logc1n':define_prior['logc1n'], 'logc1o':define_prior['logc1o'],
 'logc2n':define_prior['logc2n'], 'logc2o':define_prior['logc2o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] } # s8 c1_2

#define_prior['pion05RWRW']=\
#{'an':gv.gvar([0.60,2.70,6.75],[0.15,0.3,0.5]),'ao':gv.gvar([0.54],[0.06]),\
# 'En':gv.gvar([0.260,0.340,0.91],[0.02,0.05,0.08]),'Eo':gv.gvar([0.271],[0.04])}

## ------
## FROM MAKE_PLOT.PY
## ------
sep=2 ## -- timeslice separation for log ratio

fitargs={}
for key in lkey:
 fitargs[key]={}
def suppressKey(key,tag,line): ## -- ignore errors
 try:
  fitargs[key][tag]=line
 except KeyError:
  pass
suppressKey('G11','y_pos_limit',[1e-10,1e2])
suppressKey('G11','y_neg_limit',[1e-10,1e2])
suppressKey('G12','y_pos_limit',[1e-10,1e2])
suppressKey('G12','y_neg_limit',[1e-10,1e2])
suppressKey('G22','y_pos_limit',[1e-10,1e2])
suppressKey('G22','y_neg_limit',[1e-10,1e2])

