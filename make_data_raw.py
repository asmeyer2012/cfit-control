import math
import meta_data
import gvar as gv
import util_files as uf
import util_funcs as ut

def make_data_raw (mdp,do_makedata,filename):
 """
 -- takes and reads an input control file
 -- reads specified files and turns them into an output file
    which can be read by corrfitter
 """
 #
 fin = open(filename,'r');
 for line in fin:
  lsp = line.split(' ');
  if len(lsp) > 1: # skip empty lines
   if lsp[0] == "for": # indicates when to get correlator
    lsp.pop(0);
    update_params(mdp,lsp);
    ## -- do_makedata tells it to go ahead with generating a new data output file
    ## -- otherwise, just saves parameters to metadata
    if do_makedata:
     try:
      # open correlator file
      mdp.corr_file = open(mdp.input_path + '/' + mdp.input_fname,'r');
     except IOError:
      print "Could not open file ",mdp.input_fname;
      continue;
     if not mdp.flag_out_open:
      try:
       if mdp.flag_overwrite:
        ## -- open save file for read+write
        try:
         mdp.save_file = open(mdp.output_path + '/' + mdp.output_fname,'r+');
         mdp.save_file.seek(0);    # go to beginning
         mdp.save_file.truncate(); # delete whatever was there before
        except IOError:
         mdp.save_file = open(mdp.output_path + '/' + mdp.output_fname,'w');
         mdp.save_file.close();
         mdp.save_file = open(mdp.output_path + '/' + mdp.output_fname,'r+');
        mdp.flag_out_open = True;
        # write first header
        corr_key=uf.get_str_key(mdp.corr_file,"correlator_key",\
                            int(mdp.corr_num.strip("[]").split(',')[0]));
        uf.write_header(mdp.save_file,corr_key,mdp.corr_len);
        uf.write_section(mdp.save_file,mdp.key);
        mdp.flag_overwrite= False;
       else:
        mdp.save_file = open(mdp.output_path + '/' + mdp.output_fname,'r+');
        mdp.save_file.seek(0,2);  # seek the end of file
        mdp.flag_out_open = True;
        # write another header
        corr_key=uf.get_str_key(mdp.corr_file,"correlator_key",\
                            int(mdp.corr_num.strip("[]").split(',')[0]));
        uf.write_header(mdp.save_file,corr_key,mdp.corr_len);
        uf.write_section(mdp.save_file,mdp.key);
      #except (IOError):
      # pass;
      except (AttributeError):
       print "Attempted to open invalid output file";
     ##endif ! flag_out_open
     save_data(mdp);
     mdp.corr_file.close();
    ##endif do_makedata
   ##else "for" not found in control file
   else:
    update_params(mdp,lsp);
   ##endif lsp[0]==for
  ##endif len(lsp) > 1
 try:
  mdp.save_file.close();
  mdp.flag_out_open = False;
 except (IOError,AttributeError):
  pass;
 fin.close();
 return;
## ------
##

def write_fname(mdp,lnum):
 ## -- save the filenames (and someday correlator #s) for reference
 skey = "#" + mdp.input_path + "/" + mdp.input_fname;
 if lnum > -1:
  uf.ins_line(mdp.save_file,skey,lnum);
## ------
##

def update_params (mdp,lsp):
 ## -- if new parameter supplied,
 ##    change the value given for that parameter in metadata
 if len(lsp) == 2:
  if lsp[0] == "input_path":
   mdp.input_path = lsp[1].replace("\n","");
  elif lsp[0] == "output_path":
   # new output file path, close the old file
   try:
    mdp.save_file.close();
    mdp.flag_out_open = False;
    mdp.flag_overwrite= False;
   except (IOError,AttributeError):
    pass;
   mdp.output_path = lsp[1].replace("\n","");
  elif lsp[0] == "input_fname":
   mdp.input_fname = lsp[1].replace("\n","");
  elif lsp[0] == "output_fname":
   # new output file name, close the old one
   try:
    mdp.save_file.close();
    mdp.flag_out_open = False;
    mdp.flag_overwrite= False;
   except (IOError,AttributeError):
    pass;
   mdp.output_fname = lsp[1].replace("\n","");
   mdp.flag_overwrite = False;
  elif lsp[0] == "input_type":
   mdp.input_type = lsp[1].replace("\n","");
  elif lsp[0] == "key":
   mdp.key = lsp[1].replace("\n","");
  elif lsp[0] == "corr_num":
   mdp.corr_num = lsp[1].replace("\n","");
  elif lsp[0] == "corr_len":
   mdp.corr_len = int(lsp[1].replace("\n",""));
  elif lsp[0] == "flag_overwrite":
   mdp.flag_overwrite = lsp[1].replace("\n","");
  elif not lsp[0].startswith('#'):
   print "Unknown import file key: ",lsp[0];
## ------
##

def save_data (mdp):
 ## -- acutally write data to save file in correct format
 ## -- triggered by keyword "for" at beginning of line
 for i in mdp.corr_num.split(','):
  lnum = find_corr(mdp,int(i));    # get the line number of the correlator, if possible
  if lnum > -1:
   cdat = extract_data(mdp,lnum);  # found the correlator, save to array
   try:                            # write it to file
    lsec = uf.find_data_section(mdp.save_file,mdp.key);
    #mdp.save_file.write( mdp.key + '  ' + '  '.\
    uf.ins_line(mdp.save_file, mdp.key + '  ' + '  '.\
      join('{:e}'.format(cdat[x]) for x in range(0,mdp.corr_len))\
      , lsec[1]+1\
     );
    write_fname(mdp,lsec[0]);
   except IndexError:
    print "-- In file",mdp.corr_file.name;
    print "Could not extract data from file";
  else:
   print "-- In file",mdp.corr_file.name;
   print "Failed to find correlator #",i;
## ------
##

def find_corr (mdp,num):
 ## -- find the line number of correlator number `num` in the file
 ## -- finds first line of correlator based on:
 ##    - starts with 0
 ##    - three fields
 ##    - line has data types "int dbl dbl"
 ## -- for the `num`th correlator,
 ##    also checks for the correct number of time slices
 ctr=0;  # line counter
 mdp.corr_file.seek(0);
 lfsp=mdp.corr_file.read().split("\n");
 for i in range(0,len(lfsp)-1):
  lin=lfsp[i].strip();    # strip preceeding and trailing spaces?
  if lin.startswith("0"): # check whether it is the right form
   if test_line_type(lin,0):
    ctr += 1;
    if ctr == num:        # only reaches this point if it's the needed correlator
     for j in range(i+1,i+mdp.corr_len):  # test for the correct format, number of lines
      if not test_line_type(lfsp[j].strip(),j-i):
       print "Invalid correlator";
       return -1;
      ##endif ! test_line_type
     ##endfor j in range
     #print "valid correlator";
     return i;
    ##endif ctr==num
   ##endif test_line_type
  ##endif startswith(0)
 ##endfor i in range
 return -2;
## ------
##

#def find_data_section(save_file,key):
# ## -- returns the first and last line number of the data section
# ## -- first line is a line break: "## -- 'key'"
# ## -- last line is the last correlator data listed in file
# #
# if key in uf.get_str_key(save_file,"## --"):
#  ## -- key exists
#  lnum = uf.find_str_key(save_file,key)[0];
#  return [lnum[0],lnum[len(lnum)-1]];
# else:
#  ## -- key does not exist yet, add section to end of file
#  lnum = uf.write_section(save_file,key);
#  return [lnum,lnum];
### ------
###

def test_line_type (line,num):
 lsp = line.split('\t');
 # check number of fields
 if len(lsp) == 3:
  try:
   float(lsp[1]); # typecheck
   float(lsp[2]); # typecheck
   if int(lsp[0]) == num: # typecheck and value check
    return True; # everything checks out
   #print "Fails due to unexpected num";
  except ValueError:
   #print "Fails due to typecheck";
   return False; 
 #else:
 # print "Fails due to field nums";
 return False; 
## ------
##

def extract_data(mdp,lnum):
 ## -- get all the data starting at line `lnum`
 ## -- choose the input form of the data
 ##    - real, imaginary, mod part of the data
 if lnum > -1:
  mdp.corr_file.seek(0);
  lfsp = mdp.corr_file.read().split('\n'); # read data
  cdat = [];
  ## -- choose input type
  for i in range(lnum,lnum+mdp.corr_len):
   if mdp.input_type == "real":
    cdat.append(float(lfsp[i].split('\t')[1]));
   elif mdp.input_type == "imag":
    cdat.append(float(lfsp[i].split('\t')[2]));
   elif mdp.input_type == "mod":
    temp1=float(lfsp[i].split('\t')[1]);
    temp2=float(lfsp[i].split('\t')[2]);
    cdat.append(math.sqrt(temp1*temp1+temp2*temp2));
  return cdat;
 return [];
## ------
##
