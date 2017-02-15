import gvar as gv
import numpy as np
import defines as df
#import json
import pickle
import os
from numpy.linalg import cholesky

def generate_mock_data(fkey=None):
 if not(fkey is None) and os.path.isfile('gvar.dump.'+fkey):
  print 'reading mock data from dump file'
  dall = gv.load('gvar.dump.'+fkey)
  #with open('truth.'+fkey+'.json', 'r') as f:
  # try:
  #  truth = json.load(f)
  # except ValueError:
  #  print "could not load truth data"
  #  truth = {}
  try: 
   f = open('truth.'+fkey+'.pkl','rb')
   truth = pickle.load(f)
  except IOError:
   print "could not load truth data"
   truth = {}
  return dall,truth
 ## -- initial values
 do_test = False
 if do_test:
  Nop = 2
  opcls = [4,7]
  En = list((.7,) + tuple([.3 for i in range(Nampn-1)]))
  Eo = list((1.2,) + tuple([.3 for i in range(Nampo-1)]))
 else:
  if df.do_irrep == "8'":
   Nop = 2
   opcls = [4,7]
   En = [.9613,0.0488,0.2083,0.0477]
   Eo = [1.2131,0.1023,0.0492,0.0481,0.0469]
  elif df.do_irrep == "8":
   Nop = 5
   opcls = [1,2,3,5,6]
   En = list((.7,) + tuple([.3 for i in range(Nampn-1)]))
   Eo = list((1.2,) + tuple([.3 for i in range(Nampo-1)]))
  elif df.do_irrep == "16":
   Nop = 4
   opcls = [2,3,4,6]
   En = list((.7,) + tuple([.3 for i in range(Nampn-1)]))
   Eo = list((1.2,) + tuple([.3 for i in range(Nampo-1)]))
 Nampn = len(En)
 Nampo = len(Eo)
 Nt = 48
 Nmeas = 1500
 
 tmin = 2
 tmax = 10
 tsep = tmax-tmin
 tfit = slice(tmin,tmax+1)
 
 ## -- truth spectrum
 
 ### -- truth values
 #En = np.array( [0.75,0.80,1.00,1.05,1.25,1.30])
 #Eo = En[:5] + 0.28 + np.array([0.01,-0.02,0.01,-0.02,0.01])
 #an = np.array([[1.00,0.50,0.80,0.40,0.60,0.30],
 #               [0.50,1.00,0.40,0.80,0.30,0.60]])
 #bn = np.array([[1.00,0.33,0.80,0.27,0.60,0.20],
 #               [0.33,1.00,0.27,0.80,0.20,0.60]])
 #ao = an[:5]/3.
 #bo = bn[:5]/4.
 #Vnn= np.array([[1.00,0.10,0.30,0.05,0.10,0.05],
 #               [0.10,1.05,0.05,0.25,0.05,0.15],
 #               [0.30,0.05,1.00,0.10,0.10,0.05],
 #               [0.05,0.25,0.10,1.05,0.05,0.10],
 #               [0.10,0.05,0.10,0.05,1.00,0.10],
 #               [0.05,0.15,0.05,0.10,0.10,1.05]])
 #Von= np.array([[0.10,0.30,0.30,0.05,0.05,0.05],
 #               [0.30,0.15,0.05,0.25,0.05,0.10],
 #               [0.30,0.05,0.10,0.30,0.10,0.05],
 #               [0.05,0.25,0.30,0.15,0.05,0.10],
 #               [0.30,0.15,0.10,0.05,0.10,0.30]])
 #Voo= Vnn[:5,:5]
 #Vno= Von.T
 
 ## -- t must be an np.array
 ##    antisymmetric BCs
 def fn(a,b,e,t,T):
  return a*b*((np.exp(-e)**t)-(np.exp(-e)**(T-t)))
 def fo(a,b,e,t,T):
  return ((-1.)**t)*fn(a,b,e,t,T)
 
 ## -- two-point functions
 ## -- a,b,e are vectors of values; contributions summed
 def fnx(a,b,e,t,T):
  sum = np.zeros(len(t))
  for ax,bx,ex in zip(a,b,e):
   sum += fn(ax,bx,ex,t,T)
  return sum
 def fox(a,b,e,t,T):
  sum = np.zeros(len(t))
  for ax,bx,ex in zip(a,b,e):
   sum += fo(ax,bx,ex,t,T)
  return sum
 ## -- a,b,e are 2-tuples of vectors; contributions summed
 def fx(a,b,e,t,T,s):
  return fnx(a[0],b[0],e[0],t,T) + s*fox(a[1],b[1],e[1],t,T) +\
   np.array([ 1e-8 if tx==T/2 else 0 for tx in t])
 
 ## -- three-point functions
 ## -- a,b,ea,eb are vectors of values; V is a matrix of values; 
 ##    tau is the interaction time, t is the sink time, T is spacetime extent
 ##    eo is a 2-tuple of booleans to do even when true
 def favb(a,b,ea,eb,V,tau,t,T,eo):
  fa = fn if eo[0] else fo
  fb = fn if eo[1] else fo
  ap = np.array([fa(ax,1,ex,tau,T) for ax,ex in zip(a,ea)])
  bp = np.array([fb(1,bx,ex,t-tau,T) for bx,ex in zip(b,eb)])
  print len(ap),len(bp),np.shape(V)
  return [np.dot(ap[:,tx],np.dot(V,bp[:,tx])) for tx in np.arange(len(tau))]
 def favbx(a,b,ea,eb,v,tau,t,T):
  sum = np.zeros(len(tau))
  for i,(ax,eax,vi) in enumerate(zip(a,ea,v)):
   for j,(bx,ebx,vij) in enumerate(zip(b,eb,vi)):
    #print favb(ax,bx,eax,ebx,vij,tau,t,T,(i==0,j==0))
    sum += favb(ax,bx,eax,ebx,vij,tau,t,T,(i==0,j==0))
  return sum
 def favbx_adv(a,b,ea,eb,v,tau,t,T):
  sum = np.zeros(len(tau))
  for i,(ax,eax,vi) in enumerate(zip(a,ea,v)):
   for j,(bx,ebx,vij) in enumerate(zip(b,eb,vi)):
    #print favb(ax,bx,eax,ebx,vij,tau,t,T,(i==0,j==0))
    sum += favb(ax,bx,eax,ebx,vij,tau,t,T,(i==0,j==0))
  return sum
 
 ### -- unit tests with Mathematica script
 #print fn(1,1,1,np.array([1,2,3]),48)
 #print fnx(an[0],bn[0],En,np.array([1,2,3]),48)
 #print fox(ao[0],bo[0],Eo,np.array([1,2,3]),48)
 #print fx((an[0],ao[0]),(bn[0],bo[0]),(En,Eo),np.array([1,2,3]),48,1)
 #print fx((an[0],ao[0]),(bn[0],bo[0]),(En,Eo),np.arange(48),48,1)
 #print favb(an[0],bn[0],En,En,Vnn,np.array([1,2,3]),6,48,(True,True))
 #print favb(ao[0],bn[0],Eo,En,Von,np.array([1,2,3]),6,48,(False,True))
 #print favbx((an[0],ao[0]),(bn[0],bo[0]),(En,Eo),(En,Eo),[[Vnn,Vno],[Von,Voo]],
 # np.array([1,2,3]),6,48)
 
 ### -- eigenvalue models for correlation matrices
 ###
 #def ev2ptd(ca,cb,ea,eb,Nt,t):
 # return np.exp(-ea*t/Nl)*(ca+cb*np.exp(eb*Nl/t))
 
 ## -- fractional error models
 def er2ptd(ca,cb,co,ea,eb,eo,Nt,t,Nm):
  return np.sqrt(Nm)*(ca*np.exp(-np.power((t-Nt/2.)/ea,2.)) + cb*np.exp(-np.power((t-Nt/2.)/eb,4.))\
    + co*np.cos(np.pi*t)*np.exp(-np.power((t-Nt/2.)/eo,4.)))
 
 ### -- correlation matrix models
 ###    return lower triangular matrix
 #def cr2ptd(Nt):
 # cmat = np.triu(2.*(np.random.random((Nt,Nt))-.5*np.ones((Nt,Nt)))) # random upper triangle, (-1,1)
 # # specific fixes
 # cmat[0,0] = 1.  # because randomization sometimes gives -1
 # cmat[1,1] = 10. # because second entry in column is too powerful
 # # set some diagonals heuristically
 # xmat = np.zeros((Nt,Nt))
 # i,j = np.indices(xmat.shape)
 # for x,n in zip([4,2,2,1,1],[0,2,Nt-2,4,Nt-4]):
 #  xmat[i==j-n] = x
 # cmat += xmat
 # # normalize columns, turn into lower-triangular
 # for i in range(len(cmat)):
 #  xmat[i] = cmat.T[i]/np.linalg.norm(cmat.T[i])
 # # return lower triangular
 # return xmat
 
 ## -- correlation matrix models
 ##    return lower triangular matrix
 def cr2ptd(Nt):
  ## -- define a correction to upper corner entries
  def corccn(d,x):
   return d*np.power(2.,-np.floor(x/2.))+np.random.randn()
  cmat = np.triu(2.*(np.random.random((Nt,Nt))-.5*np.ones((Nt,Nt)))) # random upper triangle, (-1,1)
  # specific fixes
  cmat[0,0] = 1.  # because randomization sometimes gives -1
  cmat[1,1] = 10. # because second entry in column is too powerful
  for x in [1,3,5,7]:
   cmat[0,Nt-x-1] = corccn(8.,x)
   cmat[1,Nt-x] = corccn(-8.,x-1)
  for x in [1,3,5,7]:
   cmat[1,Nt-x-1] = corccn(-2.,x)
  # set some diagonals heuristically
  xmat = np.zeros((Nt,Nt))
  i,j = np.indices(xmat.shape)
  #for x,n in zip([4,2,2,1,1],[0,2,Nt-2,4,Nt-4]):
  for x,n in zip([4,2,1],[0,2,4]):
   xmat[i==j-n] = x
  cmat += xmat
  # normalize columns, turn into lower-triangular
  for i in range(len(cmat)):
   xmat[i] = cmat.T[i]/np.linalg.norm(cmat.T[i])
  # return lower triangular
  return xmat
 
 ## -- unit tests with Mathematica script
 #print er2ptd(16.,.011,-0.004,7.0711,37.606,56.2341,48,np.arange(48),1500)
 
 ### -- routine to combine correlation matrices
 #def corplus(corm,frac):
 # sum = frac[0]*corm[0]
 # for c,f in zip(corm[1:],frac[1:]):
 #  sum += f*c
 # return sum
 
 ## -- use lower triangular decomposition of correlation matrix to generate correlated vector
 def gen_correlated_vector(lmat):
  Nt = len(lmat)
  u = np.random.normal(0.,1.,Nt)
  return np.dot(lmat,u)
 
 ## -- takes an input lower triangular correlation decomposition and error model
 ##    output is a fractional deviation from central value curve
 ## !! errm must be multiplied by sign of data central values !!
 def gen_fractional_dev(errm,lmat):
  return 1 + errm*gen_correlated_vector(lmat)
 
 ## -- generates data based on models for data, errors, and a lower tri decomp of correlation
 ##    output is a single mock measurement
 def gen_mock_data_2pt(datam,errm,lmat):
  return datam*gen_fractional_dev(errm,lmat)
 
 ### -- checks
 #lmat = cr2ptd(48)
 #datac= fx((an[0],ao[0]),(bn[0],bo[0]),(En,Eo),np.arange(48),48,1)
 #errc = np.sign(datac)*er2ptd(16.,.011,-0.004,7.0711,37.606,56.2341,48,np.arange(48),1500)
 #
 #data = {}
 #data['s11'] = []
 #for i in range(1000):
 # data['s11'].append(gen_mock_data_2pt(datac,errc,lmat))
 #
 #davg = gv.dataset.avg_data(data)
 
 ## -- generate a random lower triangular matrix with normalized rows
 def random_lower(Nop):
  # random upper triangle
  cmat = np.triu(np.random.random((Nop,Nop)))
  xmat = np.zeros((Nop,Nop))
  # normalize columns, turn into lower-triangular
  for i in range(len(cmat)):
   xmat[i] = cmat.T[i]/np.linalg.norm(cmat.T[i])
  # ensure that first entry is +1
  xmat[0][0] = np.abs(xmat[0][0])
  # return lower triangular
  return xmat
 
 ## -- generate a random mixing matrix to correlate correlation functions
 #def random_mixing(Nop):
 # amat = random_lower(Nop)
 # bmat = random_lower(Nop)
 def random_mixing(amat,bmat):
  return np.kron(amat,bmat)
 
 ## -- use mixing matrix to generate a full lower-triangular correlation mixer
 #def random_corr_mix(Nop,Nt):
 # xmat = random_mixing(Nop)
 def random_corr_mix(xmat,Nt):
  return np.kron(xmat,np.identity(Nt))
 
 ### -- use mixing matrix to rotate amplitudes
 ###    doSrc controls order of Kronecker product
 #def rotate_amp(Nop,amat,doSrc):
 # if doSrc:
 #  return np.kron(amat,np.identity(Nop))
 # else:
 #  return np.kron(np.identity(Nop),amat)
 
 ## -- rescale correlators to preserve consistency between amplitude
 def rescale_op(amat,Nop):
  nscl = [1.]
  for i in range(1,Nop):
   fac = (1.-np.dot(nscl,amat[i][:i]))/amat[i][i]
   nscl.append(fac)
  return nscl
 
 ## -- take Kronecker product of rescale vectors
 def kron_rescale(arsc,brsc):
  return np.kron(arsc,brsc)
 
 ## -- define set of unrotated amplitudes for correlators
 def random_amp(Nop,Namp):
  amp = []
  for op in range(Nop):
   amp.append(np.random.normal(0.,1.,Namp))
  return amp
 
 ## -- duplicate amplitudes for sources/sinks
 ##    doSrc controls order of loops
 def duplicate_amp(amp,doSrc):
  Nop = len(amp)
  newamp = []
  if doSrc:
   for i in range(Nop):
    for op in amp:
     newamp.append(op)
  else:
   for op in amp:
    for i in range(Nop):
     newamp.append(op)
  return newamp
 
 ## -- for adding a new matrix block onto an existing matrix
 def add_block(inmat,blk):
  if len(np.shape(inmat)) > 1:
   (Nx,Ny) = np.shape(inmat)
  else:
   return blk
  (Mx,My) = np.shape(blk)
  ll = np.zeros((Nx,My)) # upper-right
  ur = np.zeros((Mx,Ny)) # lower-left
  return np.vstack((np.hstack((inmat,ll)),np.hstack((ur,blk))))
 
 ## -- turn an array of matrices into a block diagonal matrix
 def block_diagonalize(rmat):
  newmat = []
  for blk in rmat:
   newmat = add_block(newmat,blk)
  return newmat
 
 ## -- turn a matrix of matrices into a single matrix
 def block_concatenate(rmat):
  newrow = []
  for row in rmat:
   newrow.append(np.vstack(tuple(row)))
  return np.hstack(tuple(newrow))
 
 ## -- full mock data generation
 
 ##    inter-correlation prep
 
 amat = random_lower(Nop)
 bmat = random_lower(Nop)
 #arot = rotate_amp(Nop,amat,True)
 #brot = rotate_amp(Nop,bmat,False)
 opmat = random_mixing(amat,bmat)
 xmat = random_corr_mix(opmat,Nt)
 ascl = rescale_op(amat,Nop)
 bscl = rescale_op(bmat,Nop)
 opscl = kron_rescale(ascl,bscl)
 #print amat
 #print bmat
 #print arot
 #print brot
 #print opmat
 #print xmat
 #print ascl
 #print bscl
 #print opscl
 
 ##    amplitude prep
 anamp = list(np.array(random_amp(Nop,Nampn))*10.)
 bnamp = random_amp(Nop,Nampn)
 aoamp = list(np.array(random_amp(Nop,Nampo))*10.)
 boamp = random_amp(Nop,Nampo)

 scnamp = duplicate_amp(anamp,True)
 sknamp = duplicate_amp(bnamp,False)
 scoamp = duplicate_amp(aoamp,True)
 skoamp = duplicate_amp(boamp,False)

 ##     don't actually need to rotate amplitudes
 #scnrot = duplicate_amp(np.dot(amat,anamp),True)
 #sknrot = duplicate_amp(np.dot(bmat,bnamp),False)
 #scorot = duplicate_amp(np.dot(amat,aoamp),True)
 #skorot = duplicate_amp(np.dot(bmat,boamp),False)
 scnrot = scnamp
 sknrot = sknamp
 scorot = scoamp
 skorot = skoamp

 #print En
 #print Eo
 #print aamp
 #print bamp
 #print scamp
 #print skamp
 #print 'scnrot',scnrot
 #print 'sknrot',sknrot
 #print 'scorot',scorot
 #print 'skorot',skorot
 
 ##    correlator prep
 rlmat = []
 rdatc = []
 rerrc = []
 for i in range(Nop):
  for j in range(Nop):
   rlmat.append(cr2ptd(Nt)) ## only really works if Nt>=10
   rdatc.append(fx((scnrot[i*Nop+j],scorot[i*Nop+j]),(sknrot[i*Nop+j],skorot[i*Nop+j]),\
    (En,Eo),np.arange(Nt),Nt,1))
   rerrc.append(np.sign(rdatc[-1])*\
    er2ptd(16.,.011,-0.004,7.0711,37.606,56.2341,Nt,np.arange(Nt),1500))
 klmat = block_diagonalize(rlmat)
 kdatc = np.array(rdatc).flatten()
 kerrc = np.array(rerrc).flatten()
 
 ##    operator prep
 if len(opcls) != Nop:
  raise ValueError("number of classes must match number of operators!")
 ## save operator keys constructed from classes
 opkey = []
 for opi in opcls:
  for opj in opcls:
   opkey.append('s'+str(opj)+str(opi)) ## sources incremented before sinks
 ## determine slices to use for each key
 opslc = {}
 for i,key in enumerate(opkey):
  opslc[key] = slice(i*Nt,(i+1)*Nt)
 
 ##    data generation
 data = {}
 for key in opkey:
  data[key] = []
 for i in range(Nmeas):
  meas = gen_mock_data_2pt(kdatc,kerrc,klmat)
  for key in opkey:
   data[key].append(meas[opslc[key]])

 ##    prepare truth for pickling
 truth = {}
 truth['En'] = En
 truth['Eo'] = Eo
 for i,opi in enumerate(opcls):
  truth['c'+str(opi)+'n'] = scnrot[i]
  truth['c'+str(opi)+'o'] = scorot[i]
  truth['k'+str(opi)+'n'] = sknrot[i*Nop]
  truth['k'+str(opi)+'o'] = skorot[i*Nop]
 tmpcor = np.dot(klmat,klmat.T)
 for opi in opkey:
  truth['cv'+opi] = kdatc[opslc[opi]]
  truth['er'+opi] = kerrc[opslc[opi]]
  for opj in opkey:
   truth[opi,opj]  = tmpcor[opslc[opi],opslc[opj]]
 truth['lmat'] = klmat
 truth['opcls'] = opcls
 truth['opkey'] = opkey
 
 #testnum = 1
 #mean = 0
 #for meas in data[opkey[testnum]]:
 # mean += meas
 #mean /= Nmeas
 #sdev = 0
 #for meas in data[opkey[testnum]]:
 # sdev += (meas-mean)*(meas-mean)
 #sdev /= (Nmeas*(Nmeas-1.))
 #sdev = np.sqrt(sdev)
 
 #ftest = []
 #for i in range(Nop):
 # for j in range(Nop):
 #  ftest.append(fx((scnrot[i*Nop+j],scorot[i*Nop+j]),(sknrot[i*Nop+j],skorot[i*Nop+j]),(En,Eo),np.arange(Nt),Nt,1))
 
 ## -- get the averaged data and covariance
 davg = gv.dataset.avg_data(data)
 print "TRUTH VALUES:"
 print "dEn: ",En
 print " En: ",np.cumsum(En)
 print "dEo: ",Eo
 print " Eo: ",np.cumsum(Eo)
 for i,an in enumerate(np.dot(amat,anamp)):
  print "an_"+str(i)+": ",an
 for i,ao in enumerate(np.dot(amat,aoamp)):
  print "ao_"+str(i)+": ",ao
 for i,bn in enumerate(np.dot(bmat,bnamp)):
  print "bn_"+str(i)+": ",bn
 for i,bo in enumerate(np.dot(bmat,boamp)):
  print "bo_"+str(i)+": ",bo
 
 if not(fkey is None):
  print 'saving mock data to dump file'
  gv.dump(davg,'gvar.dump.'+fkey)
  #with open('truth.'+fkey+'.json', 'w') as f:
  # json.dump(truth, f)
  #f.close()
  f = open('truth.'+fkey+'.pkl','ab+')
  pickle.dump(truth,f)
  f.close()
 return davg,truth
 #covm = gv.evalcov(davg)
 
 ### -- slice out the parts to fit
 #rdifm = {}
 #rcovm = {}
 #rcovf = []
 #for opi in opkey:
 # rdifm[opi] = kdatc[opslc[opi]][tfit] - gv.mean(davg[opi][tfit])
 # rcovf.append([])
 # for opj in opkey:
 #  rcovm[opi,opj] = covm[opi,opj][tfit,tfit]
 #  rcovf[-1].append(rcovm[opi,opj])
 #
 ### -- invert the relevant part of the covariance matrix
 #covf = block_concatenate(rcovf)
 #icovf = np.linalg.inv(covf)
 #vslc = {}
 #for i,op in enumerate(opkey):
 # vslc[op] = slice(i*(tsep+1),(i+1)*(tsep+1))
 #
 ### -- compute terms to chi2 and total chi2
 #chi2 = 0
 #chi2sum = {}
 #for opi in opkey:
 # for opj in opkey:
 #  #print np.shape(rdifm[opi])
 #  #print np.shape(icovf[vslc[opi],vslc[opj]])
 #  #print np.shape(rdifm[opj])
 #  chi2sum[opi,opj] = np.dot(rdifm[opi],np.dot(icovf[vslc[opi],vslc[opj]],rdifm[opj]))
 #  chi2 += chi2sum[opi,opj]

