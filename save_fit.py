import gvar as gv
import numpy as np
import util_funcs as utf
from print_results import reduced_dof

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
   f.write(',[\''+'\', \''.join(['{:>10}'.format(x).strip() for x in obj[i]])+'\']\\\n')
  if addc:
   f.write(']),\\\n')
  else:
   f.write('])\\\n')
 except TypeError:
  ## -- if symmetric matrix, reconstruct it before writing
  if key[-2:] == 'nn' or key[-2:] == 'oo':
   objx = utf.reconstruct_upper_triangle(obj,int((int(np.sqrt(1+8*len(obj)))-1)/2))
   f.write('\''+str(key)+'\': gv.gvar([[\''+'\', \''.join(['{:>10}'.format(x).strip()\
     for x in objx[0]])+'\']\\\n')
   for i in range(1,len(objx)):
    f.write(',[\''+'\', \''.join(['{:>10}'.format(x).strip() for x in objx[i]])+'\']\\\n')
   if addc:
    f.write(']),\\\n')
   else:
    f.write('])\\\n')
  else:
   ## -- non-iterable value, so only print 1-dim array
   if addc:
    f.write('\''+str(key)+\
     '\': gv.gvar([\''+'\', \''.join(['{:>10}'.format(x).strip() for x in obj])+'\']),\\\n')
   else:
    f.write('\''+str(key)+\
     '\': gv.gvar([\''+'\', \''.join(['{:>10}'.format(x).strip() for x in obj])+'\'])\\\n')
 except IndexError:
  ## -- probably empty matrix
  pass
 pass

def save_init_from_fit(fit,file_name,do_v_symm=False):
 f = open(file_name,'w')
 f.write('import gvar as gv\n')
 f.write('init_val_import = {\\\n')
 f.write('\'dof\':'+str(fit.dof)+'\\\n')
 f.write(',\'rdof\':'+str(reduced_dof(fit,do_v_symm))+'\\\n')
 f.write(',\'chi2\':'+str(fit.chi2)+',\\\n')
 ltfp = len(fit.transformed_p)
 for i,key in zip(range(ltfp),sorted(fit.transformed_p)):
  format_entries(f,fit.transformed_p[key],key,not(i==ltfp-1))
 f.write('}\n')
 f.close()
