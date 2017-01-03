import gvar as gv
import numpy as np
import os
from make_init      import load_dict_from_fit_file_3pt
#from plot_stability import plot_stability as pstab
from plot_stability_advanced import plot_stability as pstab
from util_files     import read_fit_file

fit_collector = {}

n3st = 1
o3st = 1

#lsin = open('lsfit','r')
#fit_files = lsin.read().split('\n')
for xfile in os.walk('./fit-adv/'):
 for file in xfile[2]:
  if '.pyc' in file:
   continue ## only want non-compiled versions
  if int(file.split('_')[3][2:]) != n3st:
   continue
  if int(file.split('_')[4].split('.')[0][2:]) != o3st:
   continue
  try:
   #print file
   nst = int(file.split('_')[1][1:])
   ost = int(file.split('_')[2][1:])
   #print nst
   #print ost
   fit_collector[nst,ost,'fit'] = load_dict_from_fit_file_3pt(
    '/home/asm58/scripts/python/control-corrfitter/fit-adv/',file.split('.')[0])
  except IOError:
   print "IOError"
   continue
  except IndexError:
   continue
pstab(fit_collector)
