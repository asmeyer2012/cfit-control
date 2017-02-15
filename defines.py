from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
import meta_data
import gvar             as gv
import util_funcs       as utf
import define_prior     as dfp
import define_prior_3pt as dfp3
import define_prior_advanced as dfpa

## ------
## FROM CONTROL.PY
## ------
do_makedata=False
do_makedata_3pt=False
do_db=False
do_default_plot=False
do_plot=False
do_plot_terminal=True
do_plot_file=True
do_baryon=True
#do_uncorr=False
do_sn_minimize=False
do_initial=True
do_init2=True
do_init3=True
do_mock=False
do_v_symmetric=dfp3.do_v_symmetric
#do_irrep="8'"
do_irrep="8"
#do_irrep="16"
do_symm="s"
#do_symm="m"
do_2pt=False
do_3pt=True

## ------
## FROM MAKE_MODELS.PY
## ------
cor_len=48 # parse this from filename?
## --

num_nst_s8p=3
num_ost_s8p=2
num_nst_s8=10
num_ost_s8=10
num_nst_s16=9
num_ost_s16=9

## -- control size of matrices here!
##    symmetric puts a restriction that 3pt #states = 2pt #states
if do_v_symmetric:
 #num_n3_s8p=min(3,num_nst_s8p)
 #num_o3_s8p=min(4,num_ost_s8p)
 num_n3_s8p=num_nst_s8p
 num_o3_s8p=num_ost_s8p
 num_n3_s8 =num_nst_s8
 num_o3_s8 =num_ost_s8
 num_n3_s16=num_nst_s16
 num_o3_s16=num_ost_s16
else:
 num_n3_s8p=min(2,num_nst_s8p)
 num_o3_s8p=min(3,num_ost_s8p)
 num_n3_s8 =min(6,num_nst_s8)
 num_o3_s8 =min(5,num_ost_s8)
 num_n3_s16=min(5,num_nst_s16)
 num_o3_s16=min(5,num_ost_s16)

#rangeMin=2
#rangeMax=12
rangeMin=2
rangeMax=9
#rangeMin=5
#rangeMax=10
mesonAvgMin=12
mesonAvgMax=18
#
max_chi2=25
min_chi2=-10
#
current_list = dfp3.current_list
current_key = dfp3.current_key
tsep_list = dfp3.tsep_list

## -- other parameters
if do_irrep == "8":
  lkey=[
   's11','s12','s13','s15','s16',
   's21','s22','s23','s25','s26',
   's31','s32','s33','s35','s36',
   's51','s52','s53','s55','s56',
   's61','s62','s63','s65','s66'
   ]
  lkey3 = list()
  nlen = dfp3.nlen8
  olen = dfp3.olen8
  for cur in current_key:
   for key in lkey:
    for tsep in tsep_list:
     if not(cur+key+'t'+str(tsep) in lkey3):
      lkey3.append(cur+key+'t'+str(tsep))

elif do_irrep == "8'":
  lkey=[
   's44','s47',
   's74','s77'
  ]
  lkey3 = list()
  nlen = dfp3.nlen8p
  olen = dfp3.olen8p
  for cur in current_key:
   for key in lkey:
    for tsep in tsep_list:
     if not(cur+key+'t'+str(tsep) in lkey3):
      lkey3.append(cur+key+'t'+str(tsep))

elif do_irrep == "16":
  lkey=[
   's22','s23','s24','s26',
   's32','s33','s34','s36',
   's42','s43','s44','s46',
   's62','s63','s64','s66'
  ]
  lkey3 = list()
  nlen = dfp3.nlen16
  olen = dfp3.olen16
  for cur in current_key:
   for key in lkey:
    for tsep in tsep_list:
     if not(cur+key+'t'+str(tsep) in lkey3):
      lkey3.append(cur+key+'t'+str(tsep))
pass

## -- TODO: spectrum only test
if do_mock or False:
 lkey3 = list()

maxit      =10000   # maximum iterations
#svdcut     =None
svdcut     =1e-3
ctol       =None # tolerance for consecutive correlator points, depricated

fitargs={}
for key in lkey:
 fitargs[key]={}
for key in lkey3:
 tkey = 't'.join(key.split('t')[:-1])
 fitargs[key]={}
 fitargs[tkey]={}
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
## FROM PLOT_CORR_EFFECTIVE_MASS_CHECK.PY
## ------
ec_reference_lines = [.71,.82,.91]

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
define_modela_s8={}
define_modela_s8p={}
define_modela_s16={}
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
  for cur,ckey in zip(current_list,current_key):
   for tsep in tsep_list:
    #key_list3_s8.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
    key_list3_s8.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
pass
for sc in ['4','7']:
 for sk in ['4','7']:
  key_list_s8p.append(('s'+sc+sk,sc,sk))
  #key_list_s8p.append(('s'+sc+sk+'s',sc,'s'+sk))
  for cur,ckey in zip(current_list,current_key):
   for tsep in tsep_list:
    #key_list3_s8p.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
    key_list3_s8p.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
pass
for sc in ['2','3','4','6']:
 for sk in ['2','3','4','6']:
  key_list_s16.append(('s'+sc+sk,sc,sk))
  #key_list_s16.append(('s'+sc+sk+'s',sc,'s'+sk))
  for cur,ckey in zip(current_list,current_key):
   for tsep in tsep_list:
    #key_list3_s16.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
    key_list3_s16.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
pass

if dfp3.do_v_symmetric: ## -- if symmetric, use same string for both
 von_str = 'no'
else:
 von_str = 'on'
for key in key_list_s8:
  model_range = range(rangeMin,rangeMax)
  define_model_s8[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,1.) }
 # if (key[1] == '1' and key[2] == '3') or (key[1] == '1' and key[2] == '3')\
 # or (key[1] == '2' and key[2] == '5') or (key[1] == '5' and key[2] == '2')\
 # or (key[1] == '2' and key[2] == '6') or (key[1] == '6' and key[2] == '2'):
 #  define_model_s8[key[0]]['skey'] = (1.,-1.)
pass
for key in key_list3_s8:
  model_range = range(1,key[3])
  define_model3_s8[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,1.), 'sbkey':(1.,1.),
   'vnn':key[5]+'nn', 'vno':key[5]+'no', 'von':key[5]+von_str, 'voo':key[5]+'oo',
   'symmetric_V':dfp3.do_v_symmetric }
  define_modela_s8[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,1.), 'sbkey':(1.,1.), 'gn':key[5]+'gn','go':key[5]+'go',
   'vnn':key[5]+'nn', 'vno':key[5]+'no', 'von':key[5]+von_str, 'voo':key[5]+'oo',
   'symmetric_V':dfp3.do_v_symmetric }
  #if (key[1] == '1' and key[2] == '3') or (key[1] == '1' and key[2] == '3')\
  #or (key[1] == '2' and key[2] == '5') or (key[1] == '5' and key[2] == '2')\
  #or (key[1] == '2' and key[2] == '6') or (key[1] == '6' and key[2] == '2'):
  # define_model3_s8[key[0]]['sakey'] = (1.,-1.)
  # define_model3_s8[key[0]]['sbkey'] = (1.,-1.)
pass

for key in key_list_s8p:
  model_range = range(rangeMin,rangeMax)
  define_model_s8p[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,1.) }
  ## -- only 77 is fixed
pass
for key in key_list3_s8p:
  model_range = range(1,key[3])
  define_model3_s8p[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,1.), 'sbkey':(1.,1.),
   'vnn':key[5]+'nn', 'vno':key[5]+'no', 'von':key[5]+von_str, 'voo':key[5]+'oo',
   'symmetric_V':dfp3.do_v_symmetric }
  define_modela_s8p[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,1.), 'sbkey':(1.,1.), 'gn':key[5]+'gn', 'go':key[5]+'go',
   'vnn':key[5]+'nn', 'vno':key[5]+'no', 'von':key[5]+von_str, 'voo':key[5]+'oo',
   'symmetric_V':dfp3.do_v_symmetric }
  ## -- only 44 has freedom in both sakey and sbkey;
  ##    for others, choice of sakey fixes sbkey
  #if (key[1] == '4' and key[2] == '4'):
  # define_model3_s8p[key[0]]['sbkey'] = (1.,1.)
  # pass
  #if (key[1] == '4' and key[2] == '7'):
  # #define_model3_s8p[key[0]]['sbkey'] = (-1.,1.)
  # pass
  #if (key[1] == '7' and key[2] == '4'):
  # #define_model3_s8p[key[0]]['sbkey'] = (-1.,1.)
  # pass
  #if (key[1] == '7' and key[2] == '7'):
  # #define_model3_s8p[key[0]]['sbkey'] = (-1.,1.)
  # pass
pass
#

for key in key_list_s16:
  model_range = range(rangeMin,rangeMax)
  define_model_s16[key[0]]={\
   'tdata':range(cor_len), 'tfit':model_range, 'tp':-cor_len,\
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),\
   'ekey':('En','Eo'), 'skey':(1.,1.) }
  #if (key[1] == '4' and key[2] == '4'):
  #or (key[1] == '4' and key[2] == '6') or (key[1] == '6' and key[2] == '4'):
  #or (key[1] == '3' and key[2] == '6') or (key[1] == '6' and key[2] == '3'):
  # or (key[1] == '3' and key[2] == '2')\
  #or (key[1] == '2' and key[2] == '4') or (key[1] == '4' and key[2] == '2')\
  #if (key[1] == '3' and key[2] == '4') or (key[1] == '4' and key[2] == '3'):
  # define_model_s16[key[0]]['skey'] = (1.,-1.)
pass
for key in key_list3_s16:
  model_range = range(1,key[3])
  define_model3_s16[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,1.), 'sbkey':(1.,1.),
   'vnn':key[5]+'nn', 'vno':key[5]+'no', 'von':key[5]+von_str, 'voo':key[5]+'oo',
   'symmetric_V':dfp3.do_v_symmetric }
  define_modela_s16[key[0]]={
   'tdata':range(cor_len), 'tfit':model_range, 'T':key[3], 
   'tpa':-cor_len, 'tpb':-cor_len,
   'akey':('c'+key[1]+'n','c'+key[1]+'o'), 'bkey':('k'+key[2]+'n','k'+key[2]+'o'),
   'eakey':('En','Eo'), 'ebkey':('En','Eo'),
   'sakey':(1.,1.), 'sbkey':(1.,1.), 'gn':key[5]+'gn', 'go':key[5]+'go',
   'vnn':key[5]+'nn', 'vno':key[5]+'no', 'von':key[5]+von_str, 'voo':key[5]+'oo',
   'symmetric_V':dfp3.do_v_symmetric }
  #if (key[1] == '2' and key[2] == '3') or (key[1] == '3' and key[2] == '2')\
  #or (key[1] == '2' and key[2] == '4') or (key[1] == '4' and key[2] == '2')\
  #or (key[1] == '3' and key[2] == '4') or (key[1] == '4' and key[2] == '3')\
  #or (key[1] == '3' and key[2] == '6') or (key[1] == '6' and key[2] == '3')\
  #or (key[1] == '4' and key[2] == '6') or (key[1] == '6' and key[2] == '4'):
  # define_model3_s16[key[0]]['sakey'] = (1.,1.)
  # define_model3_s16[key[0]]['sbkey'] = (1.,1.)
pass

## -- explicit overriding
#define_model_s8['s11']['tfit'] = range(rangeMin,rangeMaxDiag+1)

## ------
## FROM MAKE_PRIOR.PY
## ------
if do_irrep == "8":
  stab_max_states=20
  stab_min_nst=5
  stab_mid_nst=5
  stab_max_nst=10
  stab_min_ost=4
  stab_mid_ost=4
  stab_max_ost=10
  #nost_3pt = ((3,2),(3,3),(3,4),(4,4),(4,5),(4,6),(5,5),(6,5),(6,6),(6,7),(6,8),(5,6),(5,7),(5,8),(7,4),(7,5))
  nost_3pt = ((5,5),(6,5),(6,6),(6,7),(6,8),(5,6),(5,7),(5,8),(7,5),(7,6),(7,7),(7,8))
  #nost_3pt = ((1,1),) ## -- test
  plot_n_maxprior = 3
  plot_o_maxprior = 2
  tmvr_tmax=range(9,14)
  num_nst=num_nst_s8
  num_ost=num_ost_s8
  define_prior=dfp.define_prior_s8
  define_init =dfp.define_init_s8
  define_model=define_model_s8
  num_nst_3pt=num_n3_s8
  num_ost_3pt=num_o3_s8
  define_prior_3pt=dfp3.define_prior3_s8
  define_init_3pt =dfp3.define_init3_s8
  define_prior_adv=dfpa.define_prior_s8
  define_model_3pt=define_model3_s8
  define_model_adv=define_modela_s8
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s8p-l3248-coul-"+key+".pdf")
   suppressKey(key,'df_save_name',"df-s8p-l3248-coul-"+key+".pdf")
   suppressKey(key,'em_save_name',"em-s8p-l3248-coul-"+key+".pdf")
   suppressKey(key,'ec_save_name',"ec-s8p-l3248-coul-"+key+".pdf")
   suppressKey(key,'fn_save_name',"fn-s8p-l3248-coul-"+key+".pdf")
   suppressKey(key,'p3_save_name',"p3-s8p-l3248-coul-"+key+".pdf")
   suppressKey(key,'plottitleem',"")
   suppressKey(key,'plottitleec',"")
   suppressKey(key,'plottitledl',"")
   suppressKey(key,'plottitledf',"")
   suppressKey(key,'plottitlefn',"")
  for key in lkey3:
   suppressKey(key,'p3_save_name',"p3-s8p-l3248-coul-"+key+".pdf")
   suppressKey(key,'plottitlep3',"")
   tkey = 't'.join(key.split('t')[:-1])
   suppressKey(tkey,'p3_save_name',"p3-s8p-l3248-coul-"+tkey+".pdf")
   suppressKey(tkey,'plottitlep3',"")

elif do_irrep == "8'":
  stab_min_nst=2
  stab_mid_nst=2
  stab_max_nst=5
  stab_min_ost=2
  stab_mid_ost=2
  stab_max_ost=7
  stab_max_states=9
  nost_3pt = ((1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,2),(3,3))
  plot_n_maxprior = 2
  plot_o_maxprior = 1
  tmvr_tmax=range(9,10)
  num_nst=num_nst_s8p
  num_ost=num_ost_s8p
  define_prior=dfp.define_prior_s8p
  define_init =dfp.define_init_s8p
  define_model=define_model_s8p
  num_nst_3pt=num_n3_s8p
  num_ost_3pt=num_o3_s8p
  define_prior_3pt=dfp3.define_prior3_s8p
  define_init_3pt =dfp3.define_init3_s8p
  define_prior_adv=dfpa.define_prior_s8p
  define_model_3pt=define_model3_s8p
  define_model_adv=define_modela_s8p
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s8m-l3248-coul-"+key+".pdf")
   suppressKey(key,'df_save_name',"df-s8m-l3248-coul-"+key+".pdf")
   suppressKey(key,'em_save_name',"em-s8m-l3248-coul-"+key+".pdf")
   suppressKey(key,'ec_save_name',"ec-s8m-l3248-coul-"+key+".pdf")
   suppressKey(key,'fn_save_name',"fn-s8m-l3248-coul-"+key+".pdf")
   suppressKey(key,'p3_save_name',"p3-s8m-l3248-coul-"+key+".pdf")
   suppressKey(key,'plottitleem',"")
   suppressKey(key,'plottitleec',"")
   suppressKey(key,'plottitledl',"")
   suppressKey(key,'plottitledf',"")
   suppressKey(key,'plottitlefn',"")
  for key in lkey3:
   suppressKey(key,'p3_save_name',"p3-s8m-l3248-coul-"+key+".pdf")
   suppressKey(key,'plottitlep3',"")
   tkey = 't'.join(key.split('t')[:-1])
   suppressKey(tkey,'p3_save_name',"p3-s8m-l3248-coul-"+tkey+".pdf")
   suppressKey(tkey,'plottitlep3',"")

elif do_irrep == "16":
  stab_min_nst=4
  stab_mid_nst=4
  stab_max_nst=8
  stab_min_ost=2
  stab_mid_ost=2
  stab_max_ost=8
  stab_max_states=18
  nost_3pt = ((6,5),(6,6),(6,4),(7,5),(7,6),(5,4),(5,5),(4,5),(4,4))
  plot_n_maxprior = 2
  plot_o_maxprior = 1
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
  define_prior_adv=dfpa.define_prior_s16
  define_model_3pt=define_model3_s16
  define_model_adv=define_modela_s16
  for key in lkey:
   suppressKey(key,'dl_save_name',"dl-s16-l3248-coul-"+key+".pdf")
   suppressKey(key,'df_save_name',"df-s16-l3248-coul-"+key+".pdf")
   suppressKey(key,'em_save_name',"em-s16-l3248-coul-"+key+".pdf")
   suppressKey(key,'ec_save_name',"ec-s16-l3248-coul-"+key+".pdf")
   suppressKey(key,'fn_save_name',"fn-s16-l3248-coul-"+key+".pdf")
   suppressKey(key,'p3_save_name',"p3-s16-l3248-coul-"+key+".pdf")
   suppressKey(key,'plottitleem',"")
   suppressKey(key,'plottitleec',"")
   suppressKey(key,'plottitledl',"")
   suppressKey(key,'plottitledf',"")
   suppressKey(key,'plottitlefn',"")
  for key in lkey3:
   suppressKey(key,'p3_save_name',"p3-s16-l3248-coul-"+key+".pdf")
   suppressKey(key,'plottitlep3',"")
   tkey = 't'.join(key.split('t')[:-1])
   suppressKey(tkey,'p3_save_name',"p3-s16-l3248-coul-"+tkey+".pdf")
   suppressKey(tkey,'plottitlep3',"")

for key in lkey:
 #suppressKey(key,'y_pos_limit',[1e-3,1e2])
 #suppressKey(key,'y_neg_limit',[1e-3,1e2])
 suppressKey(key,'y_pos_limit',[1e-5,1e2])
 suppressKey(key,'y_neg_limit',[1e-5,1e2])
if do_irrep == "8":
  for key in key_list_s8:
    suppressKey(key[0],"meff_do_fold",True)
    suppressKey(key[0],"meff_fit_min",3)
    suppressKey(key[0],"meff_fit_max",9)
    if not(do_plot_terminal):
      suppressKey(key[0],"to_terminal",False)
    if do_plot_file:
      suppressKey(key[0],"to_file",True)
  for key in key_list3_s8:
    tkey = 't'.join(key[0].split('t')[:-1]) ## -- for 3-point stacked plots
    #suppressKey(key[0],"y_scale",[-0.2,0.6])
    #suppressKey(tkey,"y_scale",[-0.2,0.6])
    suppressKey(key[0],"y_scale",[-0.03,0.05])
    suppressKey(tkey,"y_scale",[-0.03,0.05])
    #if (int(key[1]) == 1 and int(key[2]) == 1):
    # suppressKey(key[0],"y_scale",[0,1.5])
    # suppressKey(tkey,"y_scale",[0,1.5])
    suppressKey(key[0],"yaxistitle",r"$\beta C_{ij}(t,T)$")
    suppressKey(tkey,"yaxistitle",r"$\beta C_{ij}(t,T)$")
    suppressKey(key[0],"p3_do_fit",False)
    suppressKey(tkey,"p3_do_fit",False)
    if not(do_plot_terminal):
      suppressKey(key[0],"to_terminal",False)
      suppressKey(tkey,"to_terminal",False)
    if do_plot_file:
      suppressKey(key[0],"to_file",True)
      suppressKey(tkey,"to_file",True)
  pass
elif do_irrep == "8'":
  for key in key_list_s8p:
    suppressKey(key[0],"meff_do_fold",True)
    suppressKey(key[0],"meff_fit_min",2)
    suppressKey(key[0],"meff_fit_max",7)
    if not(do_plot_terminal):
      suppressKey(key[0],"to_terminal",False)
    if do_plot_file:
      suppressKey(key[0],"to_file",True)
  for key in key_list3_s8p:
    tkey = 't'.join(key[0].split('t')[:-1]) ## -- for 3-point stacked plots
    #suppressKey(key[0],"y_scale",[-0.1,0.1]) #axax
    #suppressKey(key[0],"y_scale",[-0.1,0.1]) #axp
    suppressKey(key[0],"p3_do_fit",True)
    suppressKey(tkey,"p3_do_fit",True)
    suppressKey(key[0],"yaxistitle",r"$\beta C_{ij}(t,T)$")
    suppressKey(tkey,"yaxistitle",r"$\beta C_{ij}(t,T)$")
    if not(do_plot_terminal):
      suppressKey(key[0],"to_terminal",False)
      suppressKey(tkey,"to_terminal",False)
    if do_plot_file:
      suppressKey(key[0],"to_file",True)
      suppressKey(tkey,"to_file",True)
  pass
elif do_irrep == "16":
  for key in key_list_s16:
    suppressKey(key[0],"meff_fit_max",13)
    if not(do_plot_terminal):
      suppressKey(key[0],"to_terminal",False)
    if do_plot_file:
      suppressKey(key[0],"to_file",True)
  for key in key_list3_s8p:
    tkey = 't'.join(key[0].split('t')[:-1]) ## -- for 3-point stacked plots
    if not(do_plot_terminal):
      suppressKey(key[0],"to_terminal",False)
      suppressKey(tkey,"to_terminal",False)
    if do_plot_file:
      suppressKey(key[0],"to_file",True)
      suppressKey(tkey,"to_file",True)
  pass
pass

