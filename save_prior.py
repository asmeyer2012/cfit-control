import gvar as gv

def get_prior_header(nkey,okey):
  """
  Takes key dictionary from get_prior_key_list and turns it
  into a header for the prior file to conform with code expectations
  """
  sret = "import gvar      as gv\nimport util_funcs as utf\n\n" ## -- return string
  sret = sret + "nkey = (" + ",".join(nkey) + ")\n"
  sret = sret + "okey = (" + ",".join(okey) + ")\n"
  sret = sret + "define_prior={}\n"
  sret = sret + "define_prior[\'nkey\'] = nkey\n"
  sret = sret + "define_prior[\'okey\'] = okey\n"
  for ckey in nkey:
   sret = sret + "define_prior[" + ckey + "]=[]\n"
  for ckey in okey:
   sret = sret + "define_prior[" + ckey + "]=[]\n"
  sret = sret + "\n"
  return sret

def get_prior_mean(prior_dict,fit,key,i,round_a):
  if key[:3] == 'log':
   skey = key[:3]
  else:
   skey = key
  try:
   val = fit.transformed_p[skey][i].mean
  ## -- prior not used in fit, take from previous definition
  except KeyError:
   val = prior_dict[key][i].mean
  if round_a is None:
   return val
  else: ## -- round_a is integer
   return round(val,round_a)

def get_prior_sdev(prior_dict,fit,key,i,round_a,preserve_a_widths):
  if key[:3] == 'log':
   skey = key[:3]
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

def save_prior_from_fit(prior_dict,fit,filename,
    round_e=None,round_a=None,
    preserve_e_widths=False,preserve_a_widths=False):
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
  sout = sout + "\n## -- odd states\n"
  for i in range(len(tfp[okey[0]])):
   sout = sout + "## -- " + str(i) + "\n"
   sout = sout + add_single_state(prior_dict,fit,i,'okey',
     round_e,round_a,preserve_e_widths,preserve_a_widths)
  sout = sout + "\n"
  outfile = open(filename,'w')
  outfile.write(sout)
  outfile.close()
