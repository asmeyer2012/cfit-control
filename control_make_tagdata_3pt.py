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
print "starting tag azaz..."
make_tag_data(df.mdp,filename="import-files/import-tag-azaz")
print "starting tag ayay..."
make_tag_data(df.mdp,filename="import-files/import-tag-ayay")
print "starting tag axax..."
make_tag_data(df.mdp,filename="import-files/import-tag-axax")
print "starting tag ss..."
make_tag_data(df.mdp,filename="import-files/import-tag-ss")
print "starting tag v4v4..."
make_tag_data(df.mdp,filename="import-files/import-tag-v4v4")
print "starting tag vxvx..."
make_tag_data(df.mdp,filename="import-files/import-tag-vxvx")
print "starting tag vyvy..."
make_tag_data(df.mdp,filename="import-files/import-tag-vyvy")
print "starting tag vzvz..."
make_tag_data(df.mdp,filename="import-files/import-tag-vzvz")
print "starting tag a4s..."
make_tag_data(df.mdp,filename="import-files/import-tag-a4s")
print "starting tag axp..."
make_tag_data(df.mdp,filename="import-files/import-tag-axp")
print "starting tag ayp..."
make_tag_data(df.mdp,filename="import-files/import-tag-ayp")
print "starting tag azp..."
make_tag_data(df.mdp,filename="import-files/import-tag-azp")
print "starting tag axv4..."
make_tag_data(df.mdp,filename="import-files/import-tag-axv4")
print "starting tag ayv4..."
make_tag_data(df.mdp,filename="import-files/import-tag-ayv4")
print "starting tag azv4..."
make_tag_data(df.mdp,filename="import-files/import-tag-azv4")
endtime = time.time()
print "start time: ",strtime
print "  end time: ",endtime
print "difference: ",endtime-strtime
## --
