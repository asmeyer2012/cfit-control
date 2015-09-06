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
lkey=['Gaa','Gab'] # keys to process
maxit      =5000   # maximum iterations
#svdcut     =None
svdcut     =3e-3
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
define_model['Gaa']=\
{
 'tdata':range(cor_len), 'tfit':range(2,23), 'tp':-cor_len,\
 'akey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['Gab']=\
{
 'tdata':range(cor_len), 'tfit':range(2,23), 'tp':-cor_len,\
 'akey':('an','ao'), 'bkey':('bn','bo'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
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
define_prior['Gaa']=\
{'logan':gv.gvar([3.6],[100]),'logao':gv.gvar([0.01,3.3],[100,100]),\
 'logEn':gv.gvar([0.5],[100]),'logEo':gv.gvar([0.75,0.3],[100,100])} # s8 c1_1
define_prior['Gab']=\
{'logan':gv.gvar([3.6],[100]),'logao':gv.gvar([0.01,3.3],[100,100]),\
 'logbn':gv.gvar([3.6],[100]),'logbo':gv.gvar([0.01,3.3],[100,100]),\
 'logEn':gv.gvar([0.5],[100]),'logEo':gv.gvar([0.75,0.3],[100,100])} # s8 c1_1

#define_prior['pion05RWRW']=\
#{'an':gv.gvar([0.60,2.70,6.75],[0.15,0.3,0.5]),'ao':gv.gvar([0.54],[0.06]),\
# 'En':gv.gvar([0.260,0.340,0.91],[0.02,0.05,0.08]),'Eo':gv.gvar([0.271],[0.04])}

## ------
## FROM MAKE_PLOT.PY
## ------
sep=2 ## -- timeslice separation for log ratio

