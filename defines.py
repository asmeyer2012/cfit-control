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
lkey=['G11','G12','G22','G13','G23','G33','G15','G25','G35','G55','G16','G26','G36','G56','G66']
maxit      =100   # maximum iterations
svdcut     =None
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
#config   ='l1648f211b580m013m065m838'
#campaign ='gb2pt_l1648f211b580m013m065m838'
config   ='l2064f21b676m010m050'
campaign ='gb2pt_l2064f21b676m010m050'
DBEngine = create_engine('sqlite:///'+dbpath+config+campaign+'.sqlite')
Session  = sessionmaker(bind=DBEngine)
session  = Session()
#
## -- output defines
out_path ='/project/axial/data/fit-in/'
#out_fname='gb2pt_l1648f211b580m013m065m838_s16p_db'
out_fname='gb2pt_l2064f21b676m010m050_db'

## ------
## FROM MAKE_MODELS.PY
## ------
#cor_len=48
cor_len=64 ## -- TODO: parse this number out of configuration?
define_model={}
## --

rangeMin=2
define_model['G11']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,12), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('c1n','c1o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G22']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,12), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('c2n','c2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G33']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,12), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('c3n','c3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G55']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,12), 'tp':-cor_len,\
 'akey':('c5n','c5o'), 'bkey':('c5n','c5o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G66']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,11), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('c6n','c6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }

define_model['G12']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('c2n','c2o'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
define_model['G13']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,11), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('c3n','c3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G15']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('c5n','c5o'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
define_model['G16']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('c6n','c6o'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
define_model['G23']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('c3n','c3o'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
define_model['G25']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,12), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('c5n','c5o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G26']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('c6n','c6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G35']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,11), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('c5n','c5o'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
define_model['G36']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,11), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('c6n','c6o'), 'ekey':('En','Eo'), 'skey':(1.,1.) }
define_model['G56']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,10), 'tp':-cor_len,\
 'akey':('c5n','c5o'), 'bkey':('c6n','c6o'), 'ekey':('En','Eo'), 'skey':(1.,1.) }

## ------
## FROM MAKE_PRIOR.PY
## ------
define_prior=dfp.define_prior

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

