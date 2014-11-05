import datetime

def ins_line(file,line,lnum):
 ## -- inserts line into save file such that it takes place lnum
 file.seek(0);
 lfsp = file.read().split('\n'); # save file lines to list
 lfsp.insert(lnum,line);         # insert new line
 file.seek(0);
 file.truncate();                # overwrite file
 while lfsp[len(lfsp)-1] == '':     # if empty last line, remove it
  lfsp.pop();
 for ltmp in lfsp:
  file.write(ltmp+"\n");         # write all of the lines back
## ------
##

def write_section(file,key):
 ## -- save a new section for given key at end of save_file
 ## -- return the number of lines in file
 file.seek(0);
 rval = len(file.read().split('\n'));
 file.write ( "## -- " + key +'\n');
 file.seek(0);
 return rval-1;
## ------
##

def write_header (save_file,corr_key,corr_len):
 save_file.seek(0,2); # go to end to prevent overwriting stuff
 ## -- write a header for the file
 #
 dtime = datetime.datetime.now();
 try:
  save_file.write ( "# opened           : %s/%s/%s  -  %s:%s:%s \n" %\
   (dtime.year,dtime.month,dtime.day,dtime.hour,dtime.minute,dtime.second) );
  save_file.write ( "# num t_slices     : " + str(corr_len) + "\n");
  save_file.write ( "# correlator_key   : " + corr_key + "\n");
  #write_section(save_file,key);
 except AttributeError:
  pass;
## ------
##

def get_str_key (file,skey,cnum=None):
 ## -- get `cnum`th key specified by `skey` in the file
 ## -- if no `cnum` specified, returns a list of all the keys
 lkey = find_str_key(file,skey);
 try:
  ## -- get the rest of the line after skey
  ## -- assumes line starts with skey
  indx = len(skey.split());
  if cnum is None:
   rval = [];
   for ltmp in lkey[1]:
    line = ltmp.split();
    for i in range(indx):
     line.pop(0);
    rval.append(" ".join(str(line[i]) for i in range(len(line))));
   return rval;
  else:
   line = lkey[1][int(cnum)-1].split();
   for i in range(indx):
    line.pop(0);
   return " ".join(str(line[i]) for i in range(len(line)));
 except IndexError:
  return None;
## ------
##

def find_str_key (file,skey):
 file.seek(0); # go to beginning to read entire file
 try:
  rval = [None]*2;
  rval[0] = [];
  rval[1] = [];
  lfsp = file.read().split("\n"); # marker at end of file when finished
  # look on all lines, check if skey somewhere in line
  for lnum in range(0,len(lfsp)):
   if skey in lfsp[lnum]:
    # if skey found, add line number to array rval
    rval[0].append(lnum);
    rval[1].append(lfsp[lnum]);
  # return array of line numbers
  return rval;
 except (IOError,AttributeError):
  print "-- In file",file.name;
  print "Could not search file for string",skey;
  return [];
## ------
##

