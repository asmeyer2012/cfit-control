from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
import meta_data
import gvar         as gv
import util_funcs   as utf
import define_prior as dfp

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
#do_plot=True
#do_effmass=True
do_baryon=True
#do_uncorr=True

## -- other parameters
lkey=['G22','G23','G32','G33','G24','G34','G44']
maxit      =10000   # maximum iterations
svdcut     =None
#svdcut     =3e-3
#svdcut     =3e-2
#svdcut     =1e-1  # svd cut
## -- tolerance check does not work if lots of variation from + to -
## -- need to fix
ctol       =None # tolerance for consecutive correlator points

## ------
## FROM MAKE_DATA_RAW.PY
## ------
## -- create meta_data, initial setup
## -- trying to eliminate need for meta_data
mdp = meta_data.md_params()

## ------
## FROM MAKE_DATA_DB.PY
## ------
## -- database defines
dbpath   ='/project/axial/data/dbfile/'
config   ='l1648f211b580m013m065m838'
campaign ='gb2pt_l1648f211b580m013m065m838'
#config   ='l2064f21b676m010m050'
#campaign ='gb2pt_l2064f21b676m010m050'
DBEngine = create_engine('sqlite:///'+dbpath+config+campaign+'.sqlite')
Session  = sessionmaker(bind=DBEngine)
session  = Session()
#
## -- output defines
out_path ='/project/axial/data/fit-in/'
out_fname='gb2pt_l1648f211b580m013m065m838_s16p_db'

## ------
## FROM MAKE_MODELS.PY
## ------
cor_len=48
define_model={}
## --

rangeMin=2
define_model['G22']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,12), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G33']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,11), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G44']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,12), 'tp':-cor_len,\
 'akey':('c4n','c4o'), 'bkey':('k4n','k4o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G66']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,12), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }

define_model['G23']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,8), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G24']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k4n','k4o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G26']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G34']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k4n','k4o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G36']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G46']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c4n','c4o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }

define_model['G32']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,9), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G42']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c4n','c4o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G43']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c4n','c4o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G62']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G63']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G64']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k4n','k4o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }

## ------
## FROM MAKE_PRIOR.PY
## ------
define_prior=dfp.define_prior
## -- 

define_prior['G22']=\
{'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'k2n':define_prior['k2n'], 'k2o':define_prior['k2o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G33']=\
{'c3n':define_prior['c3n'], 'c3o':define_prior['c3o'],
 'k3n':define_prior['k3n'], 'k3o':define_prior['k3o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G44']=\
{'c4n':define_prior['c4n'], 'c4o':define_prior['c4o'],
 'k4n':define_prior['k4n'], 'k4o':define_prior['k4o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G66']=\
{'c6n':define_prior['c6n'], 'c6o':define_prior['c6o'],
 'k6n':define_prior['k6n'], 'k6o':define_prior['k6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }

define_prior['G23']=\
{'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'k3n':define_prior['k3n'], 'k3o':define_prior['k3o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G24']=\
{'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'k4n':define_prior['k4n'], 'k4o':define_prior['k4o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G26']=\
{'c2n':define_prior['c2n'], 'c2o':define_prior['c2o'],
 'k6n':define_prior['k6n'], 'k6o':define_prior['k6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G34']=\
{'c3n':define_prior['c3n'], 'c3o':define_prior['c3o'],
 'k4n':define_prior['k4n'], 'k4o':define_prior['k4o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G36']=\
{'c3n':define_prior['c3n'], 'c3o':define_prior['c3o'],
 'k6n':define_prior['k6n'], 'k6o':define_prior['k6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }
define_prior['G46']=\
{'c4n':define_prior['c4n'], 'c4o':define_prior['c4o'],
 'k6n':define_prior['k6n'], 'k6o':define_prior['k6o'],
 'logEn': define_prior['logEn'],  'logEo': define_prior['logEo'] }

define_prior['G32']=define_prior['G23']
define_prior['G42']=define_prior['G24']
define_prior['G62']=define_prior['G26']
define_prior['G43']=define_prior['G34']
define_prior['G63']=define_prior['G36']
define_prior['G64']=define_prior['G46']

fitargs={}
for key in lkey:
 fitargs[key]={}

def suppressKey(key,tag,line): ## -- ignore errors
 try:
  fitargs[key][tag]=line
 except KeyError:
  pass
suppressKey('G22','y_pos_limit',[1e-10,1e2])
suppressKey('G22','y_neg_limit',[1e-10,1e2])
suppressKey('G33','y_pos_limit',[1e-10,1e2])
suppressKey('G33','y_neg_limit',[1e-10,1e2])
suppressKey('G44','y_pos_limit',[1e-10,1e2])
suppressKey('G44','y_neg_limit',[1e-10,1e2])
suppressKey('G66','y_pos_limit',[1e-10,1e2])
suppressKey('G66','y_neg_limit',[1e-10,1e2])

suppressKey('G23','y_pos_limit',[1e-10,1e2])
suppressKey('G23','y_neg_limit',[1e-10,1e2])
suppressKey('G24','y_pos_limit',[1e-10,1e2])
suppressKey('G24','y_neg_limit',[1e-10,1e2])
suppressKey('G26','y_pos_limit',[1e-10,1e2])
suppressKey('G26','y_neg_limit',[1e-10,1e2])
suppressKey('G34','y_pos_limit',[1e-10,1e2])
suppressKey('G34','y_neg_limit',[1e-10,1e2])
suppressKey('G36','y_pos_limit',[1e-10,1e2])
suppressKey('G36','y_neg_limit',[1e-10,1e2])
suppressKey('G46','y_pos_limit',[1e-10,1e2])
suppressKey('G46','y_neg_limit',[1e-10,1e2])

suppressKey('G32','y_pos_limit',[1e-10,1e2])
suppressKey('G32','y_neg_limit',[1e-10,1e2])
suppressKey('G42','y_pos_limit',[1e-10,1e2])
suppressKey('G42','y_neg_limit',[1e-10,1e2])
suppressKey('G62','y_pos_limit',[1e-10,1e2])
suppressKey('G62','y_neg_limit',[1e-10,1e2])
suppressKey('G43','y_pos_limit',[1e-10,1e2])
suppressKey('G43','y_neg_limit',[1e-10,1e2])
suppressKey('G63','y_pos_limit',[1e-10,1e2])
suppressKey('G63','y_neg_limit',[1e-10,1e2])
suppressKey('G64','y_pos_limit',[1e-10,1e2])
suppressKey('G64','y_neg_limit',[1e-10,1e2])

