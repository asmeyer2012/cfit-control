import gvar as gv
import numpy as np
import os
from make_init      import load_dict_from_fit_file_3pt
#from plot_stability import plot_stability as pstab
from plot_stability_prior import plot_stability as pstab
from util_files     import read_fit_file

fit_collector = {}

## -- for symmetric, n3st == nst, o3st == ost
#n3st = 7
#o3st = 6

#lsin = open('lsfit','r')
#fit_files = lsin.read().split('\n')
filelist = []
#for xfile in os.walk('./fits/fit-stability-16v5.4.5a/'): ## -- prevent file list from changing?
for xfile in os.walk('./fit-stability/'): ## -- prevent file list from changing?
 for file in xfile[2]:
  filelist.append(file)
for file in filelist:
#for file in xfile:
  if '.pyc' in file:
   continue ## only want non-compiled versions
  #if int(file.split('_')[3][2:]) != n3st:
  # continue
  #if int(file.split('_')[4].split('.')[0][2:]) != o3st:
  # continue
  try:
   #print file
   nst = int(file.split('_')[1][1:])
   ost = int(file.split('_')[2][1:])
   #print nst
   #print ost
   #fit_collector[nst,ost,'fit'] = load_dict_from_fit_file_3pt('./fit-stability/',file.split('.')[0])
   print file
   fit_collector[nst,ost,'fit'] =\
    load_dict_from_fit_file_3pt(os.getcwd()+'/fit-stability/',file.split('.')[0])
   #load_dict_from_fit_file_3pt(os.getcwd()+'/fits/fit-stability-16v5.4.5a/',file.split('.')[0])
   print "in ",nst,ost,fit_collector[nst,ost,'fit']['rdof'],fit_collector[nst,ost,'fit']['chi2']
  except IOError:
   print "IOError"
   continue
  except IndexError:
   continue
pstab(fit_collector)
