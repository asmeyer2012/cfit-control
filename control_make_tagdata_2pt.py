from corrfitter               import CorrFitter
from make_data                import make_tag_data
from make_data_db             import make_data_db
from meta_data                import *
from util_files               import read_fit_file
import defines           as df
import define_prior      as dfp
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np
import sys
import time

## -- raw correlator file input
strtime = time.time()
print "start time: ",strtime

print "starting baryon 2-point functions..."
make_tag_data(df.mdp,filename="import-files/import-tag-bar2pt")

endtime = time.time()
print "start time: ",strtime
print "  end time: ",endtime
print "difference: ",endtime-strtime
## --
