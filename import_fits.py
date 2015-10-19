import gvar as gv
import numpy as np
from util_files import read_fit_file
from plot_stability import plot_stability as pstab

fit_collector = {}

lsin = open('lsfit','r')
fit_files = lsin.read().split('\n')
for file in fit_files:
 try:
  nst = int(file.split('_')[1])
  ost = int((file.split('_')[2]).split('.')[0])
  fit_collector[nst,ost,'fit'] = read_fit_file(file)
 except IOError:
  continue
 except IndexError:
  continue
pstab(fit_collector)
