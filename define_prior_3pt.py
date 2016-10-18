import gvar         as gv
import numpy        as np
import util_funcs   as utf
import define_prior as dp

do_v_symmetric = True

## -- HISQ a=0.15 l3248 physical
## -- prior mass splittings

def curkey(key):
  return (key+'nn',key+'no',key+'on',key+'oo')
#current_list = ['ss']
#current_list = ['v4v4']
current_list = ['axax','ayay','azaz']
#current_list = ['vxvx','vyvy','vzvz']
#current_list = ['axax','ayay']
#current_list = ['ayay']
current_key = current_list
current_key = ['aiai','aiai','aiai']
tsep_list = [6,7]

## -- used if do_init is defined in defines.py
define_init3_s8={}
define_init3_s8p={}
define_init3_s16={}

## -- define prior objects to pass to defines.py if requested
define_prior3_s8={}
define_prior3_s8p={}
define_prior3_s16={}

## -- number of states to treat as real values
num_n3_s8 =5 #3N+2D +1radial
num_o3_s8 =7 #
num_n3_s8p=2 #0N+2D +1radial
num_o3_s8p=3 #
num_n3_s16=4 #1N+3D
num_o3_s16=1 #
Vnom  = 1     # amplitude guess for actual states (unknown sign)
xVnom = 1e-3  # amplitude guess for continuum-forbidden off-diagonal states
oVnom = 1     # amplitude guess for continuum-allowed off-diagonal states

nkey_s8 = dp.nkey_s8
okey_s8 = dp.okey_s8
nkey_s8p= dp.nkey_s8p
okey_s8p= dp.okey_s8p
nkey_s16= dp.nkey_s16
okey_s16= dp.okey_s16

vkey3_s8 = tuple()
for cur in current_key:
 vkey3_s8 += curkey(cur)
vkey3_s8p= vkey3_s8
vkey3_s16= vkey3_s8
#print vkey3_s8p
## -- match initial guesses/priors with 2-point functions for overlaps,energies
for key in nkey_s8+okey_s8:
  define_init3_s8[key] =dp.define_init_s8[key]
  define_prior3_s8[key]=dp.define_prior_s8[key]
for key in nkey_s8p+okey_s8p:
  define_init3_s8p[key] =dp.define_init_s8p[key]
  define_prior3_s8p[key]=dp.define_prior_s8p[key]
for key in nkey_s16+okey_s16:
  define_init3_s16[key] =dp.define_init_s16[key]
  define_prior3_s16[key]=dp.define_prior_s16[key]

for cur in current_key:
 # S8
 define_init3_s8 [cur+'nn']=[[Vnom]*num_n3_s8  + [xVnom]*10]*(num_n3_s8 +10)\
   + [[xVnom]*(num_n3_s8 +10)]*10
 define_init3_s8 [cur+'no']=[[Vnom]*num_n3_s8  + [xVnom]*10]*(num_o3_s8 +10)\
   + [[xVnom]*(num_n3_s8 +10)]*10
 define_init3_s8 [cur+'on']=[[Vnom]*num_o3_s8  + [xVnom]*10]*(num_n3_s8 +10)\
   + [[xVnom]*(num_o3_s8 +10)]*10
 define_init3_s8 [cur+'oo']=[[Vnom]*num_o3_s8  + [xVnom]*10]*(num_o3_s8 +10)\
   + [[xVnom]*(num_o3_s8 +10)]*10
 # S8'
 define_init3_s8p[cur+'nn']=[[Vnom]*num_n3_s8p + [xVnom]*10]*(num_n3_s8p+10)\
   + [[xVnom]*(num_n3_s8p+10)]*10
 define_init3_s8p[cur+'no']=[[Vnom]*num_n3_s8p + [xVnom]*10]*(num_o3_s8p+10)\
   + [[xVnom]*(num_n3_s8p+10)]*10
 define_init3_s8p[cur+'on']=[[Vnom]*num_o3_s8p + [xVnom]*10]*(num_n3_s8p+10)\
   + [[xVnom]*(num_o3_s8p+10)]*10
 define_init3_s8p[cur+'oo']=[[Vnom]*num_o3_s8p + [xVnom]*10]*(num_o3_s8p+10)\
   + [[xVnom]*(num_o3_s8p+10)]*10
 # S16
 define_init3_s16[cur+'nn']=[[Vnom]*num_n3_s16 + [xVnom]*10]*(num_n3_s16+10)\
   + [[xVnom]*(num_n3_s16+10)]*10
 define_init3_s16[cur+'no']=[[Vnom]*num_n3_s16 + [xVnom]*10]*(num_o3_s16+10)\
   + [[xVnom]*(num_n3_s16+10)]*10
 define_init3_s16[cur+'on']=[[Vnom]*num_o3_s16 + [xVnom]*10]*(num_n3_s16+10)\
   + [[xVnom]*(num_o3_s16+10)]*10
 define_init3_s16[cur+'oo']=[[Vnom]*num_o3_s16 + [xVnom]*10]*(num_o3_s16+10)\
   + [[xVnom]*(num_o3_s16+10)]*10

nkey3_s8 = nkey_s8
okey3_s8 = okey_s8
nkey3_s8p = nkey_s8p
okey3_s8p = okey_s8p
nkey3_s16 = nkey_s16
okey3_s16 = okey_s16
#vkey3_s8 = tuple()
#vkey3_s8p= tuple()
#vkey3_s16= tuple()
#for cur in current_key:
# vkey3_s8 += curkey(cur)
# vkey3_s8p+= curkey(cur)
# vkey3_s16+= curkey(cur)

## -- S8
#print vkey3_s8p
define_prior3_s8['nkey'] = nkey3_s8
define_prior3_s8['okey'] = okey3_s8
define_prior3_s8['vkey'] = vkey3_s8
define_prior3_s8p['nkey'] = nkey3_s8p
define_prior3_s8p['okey'] = okey3_s8p
define_prior3_s8p['vkey'] = vkey3_s8p
define_prior3_s16['nkey'] = nkey3_s16
define_prior3_s16['okey'] = okey3_s16
define_prior3_s16['vkey'] = vkey3_s16

Vm  = 0  # current mean
Vs  = 1  # current sdev (different parity entries)
#Vs  = 10 # current sdev (different parity entries)
Vd  = 10 # current sdev (diagonal same-parity entries)
#Vx  = 1  # current sdev (offdiagonal same-parity entries)
Vx  = 10  # current sdev (offdiagonal same-parity entries)
nlen8 = len(define_prior3_s8 ['logEn'])
olen8 = len(define_prior3_s8 ['logEo'])
nlen8p= len(define_prior3_s8p['logEn'])
olen8p= len(define_prior3_s8p['logEo'])
nlen16= len(define_prior3_s16['logEn'])
olen16= len(define_prior3_s16['logEo'])
for cur in current_key:
 define_prior3_s8 [cur+'no'] = gv.gvar([[Vm]*nlen8 ]*olen8 ,[[Vs]*nlen8 ]*olen8)
 if do_v_symmetric:
  #define_prior3_s8 [cur+'nn'] = utf.truncate_upper_triangle(gv.gvar([[Vm]*nlen8 ]*nlen8 ,[[Vx]*nlen8 ]*nlen8),nlen8)
  #define_prior3_s8 [cur+'oo'] = utf.truncate_upper_triangle(gv.gvar([[Vm]*olen8 ]*olen8 ,[[Vx]*olen8 ]*olen8),olen8)
  define_prior3_s8[cur+'on'] = np.transpose(define_prior3_s8[cur+'no'])
  define_prior3_s8[cur+'nn'] = gv.gvar([[Vm]*nlen8]*nlen8,[[Vx]*nlen8]*nlen8)
  define_prior3_s8[cur+'oo'] = gv.gvar([[Vm]*olen8]*olen8,[[Vx]*olen8]*olen8)
  for i in range(nlen8):
   define_prior3_s8[cur+'nn'][i][i] = gv.gvar(Vm,Vx)
  for i in range(olen8):
   define_prior3_s8[cur+'oo'][i][i] = gv.gvar(Vm,Vx)
 else:
  define_prior3_s8 [cur+'nn'] = gv.gvar([[Vm]*nlen8 ]*nlen8 ,[[Vx]*nlen8 ]*nlen8)
  define_prior3_s8 [cur+'oo'] = gv.gvar([[Vm]*olen8 ]*olen8 ,[[Vx]*olen8 ]*olen8)
  define_prior3_s8 [cur+'on'] = gv.gvar([[Vm]*olen8 ]*nlen8 ,[[Vs]*olen8 ]*nlen8)
  ## -- add extra constraints on diagonal entries
  define_prior3_s8 [cur+'nn'][1][1] = define_prior3_s8 [cur+'nn'][0][0]+gv.gvar(0,0.1) 
  define_prior3_s8 [cur+'nn'][2][2] = define_prior3_s8 [cur+'nn'][0][0]+gv.gvar(0,0.1) 
  define_prior3_s8 [cur+'nn'][4][4] = define_prior3_s8 [cur+'nn'][3][3]+gv.gvar(0,0.1) 
  define_prior3_s8 [cur+'nn'][6][6] = define_prior3_s8 [cur+'nn'][5][5]+gv.gvar(0,0.1) 
  define_prior3_s8 [cur+'nn'][7][7] = define_prior3_s8 [cur+'nn'][5][5]+gv.gvar(0,0.1) 
  define_prior3_s8 [cur+'nn'][9][9] = define_prior3_s8 [cur+'nn'][8][8]+gv.gvar(0,0.1) 
  #define_prior3_s8 [cur+'oo'][2][2] = define_prior3_s8 [cur+'oo'][1][1]+gv.gvar(0,0.1) 
  #define_prior3_s8 [cur+'oo'][3][3] = define_prior3_s8 [cur+'oo'][1][1]+gv.gvar(0,0.1) 
  define_prior3_s8 [cur+'oo'][5][5] = define_prior3_s8 [cur+'oo'][4][4]+gv.gvar(0,0.1) 
  define_prior3_s8 [cur+'oo'][6][6] = define_prior3_s8 [cur+'oo'][4][4]+gv.gvar(0,0.1) 
 #for i in range(len(define_prior3_s8[cur+'nn'][0])):
 # define_prior3_s8[cur+'nn'][i][i] = gv.gvar(Vm,Vd)
 # if do_v_symmetric:
 #  for j in range(i,len(define_prior3_s8[cur+'nn'][0])):
 #   define_prior3_s8[cur+'nn'][i][j] = define_prior3_s8[cur+'nn'][j][i]
 #for i in range(len(define_prior3_s8[cur+'oo'][0])):
 # define_prior3_s8[cur+'oo'][i][i] = gv.gvar(Vm,Vd)
 # if do_v_symmetric:
 #  for j in range(i,len(define_prior3_s8[cur+'oo'][0])):
 #   define_prior3_s8[cur+'oo'][i][j] = define_prior3_s8[cur+'oo'][j][i]

 define_prior3_s8p[cur+'no'] = gv.gvar([[Vm]*nlen8p]*olen8p,[[Vs]*nlen8p]*olen8p)
 if do_v_symmetric:
  define_prior3_s8p[cur+'on'] = np.transpose(define_prior3_s8p[cur+'no'])
  define_prior3_s8p[cur+'nn'] = gv.gvar([[Vm]*nlen8p]*nlen8p,[[Vx]*nlen8p]*nlen8p)
  define_prior3_s8p[cur+'oo'] = gv.gvar([[Vm]*olen8p]*olen8p,[[Vx]*olen8p]*olen8p)
  for i in range(nlen8p):
   define_prior3_s8p[cur+'nn'][i][i] = gv.gvar(Vm,Vx)
  for i in range(olen8p):
   define_prior3_s8p[cur+'oo'][i][i] = gv.gvar(Vm,Vx)
  ## -- add extra constraints on diagonal entries
  define_prior3_s8p[cur+'nn'][1][1] = define_prior3_s8p[cur+'nn'][0][0]+gv.gvar(0,0.1) 
  define_prior3_s8p[cur+'nn'][3][3] = define_prior3_s8p[cur+'nn'][2][2]+gv.gvar(0,0.1) 
  define_prior3_s8p[cur+'oo'][2][2] = define_prior3_s8p[cur+'oo'][1][1]+gv.gvar(0,0.1) 
  define_prior3_s8p[cur+'oo'][3][3] = define_prior3_s8p[cur+'oo'][1][1]+gv.gvar(0,0.1) 
  define_prior3_s8p[cur+'oo'][4][4] = define_prior3_s8p[cur+'oo'][1][1]+gv.gvar(0,0.1) 
  ## -- add extra constraints on off-diagonal entries
  #define_prior3_s8p[cur+'nn'][0][1] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'nn'][1][0] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'nn'][2][3] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'nn'][3][2] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][1][2] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][1][3] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][1][4] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][2][1] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][2][3] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][2][4] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][3][1] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][3][2] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][3][4] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][4][1] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][4][2] = gv.gvar(Vm,Vs)
  #define_prior3_s8p[cur+'oo'][4][3] = gv.gvar(Vm,Vs)
 else:
  define_prior3_s8p[cur+'nn'] = gv.gvar([[Vm]*nlen8p]*nlen8p,[[Vx]*nlen8p]*nlen8p)
  define_prior3_s8p[cur+'oo'] = gv.gvar([[Vm]*olen8p]*olen8p,[[Vx]*olen8p]*olen8p)
  define_prior3_s8p[cur+'on'] = gv.gvar([[Vm]*olen8p]*nlen8p,[[Vs]*olen8p]*nlen8p)

 define_prior3_s16[cur+'no'] = gv.gvar([[Vm]*nlen16]*olen16,[[Vs]*nlen16]*olen16)
 if do_v_symmetric:
  define_prior3_s16[cur+'nn'] = gv.gvar([[Vm]*nlen16]*nlen16,[[Vx]*nlen16]*nlen16)
  define_prior3_s16[cur+'oo'] = gv.gvar([[Vm]*olen16]*olen16,[[Vx]*olen16]*olen16)
  for i in range(nlen16):
   define_prior3_s16[cur+'nn'][i][i] = gv.gvar(Vm,Vx)
  for i in range(olen16):
   define_prior3_s16[cur+'oo'][i][i] = gv.gvar(Vm,Vx)
  #define_prior3_s16[cur+'nn'] = utf.truncate_upper_triangle(define_prior3_s16[cur+'nn'],nlen16)
  #define_prior3_s16[cur+'oo'] = utf.truncate_upper_triangle(define_prior3_s16[cur+'oo'],olen16)
  #define_prior3_s16[cur+'nn'] = utf.truncate_upper_triangle(
  # gv.gvar([[Vm]*nlen16]*nlen16,[[Vx]*nlen16]*nlen16),nlen16)
  #define_prior3_s16[cur+'oo'] = utf.truncate_upper_triangle(
  # gv.gvar([[Vm]*olen16]*olen16,[[Vx]*olen16]*olen16),olen16)
  define_prior3_s16[cur+'on'] = np.transpose(define_prior3_s16[cur+'no'])
 else:
  define_prior3_s16[cur+'nn'] = gv.gvar([[Vm]*nlen16]*nlen16,[[Vx]*nlen16]*nlen16)
  define_prior3_s16[cur+'oo'] = gv.gvar([[Vm]*olen16]*olen16,[[Vx]*olen16]*olen16)
  define_prior3_s16[cur+'on'] = gv.gvar([[Vm]*olen16]*nlen16,[[Vs]*olen16]*nlen16)
 #for i in range(len(define_prior3_s16[cur+'nn'][0])):
 # define_prior3_s16[cur+'nn'][i][i] = gv.gvar(Vm,Vd)
 # #for j in range(i,len(define_prior3_s16[cur+'nn'][0])):
 # # define_prior3_s16[cur+'nn'][i][j] = define_prior3_s16[cur+'nn'][j][i]
 #for i in range(len(define_prior3_s16[cur+'oo'][0])):
 # define_prior3_s16[cur+'oo'][i][i] = gv.gvar(Vm,Vd)
 # #for j in range(i,len(define_prior3_s16[cur+'oo'][0])):
 # # define_prior3_s16[cur+'oo'][i][j] = define_prior3_s16[cur+'oo'][j][i]

## -- construct models quickly using loops
key_list3_s8 = list()
key_list3_s8p = list()
key_list3_s16 = list()
log_s8='1'
log_s8p='4'
log_s16='2'
for cur,ckey in zip(current_list,current_key):
 for tsep in tsep_list:
  for sc in ['1','2','3','5','6']:
   for sk in ['1','2','3','5','6']:
    #key_list3_s8.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
    key_list3_s8.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
  pass
  for sc in ['4','7']:
   for sk in ['4','7']:
    #key_list3_s8p.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
    key_list3_s8p.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
  pass
  for sc in ['2','3','4','6']:
   for sk in ['2','3','4','6']:
    #key_list3_s16.append((cur+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
    key_list3_s16.append((ckey+'s'+sc+sk+'t'+str(tsep),sc,sk,tsep,cur,ckey))
  pass

for key in key_list3_s8:
  if key[1] == log_s8:
    logstr1='log'
  else:
    logstr1=''
  try:
    define_prior3_s8[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior3_s8[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior3_s8[logstr1+'c'+key[1]+'o'],
      'k'+key[2]+'n':define_prior3_s8['k'+key[2]+'n'],
      'k'+key[2]+'o':define_prior3_s8['k'+key[2]+'o'],
      'logEn':define_prior3_s8['logEn'],
      'logEo':define_prior3_s8['logEo'] }
    for cur in current_list:
     for tsep in tsep_list:
      define_prior3_s8[key[0]][key[5]+'nn']=define_prior3_s8[key[5]+'nn']
      define_prior3_s8[key[0]][key[5]+'no']=define_prior3_s8[key[5]+'no']
      define_prior3_s8[key[0]][key[5]+'on']=define_prior3_s8[key[5]+'on']
      define_prior3_s8[key[0]][key[5]+'oo']=define_prior3_s8[key[5]+'oo']
  except KeyError:
    continue ## -- key is not defined, don't worry about it
pass
for key in key_list3_s8p:
  if key[1] == log_s8p:
    logstr1='log'
  else:
    logstr1=''
  try:
    define_prior3_s8p[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior3_s8p[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior3_s8p[logstr1+'c'+key[1]+'o'],
      'k'+key[2]+'n':define_prior3_s8p['k'+key[2]+'n'],
      'k'+key[2]+'o':define_prior3_s8p['k'+key[2]+'o'],
      'logEn':define_prior3_s8p['logEn'],
      'logEo':define_prior3_s8p['logEo'] }
    define_prior3_s8p[key[0]][key[5]+'nn']=define_prior3_s8p[key[5]+'nn']
    define_prior3_s8p[key[0]][key[5]+'no']=define_prior3_s8p[key[5]+'no']
    define_prior3_s8p[key[0]][key[5]+'on']=define_prior3_s8p[key[5]+'on']
    define_prior3_s8p[key[0]][key[5]+'oo']=define_prior3_s8p[key[5]+'oo']
  except KeyError:
    continue ## -- key is not defined, don't worry about it
pass
for key in key_list3_s16:
  if key[1] == log_s16:
    logstr1='log'
  else:
    logstr1=''
  try:
    define_prior3_s16[key[0]]=\
     {logstr1+'c'+key[1]+'n':define_prior3_s16[logstr1+'c'+key[1]+'n'],
      logstr1+'c'+key[1]+'o':define_prior3_s16[logstr1+'c'+key[1]+'o'],
      'k'+key[2]+'n':define_prior3_s16['k'+key[2]+'n'],
      'k'+key[2]+'o':define_prior3_s16['k'+key[2]+'o'],
      'logEn':define_prior3_s16['logEn'],
      'logEo':define_prior3_s16['logEo'] }
    for cur in current_list:
     for tsep in tsep_list:
      define_prior3_s16[key[0]][key[5]+'nn']=define_prior3_s16[key[5]+'nn']
      define_prior3_s16[key[0]][key[5]+'no']=define_prior3_s16[key[5]+'no']
      define_prior3_s16[key[0]][key[5]+'on']=define_prior3_s16[key[5]+'on']
      define_prior3_s16[key[0]][key[5]+'oo']=define_prior3_s16[key[5]+'oo']
  except KeyError:
    continue ## -- key is not defined, don't worry about it
pass

## -- end

