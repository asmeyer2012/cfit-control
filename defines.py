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

## -- switches
#do_makedata=True
#do_db=True
#do_default_plot=True
do_plot=True
#do_effmass=True
do_baryon=True

## -- other parameters
lkey=['Gaa'] # keys to process
maxit      =5000   # maximum iterations
#svdcut     =1e-2  # svd cut
#svdcut     =3e-3
#svdcut     =1e-6
svdcut     =None
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
mdp.corr_len=-64
mdp.t_min   =4
#mdp.n_nfit = 1
#mdp.n_ofit = 0
mdp.n_nfit = 1
mdp.n_ofit = 1
mdp.n_bs   = 10
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
tmin=4
trang=64
define_model={}
## --
define_model['Gaa']=\
{
 'tdata':range(trang), 'tfit':range(tmin,trang-tmin+1), 'tp':-trang,\
 'akey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
## --
#define_model['pion5RWRW']=\
#{#'n_nfit':1, 'n_ofit':0,\
# 'tdata':range(trang), 'tfit':range(tmin,trang-tmin+1), 'tp':trang,\
# 'akey':'an', 'bkey':'an', 'ekey':'En', 'skey':1. }
## 'akey':('an','ao'), 'bkey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
### --
#define_model['pion05RWRW']=\
#{#'n_nfit':1, 'n_ofit':1,\
# 'tdata':range(trang), 'tfit':range(tmin,trang-tmin+1), 'tp':trang,\
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
tmin=4 #3+1
#tmin=9 #1+1
#define_model['pion05RWRW']['tfit']=range(tmin,trang-tmin+1)

## ------
## FROM MAKE_PRIOR.PY
## ------
define_prior={}
define_prior['Gaa']=\
{'an':gv.gvar([3.2,2.0],[0.4,0.5]),'ao':gv.gvar([0.001],[0.001]),\
 'En':gv.gvar([0.930,0.2],[0.05,0.1]),'Eo':gv.gvar([0.95],[0.1])}
#{'an':gv.gvar([3.2,0.1],[0.4,0.3]),'ao':gv.gvar([0.004],[0.01]),\
# 'En':gv.gvar([0.930,0.2],[0.05,0.1]),'Eo':gv.gvar([0.43],[0.1])}

#define_prior['pion05RWRW']=\
#{'an':gv.gvar([0.60,2.70,6.75],[0.15,0.3,0.5]),'ao':gv.gvar([0.54],[0.06]),\
# 'En':gv.gvar([0.260,0.340,0.91],[0.02,0.05,0.08]),'Eo':gv.gvar([0.271],[0.04])}

## ------
## FROM MAKE_PLOT.PY
## ------
sep=2 ## -- timeslice separation for log ratio

