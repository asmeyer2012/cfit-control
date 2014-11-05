from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
import util_files as uf
import numpy      as np
import defines    as df
import bz2
import sys
sys.path.append('/project/axial/database/scripts/');
from DB             import *

### -- database defines
#dbpath   ='/project/axial/database/db-files/';
#config   ='l1648f211b580m013m065m838';
#campaign ='-pi2pt-2';
#DBEngine = create_engine('sqlite:///'+dbpath+config+campaign+'.sqlite');
#Session  = sessionmaker(bind=DBEngine);
#session  = Session();
##
### -- output defines
#out_path ='/project/axial/database/corrfitter-input/';
#out_fname='pi2pt-2-db';
#do_makedata=True;

## -- Database tables:
##      TABLENAME        -> CLASS
##    - correlator_files -> InputFile
##    - correlators      -> Correlator
##    - data             -> Datum
##    - modify_times     -> DBtimestamp
##    - parameters       -> ParameterSet
## 
## -- Access to other parts of database granted through id's
##    - for datum in session.query(Datum).all():
##    -  print session.query(Correlator).filter('id=='+str(datum.correlator_id)).one().id;

#for datum in session.query(Datum).all():
def make_data_db():
 gdat ={};
 gckey={};
 #
 for corr in df.session.query(Correlator):
  #
  # should make a better version of construct_key using source types
  key = construct_key(corr.name,"2pt"); 
  gdat [key]=[];
  gckey[key]=str(corr.name);
  #
  for datum in df.session.query(Datum).filter('correlator_id=='+str(corr.id)):
   #for datum in session.query(Datum).filter(and_('correlator_id=='+str(corr.id),'id==1')):
   adat=np.array(map(float,bz2.decompress(datum.dataBZ2).split()));
   cktol=False;
   if not (df.ctol is None):
    for i in range(len(adat)-1):
     cktol=cktol or\
          (int(np.abs(df.ctol*adat[i]/adat[i+1]))>0 and\
           int(np.abs(adat[i]/adat[i+1]/df.ctol))>0);
   if cktol:
    print " Correlator violated tolerance cut:";
    print " -- correlator key        : "+str(corr.name);
    print " -- correlator datum id   : ",datum.id;
    print " -- correlator trajectory : ",datum.trajectory;
   else:
    gdat[key].append(adat);
  ##endfor datum
 ##endfor corr

 save_all_data(gdat,gckey,df.out_path+df.out_fname);
 return gdat;
## ------
##

def construct_key(corr_name,corr_type):
 spcn = map(str,corr_name.split('_'));
 if corr_type is "2pt":
  #return 'G'+spcn[1]+spcn[2];
  return spcn[0]+spcn[1]+spcn[2];
 else:
  print "Correlator type ",corr_type," not defined, returning generic key";
  return 'Gab';
## ------
##

def save_all_data(gdat,gckey,fname):
 fout = open(fname,'w');
 fout.close();
 fout = open(fname,'r+');
 fout.write("# database file : "+df.dbpath+df.config+df.campaign+".sqlite\n");
 for key in gdat:
  uf.write_header(fout,gckey[key],len(gdat[key][0]));
  uf.write_section(fout,key);
  fout.seek(0,2);
  for i in range(len(gdat[key])):
   fout.write(key+' '+' '.join(map('{:e}'.format,gdat[key][i]))+'\n');
 fout.close();
## ------
##

