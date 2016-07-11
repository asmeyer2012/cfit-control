import gvar as gv
import numpy as np

def extract_2pt_val(dat,key,tsep):
  if len(tsep)>0:
   return [extract_2pt_val(dat,key,t) for t in tsep]
  else:
   return dat[key][t]

def get_overlap_keys(fit):
  cKey = list()
  kKey = list()
  for key in fit.transformed_p:
   ## -- sort keys; assuming keys start with E,c,k,ks; neglecting ks,E, odd keys
   if key[:3] == 'log' or key[:4] == 'sqrt':
    continue # only use transformed
   if key[1] == 's':
    continue # no alternate sinks
   if key[-1] == 'o':
    continue # only even states
   if key[0] == 'c':
    cKey.append(key)
   elif key[0] == 'k':
    kKey.append(key)
  ## -- sort lists by class so output is consistent
  cKey = sorted(cKey)
  kKey = sorted(kKey)
  return [cKey,kKey]

def extract_3pt_cov(fit):
  cKey=list()
  kKey=list()
  #for key in fit.transformed_p:
  # ## -- sort keys; assuming keys start with E,c,k,ks; neglecting ks,E, odd keys
  # if key[:3] == 'log' or key[:4] == 'sqrt':
  #  continue # only use transformed
  # if key[1] == 's':
  #  continue # no alternate sinks
  # if key[-1] == 'o':
  #  continue # only even states
  # if key[0] == 'c':
  #  cKey.append(key)
  # elif key[0] == 'k':
  #  kKey.append(key)
  ### -- sort lists by class so output is consistent
  #cKey = sorted(cKey)
  #kKey = sorted(kKey)
  cKey,kKey = get_overlap_keys(fit)
  cMat = list()
  kMat = list()
  ## -- get matrix entries
  for key in cKey:
   cMat.append(gv.mean(fit.transformed_p[key][:len(cKey)]))
  for key in kKey:
   kMat.append(gv.mean(fit.transformed_p[key][:len(kKey)]))
  cMat = np.array(cMat)
  kMat = np.array(kMat)
  ## -- return inverses, need to transpose sink matrix when diagonalizing
  return [np.linalg.inv(cMat),np.linalg.inv(kMat)]

def extract_3pt_min(corr):
  ## -- attempt to choose the matrices which optimize statistical error for the lowest-lying states
  ##    returns the source/sink transformation matrices
  ## 
  cKey=list()
  kKey=list()
  #for key in fit.transformed_p:
  # ## -- sort keys; assuming keys start with E,c,k,ks; neglecting ks,E, odd keys
  # if key[:3] == 'log' or key[:4] == 'sqrt':
  #  continue # only use transformed
  # if key[1] == 's':
  #  continue # no alternate sinks
  # if key[-1] == 'o':
  #  continue # only even states
  # if key[0] == 'c':
  #  cKey.append(key)
  # elif key[0] == 'k':
  #  kKey.append(key)
  ### -- sort lists by class so output is consistent
  #cKey = sorted(cKey)
  #kKey = sorted(kKey)
  cKey,kKey = get_overlap_keys(fit)
  cMat = list()
  kMat = list()
  ## -- get matrix entries
  for key in cKey:
   cMat.append(gv.mean(fit.transformed_p[key][:len(cKey)]))
  for key in kKey:
   kMat.append(gv.mean(fit.transformed_p[key][:len(kKey)]))
  cMat = np.array(cMat)
  kMat = np.array(kMat)
  ## -- return inverses, need to transpose sink matrix when diagonalizing
  return [np.linalg.inv(cMat),np.linalg.inv(kMat)]

def diagonalize_correlator(corr,cmat,kmat):
  ## -- reshape data so first index is time
  incor = np.transpose(corr,[2,0,1])
  diag = np.array([np.dot(np.dot(cmat,t),np.transpose(kmat)) for t in incor])
  return np.transpose(diag,[1,2,0])
