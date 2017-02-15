import gvar as gv

def get_prior_header(nkey,okey):
  """
  Takes key dictionary from get_prior_key_list and turns it
  into a header for the prior file to conform with code expectations
  """
  sret = "import gvar      as gv\nimport util_funcs as utf\n\n" ## -- return string
  sret = sret + "nkey = (\'" + "\',\'".join(nkey) + "\')\n"
  sret = sret + "okey = (\'" + "\',\'".join(okey) + "\')\n"
  sret = sret + "define_prior={}\n"
  sret = sret + "define_prior[\'nkey\'] = nkey\n"
  sret = sret + "define_prior[\'okey\'] = okey\n"
  for ckey in nkey:
   sret = sret + "define_prior[\'" + ckey + "\']=[]\n"
  for ckey in okey:
   sret = sret + "define_prior[\'" + ckey + "\']=[]\n"
  sret = sret + "\n"
  return sret

def get_prior_mean(prior_dict,fit,key,i,round_a):
  """
  Read a fit and write the mean value, taking from the prior_dict object
  if none exists in fit. Done for a specific key and state number i.
  Rounds if requested.
  """
  bkey = utf.get_basekey(key)
  if bkey[0] == 'log':
   skey = key[3:]
  else:
   skey = key
  try:
   if bkey[0] == 'log': ## -- prevent log(0)
    val = max(fit.transformed_p[skey][i].mean,0.1)
   else:
    val = fit.transformed_p[skey][i].mean
  ## -- prior not used in fit, take from previous definition
  except KeyError:
   val = prior_dict[key][i].mean
  if round_a is None:
   return val
  else: ## -- round_a is integer
   return round(val,round_a)

def get_prior_sdev(prior_dict,fit,key,i,round_a,preserve_a_widths):
  """
  Read a fit and write the sdev value, taking from the prior_dict object
  if none exists in fit. Done for a specific key and state number i.
  Rounds if requested, and can bypass fit value and take sdev from prior_dict
  if requested.
  """
  bkey = utf.get_basekey(key)
  if bkey[0] == 'log':
   skey = bkey[0]
  else:
   skey = key
  try:
   if preserve_a_widths:
    raise KeyError() ## -- artificial KeyError
   val = fit.transformed_p[skey][i].sdev
  except KeyError:
   val = prior_dict[key][i].sdev
  if round_a is None:
   return val
  else: ## -- round_a is integer
   return round(val,round_a)

def add_single_state(prior_dict,fit,i,lkey_name,
    round_e,round_a,
    preserve_e_widths,preserve_a_widths):
  """
  Append a single prior state to the dictionary object.
  """
  lmean = []
  lsdev = []
  for key,j in zip(prior_dict[lkey_name],range(len(prior_dict[lkey_name]))):
   if j == 0: ## -- energy
    lmean.append(get_prior_mean(prior_dict,fit,key,i,round_e))
    lsdev.append(get_prior_sdev(prior_dict,fit,key,i,round_e,preserve_e_widths))
   else: ## -- amplitudes
    lmean.append(get_prior_mean(prior_dict,fit,key,i,round_a))
    lsdev.append(get_prior_sdev(prior_dict,fit,key,i,round_a,preserve_a_widths))
  sret = "" ## -- string to return
  sret = sret + "utf.append_prior_state(define_prior," + lkey_name + ",\ngv.gvar(\n"
  sret = sret + "[" + ",".join([str(x) for x in lmean]) + "],\n"
  sret = sret + "[" + ",".join([str(x) for x in lsdev]) + "]))\n"
  return sret

def get_prior_model_dicts(prior_dict,model_dict):
  """
  Write all of the prior dictionary calls into the prior dictionary object
  so that the code knows what to read for which model.
  All possible models should be available in model_dict, even
  if not all of them are used in the fitting.
  """
  nkey = prior_dict['nkey']
  okey = prior_dict['okey']
  sret = "" ## -- string return value
  for mkey in model_dict:
   model = model_dict[mkey]
   sret = sret + "define_prior[\'" + mkey + "\']=\\\n{"
   stmp = [] ## -- temporarily store strings to append
   for key in model['akey'] + model['bkey'] + model['ekey']:
    if key in prior_dict:
     stmp.append("\'" + key + "\':define_prior[\'" + key + "\']")
    elif 'log'+key in prior_dict:
     stmp.append("\'log" + key + "\':define_prior[\'log" + key + "\']")
   sret = sret + ",\n".join(stmp) + " }\n"
  return sret

def save_prior_from_fit(prior_dict,model_dict,fit,filename,
    round_e=None,round_a=None,
    preserve_e_widths=False,preserve_a_widths=False):
  """
  Turn a fit result into a prior file which can be read in again.
  Does the transformations on the data to get it into the correct format
  and builds a dictionary object which can be imported into python.
  """
  nkey = prior_dict['nkey']
  okey = prior_dict['okey']
  sout = get_prior_header(nkey,okey) ## -- string to write to file
  tfp = fit.transformed_p
  ## -- 
  sout = sout + "## -- even states\n"
  for i in range(len(tfp[nkey[0]])):
   sout = sout + "## -- " + str(i) + "\n"
   sout = sout + add_single_state(prior_dict,fit,i,'nkey',
     round_e,round_a,preserve_e_widths,preserve_a_widths)
  sout = sout + "## -- end even states\n\n## -- odd states\n"
  for i in range(len(tfp[okey[0]])):
   sout = sout + "## -- " + str(i) + "\n"
   sout = sout + add_single_state(prior_dict,fit,i,'okey',
     round_e,round_a,preserve_e_widths,preserve_a_widths)
  sout = sout + "## -- end odd states\n\n"
  sout = sout + get_prior_model_dicts(prior_dict,model_dict)
  outfile = open(filename,'w')
  outfile.write(sout)
  outfile.close()
