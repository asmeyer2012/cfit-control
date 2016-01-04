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
lkey=['G44']
#lkey=[
# 'G11','G12','G13','G15','G16','G21','G22','G23','G25','G26',
# 'G31','G32','G33','G35','G36','G51','G52','G53','G55','G56',
# 'G61','G62','G63','G65','G66']
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
## --
num_nst_s8=8
num_ost_s8=6
num_nst_s8p=2
num_ost_s8p=1
num_nst_s16=8
num_ost_s16=6

rangeMin=2
rangeMaxDiag=12
rangeMaxOffD=10
max_chi2=3

define_model_s8={}
define_model_s8p={}
define_model_s16={}
## -- construct models quickly using loops
key_list_s8 = list()
key_list_s8p = list()
key_list_s16 = list()
for sc in ['1','2','3','5','6']:
 for sk in ['1','2','3','5','6']:
  key_list_s8.append(('G'+sc+sk,sc,sk))
  key_list_s8.append(('G'+sc+sk+'s',sc,'s'+sk))
pass
for sc in ['4','7']:
 for sk in ['4','7']:
  key_list_s8p.append(('G'+sc+sk,sc,sk))
  key_list_s8p.append(('G'+sc+sk+'s',sc,'s'+sk))
pass
for sc in ['2','3','4','6']:
 for sk in ['2','3','4','6']:
  key_list_s16.append(('G'+sc+sk,sc,sk))
  key_list_s16.append(('G'+sc+sk+'s',sc,'s'+sk))
pass
for key in key_list_s8:
  define_model_s8[key[0]]={\
   'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxDiag), 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
pass
for key in key_list_s8p:
  define_model_s8p[key[0]]={\
   'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxDiag), 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
pass
for key in key_list_s16:
  define_model_s16[key[0]]={\
   'tdata':range(cor_len), 'tfit':range(rangeMin,rangeMaxDiag), 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
pass

## ------
## FROM MAKE_PRIOR.PY
## ------
num_nst=num_nst_s8p
num_ost=num_ost_s8p
define_prior=dfp.define_prior_s8p
define_init =dfp.define_init_s8p
define_model=define_model_s8p

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
