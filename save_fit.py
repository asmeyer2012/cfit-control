import gvar as gv

## -- save a fit so it can be used as initial values in the next calculation

def format_entries(f,obj,key,addc=True):
 ## -- input: file, array/matrix of gvars to write
 try:
  ## -- test object, will fail if 1-dim array
  len(obj[0])
  ## -- print matrix
  f.write('\''+str(key)+'\': gv.gvar([[\''+'\', \''.join(['{:>10}'.format(x).strip()\
    for x in obj[0]])+'\']\\\n')
  for i in range(1,len(obj)):
   f.write(',[\''+'\', \''.join(['{:>10}'.format(x).strip() for x in obj[i]])+']\\\n')
  if addc:
   f.write(']),\\\n')
  else:
   f.write('])\\\n')
 except TypeError:
  ## -- non-iterable value, so only print 1-dim array
  if addc:
   f.write('\''+str(key)+\
    '\': gv.gvar([\''+'\', \''.join(['{:>10}'.format(x).strip() for x in obj])+'\']),\\\n')
  else:
   f.write('\''+str(key)+\
    '\': gv.gvar([\''+'\', \''.join(['{:>10}'.format(x).strip() for x in obj])+'\'])\\\n')
 pass

def save_init_from_fit(fit,file_name):
 f = open(file_name,'w')
 f.write('import gvar as gv\n')
 f.write('init_val_import = {\\\n')
 ltfp = len(fit.transformed_p)
 for i,key in zip(range(ltfp),fit.transformed_p):
  format_entries(f,fit.transformed_p[key],key,not(i==ltfp-1))
 f.write('}\n')
 f.close()
