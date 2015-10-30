from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
import meta_data
import gvar         as gv
import util_funcs   as utf
import define_prior as dfp

## ------
## FROM CONTROL.PY
## ------
do_makedata=False
do_db=False
do_default_plot=False
do_plot=True
do_effmass=False
do_baryon=True
do_uncorr=False
do_initial=True

## -- other parameters
lkey=[
 'G11','G12','G13','G15','G16','G21','G22','G23','G25','G26',
 'G31','G32','G33','G35','G36','G51','G52','G53','G55','G56',
 'G61','G62','G63','G65','G66']
maxit      =10000   # maximum iterations
svdcut     =None
svdcut     =1e-3
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
config   ='l1648f211b580m013m065m838'
campaign ='gb2pt_l1648f211b580m013m065m838'
DBEngine = create_engine('sqlite:///'+dbpath+config+campaign+'.sqlite')
Session  = sessionmaker(bind=DBEngine)
session  = Session()
#
## -- output defines
out_path ='/project/axial/data/fit-in/'
#out_fname='gb2pt_l1648f211b580m013m065m838_s16p_db'
out_fname='gb2pt_l1648f211b580m013m065m838_s8_l1648'

## ------
## FROM MAKE_MODELS.PY
## ------
cor_len=48
#cor_len=64 ## -- TODO: parse this number out of configuration?
define_model={}
## --
num_nst=8
num_ost=6

rangeMin=2
rangeMaxDiag=12
rangeMaxOffD=10

define_model['G11']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxDiag), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('k1n','k1o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G22']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxDiag), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G33']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxDiag), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G55']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxDiag), 'tp':-cor_len,\
 'akey':('c5n','c5o'), 'bkey':('k5n','k5o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G66']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxDiag), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }

define_model['G12']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G21']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k1n','k1o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G13']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G31']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k1n','k1o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G15']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('k5n','k5o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G51']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c5n','c5o'), 'bkey':('k1n','k1o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G16']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c1n','c1o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G61']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k1n','k1o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G23']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G32']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G25']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k5n','k5o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G52']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c5n','c5o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G26']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c2n','c2o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G62']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k2n','k2o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G35']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k5n','k5o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G53']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c5n','c5o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G36']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c3n','c3o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G63']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k3n','k3o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G56']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c5n','c5o'), 'bkey':('k6n','k6o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }
define_model['G65']=\
{
 'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxOffD), 'tp':-cor_len,\
 'akey':('c6n','c6o'), 'bkey':('k5n','k5o'), 'ekey':('En','Eo'), 'skey':(1.,-1.) }

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
for key in lkey:
 suppressKey(key,'y_pos_limit',[1e-13,1e2])
 suppressKey(key,'y_neg_limit',[1e-13,1e2])
 suppressKey(key,'dl_save_name',"dl-s8-l1648-"+key+".png")
 suppressKey(key,'em_save_name',"em-s8-l1648-"+key+".png")
 suppressKey(key,'fn_save_name',"fn-s8-l1648-"+key+".png")
