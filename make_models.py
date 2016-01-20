import gvar    as gv
import defines as df
from corrfitter  import Corr2
#from util_class  import coef_handle
#from model_maker import model_object
#from model_maker import use_model_definition

def make_models(data=None,mdp=None,lkey=None,mdef=None):
 """
 -- mdp is meta_data parameters, contains everything for a generic fit
 -- data is the averaged data, used to construct default models for each key
 """
 if data is None:
  ## -- nothing to do
  return None
 else:
  if mdef is None:
    ## -- standard operation/stability loop
    models = use_model_definition(data,df.define_model,lkey)
    return models
  else:
    ## -- time vary loop
    models = use_model_definition(data,mdef,lkey)
    return models
## ------
##

class model_object:
 def __init__(self,datatag,tdata,tfit,tp,akey,bkey,ekey,skey):
  self.datatag=datatag
  self.tdata=tdata
  self.tfit=tfit
  self.tp=tp
  self.akey=akey
  self.bkey=bkey
  self.ekey=ekey
  self.skey=skey
 #
 def generate(self):
  model_obj = Corr2(datatag=self.datatag, tdata=self.tdata,\
                    tfit=self.tfit,       tp=self.tp,      \
                    a=self.akey,          b=self.bkey,  \
                    dE=self.ekey,         s=self.skey)
  return model_obj
## ------
##

def use_model_definition(data,model_define,lkey=None):
 models=[]
 if lkey is None:
  keysrc=data
 else:
  keysrc=lkey
 for key in keysrc:
  try: # all of these must be defined
   tdata=model_define[key]['tdata']
   tfit =model_define[key]['tfit']
   tp   =model_define[key]['tp'  ]
   akey =model_define[key]['akey']
   ekey =model_define[key]['ekey']
   skey =model_define[key]['skey']
  except KeyError:
   continue
  try: # does not need to be defined
   bkey =model_define[key]['bkey']
  except KeyError:
   bkey =model_define[key]['akey']
  model_obj=\
    model_object(datatag=key, tdata=tdata,\
                 tfit=tfit,   tp=tp,\
                 akey=akey,   bkey=bkey,\
                 ekey=ekey,   skey=skey)
  models.append(model_obj.generate())
 return models
## ------
##
