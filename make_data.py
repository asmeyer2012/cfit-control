import math
import meta_data
import gvar as gv
import util_files as uf
import util_funcs as ut
from make_data_db  import make_data_db
from make_data_raw import make_data_raw

def make_data (mdp,do_makedata,do_db=True,filename=""):
 """
 --'filename' specifies list of files to import data from
 -- takes data from those files and imports to gv.dataset object
 """
 ## -- for database objects (missing)
 if do_db:
  if do_makedata:
   print "Making data from database";
   make_data_db();
 ## -- for raw fnal-type correlators
 else:
  print "Making data from raw correlators";
  import_file = filename;
  make_data_raw(mdp,do_makedata,import_file);
 #
 data_file_out = mdp.output_path + '/' + mdp.output_fname;
 print "Output data file : "+data_file_out;
 dset = gv.dataset.Dataset(data_file_out);
 return gv.dataset.avg_data(dset),dset;
## ------
##
