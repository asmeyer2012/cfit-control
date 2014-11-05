from corrfitter import Corr2
import gvar as gv

class model_object:
 def __init__(self,datatag,tdata,tfit,tp,akey,bkey,ekey,skey):
  self.datatag=datatag;
  self.tdata=tdata;
  self.tfit=tfit;
  self.tp=tp;
  self.akey=akey;
  self.bkey=bkey;
  self.ekey=ekey;
  self.skey=skey;
 #
 def add_to_op_basis(self,datatag,akey,bkey,tfit=[]):
  ## -- generate a model object which has similar parameters
  ## -- akey and bkey are specified separately
  ## -- tfit may also be specified
  if tfit != []:
   newtfit=tfit;
  else:
   newtfit=self.tfit;
  model = model_object(datatag=datatag, tdata=tdata,\
                      tfit=newtfit,     tp=self.tp, \
                      akey=akey,        bkey=bkey,  \
                      ekey=self.ekey,   skey=self.skey);
  return model;
 def generate(self):
  model_obj = Corr2(datatag=self.datatag, tdata=self.tdata,\
                    tfit=self.tfit,       tp=self.tp,      \
                    a=self.akey,          b=self.bkey,  \
                    dE=self.ekey,         s=self.skey);
  return model_obj;
 #

def use_model_definition(data,model_define):
 models=[];
 for key in data:
  try:
   tdata=model_define[key]['tdata'];
   tfit =model_define[key]['tfit'];
   tp   =model_define[key]['tp'  ];
   akey =model_define[key]['akey'];
   bkey =model_define[key]['bkey'];
   ekey =model_define[key]['ekey'];
   skey =model_define[key]['skey'];
   model_obj=\
     model_object(datatag=key, tdata=tdata,\
                  tfit=tfit,   tp=tp,\
                  akey=akey,   bkey=bkey,\
                  ekey=ekey,   skey=skey);
   models.append(model_obj.generate());
  except KeyError:
   continue;
 return models;
