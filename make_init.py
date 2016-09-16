import gvar as gv
import defines as df
import numpy as np
import os

def load_dict_from_fit_file_3pt(directory,filename):
 initdir = os.getcwd()
 os.chdir(directory)
 infile = __import__(filename)
 rdict = infile.init_val_import
 os.chdir(initdir)
 return rdict

def make_init_from_fit_file_3pt(models,filename,prior_dict=None,nst=-1,ost=-1):
 init = {}
 infit = __import__(filename)
 nn = nst
 no = ost
 if nn < 0:
  nn = df.num_nst
 if no < 0:
  no = df.num_ost
 nn3 = nst
 no3 = ost
 if nn3 < 0:
  nn3 = df.num_nst
 if no3 < 0:
  no3 = df.num_ost
 
 for model in models:
  skey=model.all_datatags[0]

  listpkey = list()
  for pkey in df.define_prior:
   listpkey.append(pkey)
  for pkey in df.define_prior_3pt:
   listpkey.append(pkey)
  for pkey in listpkey:
   #print pkey
   if pkey in init:
    continue ## -- no double counting
   if pkey in infit.init_val_import:
    ## -- not sensitive to number of entries as long as there are more than needed
    try:
     init[pkey] = df.define_init_3pt[pkey]
    except KeyError:
     init[pkey] = df.define_init[pkey]

    #init[pkey] = infit.init_val_import[pkey]
    #if pkey[-2:] == 'nn':
    # ## -- if entries missing, fill in blanks
    # if len(init[pkey]) < nn3:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(nn3-len(init[pkey]),nn3):
    #   init[pkey].append(df.define_init_3pt[pkey][i][:len(init[pkey][0])])
    # if len(init[pkey][0]) < nn3:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(nn3-len(init[pkey]),nn3):
    #   init[pkey].append(df.define_init_3pt[pkey][i][:len(init[pkey])])
    # init[pkey] = np.resize(df.define_init_3pt[pkey],(nn3,nn3))
    #elif pkey[-2:] == 'no':
    # if len(init[pkey]) < no3:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(no3-len(init[pkey]),no3):
    #   init[pkey].append(df.define_init_3pt[pkey][i][:len(init[pkey][0])])
    # if len(init[pkey][0]) < nn3:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(nn3-len(init[pkey]),nn3):
    #   init[pkey].append(df.define_init_3pt[pkey][i][:len(init[pkey])])
    # init[pkey] = np.resize(df.define_init_3pt[pkey],(nn3,no3))
    #elif pkey[-2:] == 'on':
    # if len(init[pkey]) < nn3:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(nn3-len(init[pkey]),nn3):
    #   init[pkey].append(df.define_init_3pt[pkey][i][:len(init[pkey][0])])
    # if len(init[pkey][0]) < no3:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(no3-len(init[pkey]),no3):
    #   init[pkey].append(df.define_init_3pt[pkey][i][:len(init[pkey])])
    # init[pkey] = np.resize(df.define_init_3pt[pkey],(no3,nn3))
    #elif pkey[-2:] == 'oo':
    # if len(init[pkey]) < no3:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(no3-len(init[pkey]),no3):
    #   init[pkey].append(df.define_init_3pt[pkey][i][:len(init[pkey][0])])
    # if len(init[pkey][0]) < no3:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(no3-len(init[pkey]),no3):
    #   init[pkey].append(df.define_init_3pt[pkey][i][:len(init[pkey])])
    # init[pkey] = np.resize(df.define_init_3pt[pkey],(no3,no3))
    # ## -- 
    #elif pkey[-1] == 'n':
    # if len(init[pkey]) < nn:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(nn-len(init[pkey]),nn):
    #   init[pkey].append(df.define_init_3pt[pkey][i])
    # init[pkey] = df.define_init_3pt[pkey][:nn]
    #elif pkey[-1] == 'o':
    # if len(init[pkey]) < no:
    #  print "key",pkey,"from file not long enough to fill initial values, taking from default"
    #  for i in range(no-len(init[pkey]),no):
    #   init[pkey].append(df.define_init_3pt[pkey][i])
    # init[pkey] = df.define_init_3pt[pkey][:no]

    if pkey[-2:] == 'nn':
     ## -- if entries missing, fill in blanks
     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
      for j,y in zip(range(len(x)),x):
       init[pkey][i][j] = y.mean
     init[pkey] = np.resize(df.define_init_3pt[pkey],(nn3,nn3))
    elif pkey[-2:] == 'no':
     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
      for j,y in zip(range(len(x)),x):
       init[pkey][i][j] = y.mean
     init[pkey] = np.resize(df.define_init_3pt[pkey],(nn3,no3))
    elif pkey[-2:] == 'on':
     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
      for j,y in zip(range(len(x)),x):
       init[pkey][i][j] = y.mean
     init[pkey] = np.resize(df.define_init_3pt[pkey],(no3,nn3))
    elif pkey[-2:] == 'oo':
     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
      for j,y in zip(range(len(x)),x):
       init[pkey][i][j] = y.mean
     init[pkey] = np.resize(df.define_init_3pt[pkey],(no3,no3))
     ## -- 
    elif pkey[-1] == 'n':
     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
      init[pkey][i] = x.mean
     init[pkey] = df.define_init_3pt[pkey][:nn]
    elif pkey[-1] == 'o':
     for i,x in zip(range(len(infit.init_val_import[pkey])),infit.init_val_import[pkey]):
      init[pkey][i] = x.mean
     init[pkey] = df.define_init_3pt[pkey][:no]

   else:
    #print "key",pkey,"missing from imported dictionary, using default"
    pass
 return init
