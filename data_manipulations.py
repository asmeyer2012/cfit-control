from corrfitter               import CorrFitter
from make_data                import make_data,import_corfit_file
from manipulate_dataset       import *
from meta_data                import *
from util_files               import read_fit_file
import defines           as df
import define_prior_3pt  as dfp3
import dnc_correlations  as dnc
import gvar              as gv
import gvar.dataset      as gvd
import numpy             as np
import sn_minimizer      as snm
import argparse
import hashlib
import sys


## -- requires current_list and current_key set in define_prior_3pt
def standard_load(taglist,filekey,argsin):
  ## -- assume that data has already been parsed into import files, complete with config tags
  dset0 = {}
  dset1 = {}
  dset2 = {}
  dset3 = {}
  davg  = {}
  
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

   for tag in taglist:
    if tag[-1] == '16p':
     #or tag[-1] == '16m':
     ## -- special averaging of 16 irrep
     def fn16(cora,corb):
      cout = list()
      for cor in cora:
       cout.append(cor)
      for cor in corb:
       cout.append(cor)
      return average_tag_fn(cout)
     ## -- apply function
     dset0[tag[1:-1]] = gv.dataset.Dataset()
     for key in dset0[tag[1:]]:
      try:
       dset0[tag[1:-1]][key] = fn16(dset0[tag[1:]][key],dset0[tag[1:-1]+('16m',)][key])
      except KeyError:
       print "missing tag: ",tag[1:-1]+('16m',)," : ",key
       continue
     pass
  
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
    if 'bar2pt' in key\
    or '2pt'    in key:
     ## -- just consolidate 2-points, skip current averaging
     dset2[key] = consolidate_tags(dset0[key])
    elif '16p' in key\
    or   '16m' in key:
     ## -- don't want anymore
     continue
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
    dset3[key] = consolidate_tags(dset2[key])

   ## -- order data and pay attention to missing configurations
   dnavg = gv.dataset.Dataset()
   for key in dset2:
    for xkey in dset2[key]:
     if 'm' in xkey:
      #print "skipping mixed symmetry key",key,xkey,"..."
      continue
     #if 'axax' in xkey\
     #or 'ayay' in xkey\
     #or 'azaz' in xkey\
     #or 'aiai' in xkey\
     #or 'vxvx' in xkey\
     #or 'vyvy' in xkey\
     #or 'vzvz' in xkey\
     #or 'vivi' in xkey:
     # print "applying filter to key",key,xkey
     # munich_filter(dset2[key],xkey)
     # pass
     if 't7' in xkey:
      print "multiplying by -1 for key",xkey
      scale_tag(dset2[key],xkey,-1)
     dnavg[xkey] = dset2[key][xkey]
   ## -- compute correlations
   dall = dnc.divide_and_conquer_correlations(dnavg)
   
   ### -- post-consolidation manipulation
   #for key in dset3:
   # for xkey in dset3[key]:
   #  if 'axax' in xkey\
   #  or 'ayay' in xkey\
   #  or 'azaz' in xkey\
   #  or 'aiai' in xkey\
   #  or 'vxvx' in xkey\
   #  or 'vyvy' in xkey\
   #  or 'vzvz' in xkey\
   #  or 'vivi' in xkey:
   #   #print "applying filter to key",key,xkey
   #   #munich_filter(dset3[key],xkey)
   #   pass
   #  if 't7' in xkey:
   #   #print "multiplying by -1 for key",xkey
   #   #scale_tag(dset3[key],xkey,-1)
   #   pass
   #pass
   #
   #dnavg = gv.dataset.Dataset()
   #for key in dset3:
   # for xkey in dset3[key]:
   #  if 'm' in xkey:
   #   #print "skipping mixed symmetry key",key,xkey,"..."
   #   continue
   #  dnavg[xkey] = dset3[key][xkey]
   ##return dnavg
   #raise ValueError("test")
   #dall = gv.dataset.avg_data(dnavg)

   ## -- if requested, save to pickle file
   if argsin['dump_gvar']:
    gvarhash = hashlib.md5(''.join(filelist)+filekey).hexdigest()[:8]
    gv.dump(dall,'gvar.dump.'+gvarhash)
    print "dumped data to gvar file: gvar.dump."+gvarhash

  return dall ## -- return averaged data
pass # end of function

def sn_minimize_postload(dall,tmax):
 #dall = standard_load(taglist,filekey,argsin)
 cmat = list()
 clist = list()
 klist = list()
 for key in dall:
  if len(key) > 3: ## -- need better way to weed out 3-points
   continue
  ## -- deconstruct key based on current conventions
  k = int(key[-1])
  if not(k in klist):
   klist.append(k)
  c = int(key[-2])
  if not(c in clist):
   clist.append(c)
 for c in sorted(clist):
  datin = list()
  for k in sorted(klist):
   datin.append(dall['s'+str(c)+str(k)])
  cmat.append(datin)
 cmat = np.array(cmat)
 cvec,kvec = snm.minimize_3pt(cmat,tmax) ## -- I guess it works for 2-points
 return cvec,kvec,cmat

def sn_minimize_postload_3pt(dall,t,v):
 cmat = list()
 clist = list()
 klist = list()
 for key in dall:
  if not(v in key):
   continue
  ## -- deconstruct key based on current conventions
  if t != int(key.split('t')[-1]):
   continue
  tkey = 't'.join(key.split('t')[:-1])
  if v != tkey[:-3]:
   continue
  k = int(tkey[-1])
  if not(k in klist):
   klist.append(k)
  c = int(tkey[-2])
  if not(c in clist):
   clist.append(c)
 for c in sorted(clist):
  datin = list()
  for k in sorted(klist):
   datin.append(dall[v+'s'+str(c)+str(k)+'t'+str(t)])
  cmat.append(datin)
 print cmat
 cmat = np.array(cmat)
 cvec,kvec = snm.minimize_3pt(cmat,t)
 return cvec,kvec,cmat
