import gvar as gv
import numpy as np
import matplotlib.pyplot as plt

def diagonalize_correlator(corr,cmat,kmat):
  ## -- apply cmat,kmat to diagonalize correlator; reshape data so first index is time
  incor = np.transpose(corr,[2,0,1])
  diag = np.array([np.dot(np.dot(cmat,t),np.transpose(kmat)) for t in incor])
  return np.transpose(diag,[1,2,0])

def apply_vectors(corr,cvec,kvec):
  ## -- apply cmat,kmat to diagonalize correlator; reshape data so first index is time
  incor = np.transpose(corr,[2,0,1])
  diag = np.array([np.dot(np.dot(cvec,t),kvec) for t in incor])/\
   (np.linalg.norm(cvec)*np.linalg.norm(kvec))
  return diag

def apply_matrices(corr,cmat,kmat):
  ## -- apply cmat,kmat to diagonalize correlator; reshape data so first index is time
  incor = np.transpose(corr,[2,0,1])
  diag = np.array([np.dot(np.dot(cmat,t),np.transpose(kmat)) for t in incor])
  return np.transpose(diag,[1,2,0])

def error_function(c,tmax):
  ## -- signal to noise
  return -np.dot(gv.mean(c[1:tmax]),gv.mean(c[1:tmax]))/\
    np.dot(gv.sdev(c[1:tmax]),gv.sdev(c[1:tmax]))

## -- build up nelder mead algorithm
def order(k):
  return sorted(k,key=lambda x: x[1])
def centroid(k):
  return sum(np.transpose(k)[0][:-1])/(len(k)-1)
def reflect(xo,xn1,alf):
  return xo + alf*(xo-xn1)
def expand(xo,xr,gam):
  return xo + gam*(xr-xo)
def contract(xo,xn1,rho):
  return xo + rho*(xn1-xo)
def setup_reduction(corr,tmax):
  n = len(corr)
  ## -- inline the error function calculation
  def reduction(k,sig):
    k0 = k[0][0]
    knew0 = [(k0 + sig*(x-k0))/np.linalg.norm(k0+sig*(x-k0)) for x in np.transpose(k)[0][1:]]
    #knew0 = [np.array([y0 + sig*(y-y0) for y,y0 in zip(x,k0)]) for x in np.transpose(k)[0][1:]]
    knew1 = np.array([error_function(apply_vectors(corr,x[:n],x[n:]),tmax) for x in knew0])
    return np.insert(zip(knew0,knew1),0,k[0],axis=0)
  ## -- return the function, otherwise loses scope
  return reduction
def stopping(k):
  ## -- stop if the values of k are near enough to each other
  kval = np.transpose(k)[1]
  kavg = sum(kval)/(len(kval)+1)
  ksqr = np.dot(kval,kval)
  #return np.dot(kval-kavg,kval-kavg)/(len(kval)+1) 
  if np.dot(kval-kavg,kval-kavg)/(len(kval)+1) < ksqr*1e-6:
    #print 'stopping condition reached'
    return True
  else:
    return False
def nelder_mead(corr,tmax):
  ## -- minimize using nelder-mead algorithm
  alf = 1
  gam = 2
  rho = 0.5
  sig = 0.5
  npt = 1000
  maxit = 1000
  #npt = 3
  n = len(corr)
  k = list()
  doPrint = False
  ## -- generate random vectors
  for i in range(npt):
   vec = -1+2*np.random.random([2*n])
   try:
     val = error_function(apply_vectors(corr,vec[:n],vec[n:]),tmax)
   except ValueError:
     print vec
     raise
   k.append([vec,val]) # [-1,1)
  reduction = setup_reduction(corr,tmax)
  for i in range(maxit):
    k = order(k)
    #print k
    if doPrint:
      print 'best so far: ',np.sqrt(np.abs(k[0][1]))
    if stopping(k):
      break
    xo  = centroid(k)
    xn1 = k[-1][0]
    xr  = reflect(xo,xn1,alf)
    valn = k[-2][1]
    valr = error_function(apply_vectors(corr,xr[:n],xr[n:]),tmax)
    if valr < valn:
      if valr > k[0][1]:
        if doPrint:
          print 'better: ',valn,'>',valr
        k[-1] = [xr,valr]
        continue
      else:
        if doPrint:
          print 'best  : ',k[0][1],'>',valr
        xe = expand(xo,xr,gam)
        vale = error_function(apply_vectors(corr,xe[:n],xe[n:]),tmax)
        if vale < valr:
          if doPrint:
            print 'better expanded : ',valr,'>',vale
          k[-1] = [xe,vale]
        else:
          if doPrint:
            print 'worse  expanded : ',valr,'<',vale
          k[-1] = [xr,valr]
        continue
    else:
      if doPrint:
        print 'worse : ',valn,'<',valr
      xc = contract(xo,xn1,rho)
      valc = error_function(apply_vectors(corr,xc[:n],xc[n:]),tmax)
      if valc < valn:
        if doPrint:
          print 'better contracted: ',valn,'>',valc
        k[-1] = [xc,valc]
        continue
      else:
        if doPrint:
          print 'worse  contracted: ',valn,'<',valc
        k = reduction(k,sig)
        continue
  pass
  if i == maxit:
    print 'warning: iteration limit reached'
  ## -- 
  print 'best fit S/N: ',np.sqrt(np.abs(k[0][1]))
  return [k[0][0][:n]/np.linalg.norm(k[0][0][:n]),k[0][0][n:]/np.linalg.norm(k[0][0][n:])]

def minimizer(corr,tmax):
  ## -- abstraction
  return nelder_mead(corr,tmax)

def get_perp(v1,v2):
  ## -- return v2 contribution perpendicular to v1
  return np.array(v2)-np.array(v1)*np.dot(np.array(v1),np.array(v2))/\
   (np.linalg.norm(v1)*np.linalg.norm(v1))
def get_perp_vec(vl,v2):
  ## -- return v2 contribution perpendicular to all vectors in vl
  vnow = v2
  for v in vl:
    vnow = get_perp(v,vnow)
  return vnow
def get_perp_list(vl):
  ## -- return list with all vectors perpendicular to each other
  vnow = list()
  vnow.append(vl[0])
  for v in vl[1:]:
    vnow.append(get_perp_vec(vnow,v))
  return vnow
def get_perp_matrix(vl):
  ## -- takes a list of x length-n vectors
  ##    makes a list of n-x length-n vectors perpendicular to all provided and each other
  x = len(vl)
  n = len(vl[0])
  vlnow = list(get_perp_list(vl))
  vlnew = list()
  for i in range(n-x):
    vnew = -1+2*np.random.random([n])
    vnew = get_perp_vec(vlnow,vnew)
    vnew = vnew/np.linalg.norm(vnew)
    vlnow.append(vnew)
    vlnew.append(vnew)
  return vlnew

def project_contributions(corr,vc,vk):
  ## -- apply vc,vk to project out already minimized contributions
  ##    vc,vk assumed to be lists of perpendicular unit vectors
  vcp = get_perp_matrix(vc)
  vkp = get_perp_matrix(vk)
  incor = np.transpose(corr,[2,0,1])
  mc = np.dot(np.transpose(vcp),vcp)
  mk = np.dot(np.transpose(vkp),vkp)
  proj = np.array([np.dot(np.dot(mc,t),mk) for t in incor])
  return np.transpose(proj,[1,2,0])

def minimize_3pt(corr,tmax):
  ## -- minimize the correlation function for a particular correlation function linear combination
  doPrint = False
  corNow = corr
  vcNow = list()
  vkNow = list()
  vc,vk = minimizer(corNow,tmax)
  vcNow.append(vc)
  vkNow.append(vk)
  if doPrint:
    print 'optimization 0 : '
    opt = apply_vectors(corNow,vcNow[-1],vkNow[-1])
    for t in range(7):
      print t,opt[t]
  for i in range(len(vc)-1):
    corNow = project_contributions(corNow,vcNow,vkNow)
    #testperp = apply_vectors(corNow,vc,vk)
    #print 'testing perp'
    #for t in range(7):
    #  print t,testperp[t]
    vc,vk = minimizer(corNow,tmax)
    vcNow.append(vc)
    vkNow.append(vk)
    if doPrint:
      #print 'perp test:'
      #testperp = np.transpose(get_perp_list(vcNow))
      #print testperp,np.transpose(vcNow)
      #print np.dot(get_perp_matrix(vcNow),testperp)
      print 'optimization',i+1,': '
      #opt0 = apply_vectors(corNow,vcNow[0],vkNow[0])
      opt = apply_vectors(corNow,vcNow[-1],vkNow[-1])
      test = apply_vectors(corr,vcNow[-1],vkNow[-1])
      for t in range(7):
        #print t,opt0[t],opt[t],test[t]
        #print t,opt[t],test[t]
        print t,opt[t]
  if doPrint:
    opt = np.array(apply_matrices(corr,vcNow,vkNow))
    print 'optimized correlator: '
    for t in range(7):
      print t,opt[:,:,t]
    print 'optimized matrices: '
    print vcNow
    print vkNow
  return [vcNow,vkNow]

