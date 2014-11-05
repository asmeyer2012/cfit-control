
class coef_handle:
 ## -- The generator needs to be started before first use!
 ##    - ch=coef_handle()
 ##    - ch.get_coef(None)   <--
 #
 def __init__(self):
  self.colist={};
  self.costr="abcdefghijklmnopqrstuvwxyz";
  self.cogen=self.coef(None);
  self.get_coef(None); ## need to start the generator
 ## --

 def coef(self,letter):
  letter = yield;
  while not (self.costr == ""):
   try:
    if len(letter) == 1:
     ## -- remove the specified letter
     idx = self.costr.index(letter);
     popval,self.costr = self.costr[idx],self.costr[:idx]+self.costr[idx+1:];
     letter = yield popval;
    else:
     ## -- not a single letter key, just use it
     letter = yield letter;
   except ValueError:
    ## -- already removed
    letter = yield letter;
   except TypeError:
    ## -- remove the next letter from costr and yield it
    popval,self.costr = self.costr[0],self.costr[1:];
    letter = yield popval;
  ##endwhile
  print "Error: all coefficients used";
 ## --

 def get_coef(self,src_key,override=None):
  if override is None:
   try:
    ## -- if src_key has been used before, return the same
    return self.colist[src_key];
   except KeyError:
    ## -- first use of src_key
    self.colist[src_key] = self.cogen.send(None);
    return self.colist[src_key];
  else:
   ## -- override and specify the coefficient manually
   self.colist[src_key] = self.cogen.send(override);
   return self.colist[src_key];
 ## --

 def print_key_coef(self):
  print " SRC_KEY     : COEF_KEY";
  for key in self.colist:
   print '  {:<10}'.format(key)+" :  "+self.colist[key];
 ## --
## ------
##
