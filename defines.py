from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
import meta_data
import gvar             as gv
import util_funcs       as utf
import define_prior     as dfp
import define_prior_3pt as dfp3

## ------
## FROM CONTROL.PY
## ------
do_makedata=False
do_makedata_3pt=False
do_db=False
do_default_plot=False
do_plot=True
do_baryon=True
do_uncorr=False
do_initial=True
#do_irrep="8"
do_irrep="8'"
#do_irrep="16"
do_symm="s"
#do_symm="m"
do_2pt=False
do_3pt=False

## ------
## FROM MAKE_MODELS.PY
## ------
cor_len=48 # parse this from filename?
## --

# 8  = 3N 2D / 4N 1D 1?
# 8' = 0N 2D / 0N 1D 0?
# 16 = 1N 3D / 3N 4D 0?
num_nst_s8=7
num_ost_s8=6
num_nst_s8p=5
num_ost_s8p=3
num_nst_s16=6
num_ost_s16=5

## -- control size of matrices here!
num_n3_s8 =2
num_o3_s8 =2
num_n3_s8p=3
num_o3_s8p=2
num_n3_s16=2
num_o3_s16=2

rangeMin=2
rangeMax=9
#
max_chi2=25
min_chi2=-10
#
current_list = dfp3.current_list
tsep_list = dfp3.tsep_list

## -- other parameters
if do_irrep == "8":
  lkey=[
   's61','s62','s63','s65','s66',
   's11','s12','s13','s15','s16',
   's21','s22','s23','s25','s26',
   's31','s32','s33','s35','s36',
   's51','s52','s53','s55','s56',
   ]
  lkey3 = list()
  for cur in current_list:
   for key in lkey:
    for tsep in tsep_list:
     lkey3.append(cur+key+'t'+str(tsep))
elif do_irrep == "8'":
  lkey=[
   's44','s47', 's74', 's77'
  ]
  lkey3 = list()
  for cur in current_list:
   for key in lkey:
    for tsep in tsep_list:
     lkey3.append(cur+key+'t'+str(tsep))
elif do_irrep == "16":
  lkey=[
   's22','s23','s24','s26',
   's32','s33','s36',
   's34','s43', # noisy
   's42','s44','s46',
   's62','s63','s64','s66'
  ]
  lkey3 = list()
  for cur in current_list:
   for key in lkey:
    for tsep in tsep_list:
     lkey3.append(cur+key+'t'+str(tsep))
pass

maxit      =10000   # maximum iterations
svdcut     =None
svdcut     =1e-3
ctol       =None # tolerance for consecutive correlator points, depricated

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
config   ='l3248f211b580m002426m06730m8447'
#campaign ='gb2pt_l1648f211b580m013m065m838'
#campaign ='gb3pt_full'
campaign ='axial_gb3pt_1'
DBEngine = create_engine('sqlite:///'+dbpath+config+campaign+'.sqlite')
Session  = sessionmaker(bind=DBEngine)
session  = Session()
#
## -- output defines
out_path ='/project/axial/data/fit-in/'
#out_fname='full2pt_s8p'
out_fname='bar2pt.s8'

define_model_s8={}
define_model_s8p={}
define_model_s16={}
define_model3_s8={}
define_model3_s8p={}
define_model3_s16={}
## -- construct models quickly using loops
key_list_s8 = list()
key_list_s8p = list()
key_list_s16 = list()
key_list3_s8 = list()
key_list3_s8p = list()
key_list3_s16 = list()
for sc in ['1','2','3','5','6']:
 for sk in ['1','2','3','5','6']:
  key_list_s8.append(('s'+sc+sk,sc,sk))
  #key_list_s8.append(('s'+sc+sk+'s',sc,'s'+sk))
  for cur in current_list:
   for tsep in tsep_list:
    key_list3_s8.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur))
pass
for sc in ['4','7']:
 for sk in ['4','7']:
  key_list_s8p.append(('s'+sc+sk,sc,sk))
  #key_list_s8p.append(('s'+sc+sk+'s',sc,'s'+sk))
  for cur in current_list:
   for tsep in tsep_list:
    key_list3_s8p.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur))
pass
for sc in ['2','3','4','6']:
 for sk in ['2','3','4','6']:
  key_list_s16.append(('s'+sc+sk,sc,sk))
  #key_list_s16.append(('s'+sc+sk+'s',sc,'s'+sk))
  for cur in current_list:
   for tsep in tsep_list:
    key_list3_s16.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur))
pass

for key in key_list_s8:
  model_range = range(rangeMin,rangeMax)
  define_model_s8[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
  if (key[1] == '1' and key[2] == '3') or (key[1] == '1' and key[2] == '3')\
  or (key[1] == '2' and key[2] == '5') or (key[1] == '5' and key[2] == '2')\
  or (key[1] == '2' and key[2] == '6') or (key[1] == '6' and key[2] == '2'):
   define_model_s8[key[0]]['skey'] = (1.,1.)
pass
for key in key_list3_s8:
  model_range = range(1,key[3]-1)
  define_model3_s8[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,-1.), 'sbkey':(1.,-1.),
   'vnn':key[4]+'nn', 'vno':key[4]+'no', 'von':key[4]+'on', 'voo':key[4]+'oo' }
  if (key[1] == '1' and key[2] == '3') or (key[1] == '1' and key[2] == '3')\
  or (key[1] == '2' and key[2] == '5') or (key[1] == '5' and key[2] == '2')\
  or (key[1] == '2' and key[2] == '6') or (key[1] == '6' and key[2] == '2'):
   define_model3_s8[key[0]]['sakey'] = (1.,1.)
   define_model3_s8[key[0]]['sbkey'] = (1.,1.)
pass

for key in key_list_s8p:
  model_range = range(rangeMin,rangeMax)
  define_model_s8p[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
pass
for key in key_list3_s8p:
  model_range = range(1,key[3]-1)
  define_model3_s8p[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,-1.), 'sbkey':(1.,-1.),
   'vnn':key[4]+'nn', 'vno':key[4]+'no', 'von':key[4]+'on', 'voo':key[4]+'oo' }
pass
#

for key in key_list_s16:
  model_range = range(rangeMin,rangeMax)
  define_model_s16[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,-1.) }
  if (key[1] == '2' and key[2] == '3') or (key[1] == '3' and key[2] == '2')\
  or (key[1] == '2' and key[2] == '4') or (key[1] == '4' and key[2] == '2')\
  or (key[1] == '3' and key[2] == '4') or (key[1] == '4' and key[2] == '3')\
  or (key[1] == '3' and key[2] == '6') or (key[1] == '6' and key[2] == '3')\
  or (key[1] == '4' and key[2] == '6') or (key[1] == '6' and key[2] == '4'):
   define_model_s16[key[0]]['skey'] = (1.,1.)
pass
for key in key_list3_s16:
  model_range = range(1,key[3]-1)
  define_model3_s16[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,-1.), 'sbkey':(1.,-1.),
   'vnn':key[4]+'nn', 'vno':key[4]+'no', 'von':key[4]+'on', 'voo':key[4]+'oo' }
  if (key[1] == '2' and key[2] == '3') or (key[1] == '3' and key[2] == '2')\
  or (key[1] == '2' and key[2] == '4') or (key[1] == '4' and key[2] == '2')\
  or (key[1] == '3' and key[2] == '4') or (key[1] == '4' and key[2] == '3')\
  or (key[1] == '3' and key[2] == '6') or (key[1] == '6' and key[2] == '3')\
  or (key[1] == '4' and key[2] == '6') or (key[1] == '6' and key[2] == '4'):
   define_model3_s16[key[0]]['sakey'] = (1.,1.)
   define_model3_s16[key[0]]['sbkey'] = (1.,1.)
pass

## -- explicit overriding
#define_model_s8['s11']['tfit'] = range(rangeMin,rangeMaxDiag+1)

## ------
## FROM MAKE_PRIOR.PY
## ------
if do_irrep == "8":
  stab_min_nst=3
  stab_mid_nst=3
  stab_max_nst=10
  stab_min_ost=2
  stab_mid_ost=2
  stab_max_ost=10
  stab_max_states=15
  tmvr_tmax=range(9,10)
  num_nst=num_nst_s8
  num_ost=num_ost_s8
  define_prior=dfp.define_prior_s8
  define_init =dfp.define_init_s8
  define_model=define_model_s8
  num_nst_3pt=num_n3_s8
  num_ost_3pt=num_o3_s8
  define_prior_3pt=dfp3.define_prior3_s8
  define_init_3pt =dfp3.define_init3_s8
  define_model_3pt=define_model3_s8
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s8-l1648-coul-"+key+".pdf")
   suppressKey(key,'em_save_name',"em-s8-l1648-coul-"+key+".pdf")
   suppressKey(key,'fn_save_name',"fn-s8-l1648-coul-"+key+".pdf")
   suppressKey(key,'plottitledl',"")
   suppressKey(key,'plottitlefn',"")
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
  num_nst_3pt=num_n3_s8p
  num_ost_3pt=num_o3_s8p
  define_prior_3pt=dfp3.define_prior3_s8p
  define_init_3pt =dfp3.define_init3_s8p
  define_model_3pt=define_model3_s8p
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s8p-l1648-coul-"+key+".pdf")
   suppressKey(key,'em_save_name',"em-s8p-l1648-coul-"+key+".pdf")
   suppressKey(key,'fn_save_name',"fn-s8p-l1648-coul-"+key+".pdf")
elif do_irrep == "16":
  stab_min_nst=2
  stab_mid_nst=2
  stab_max_nst=8
  stab_min_ost=2
  stab_mid_ost=2
  stab_max_ost=8
  stab_max_states=14
  tmvr_tmax=range(9,10)
  num_nst=num_nst_s16
  num_ost=num_ost_s16
  define_prior=dfp.define_prior_s16
  define_init =dfp.define_init_s16
  define_model=define_model_s16
  num_nst_3pt=num_n3_s16
  num_ost_3pt=num_o3_s16
  define_prior_3pt=dfp3.define_prior3_s16
  define_init_3pt =dfp3.define_init3_s16
  define_model_3pt=define_model3_s16
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s16-l1648-coul-"+key+".pdf")
   suppressKey(key,'em_save_name',"em-s16-l1648-coul-"+key+".pdf")
   suppressKey(key,'fn_save_name',"fn-s16-l1648-coul-"+key+".pdf")
   suppressKey(key,'plottitledl',"")
   suppressKey(key,'plottitlefn',"")

for key in lkey:
 suppressKey(key,'y_pos_limit',[1e-13,1e2])
 suppressKey(key,'y_neg_limit',[1e-13,1e2])
if do_irrep == "8":
  for key in key_list_s8:
    suppressKey(key[0],"meff_fit_max",13)
  pass
elif do_irrep == "8'":
  for key in key_list_s8p:
    #suppressKey(key[0],"meff_fit_min",10)
    suppressKey(key[0],"meff_fit_max",13)
  pass
elif do_irrep == "16":
  for key in key_list_s16:
    suppressKey(key[0],"meff_fit_max",13)
  pass
pass

