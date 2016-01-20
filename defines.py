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
do_baryon=True
do_uncorr=False
do_initial=True
do_irrep="8"
#do_irrep="8'"
#do_irrep="16"

## -- other parameters
if do_irrep == "8":
  lkey=[
   'G11','G12','G13','G15',#'G16',
   'G21','G22','G23','G25',#'G26',
   'G31','G32','G33','G35',#'G36',
   'G51','G52','G53','G55',#'G56',
   #'G61','G62','G63','G65','G66',
   'G11s','G12s','G13s','G15s',#'G16s',
   'G21s','G22s','G23s','G25s',#'G26s',
   'G31s','G32s','G33s','G35s',#'G36s',
   'G51s','G52s','G53s','G55s'#,#'G56s',
   #'G61s','G62s','G63s','G65s','G66s'
   ]
elif do_irrep == "8'":
  lkey=[
   'G44','G47',#'G74',
   'G77',
   'G44s', 'G47s','G74s',
   'G77s'
  ]
elif do_irrep == "16":
  lkey=[
   'G22','G24',#'G26',
   'G42','G44',#'G46',
   #'G62','G64',#'G66',
   'G22s','G24s',#'G26s',
   'G42s','G44s',#'G46s',
   #'G62s','G64s','G66s'
   'G32','G33','G34',#'G36',
   'G23','G43',#'G63',
   'G32s','G34s',#'G36s',
   'G23s','G33s','G43s'#,'G63s'

  ]

maxit      =10000   # maximum iterations
svdcut     =None
svdcut     =1e-3
## -- tolerance check does not work if lots of variation from + to -
## -- need to fix
ctol       =None # tolerance for consecutive correlator points

fitargs={}
for key in lkey:
 fitargs[key]={}
def suppressKey(key,tag,line): ## -- ignore errors
 try:
  fitargs[key][tag]=line
 except KeyError:
  pass

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
# 3N 2D / 4N 1D 1?
num_nst_s8=7
num_ost_s8=6
# 0N 2D / 0N 1D 0?
num_nst_s8p=4
num_ost_s8p=3
# 1N 3D / 3N 4D 0?
num_nst_s16=6
num_ost_s16=5

rangeMin=2
rangeMax=13
#
max_chi2=25
min_chi2=-10

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
  model_range = range(rangeMin,rangeMax)
  define_model_s8[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
pass
for key in key_list_s8p:
  model_range = range(rangeMin,rangeMax)
  define_model_s8p[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
pass
for key in key_list_s16:
  model_range = range(rangeMin,rangeMax)
  define_model_s16[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
pass
## -- explicit overriding
#define_model_s8['G11']['tfit'] = range(rangeMin,rangeMaxDiag+1)

## ------
## FROM MAKE_PRIOR.PY
## ------
if do_irrep == "8":
  stab_min_nst=3
  stab_mid_nst=3
  stab_max_nst=13
  stab_min_ost=2
  stab_mid_ost=2
  stab_max_ost=13
  stab_max_states=18
  tmvr_tmax=range(7,14)
  num_nst=num_nst_s8
  num_ost=num_ost_s8
  define_prior=dfp.define_prior_s8
  define_init =dfp.define_init_s8
  define_model=define_model_s8
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s8-l1648-coul-"+key+".png")
   suppressKey(key,'em_save_name',"em-s8-l1648-coul-"+key+".png")
   suppressKey(key,'fn_save_name',"fn-s8-l1648-coul-"+key+".png")
   suppressKey(key,'plottitledl',"")
   suppressKey(key,'plottitlefn',"Fit-normalized Correlator")
elif do_irrep == "8'":
  stab_min_nst=1
  stab_mid_nst=1
  stab_max_nst=7
  stab_min_ost=1
  stab_mid_ost=1
  stab_max_ost=6
  stab_max_states=9
  tmvr_tmax=[3,4]
  num_nst=num_nst_s8p
  num_ost=num_ost_s8p
  define_prior=dfp.define_prior_s8p
  define_init =dfp.define_init_s8p
  define_model=define_model_s8p
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s8p-l1648-coul-"+key+".png")
   suppressKey(key,'em_save_name',"em-s8p-l1648-coul-"+key+".png")
   suppressKey(key,'fn_save_name',"fn-s8p-l1648-coul-"+key+".png")
elif do_irrep == "16":
  stab_min_nst=2
  stab_mid_nst=2
  stab_max_nst=8
  stab_min_ost=2
  stab_mid_ost=2
  stab_max_ost=8
  stab_max_states=14
  num_nst=num_nst_s16
  num_ost=num_ost_s16
  define_prior=dfp.define_prior_s16
  define_init =dfp.define_init_s16
  define_model=define_model_s16
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s16-l1648-coul-"+key+".png")
   suppressKey(key,'em_save_name',"em-s16-l1648-coul-"+key+".png")
   suppressKey(key,'fn_save_name',"fn-s16-l1648-coul-"+key+".png")

for key in lkey:
 suppressKey(key,'y_pos_limit',[1e-13,1e2])
 suppressKey(key,'y_neg_limit',[1e-13,1e2])
if do_irrep == "8":
  #for key in key_list_s8:
  #  suppressKey(key[0],"meff_fit_max",11)
  pass
elif do_irrep == "8'":
  #suppressKey('G44',"meff_fit_max",0)
  pass
elif do_irrep == "16":
  #suppressKey('G23',"meff_fit_max",0)
  pass
pass

