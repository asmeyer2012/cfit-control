import gvar as gv
import numpy as np
from util_files import read_fit_file
from plot_timevary_clean import plot_timevary as ptmvr
#from plot_timevary import plot_timevary as ptmvr

fit_collector = {}

tmin_low_cut = 2
tmin_up_cut = 100
tmax_low_cut = 1
tmax_up_cut = 12

lsin = open('lsfit','r')
fit_files = lsin.read().split('\n')
for file in fit_files:
 try:
  tmin = int(file.split('_')[1])
  tmax = int((file.split('_')[2]).split('.')[0])
  if (tmax < tmax_low_cut or tmax > tmax_up_cut):
   continue
  if (tmin < tmin_low_cut or tmin > tmin_up_cut):
   continue
  fit_collector[tmin,tmax,'fit'] = read_fit_file(file)
 except IOError:
  print "IOError"
  continue
 except IndexError:
  continue
ptmvr(fit_collector)
