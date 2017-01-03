import gvar as gv
import defines as df
import make_prior as mp
import make_prior_advanced as mpa
import numpy as np
import os
import importlib

def load_dict_from_fit_file_3pt(directory,filename):
 #initdir = os.getcwd()
 #print initdir,filename
 #os.chdir(directory)
 #print os.getcwd()
 #infile = __import__(filename) ## weird behavior
 #infile = __import__('fit-stability.'+filename) ## not working
 #rdict = infile.init_val_import
 #os.chdir(initdir)
 initdir = os.getcwd()
 os.chdir(directory)
 #print os.getcwd(),filename
 infile = importlib.import_module(filename,'init_val_import') ## still weird behavior
 rdict = infile.init_val_import
 os.chdir(initdir)
 return rdict

#def make_init_from_fit_file_3pt(models,filename,nst=-1,ost=-1,n3st=-1,o3st=-1):
# init = {}
# infit = __import__(filename)
# nn = nst
# no = ost
# if nn < 0:
#  nn = df.num_nst
# if no < 0:
#  no = df.num_ost
# nn3 = n3st
# no3 = o3st
# if nn3 < 0:
#  nn3 = df.num_nst_3pt
# if no3 < 0:
#  no3 = df.num_ost_3pt
# 
# for model in models:
#  skey=model.all_datatags[0]
#
#  listpkey = list()
#  for pkey in df.define_prior:
#   listpkey.append(pkey)
#  for pkey in df.define_prior_3pt:
#   listpkey.append(pkey)
#  for pkey in listpkey:
#   #print pkey
#   if pkey in init:
#    continue ## -- no double counting
#   if pkey in infit.init_val_import:
#    ## -- not sensitive to number of entries as long as there are more than needed
#    try:
#     init[pkey] = df.define_init_3pt[pkey]
#    except KeyError:
#     init[pkey] = df.define_init[pkey]
#
#    if pkey[-2:] == 'nn':
#     ## -- if entries missing, fill in blanks
#     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
#      for j,y in zip(range(len(x)),x):
#       init[pkey][i][j] = y.mean
#     init[pkey] = np.resize(df.define_init_3pt[pkey],(nn3,nn3))
#    elif pkey[-2:] == 'no':
#     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
#      for j,y in zip(range(len(x)),x):
#       init[pkey][i][j] = y.mean
#     init[pkey] = np.resize(df.define_init_3pt[pkey],(nn3,no3))
#    elif pkey[-2:] == 'on':
#     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
#      for j,y in zip(range(len(x)),x):
#       init[pkey][i][j] = y.mean
#     init[pkey] = np.resize(df.define_init_3pt[pkey],(no3,nn3))
#    elif pkey[-2:] == 'oo':
#     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
#      for j,y in zip(range(len(x)),x):
#       init[pkey][i][j] = y.mean
#     init[pkey] = np.resize(df.define_init_3pt[pkey],(no3,no3))
#     ## -- 
#    elif pkey[-1] == 'n':
#     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
#      init[pkey][i] = x.mean
#     init[pkey] = df.define_init_3pt[pkey][:nn]
#    elif pkey[-1] == 'o':
#     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
#      init[pkey][i] = x.mean
#     init[pkey] = df.define_init_3pt[pkey][:no]
#
#   else:
#    #print "key",pkey,"missing from imported dictionary, using default"
#    pass
# return init

def make_adv_init_from_fit_file_3pt(models,filename,nst=-1,ost=-1,n3st=-1,o3st=-1,
  fresh_overlap=False,fresh_amplitude=True):
 init = {}
 infit = __import__(filename)
 nn = nst
 no = ost
 if nn < 0:
  nn = df.num_nst
 if no < 0:
  no = df.num_ost
 if n3st < 0:
  nn3 = df.num_nst_3pt
 else:
  nn3 = n3st
 if o3st < 0:
  no3 = df.num_ost_3pt
 else:
  no3 = o3st

 ## -- save a list of keys for quick reference
 klst = tuple() ## all keys
 glst = tuple() ## diagonal terms only
 olst = tuple() ## overlaps only
 for model in models:
  try:
   for item in [model.dEa,model.dEb,model.a,model.b]:
    klst += tuple(item)
   klst += tuple(model.V[0]) + tuple(model.V[1]) ## -- need to split matrix up
   klst += tuple(model.g) ## -- probably not necessary
  except AttributeError:  ## -- 2 point function
   for item in [model.dE,model.a,model.b]:
    klst += tuple(item)
  olst += tuple(model.a) + tuple(model.b)
  try:
   glst += tuple(model.g)
  except AttributeError:
   pass
 klst = tuple(set(klst)) ## -- delete duplicates
 olst = tuple(set(olst))
 glst = tuple(set(glst))

 for key in infit.init_val_import:
  skey = key.split('_')
  if skey[0] in klst:
   ## -- add to initial value dictionary
   init[key] = gv.mean(infit.init_val_import[key])
   ## -- if requested, wipe values
   sk = skey[0][-2:]
   if fresh_amplitude and\
     (sk == 'nn' or sk == 'no' or sk == 'on' or sk == 'oo'):
    init[key] = np.ones(np.shape(init[key]))
   if fresh_amplitude and skey[0] in glst:
    init[key] = np.ones(np.shape(init[key]))
   if fresh_overlap and (skey[0] in olst):
    init[key] = np.ones(np.shape(init[key]))
 ## -- finish up
 return mpa.truncate_prior_states(init,nn,no,nn3,no3)

def make_init_from_fit_file_3pt(models,filename,nst=-1,ost=-1,n3st=-1,o3st=-1,
  fresh_overlap=False,fresh_amplitude=True):
 #print "test in"
 init = {}
 infit = __import__(filename)
 nn = nst
 no = ost
 if nn < 0:
  nn = df.num_nst
 if no < 0:
  no = df.num_ost
 if n3st < 0:
  nn3 = df.num_nst_3pt
 else:
  nn3 = n3st
 if o3st < 0:
  no3 = df.num_ost_3pt
 else:
  no3 = o3st

 ## -- save a list of keys for quick reference
 klst = tuple() ## all keys
 olst = tuple() ## overlaps only
 for model in models:
  try:
   for item in [model.dEa,model.dEb,model.a,model.b]:
    klst += tuple(item)
   klst += tuple(model.V[0]) + tuple(model.V[1]) ## -- need to split matrix up
  except AttributeError:  ## -- 2 point function
   for item in [model.dE,model.a,model.b]:
    klst += tuple(item)
  olst += tuple(model.a) + tuple(model.b)
 klst = tuple(set(klst)) ## -- delete duplicates
 olst = tuple(set(olst))

 for key in infit.init_val_import:
  if key in klst:
   ## -- add to initial value dictionary
   init[key] = gv.mean(infit.init_val_import[key])
   ## -- if requested, wipe values
   sk = key[-2:]
   if fresh_amplitude and\
     (sk == 'nn' or sk == 'no' or sk == 'on' or sk == 'oo'):
    init[key] = np.ones(np.shape(init[key]))
   if fresh_overlap and (key in olst):
    init[key] = np.ones(np.shape(init[key]))
 ## -- finish up
 return mp.truncate_prior_states(init,nn,no,nn3,no3,df.do_v_symmetric)

#def make_adv_init_from_default(models,prior_dict=None,nst=-1,ost=-1,n3st=-1,o3st=-1):
# init = {}
 
