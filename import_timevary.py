import gvar as gv
import numpy as np
from util_files import read_fit_file
from plot_timevary import plot_timevary as ptmvr

fit_collector = {}

lsin = open('lsfit','r')
fit_files = lsin.read().split('\n')
for file in fit_files:
 try:
  tmin = int(file.split('_')[1])
  tmax = int((file.split('_')[2]).split('.')[0])
  fit_collector[tmin,tmax,'fit'] = read_fit_file(file)
 except IOError:
  print "IOError"
  continue
 except IndexError:
  continue
ptmvr(fit_collector)
