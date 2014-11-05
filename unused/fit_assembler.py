import gvar as gv
import util_funcs as ut

class fit_assembler:
 def __init__(modeltag=None):
  self.model_tag=modeltag;
  self.model_dict={};

 def add_model_definition\
   (self,modeltag,datatag,tdata,tfit,tp,akey,bkey,ekey,skey):
  ## -- add a model to the assembler
  if modeltag == self.modeltag or self.modeltag is None:
   self.model_dict[datatag]={};
   self.model_dict[datatag]['tdata']=tdata;
   self.model_dict[datatag]['tfit']=tfit;
   self.model_dict[datatag]['tp'  ]=tp;
   self.model_dict[datatag]['akey']=akey;
   self.model_dict[datatag]['bkey']=bkey;
   self.model_dict[datatag]['ekey']=ekey;
   self.model_dict[datatag]['skey']=skey;

 def generate_models(datatag_list):
  ## -- create the models object for use in corrfitter
  models=[];
  for datatag in datatag_list:
   try:
    tdata=self.model_dict[datatag]['tdata'];
    tfit =self.model_dict[datatag]['tfit'];
    tp   =self.model_dict[datatag]['tp'  ];
    akey =self.model_dict[datatag]['akey'];
    bkey =self.model_dict[datatag]['bkey'];
    ekey =self.model_dict[datatag]['ekey'];
    skey =self.model_dict[datatag]['skey'];
    model_obj = Corr2(datatag=datatag, tdata=tdata,   \
                      tfit=tfit, tp=tp,               \
                      a=akey, b=bkey, dE=ekey, s=skey);
    models.append(model_obj);
   except KeyError:
    continue;
  return models;

 def generate_fit_function(datatag,fit):
  ## -- generate a function from the fit parameters
  tdata=self.model_dict[datatag]['tdata'];
  tfit =self.model_dict[datatag]['tfit'];
  tp   =self.model_dict[datatag]['tp'  ];
  akey =self.model_dict[datatag]['akey'];
  bkey =self.model_dict[datatag]['bkey'];
  ekey =self.model_dict[datatag]['ekey'];
  skey =self.model_dict[datatag]['skey'];
  if tp is None:
   ts=0.;
   tmax=0;
  else:
   ts=np.sign(tp);
   tmax=tp;
  try:
   ## -- even + odd, or odd only function
   sn=skey[0];
   so=skey[1];
   anar = gv.mean(fit.transformed_p[akey[0]]);
   aoar = gv.mean(fit.transformed_p[akey[1]]);
   bnar = gv.mean(fit.transformed_p[bkey[0]]);
   boar = gv.mean(fit.transformed_p[bkey[1]]);
   ensm = gv.mean(ut.sum_dE(fit.transformed_p[ekey[0]]));
   eosm = gv.mean(ut.sum_dE(fit.transformed_p[ekey[1]]));
   def new_func(t):
    return sum([sn*anar[i]*bnar[i]*(gv.exp(-ensm[i]*t)+ts*gv.exp(-ensm[i]*(tmax-t)))\
            for i in range(len(ensm))]) +\
           sum([np.power(-1,i)\
               *so*aoar[i]*boar[i]*(gv.exp(-eosm[i]*t)+ts*gv.exp(-eosm[i]*(tmax-t)))\
            for i in range(len(eosm))]);
  except TypeError:
   ## -- even only function
   aarr = gv.mean(fit.transformed_p[akey]);
   barr = gv.mean(fit.transformed_p[bkey]);
   esum = gv.mean(ut.sum_dE(fit.transformed_p[ekey]));
   def new_func(t):
    return sum([skey.s*aarr[i]*barr[i]*(gv.exp(-esum[i]*t)+ts*gv.exp(-esum[i]*(tmax-t)))\
                for i in range(len(esum))]);
  return new_func;
## ------
##
