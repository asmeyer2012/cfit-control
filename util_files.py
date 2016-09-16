import gvar  as gv
import numpy as np
import datetime
from collections import namedtuple 
Node = namedtuple('Node', ['pos', 'next'])

## -- looking for faster search algorithm
def build_corr_table(f, size):
  table = [ None ] * size
  keyList = list()
  f.seek(0)
  while True:
    pos = f.tell()
    line = f.readline()
    if not line: break
    #if line.find('correlator_key') != -1:
    if 'correlator_key' in line:
      keyList.append(line.split(' ')[-1])
      i = hash(keyList[-1]) % size
      if table[i] is None:
        table[i] = pos
      else:
        table[i] = Node(pos, table[i])
  return table,keyList

def search_corr_table(string, table, f):
  i = hash(string) % len(table)
  entry = table[i]
  while entry is not None:
    pos = entry.pos if isinstance(entry, Node) else entry
    f.seek(pos)
    #if f.readline().find(string) != -1:
    if string in f.readline():
      return pos
    entry = entry.next if isinstance(entry, Node) else None
  return -1

#SIZE = 2**24
#with open('data.txt', 'r') as f:
#    table = build_table(f, SIZE)
#    print search('Some test string\n', table, f)

def ins_line(file,line,lnum):
 """
 -- inserts line into save file such that it takes place lnum
 """
 file.seek(0)
 lfsp = file.read().split('\n') # save file lines to list
 lfsp.insert(lnum,line)         # insert new line
 file.seek(0)
 file.truncate()                # overwrite file
 while lfsp[len(lfsp)-1] == '':     # if empty last line, remove it
  lfsp.pop()
 for ltmp in lfsp:
  file.write(ltmp+"\n")         # write all of the lines back
## ------
##

def append_line(file,line):
 """
 -- simple implementation for faster file writes
 """
 file.seek(0,2)
 file.write(line +'\n')
## ------
##

def write_section(file,key):
 """
 -- save a new section for given key at end of save_file
 -- return the number of lines in file
 """
 file.seek(0)
 rval = len(file.read().split('\n'))
 file.write ( "## -- " + key +'\n')
 file.seek(0)
 return rval-1
## ------
##

def write_header (save_file,corr_key,corr_len):
 save_file.seek(0,2) # go to end to prevent overwriting stuff
 """
 -- write a header for the file
 """
 dtime = datetime.datetime.now()
 try:
  save_file.write ( "# opened           : %s/%s/%s  -  %s:%s:%s \n" %\
   (dtime.year,dtime.month,dtime.day,dtime.hour,dtime.minute,dtime.second) )
  save_file.write ( "# num t_slices     : " + str(corr_len) + "\n")
  save_file.write ( "# correlator_key   : " + corr_key + "\n")
  #write_section(save_file,key)
 except AttributeError:
  pass
## ------
##

def get_str_key (file,skey,cnum=None):
 """
 -- get `cnum`th key specified by `skey` in the file
 -- if no `cnum` specified, returns a list of all the keys
 """
 lkey = find_str_key(file,skey)
 try:
  ## -- get the rest of the line after skey
  ## -- assumes line starts with skey
  indx = len(skey.split())
  if cnum is None:
   rval = []
   for ltmp in lkey[1]:
    line = ltmp.split()
    for i in range(indx):
     line.pop(0)
    rval.append(" ".join(str(line[i]) for i in range(len(line))))
   return rval
  else:
   line = lkey[1][int(cnum)-1].split()
   for i in range(indx):
    line.pop(0)
   return " ".join(str(line[i]) for i in range(len(line)))
 except IndexError:
  return None
## ------
##

def find_str_key (file,skey,exclusive=False):
 file.seek(0) # go to beginning to read entire file
 try:
  rval = [None]*2
  rval[0] = []
  rval[1] = []
  lfsp = file.read().split("\n") # marker at end of file when finished
  # look on all lines, check if skey somewhere in line
  for lnum in range(0,len(lfsp)):
   if skey in lfsp[lnum]:
    # if skey found, add line number to array rval
    if exclusive==False or check_exclusive(lfsp[lnum],skey):
     rval[0].append(lnum)
     rval[1].append(lfsp[lnum])
  # return array of line numbers
  return rval
 except (IOError,AttributeError):
  print "-- In file",file.name
  print "Could not search file for string",skey
  return []
## ------
##

def check_exclusive(line,key):
 lsp = line.split(key)
 for i in range(len(lsp)-1):
  if lsp[i] is '':
   if lsp[i+1] is '':
    return True
   else:
    if lsp[i+1][0] is ' ':
     return True
    continue
  elif lsp[i+1] is '':
   if lsp[i][-1] is ' ':
    return True
   continue
  else:
   if lsp[i][-1] is ' ' and lsp[i+1][0] is ' ':
    return True
   continue
 return False
## ------
##

def find_data_section(save_file,key):
 """
 -- returns the first and last line number of the data section
 -- first line is a line break: "## -- 'key'"
 -- last line is the last correlator data listed in file
 """
 if key in get_str_key(save_file,"## --"):
  ## -- key exists
  lnum = find_str_key(save_file,key,True)[0]
  return [lnum[0],lnum[len(lnum)-1]]
 else:
  ## -- key does not exist yet, add section to end of file
  lnum = write_section(save_file,key)
  return [lnum,lnum]
## ------
##

def read_fit_file(fit_file):
 """
 Reads a fit file and returns the fit parameters as a dictionary
 """
 rdict = {} ## -- return dictionary
 mdict = {} ## -- temporary dictionary (mean)
 sdict = {} ## -- temporary dictionary (sdev)
 fitin = open(fit_file,'r')
 lread = fitin.read().split('\n')
 for line in lread:
  lspl = line.split(' ')
  if lspl[0] == 'chi2/dof':
   rdict['chi2'] = float(lspl[1])
  elif lspl[0] == 'dof':
   rdict['dof'] = int(lspl[1])
  elif lspl[0] == 'rdof':
   rdict['rdof'] = int(lspl[1])
  elif lspl[0] == 'Q':
   rdict['Q'] = float(lspl[1])
  elif lspl[0] == 'fit_mean':
   key = lspl[1]
   mdict[key] = []
   for x in lspl[2:]:
    mdict[key].append(x)
  elif lspl[0] == 'fit_sdev':
   key = lspl[1]
   sdict[key] = []
   for x in lspl[2:]:
    sdict[key].append(x)
 for key in mdict:
  rdict[key] = gv.gvar(mdict[key],sdict[key])
 return rdict

