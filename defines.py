from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
import meta_data
import gvar as gv

## ------
## FROM CONTROL.PY
## ------
## -- define some parameters as False
##    - if want to turn on, uncomment in switches
do_makedata=False;
do_db=False;
do_default_plot=False;
do_plot=False;

## -- switches
#do_makedata=True;
do_db=True;
#do_default_plot=True;
do_plot=True;

## -- other parameters
lkey=['pion05RWRW'] # keys to process
maxit      =5000;   # maximum iterations
#svdcut     =1e-2;  # svd cut
#svdcut     =3e-3;
#svdcut     =1e-6;
svdcut     =None;
## -- tolerance check does not work if lots of variation from + to -
## -- need to fix
ctol       =None; # tolerance for consecutive correlator points
#ctol       =1e2; 

## ------
## FROM MAKE_DATA_RAW.PY
## ------
## -- create meta_data, initial setup
## -- trying to eliminate need for meta_data
mdp = meta_data.md_params();
mdp.corr_len=48;
mdp.t_min   =4;
#mdp.n_nfit = 1;
#mdp.n_ofit = 0;
mdp.n_nfit = 2;
mdp.n_ofit = 1;
mdp.n_bs   = 10;
mdp.output_path="/project/axial/database/corrfitter-input/";
mdp.output_fname="pi2pt-4-db";

## ------
## FROM MAKE_DATA_DB.PY
## ------
## -- database defines
dbpath   ='/project/axial/database/db-files/';
config   ='l1648f211b580m013m065m838';
campaign ='-pi2pt-4';
DBEngine = create_engine('sqlite:///'+dbpath+config+campaign+'.sqlite');
Session  = sessionmaker(bind=DBEngine);
session  = Session();
#
## -- output defines
out_path ='/project/axial/database/corrfitter-input/';
out_fname='pi2pt-4-db';

## ------
## FROM MAKE_MODELS.PY
## ------
tmin=4;
trang=48;
define_model={};
## --
define_model['G00']=\
{#'n_nfit':1, 'n_ofit':1,\
 'tdata':range(trang), 'tfit':range(tmin,trang-tmin+1), 'tp':trang,\
 'akey':('an','ao'), 'bkey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,1.) };
define_model['Gaa']=\
{#'n_nfit':1, 'n_ofit':1,\
 'tdata':range(trang), 'tfit':range(tmin,trang-tmin+1), 'tp':trang,\
 'akey':('an','ao'), 'bkey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,1.) };
## --
define_model['pion5RWRW']=\
{#'n_nfit':1, 'n_ofit':0,\
 'tdata':range(trang), 'tfit':range(tmin,trang-tmin+1), 'tp':trang,\
 'akey':'an', 'bkey':'an', 'ekey':'En', 'skey':1. };
# 'akey':('an','ao'), 'bkey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,1.) };
## --
define_model['pion05RWRW']=\
{#'n_nfit':1, 'n_ofit':1,\
 'tdata':range(trang), 'tfit':range(tmin,trang-tmin+1), 'tp':trang,\
 'akey':('an','ao'), 'bkey':('an','ao'), 'ekey':('En','Eo'), 'skey':(1.,-1.) };
define_model['pioni0RWRW']=define_model['pion05RWRW'];
define_model['pioniRWRW' ]=define_model['pion05RWRW'];
define_model['pion0RWRW' ]=define_model['pion05RWRW'];
define_model['pionsRWRW' ]=define_model['pion05RWRW'];
define_model['rhoiRWRW'  ]=define_model['pion05RWRW'];
define_model['rhoi0RWRW' ]=define_model['pion05RWRW'];
define_model['rho0RWRW'  ]=define_model['pion05RWRW'];
define_model['rhoisRWRW' ]=define_model['pion05RWRW'];
define_model['pioni5RWRW']=define_model['pion5RWRW' ];
define_model['pionijRWRW']=define_model['pion5RWRW' ];
## -- more specific assignments
tmin=4; #3+1
#tmin=9; #1+1
define_model['pion05RWRW']['tfit']=range(tmin,trang-tmin+1);

## ------
## FROM MAKE_PRIOR.PY
## ------
define_prior={};
define_prior['pion5RWRW']=\
{'an':gv.gvar([4.542],[0.4]),\
 'En':gv.gvar([0.230],[0.01])};
define_prior['pion05RWRW']=\
{'an':gv.gvar([0.60,2.70,6.75],[0.15,0.3,0.5]),'ao':gv.gvar([0.54],[0.06]),\
 'En':gv.gvar([0.260,0.340,0.91],[0.02,0.05,0.08]),'Eo':gv.gvar([0.271],[0.04])};
#{'an':gv.gvar([0.43,2.70],[0.15,0.3]),'ao':gv.gvar([0.56,0.2],[0.06,0.05]),\
# 'En':gv.gvar([0.238,0.335],[0.02,0.05]),'Eo':gv.gvar([0.277,0.250],[0.04,0.05])};
#{'an':gv.gvar([0.42,2.60],[0.15,0.3]),'ao':gv.gvar([0.56],[0.06]),\
# 'En':gv.gvar([0.238,0.320],[0.02,0.05]),'Eo':gv.gvar([0.277],[0.04])};
#{'an':gv.gvar([0.45],[0.15]),'ao':gv.gvar([0.49],[0.06]),\
# 'En':gv.gvar([0.235],[0.02]),'Eo':gv.gvar([0.263],[0.04])};
#tmin = 9
#{'an':gv.gvar([0.70],[0.12]),'ao':gv.gvar([0.441],[0.032]),\
# 'En':gv.gvar([0.302],[0.012]),'Eo':gv.gvar([0.270],[0.012])};
## -- 
#tmin = 4
#{'an':gv.gvar([0.47,2.48,6.75],[0.15,0.3,0.5]),'ao':gv.gvar([0.54],[0.06]),\
# 'En':gv.gvar([0.238,0.330,0.91],[0.02,0.05,0.08]),'Eo':gv.gvar([0.271],[0.04])};
define_prior['pioni5RWRW']=\
{'an':gv.gvar([0.31,1.54],[0.08,0.2]),\
 'En':gv.gvar([0.253,0.22],[0.01,0.03])};
define_prior['pionijRWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),\
 'En':gv.gvar([0.167,0.15],[0.01,0.03])};
define_prior['pioni0RWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),'ao':gv.gvar([0.035],[0.005]),\
 'En':gv.gvar([0.239,0.46],[0.01,0.03]),'Eo':gv.gvar([0.265],[0.01])};
define_prior['pioniRWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),'ao':gv.gvar([0.035],[0.005]),\
 'En':gv.gvar([0.239,0.46],[0.01,0.03]),'Eo':gv.gvar([0.265],[0.01])};
define_prior['pion0RWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),'ao':gv.gvar([0.035],[0.005]),\
 'En':gv.gvar([0.239,0.46],[0.01,0.03]),'Eo':gv.gvar([0.265],[0.01])};
define_prior['pionsRWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),'ao':gv.gvar([0.035],[0.005]),\
 'En':gv.gvar([0.239,0.46],[0.01,0.03]),'Eo':gv.gvar([0.265],[0.01])};
define_prior['rhoiRWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),'ao':gv.gvar([0.035],[0.005]),\
 'En':gv.gvar([0.239,0.46],[0.01,0.03]),'Eo':gv.gvar([0.265],[0.01])};
define_prior['rhoi0RWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),'ao':gv.gvar([0.035],[0.005]),\
 'En':gv.gvar([0.239,0.46],[0.01,0.03]),'Eo':gv.gvar([0.265],[0.01])};
define_prior['rho0RWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),'ao':gv.gvar([0.035],[0.005]),\
 'En':gv.gvar([0.239,0.46],[0.01,0.03]),'Eo':gv.gvar([0.265],[0.01])};
define_prior['rhoisRWRW']=\
{'an':gv.gvar([0.6,3.5],[0.08,0.2]),'ao':gv.gvar([0.035],[0.005]),\
 'En':gv.gvar([0.239,0.46],[0.01,0.03]),'Eo':gv.gvar([0.265],[0.01])};

## ------
## FROM MAKE_PLOT.PY
## ------
sep=2; ## -- timeslice separation for log ratio

