#import gvar as gv
import datetime
import meta_data

def save_data(out_fname,fit,data):
 ## -- save the fit parameters found after fitting
 try:
  fit_file = open(out_fname,'w');
  write_header(fit_file);
  for ctag in data:
   fit_file.write( ctag + " dat_mean " +\
    " ".join(str('{:e}'.format(data[ctag][i].mean))\
    for i in range(len(data[ctag]))) + '\n');
   fit_file.write( ctag + " dat_sdev " +\
    " ".join(str('{:e}'.format(data[ctag][i].sdev))\
    for i in range(len(data[ctag]))) + '\n');
   for ptag in fit.p:
    if ptag == 'dE':
     E = [sum(fit.p['dE'][:i+1]) for i in range(len(fit.p['dE']))];
     fit_file.write( ctag + " fit_mean E " +\
      " ".join(str('{:e}'.format(E[i].mean))\
      for i in range(len(fit.p[ptag]))) + '\n');
     fit_file.write( ctag + " fit_sdev E " +\
      " ".join(str('{:e}'.format(fit.p['dE'][i].sdev))\
      for i in range(len(fit.p[ptag]))) + '\n');
    else:
     fit_file.write( ctag + " fit_mean " + ptag + " " +\
      " ".join(str('{:e}'.format(fit.p[ptag][i].mean))\
      for i in range(len(fit.p[ptag]))) + '\n');
     fit_file.write( ctag + " fit_sdev " + ptag + " " +\
      " ".join(str('{:e}'.format(fit.p[ptag][i].sdev))\
      for i in range(len(fit.p[ptag]))) + '\n');
  print "Wrote fit information to file: "
  print "  " + out_fname;
  fit_file.close();
 except IOError:
  print "Could not save data";
  pass;

def write_header(outfile):
 ## -- write a header to the output file
 outfile.seek(0,2);
 dtime = datetime.datetime.now();
 try:
  outfile.write("# opened           : %s/%s/%s  -  %s:%s:%s \n" %\
   (dtime.year,dtime.month,dtime.day,dtime.hour,dtime.minute,dtime.second) );
 except AttributeError:
  pass;

