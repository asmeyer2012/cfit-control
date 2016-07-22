from corrfitter               import CorrFitter
from extract_3pt_info         import *
from make_data                import make_data,import_corfit_file
from make_data_db             import make_data_db
from make_init                import make_init_from_fit_file_3pt
from make_models              import make_models
from make_models_3pt          import make_models_3pt
from make_prior               import make_prior
from make_prior_3pt           import make_prior_3pt
from make_bootstrap           import make_bootstrap
from manipulate_dataset       import *
from print_results            import print_fit
from print_results            import print_error_budget
from save_data                import save_data
from save_fit                 import save_init_from_fit
from save_prior               import save_prior_from_fit
from make_plot                import make_plot
from make_plot                import make_plot_corr_neg
from make_plot                import make_plot_1plus1
from plot_corr_double_log     import plot_corr_double_log
#from plot_corr_effective_mass import plot_corr_effective_mass
from plot_corr_effective_mass_check import plot_corr_effective_mass_check
from plot_corr_normalized     import plot_corr_normalized
from plot_corr_3pt            import plot_corr_3pt
from meta_data                import *
from util_files               import read_fit_file
import defines           as df
import define_prior      as dfp
import define_prior_3pt  as dfp3
import gvar              as gv
import gvar.dataset      as gvd
import matplotlib.pyplot as plt
import numpy             as np
import argparse
import hashlib
import sys

parser = argparse.ArgumentParser(description='fit 3-point correlators') # description of what?
parser.add_argument('-r','--reset',dest='override_init',action='store_true')
parser.add_argument('-p','--plot',dest='override_plot',action='store_true')
parser.add_argument('-d','--dump',dest='dump_gvar',action='store_true')
parser.add_argument('-D','--dump-by-name',dest='dump_gvar_name',action='store_const',const=None)
parser.add_argument('-l','--load',dest='load_gvar',action='store_true')
parser.add_argument('-L','--load-by-name',dest='load_gvar_name',action='store_const',const=None)
argsin = parser.parse_known_args(sys.argv[1:]) ## in namespace
argsin = vars(argsin[0]) ## pull out of namespace
print argsin

## -- assume that data has already been parsed into import files, complete with config tags
dset0 = {}
dset1 = {}
dset2 = {}
dset3 = {}
davg  = {}

if df.do_irrep == "8":
  irrepStr = '8p'
elif df.do_irrep == "8'":
  irrepStr = '8m'
elif df.do_irrep == "16":
  irrepStr = '16p'

## 8- representation
#taglist = list() # for gvar.dump hash key
#filekey = ''
##taglist.append(('l32v4.mes2pt','mes'))
#taglist.append(('l32v4.bar2pt.'+irrepStr,'2pt'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6'))
#taglist.append(('l32v4.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7'))

## 8+ representation
taglist = list() # for gvar.dump hash key
#filekey = ''   ## -- e2dd3e49
#filekey = 'm'  ## -- b41cef9f
filekey = 'n'  ## -- 75f113be
#filekey = 'mn' ## -- c58f8d33 #
#taglist.append(('l32v4.mes2pt','mes'))
taglist.append(('l32v4.bar2pt.'+irrepStr,'bar2pt'))
taglist.append(('l32v4.bar3pt.'+irrepStr+'.axax.t06.p00','axax','t6'))
taglist.append(('l32v4.bar3pt.'+irrepStr+'.axax.t-7.p00','axax','t7'))
taglist.append(('l32v4.bar3pt.'+irrepStr+'.ayay.t06.p00','ayay','t6'))
taglist.append(('l32v4.bar3pt.'+irrepStr+'.ayay.t-7.p00','ayay','t7'))
taglist.append(('l32v4.bar3pt.'+irrepStr+'.azaz.t06.p00','azaz','t6'))
taglist.append(('l32v4.bar3pt.'+irrepStr+'.azaz.t-7.p00','azaz','t7'))

#taglist = list() # for gvar.dump hash key
#taglist.append(('l32v3.bar2pt.'+irrepStr,'2pt'))
#taglist.append(('l32v3.bar3pt.'+irrepStr+'.vxvx.t06.p00','vxvx','t6'))
#taglist.append(('l32v3.bar3pt.'+irrepStr+'.vxvx.t-7.p00','vxvx','t7'))
#taglist.append(('l32v3.bar3pt.'+irrepStr+'.vyvy.t06.p00','vyvy','t6'))
#taglist.append(('l32v3.bar3pt.'+irrepStr+'.vyvy.t-7.p00','vyvy','t7'))
#taglist.append(('l32v3.bar3pt.'+irrepStr+'.vzvz.t06.p00','vzvz','t6'))
#taglist.append(('l32v3.bar3pt.'+irrepStr+'.vzvz.t-7.p00','vzvz','t7'))

## -- get just the first entry of array
filelist = list(np.transpose(np.array(taglist))[0])

if argsin['load_gvar']:
 gvarhash = hashlib.md5(''.join(filelist)+filekey).hexdigest()[:8]
 print "loading data from gvar file: gvar.dump."+gvarhash
 dall = gv.load('gvar.dump.'+gvarhash)
 print "data load complete"
else:
 for tag in taglist:
  dset0[tag[1:]] = import_corfit_file(tag[0]) ## -- import all of the files in taglist

 ### -- remove baryon filter, since I didn't do that before
 ###    I did not name this filter either
 #meyerfilt = [1 if t<df.cor_len/2 else np.power(-1,t) for t in range(df.cor_len)]
 #def fn_meyerfilt(cor,t):
 # return cor[t]*meyerfilt[t]
 #def apply_meyerfilt(cor):
 # return apply_t_fn(cor,fn_meyerfilt)
 #loopkeylist = list()
 #for key in dset0[('mes',)]:
 # if not('_'.join(key.split('_')[:-1]) in loopkeylist):
 #  loopkeylist.append('_'.join(key.split('_')[:-1]))
 #dset0[('mes',)] = fn_apply_tags(dset0[('mes',)],apply_meyerfilt,loopkeylist)

 ### -- make an ensemble average of the meson data
 ### -- long because I didn't do it right the first time
 #dmescw = separate_tags(dset0[('mes',)],'cw')
 #dmesrw = separate_tags(dset0[('mes',)],['r0','r1','r2','r3'])
 #dmes  = {}
 #dmest = {}
 #dmest['cw'] = consolidate_tags(dmescw) ## -- (cw avg) separate meson manipulation
 #dmest['rw'] = consolidate_tags(dmesrw) ## -- (rndx avg)
 #dmest['cw'] = consolidate_tags(dmest['cw']) ## -- (config avg)
 #dmest['rw'] = consolidate_tags(dmest['rw']) ## -- (config avg)
 #for key in dmest['cw']:
 # dmes['cw'+key] = dmest['cw'][key]
 #for key in dmest['rw']:
 # dmes['rw'+key] = dmest['rw'][key]
 #mavg = gv.dataset.avg_data(dmes)

 ### -- take appropriate averages of the data
 ###    effective mass probably not good enough!
 #mmnp = {}
 #tmes = range(df.mesonAvgMin,df.mesonAvgMax+1) + \
 # range(df.cor_len-df.mesonAvgMax,df.cor_len-df.mesonAvgMin+1)
 #for key in mavg:
 # #if key[-2:] == 'pp':
 # # continue
 # mmnp[key] = list()
 # #for t in tmes:
 # # mmnp[key].append(mavg[key][t]/mavg[key][t+2])
 # for t in range(df.mesonAvgMin,df.mesonAvgMax+1):
 #  mmnp[key].append(mavg[key][t]/mavg[key][t+2])
 # for t in range(df.cor_len-df.mesonAvgMax,df.cor_len-df.mesonAvgMin+1):
 #  mmnp[key].append(mavg[key][t]/mavg[key][t-2]) ## t+2 vs t-2!
 #mmnp['tot'] = (np.array(mmnp['cwa4a4'])+np.array(mmnp['rwa4a4']))/2.
 #mmnp['empi'] = gv.sqrt(np.sum(mmnp['tot'])/len(mmnp['tot'])) ## exp{m_pi*a}
 ### -- for a check
 #mmnp['totpp'] = (np.array(mmnp['cwpp'])+np.array(mmnp['rwpp']))/2.
 #mmnp['empipp'] = gv.sqrt(np.sum(mmnp['totpp'])/len(mmnp['totpp']))
 ### -- non-negligible sinh effects! just ignore for now...

 ### -- don't need/care for cw anymore...
 ###    they have different amplitude from cw, so will give different answer anyway
 ###    just get rid of them
 #def corr_pi_ratio6(cora,corb):
 # correlator_pion_ratio_fn(cora,corb,[6],df.cor_len,mmnp['empi'],1./8.)
 #def corr_pi_ratio7(cora,corb): ## -- TODO: check this factor of 8!
 # correlator_pion_ratio_fn(cora,corb,[7],df.cor_len,mmnp['empi'],1./8.)
 #for key in dset0:
 # if key == ('mes',) or key == ('2pt',):
 #  continue
 # dtmp = gv.BufferDict()
 # keyalist = list()
 # #print key
 # #for keyb in dmesrw:
 # # print keyb
 # for keya in dset0[key]:
 #  #if not('_'.join(keya.split('_')[:-1]) in keyalist):
 #  # keyalist.append('_'.join(keya.split('_')[:-1]))
 #  # #keyblist.append('rwa4a4_'+keya.split('_')[1])
 #  if int(key[-1][-1]) == 6:
 #   dtmp[keya] = fn_apply_tags2(dset0[key],dmesrw,corr_pi_ratio6,
 #    '_'.join(keya.split('_')[:-1]),'a4a4_'+keya.split('_')[1])
 #  else:
 #   dtmp[keya] = fn_apply_tags2(dset0[key],dmesrw,corr_pi_ratio7,
 #    '_'.join(keya.split('_')[:-1]),'a4a4_'+keya.split('_')[1])
 # dset0[key] = dtmp

 for key in dset0:
  if 'bar2pt' in key:
   ## -- just consolidate 2-points, skip current averaging
   dset2[key] = consolidate_tags(dset0[key])
  else:
   ## -- average random walls for 3-points per configuration per current
   dset1[key] = average_tags(dset0[key])
   ## -- collect currents by their "current_key"s in define_prior_3pt
   newkey = (dfp3.current_key[dfp3.current_list.index(key[0])],) + key[1:]
   try: #check if dataset exists; if not, add it
    dset2[newkey]
   except KeyError:
    dset2[newkey] = gv.dataset.Dataset()
   for xkey in dset1[key]:
    newxkey = newkey[0].join(xkey.split(key[0])) #replace with new current key
    try:
     dset2[newkey][newxkey]
    except KeyError:
     dset2[newkey][newxkey] = list()
    for cor in dset1[key][xkey]:
     dset2[newkey][newxkey].append(cor)

 for key in dset2:
  ## -- average 3-point currents per configuration
  if not('bar2pt' in key):
   for xkey in dset2[key]:
    dset2[key][xkey] = average_tag_fn(dset2[key][xkey])
  ## -- why is this not consolidating?
  dset3[key] = consolidate_tags(dset2[key])
 
 ## -- post-consolidation manipulation
 for key in dset3:
  for xkey in dset3[key]:
   if 'axax' in xkey\
   or 'ayay' in xkey\
   or 'azaz' in xkey\
   or 'aiai' in xkey\
   or 'vxvx' in xkey\
   or 'vyvy' in xkey\
   or 'vzvz' in xkey\
   or 'vivi' in xkey:
    #print "applying filter to key",key,xkey
    #munich_filter(dset3[key],xkey)
    pass
   #print xkey
   if 't7' in xkey:
    print "multiplying by -1 for key",xkey
    scale_tag(dset3[key],xkey,-1)
    pass
 pass
 
 dnavg = gv.dataset.Dataset()
 for key in dset3:
  for xkey in dset3[key]:
   if 'm' in xkey:
    #print "skipping mixed symmetry key",key,xkey,"..."
    continue
   print "dnavg key",xkey
   dnavg[xkey] = dset3[key][xkey]
 dall = gv.dataset.avg_data(dnavg)
 for key in dall:
   print 'data avg key:',key
 ## -- if requested, save to pickle file
 if argsin['dump_gvar']:
  gvarhash = hashlib.md5(''.join(filelist)+filekey).hexdigest()[:8]
  gv.dump(dall,'gvar.dump.'+gvarhash)
  print "dumped data to gvar file: gvar.dump."+gvarhash
pass # dataset
  
models2 = make_models    (data=dall,lkey=df.lkey)
models3 = make_models_3pt(data=dall,lkey=df.lkey3)
priors2 = make_prior    (models2)
priors3 = make_prior_3pt(models3)

models = list()
for model in models2:
 models.append(model)
for model in models3:
 models.append(model)
priors = gv.BufferDict()
for key in priors2:
 priors[key] = priors2[key]
for key in priors3:
 if key in priors2:
  continue
 priors[key] = priors3[key]
if df.do_init2:
  init2={}
  if argsin['override_init']:
   init2 = make_init_from_fit_file_3pt(models2,'fit_dict')
  else:
   for key in df.define_init:
     if key[-1] == 'n':
      init2[key] = df.define_init[key][:df.num_nst]
     elif key[-1] == 'o':
      init2[key] = df.define_init[key][:df.num_ost]
else:
  init2=None
if df.do_init3:
  init3={}
  if argsin['override_init']:
   init3 = make_init_from_fit_file_3pt(models3,'fit_dict')
  else:
   for key in df.define_init_3pt:
     if key[-2:] == 'nn':
      init3[key] = np.resize(df.define_init_3pt[key],(df.num_nst,df.num_nst))
     elif key[-2:] == 'no':
      init3[key] = np.resize(df.define_init_3pt[key],(df.num_nst,df.num_ost))
     elif key[-2:] == 'on':
      init3[key] = np.resize(df.define_init_3pt[key],(df.num_ost,df.num_nst))
     elif key[-2:] == 'oo':
      init3[key] = np.resize(df.define_init_3pt[key],(df.num_ost,df.num_ost))
     elif key[-1] == 'n':
      init3[key] = df.define_init_3pt[key][:df.num_nst]
     elif key[-1] == 'o':
      init3[key] = df.define_init_3pt[key][:df.num_ost]
else:
  init3=None
pass 

fitter2 = CorrFitter(models=models2,maxit=df.maxit)
fitter3 = CorrFitter(models=models,maxit=df.maxit)
if df.do_2pt:
 print "starting 2pt fit..."
 fit2 = fitter2.lsqfit(data=dall,prior=priors2,p0=init2,svdcut=df.svdcut)
print "starting 3pt fit..."
fit3 = fitter3.lsqfit(data=dall,prior=priors,p0=init3,svdcut=df.svdcut)
#save_data('./test.fit.out',fit,dall)

## -- print
if df.do_2pt:
 print_fit(fit2,priors2)
print_fit(fit3,priors)

## -- save fit as an initial value dictionary
save_init_from_fit(fit3,'fit_dict.py')

## -- test routines
#import util_plots as utp
#for model in models:
# try:
#  fn = utp.create_fit_func_3pt(model,fit3)
#  test1 = model.fitfcn(fit3.transformed_p)
#  test2 = fn(model.tfit)
#  print model.datatag
#  print test1
#  print test2
# except AttributeError:
#  ## -- 2pt
#  pass

## -- plot
if df.do_plot or argsin['override_plot']:
 #plot_corr_effective_mass(models2,dall,None,**df.fitargs)
 plot_corr_effective_mass_check(models2,dall,None,**df.fitargs)
 plot_corr_double_log(models2,dall,fit3,**df.fitargs)
 plot_corr_normalized(models2,dall,fit3,**df.fitargs)
 plot_corr_3pt(models3,dall,fit3,**df.fitargs)
 if df.do_plot_terminal:
  plt.show()

#fit = fitter.chained_lsqfit(data=data, prior=prior)
#fit = fitter.lsqfit(data=data, prior=fit.p)
#fit = fitter.lsqfit(data=data,prior=prior,p0="test.init.out",svdcut=df.svdcut)
#if df.do_2pt:
#  if df.do_initial:
#   try:
#    p0={}
#    for key in df.define_init:
#     if key[-1] == 'o':
#      p0[key] = df.define_init[key][:df.num_ost]
#     else:
#      p0[key] = df.define_init[key][:df.num_nst]
#    fit = fitter.lsqfit(data=data,prior=prior,p0=p0,svdcut=df.svdcut)
#   except KeyError:
#    print "Could not use initial point definitions"
#    fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
#  else:
#   fit = fitter.lsqfit(data=data,prior=prior,svdcut=df.svdcut)
#  #bs_avg = make_bootstrap(fitter,dset,df.mdp.n_bs)
#  print_fit(fit,prior)
#  print_error_budget(fit)
#  #save_data(mdp.output_path +'/'+ mdp.fit_fname,fit,data)
#  save_data('./test.fit.out',fit,data)
#  save_prior_from_fit(df.define_prior,df.define_model,fit,"test.prior.out",
#    round_e=2,round_a=1,preserve_e_widths=True,preserve_a_widths=True)
#  
#  if df.do_plot:
#   if df.do_default_plot:
#    fitter.display_plots()
#   plt.show()
#pass #do_2pt
