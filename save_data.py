#import gvar as gv
import datetime
import meta_data

def save_data(out_fname,fit,data):
 ## -- save the fit parameters found after fitting
 try:
  fit_file = open(out_fname,'w')
  write_header(fit_file)
  fit_file.write('chi2/dof ' + str(round(fit.chi2/fit.dof,2)) + '\n')
  fit_file.write('dof ' + str(fit.dof) + '\n')
  fit_file.write('Q ' + str(round(fit.Q,2)) + '\n')
  for ptag in fit.transformed_p:
   if ptag == 'dE':
    E = [sum(fit.p['dE'][:i+1]) for i in range(len(fit.p['dE']))]
    fit_file.write( "fit_mean E " +\
     " ".join(str('{:1.4e}'.format(E[i].mean))\
     for i in range(len(fit.transformed_p[ptag]))) + '\n')
    fit_file.write( "fit_sdev E " +\
     " ".join(str('{:1.4e}'.format(fit.transformed_p['dE'][i].sdev))\
     for i in range(len(fit.transformed_p[ptag]))) + '\n')
   else:
    fit_file.write( "fit_mean " + ptag + " " +\
     " ".join(str('{:1.4e}'.format(fit.transformed_p[ptag][i].mean))\
     for i in range(len(fit.transformed_p[ptag]))) + '\n')
    fit_file.write( "fit_sdev " + ptag + " " +\
     " ".join(str('{:1.4e}'.format(fit.transformed_p[ptag][i].sdev))\
     for i in range(len(fit.transformed_p[ptag]))) + '\n')
  #for ctag in data:
  # fit_file.write( ctag + " dat_mean " +\
  #  " ".join(str('{:e}'.format(data[ctag][i].mean))\
  #  for i in range(len(data[ctag]))) + '\n')
  # fit_file.write( ctag + " dat_sdev " +\
  #  " ".join(str('{:e}'.format(data[ctag][i].sdev))\
  #  for i in range(len(data[ctag]))) + '\n')
  print "Wrote fit information to file: "
  print "  " + out_fname
  fit_file.close()
 except IOError:
  print "Could not save data"
  pass

def write_header(outfile):
 ## -- write a header to the output file
 outfile.seek(0,2)
 dtime = datetime.datetime.now()
 try:
  outfile.write("# opened           : %s/%s/%s  -  %s:%s:%s \n" %\
   (dtime.year,dtime.month,dtime.day,dtime.hour,dtime.minute,dtime.second) )
 except AttributeError:
  pass

