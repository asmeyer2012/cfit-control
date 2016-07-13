class md_params:
 ## -- initialize list of parameters
 def __init__(self):
  ## -- file variables
  self.output_path="."
  self.input_path ="."
  self.output_fname="test-out.out"
  self.input_fname=""
  self.fit_fname="test-fit.out"
  self.flag_out_open=False  # indicates open output file
  self.flag_overwrite=False # overwrites output file if true
  ## -- file objects
  self.corr_file=None
  self.save_file=None
  ## -- input variables
  self.input_type="real"
  self.key="default_key" #reference key for 
  self.tag=""      # tag for pre-average manipulation
  self.corr_num=1  # correlator position in file
  self.corr_len=0  # length of correlator 
  ## -- fit variables
  self.n_nfit=1    # number of even parameters
  self.n_ofit=1    # number of odd  parameters
  self.t_min=0     # minimum timeslice
  self.t_fit=[0]   # range of values to fit
  #self.n_conf=0    # number of gauge configurations
  self.n_bs=0      # number of bootstrap iterations
 #
 ## -- in case it's needed
 def print_att(self):
  print "Output file name: ",self.output_path + '/' + self.output_fname
  print " Input file name: ",self.input_path  + '/' + self.input_fname
  print "   Fit file name: ",self.output_path + '/' + self.fit_fname
  print "Flag out open   : ",self.flag_out_open
  print "Flag overwrite  : ",self.flag_overwrite
  print "Input type      : ",self.input_type
  print "Reference key   : ",self.key
  print "Reference tag   : ",self.tag
  print "Correlator #    : ",self.corr_num
  print "Correlator len  : ",self.corr_len
  print "Even fit param  : ",self.n_nfit
  print "Odd  fit param  : ",self.n_ofit
  print "Min timeslice   : ",self.t_min
  print "Fit range       : ",self.t_fit
  #print "Number Gauge Con: ",self.n_conf
  print "Number Bootstrap: ",self.n_bs
