import gvar as gv
import numpy as np
import defines as df

def make_prior(models=None,priorkey=None):
 prior = gv.BufferDict();
 
 if models is None:
  pass;
 else:
  if priorkey is None:
   skey=models[0].all_datatags[0];
  else:
   skey=priorkey; ## -- fix later

  for pkey in df.define_prior[skey]:
   prior[pkey]=df.define_prior[skey][pkey];

  #n_nfit=df.define_model[skey]['n_nfit'];
  #n_ofit=df.define_model[skey]['n_ofit'];
 
  ### --
  #prior[can]         = gv.gvar(n_nfit* ['1.170 +- 0.80']);
  #try:
  # prior[can][0]      = gv.gvar(0.6,0.08); #pion05
  # prior[can][1]      = gv.gvar(3.5,0.2); #pion05
  # #prior[coefan][0]      = gv.gvar(4.542,0.4); #pion5
  #except IndexError:
  # pass;
 
  #prior[cEn]     = gv.gvar(n_nfit * ['0.02 +- 0.05']);
  #try:
  # prior[cEn][0]  = gv.gvar(0.239,0.01); #pion05
  # prior[cEn][1]  = gv.gvar(0.46,0.03); #pion05
  # #prior[cEn][0]  = gv.gvar(0.230,0.01); #pion5
  #except IndexError:
  # pass;

  #try:
  # ## -- at least one alternating component
  # if not (models[0].s[1] is None):
  #  prior[cao]        = gv.gvar(n_ofit * ['0.035 +- 0.005']);
  #  try:
  #   prior[cao][0]     = gv.gvar(0.51,0.05);
  #  except IndexError:
  #   pass;
 
  #  prior[cEo]    = gv.gvar(n_ofit * ['0.047 +- 0.04']);
  #  try:
  #   #prior[cEo][0] = gv.gvar(0.22,0.1);
  #   prior[cEo][0] = gv.gvar(0.265,0.01);
  #  except IndexError:
  #   pass;
 
  #except TypeError:
  # ## -- s is a float/int: no oscillating component
  # pass;

  for pkey in prior: # logarithmize the logarithmic coefficients
   if pkey[:3] == 'log':
    prior[pkey] = gv.log(prior[pkey]);
 ##endif

 return prior;
