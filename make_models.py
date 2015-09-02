import gvar    as gv
import defines as df
from corrfitter  import Corr2
#from util_class  import coef_handle
#from model_maker import model_object
#from model_maker import use_model_definition

def make_models(mdp=None,data=None,lkey=None):
 """
 -- mdp is meta_data parameters, contains everything for a generic fit
 -- data is the averaged data, used to construct default models for each key
 """
 if mdp is None:
  if data is None:
   ## -- nothing to do
   return None
  else:
   models = use_model_definition(data,df.define_model,lkey)
   return models
 else:
  return mdp_default_model(mdp)
## ------
##

def mdp_default_model(mdp):
 """
 -- if specification of log wanted, done in make_priors
 """
 tslice=-mdp.corr_len
 tdata=range(abs(tslice))
 #tdata=range(abs(tslice)/2+1)
 if mdp.t_min == 0:
  mdp.t_fit   = df.define_model[mdp.key]['tfit']
 else:
  #mdp.t_fit   = range(mdp.t_min,mdp.corr_len+1-mdp.t_min)
  mdp.t_fit   = range(mdp.t_min,mdp.t_max)+range(mdp.corr_len+1-mdp.t_max,mdp.corr_len-mdp.t_min)
  #mdp.t_fit   = range(mdp.t_min,mdp.t_max)
 if mdp.n_nfit > 0:
  if mdp.n_ofit > 0:
   skey=(1.,-1.)
   akey=('an','ao')
   ekey=('En','Eo')
  else:
   skey=1.
   akey='an'
   ekey='En'
 else:
  skey=(0.,1.)
  akey=(None,'ao')
  ekey=(None,'Eo')
   
 #print "using default model"
 models = [
   Corr2(datatag='Gaa', tdata=tdata, tfit=mdp.t_fit,
   a=akey, b=akey, dE=ekey, tp=tslice, s=skey)
  ]
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
 #def add_to_op_basis(self,datatag,akey,bkey,tfit=[]):
 # ## -- generate a model object which has similar parameters
 # ## -- akey and bkey are specified separately
 # ## -- tfit may also be specified
 # if tfit != []:
 #  newtfit=tfit
 # else:
 #  newtfit=self.tfit
 # model = model_object(datatag=datatag, tdata=tdata,\
 #                      tfit=newtfit,    tp=self.tp, \
 #                      akey=akey,       bkey=bkey,  \
 #                      ekey=self.ekey,  skey=self.skey)
 # return model
 def generate(self):
  model_obj = Corr2(datatag=self.datatag, tdata=self.tdata,\
                    tfit=self.tfit,       tp=self.tp,      \
                    a=self.akey,          b=self.bkey,  \
                    dE=self.ekey,         s=self.skey)
  return model_obj
 #
## ------
##

def use_model_definition(data,model_define,lkey=None):
 models=[]
 if lkey is None:
  keysrc=data
 else:
  keysrc=lkey
 for key in keysrc:
  try:
   tdata=model_define[key]['tdata']
   tfit =model_define[key]['tfit']
   tp   =model_define[key]['tp'  ]
   akey =model_define[key]['akey']
   bkey =model_define[key]['bkey']
   ekey =model_define[key]['ekey']
   skey =model_define[key]['skey']
   model_obj=\
     model_object(datatag=key, tdata=tdata,\
                  tfit=tfit,   tp=tp,\
                  akey=akey,   bkey=bkey,\
                  ekey=ekey,   skey=skey)
   models.append(model_obj.generate())
  except KeyError:
   continue
 return models
## ------
##
