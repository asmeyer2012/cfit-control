import gvar as gv
import numpy as np
from numpy.linalg import cholesky

## -- truth values
En = np.array( [0.75,0.80,1.00,1.05,1.25,1.30])
Eo = En + 0.28 + np.array([0.01,-0.02,0.01,-0.02,0.01,-0.02])
an = np.array([[1.00,0.50,0.80,0.40,0.60,0.30],
               [0.50,1.00,0.40,0.80,0.30,0.60]])
bn = np.array([[1.00,0.33,0.80,0.27,0.60,0.20],
               [0.33,1.00,0.27,0.80,0.20,0.60]])
ao = an/3.
bo = bn/4.
Vnn= np.array([[1.00,0.10,0.30,0.05,0.10,0.05],
               [0.10,1.05,0.05,0.25,0.05,0.15],
               [0.30,0.05,1.00,0.10,0.10,0.05],
               [0.05,0.25,0.10,1.05,0.05,0.10],
               [0.10,0.05,0.10,0.05,1.00,0.10],
               [0.05,0.15,0.05,0.10,0.10,1.05]])
Von= np.array([[0.10,0.30,0.30,0.05,0.05,0.05],
               [0.30,0.15,0.05,0.25,0.05,0.10],
               [0.30,0.05,0.10,0.30,0.10,0.05],
               [0.05,0.25,0.30,0.15,0.05,0.10],
               [0.30,0.15,0.10,0.05,0.10,0.30],
               [0.15,0.35,0.05,0.10,0.30,0.15]])
Voo= Vnn
Vno= Von

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

## -- checks
lmat = cr2ptd(48)
datac= fx((an[0],ao[0]),(bn[0],bo[0]),(En,Eo),np.arange(48),48,1)
errc = np.sign(datac)*er2ptd(16.,.011,-0.004,7.0711,37.606,56.2341,48,np.arange(48),1500)

data = {}
data['s11'] = []
for i in range(1000):
 data['s11'].append(gen_mock_data_2pt(datac,errc,lmat))

davg = gv.dataset.avg_data(data)

