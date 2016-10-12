import gvar    as gv
import defines as df
import util_funcs as utf
from corrfitter  import Corr3

def make_models_3pt(data,lkey=None,mdef=None):
 """
 -- data is the averaged data, used to construct default models for each key
 """
 ## -- standard operation/stability loop
 models = use_model_definition_3pt(data,df.define_model_3pt,lkey)
 return models
## ------
##

class model_object_3pt:
 def __init__(self,datatag,tdata,T,tfit,tpa,tpb,akey,bkey,eakey,ebkey,sakey,sbkey,
  vnn,vno,von,voo,transpose_V=False,symmetric_V=False):
  self.datatag=datatag
  self.tdata=tdata
  self.T=T
  self.tfit=tfit
  self.tpa=tpa
  self.tpb=tpb
  self.akey=akey
  self.bkey=bkey
  self.eakey=eakey
  self.ebkey=ebkey
  self.sakey=sakey
  self.sbkey=sbkey
  self.vnn=vnn
  self.vno=vno
  self.von=von
  self.voo=voo
  self.transpose_V=False
  self.symmetric_V=symmetric_V
 #
 def generate(self):
  model_obj = Corr3(datatag=self.datatag,
                    tdata=self.tdata, T=self.T, tfit=self.tfit, 
                    tpa=self.tpa,   tpb=self.tpb,
                    a=self.akey,    b=self.bkey,  
                    dEa=self.eakey, dEb=self.ebkey, 
                    sa=self.sakey,  sb=self.sbkey,
                    Vnn=self.vnn, Vno=self.vno, Von=self.von, Voo=self.voo,
                    transpose_V=self.transpose_V, symmetric_V=self.symmetric_V )
  return model_obj
## ------
##

def use_model_definition_3pt(data,model_define,lkey=None):
 models=[]
 if lkey is None:
  keysrc=data
 else:
  keysrc=lkey
 for key in keysrc:
  try: # all of these must be defined
   tdata =model_define[key]['tdata']
   tfit  =model_define[key]['tfit' ]
   T     =model_define[key]['T'    ]
   tpa   =model_define[key]['tpa'  ]
   tpb   =model_define[key]['tpb'  ]
   akey  =model_define[key]['akey' ]
   eakey =model_define[key]['eakey']
   sakey =model_define[key]['sakey']
   vnn   =model_define[key]['vnn'  ]
   vno   =model_define[key]['vno'  ]
   von   =model_define[key]['von'  ]
   voo   =model_define[key]['voo'  ]
  except KeyError:
   raise KeyError("need to define all of the keys for the 3-point function!")
  try: # does not need to be defined
   bkey  =model_define[key]['bkey' ]
   ebkey =model_define[key]['ebkey']
   sbkey =model_define[key]['sbkey']
  except KeyError:
   bkey  =model_define[key]['akey' ]
   ebkey =model_define[key]['eakey']
   sbkey =model_define[key]['sakey']
  try:
   transpose_V=model_define[key]['transpose_V']
  except KeyError:
   transpose_V=False
  try:
   symmetric_V=model_define[key]['symmetric_V']
  except KeyError:
   symmetric_V=False
  model_obj=\
    model_object_3pt(datatag=key,
                 tdata=tdata, T=T, tfit=tfit,   
                 tpa=tpa,      tpb=tpb,
                 akey=akey,    bkey=bkey,  
                 eakey=eakey,  ebkey=ebkey, 
                 sakey=sakey,  sbkey=sbkey,
                 vnn=vnn, vno=vno, von=von, voo=voo,
                 transpose_V=transpose_V, symmetric_V=symmetric_V )
  models.append(model_obj.generate())
 return models
## ------
##
