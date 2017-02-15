import collections
import copy
#import corrfitter
import fileinput
import math
import time
import gvar as _gvar
import lsqfit
import numpy
import random
from corrfitter import BaseModel
#from corrfitter.BaseModel import basekey ## -- not implemented in current version!
import time

#__version__ = '5.0.1'

if not hasattr(collections,'OrderedDict'):
    # for older versions of python
    collections.OrderedDict = dict

## -- keys have underscores and numbers appended to indicate blocks
##    pull all keys which start with a specific string, group them
def retrieve_block_keys(prior, key):
    keyList = []
    for pkey in prior:
      #print key,pkey
      if key in pkey:
        keyList.append(utf.get_basekey(key)[1])
        #if   pkey[3:] == 'log':
        #  #print "appending key ",pkey
        #  keyList.append(pkey[3:])
        #elif pkey[4:] == 'sqrt':
        #  keyList.append(pkey[4:])
        #else:
        #  #print "appending key ",pkey
        #  keyList.append(pkey)
    return sorted(keyList)

class Corr2Test(BaseModel):
    """
    """
    def __init__(
        self, datatag, tdata, tfit, a, b, dE=None, logdE=None,  
        s=1.0, tp=None, othertags=[]
        ):
        super(Corr2Test, self).__init__(datatag, othertags)
        self.a = self._param(a)
        self.b = self._param(b)
        self.dE = self._dE(dE, logdE)
        self.tdata = list(tdata)
        self.tp = tp
        self.s = self._param(s, -1.)
        # verify and compress tfit 
        ntfit = []
        for t in tfit:
            if tp is None:
                assert t in tdata, ("tfit incompatible with tdata: "
                                  +str(tfit)+" "+str(tdata))
                ntfit.append(t)
            else:
                t1, t2 = sorted([t, abs(tp)-t])
                if t1 in ntfit or t2 in ntfit:
                    continue
                assert (t >= 0 and t < abs(tp)), "illegal t in tfit: "+str(t)
                if t1 in tdata:
                    ntfit.append(t1)
                elif t2 in tdata:
                    ntfit.append(t2)
                else:
                    raise ValueError("tfit incompatible with tdata: "
                                      +str(tfit)+" "+str(tdata))
        
        self.tfit = numpy.array(ntfit)
        self._abscissa = self.tfit
    
    def buildprior(self, prior, nterm):
        """ Create fit prior by extracting relevant pieces of ``prior``. 

        Priors for the fit parameters, as specificied by ``self.a`` etc., 
        are copied from ``prior`` into a new dictionary for use by the
        fitter. If a key ``"XX"`` cannot be found in ``prior``, the
        ``buildprior`` looks for one of ``"logXX"``, ``"log(XX)"``, 
        ``"sqrtXX"``, or ``"sqrt(XX)"`` and includes the corresponding
        prior instead.

        The number of terms kept in each part of the fit can be 
        specified using ``nterm = (n, no)`` where ``n`` is the 
        number of non-oscillating terms and ``no`` is the number 
        of oscillating terms. Setting ``nterm = None`` keeps 
        all terms.
        """

        newprior = _gvar.BufferDict()
        for ai, bi, dEi, ntermi in zip(self.a, self.b, self.dE, nterm):
            for x in [ai, bi, dEi]:
                if x is None:
                    continue
                #print "prior key   ",x
                x = self._priorkey(prior, x)
                #print "prior after ",x
                newprior[x] = prior[x][None:ntermi]
        return newprior        
    
    def builddata(self, data):
        """ Assemble fit data from dictionary ``data``. 
            
        Extracts parts of array ``data[self.datatag]`` that are needed for
        the fit, as specified by ``self.tp`` and ``self.tfit``. The entries
        in the (1-D) array ``data[self.datatag]`` are assumed to be
        |GVar|\s and correspond to the ``t``s in ``self.tdata``.
        """
        # tags = self.all_datatags
        # if self.othertags is not None:
        #     tags.extend(self.othertags)
        tdata = self.tdata
        tp = self.tp
        if tp is not None:
            pfac = math.copysign(1,tp)
            tp = abs(tp)
        ans = []
        for tag in self.all_datatags:
            odata = data[tag]
            ndata = [] 
            for t in self.tfit:
                idt = tdata.index(t)
                if tp is None or tp-t not in tdata or t == tp-t:
                    ndata.append(odata[idt])
                else:
                    idt_r = tdata.index(tp-t)
                    ndata.append(lsqfit.wavg([odata[idt], pfac*odata[idt_r]]))
            ans.append(ndata)
        fdata = numpy.array(ans[0]) if len(ans) == 1 else lsqfit.wavg(ans)
        return fdata 
    
    def fitfcn(self, p, nterm=None, t=None):
        """ Return fit function for parameters ``p``. """
        #stime = time.time()
        if t is None:
            t = self.tfit
        if self.tp is None:
            tp_t = None
        elif self.tp >= 0:
            tp_t = self.tp - t
            pfac = 1
        else:
            tp_t = -self.tp - t
            pfac = -1
        if nterm is None:
            nterm = (None, None)
        ofac = (None if self.s[0] == 0.0 else self.s[0],
                (None if self.s[1] == 0.0 else self.s[1]*(-1)**t))
        ans = 0.0
        for _ai, _bi, _dEi, ofaci, ntermi in zip(self.a, self.b, 
                                              self.dE, ofac, nterm):
            if _ai is None or _bi is None or _dEi is None or ofaci is None:
                continue
            if ntermi is not None:
                if ntermi == 0:
                    continue
                ai = p[_ai][:ntermi]
                bi = p[_bi][:ntermi]
                dEi = p[_dEi][:ntermi]
            else:
                ai = p[_ai]
                bi = p[_bi]
                dEi = p[_dEi]
            if tp_t is None:
                exp_t = _gvar.exp(-t)
                for aij, bij, sumdE in zip(ai, bi, numpy.cumsum(dEi)):
                    ans += ofaci * aij * bij * exp_t ** sumdE
            else:
                exp_t = _gvar.exp(-t)
                exp_tp_t = _gvar.exp(-tp_t)
                for aij, bij, sumdE in zip(ai, bi, numpy.cumsum(dEi)):
                    ans += ofaci * aij * bij * (exp_t ** sumdE + pfac * exp_tp_t ** sumdE)
        #print "iteration time: ",time.time()-stime
        return ans    


## -- test
class Corr3Test(BaseModel):
    """ Three-point correlators ``Gavb(t, T) = <b(T) V(t) a(0)>``.
        
    |Corr3| models the ``t`` dependence of a 3-point correlator
    ``Gavb(t, T)`` using ::
        
        Gavb(t, T) = 
         sum_i,j san*an[i]*fn(Ean[i],t)*Vnn[i,j]*sbn*bn[j]*fn(Ebn[j],T-t)
        +sum_i,j san*an[i]*fn(Ean[i],t)*Vno[i,j]*sbo*bo[j]*fo(Ebo[j],T-t)
        +sum_i,j sao*ao[i]*fo(Eao[i],t)*Von[i,j]*sbn*bn[j]*fn(Ebn[j],T-t)
        +sum_i,j sao*ao[i]*fo(Eao[i],t)*Voo[i,j]*sbo*bo[j]*fo(Ebo[j],T-t)
       
    where ::
        
        fn(E, t) =  exp(-E*t) + exp(-E*(tp-t)) # tp>0 -- periodic
               or   exp(-E*t) - exp(-E*(-tp-t))# tp<0 -- anti-periodic
               or   exp(-E*t)                  # if tp is None (nonperiodic)
        
        fo(E, t) = (-1)**t * fn(E, t)
        
    The fit parameters for the non-oscillating piece of ``Gavb`` (first term)
    are ``Vnn[i,j]``, ``an[i]``, ``bn[j]``, ``dEan[i]`` and ``dEbn[j]`` where,
    for example::
        
        dEan[0] = Ean[0] > 0
        dEan[i] = Ean[i]-Ean[i-1] > 0     (for i>0)
        
    and therefore ``Ean[i] = sum_j=0..i dEan[j]``. The parameters for the
    other terms are similarly defined.
        
    :param datatag: Tag used to label correlator in the input |Dataset|.
    :type datatag: string
    :param a: Key identifying the fit parameters for the source amplitudes
        ``an``, for ``a->V``, in the dictionary of priors provided by
        |CorrFitter|; or a two-tuple of keys for the source amplitudes
        ``(an, ao)``. The corresponding values in the dictionary of priors
        are (1-d) arrays of prior values with one term for each ``an[i]``
        or ``ao[i]``. Replacing either key by ``None`` causes the
        corresponding term to be dropped from the fit function. These keys
        are used to label the corresponding parameter arrays in the fit
        results as well as in the prior. 
    :type a: string, or two-tuple of strings or ``None``
    :param b: Same as ``self.a`` except for sink amplitudes ``(bn, bo)`` 
        for ``V->b`` rather than for ``(an, ao)``.
    :type b: string, or two-tuple of strings or ``None``
    :param dEa: Fit-parameter label for ``a->V`` intermediate-state energy 
        differences ``dEan``, or two-tuple of labels for the differences
        ``(dEan,dEao)``. Each label represents an array of energy differences.
        Replacing either label by ``None`` causes the corresponding term in
        the correlator function to be dropped. These keys
        are used to label the corresponding parameter arrays in the fit
        results as well as in the prior. 
    :type dEa: string, or two-tuple of strings or ``None``
    :param dEb: Fit-parameter label for ``V->b`` intermediate-state energy 
        differences ``dEbn``, or two-tuple of labels for the differences
        ``(dEbn,dEbo)``. Each label represents an array of energy differences.
        Replacing either label by ``None`` causes the corresponding term in
        the correlator function to be dropped. These keys
        are used to label the corresponding parameter arrays in the fit
        results as well as in the prior. 
    :type dEb: string, or two-tuple of strings or ``None``
    :param sa: Overall factor ``san`` for the non-oscillating ``a->V`` terms 
        in the correlator, or two-tuple containing the overall factors
        ``(san,sao)`` for the non-oscillating and oscillating terms.
    :type sa: number, or two-tuple of numbers
    :param sb: Overall factor ``sbn`` for the non-oscillating ``V->b`` terms 
        in the correlator, or two-tuple containing the overall factors
        ``(sbn,sbo)`` for the non-oscillating and oscillating terms.
    :type sb: number, or two-tuple of numbers
    :param Vnn: Fit-parameter label for the matrix of current matrix 
        elements ``Vnn[i,j]`` connecting non-oscillating states. Labels that
        begin with "log" indicate that the corresponding matrix elements are
        replaced by their exponentials; these parameters are logarithms of the
        corresponding matrix elements, which must then be positive.
    :type Vnn: string or ``None``
    :param Vno: Fit-parameter label for the matrix of current matrix 
        elements ``Vno[i,j]`` connecting non-oscillating to oscillating
        states. Labels that begin with "log" indicate that the corresponding
        matrix elements are replaced by their exponentials; these parameters
        are logarithms of the corresponding matrix elements, which must then
        be positive.
    :type Vno: string or ``None``
    :param Von: Fit-parameter label for the matrix of current matrix 
        elements ``Von[i,j]`` connecting oscillating to non-oscillating 
        states. Labels that begin with "log" indicate that the corresponding
        matrix elements are replaced by their exponentials; these parameters
        are logarithms of the corresponding matrix elements, which must then
        be positive.
    :type Von: string or ``None``
    :param Voo: Fit-parameter label for the matrix of current matrix 
        elements ``Voo[i,j]`` connecting oscillating states. Labels that begin
        with "log" indicate that the corresponding matrix elements are
        replaced by their exponentials; these parameters are logarithms of the
        corresponding matrix elements, which must then be positive.
    :type Voo: string or ``None``
    :param transpose_V: If ``True``, the transpose ``V[j,i]`` is used in
        place of ``V[i,j]`` for each current matrix element in the fit 
        function. This is useful for doing simultaneous fits to 
        ``a->V->b`` and ``b->V->a``, where the current matrix elements
        for one are the transposes of those for the other. Default value 
        is ``False``.
    :type transpose_V: boolean
    :param symmetric_V: If ``True``, the fit function for ``a->V->b`` is 
        unchanged (symmetrical) under the the interchange of ``a`` and
        ``b``. Then ``Vnn`` and ``Voo`` are square, symmetric matrices
        with ``V[i,j]=V[j,i]`` and their priors are one-dimensional arrays
        containing only elements ``V[i,j]`` with ``j>=i`` in the following
        layout::
        
            [V[0,0],V[0,1],V[0,2]...V[0,N],
                    V[1,1],V[1,2]...V[1,N],
                           V[2,2]...V[2,N],
                                 .
                                  .
                                   .
                                    V[N,N]]
                                    
        Furthermore the matrix specified for ``Von`` is transposed before
        being used by the fitter; normally the matrix specified for ``Von``
        is the same as the matrix specified for ``Vno`` when the amplitude
        is symmetrical. Default value is ``False``.
    :type symmetric_V: boolean
    :param tdata: The ``t``\s corresponding to data entries in the input
        |Dataset|.
    :type tdata: list of integers
    :param tfit: List of ``t``\s to use in the fit. Only data with these
        ``t``\s (all of which should be in ``tdata``) is used in the fit.
    :type tfit: list of integers
    :param tpa: If not ``None`` and positive, the ``a->V`` correlator is 
        assumed to be periodic with period ``tpa``. If negative, the
        correlator is anti-periodic with period ``-tpa``. Setting
        ``tpa=None`` implies that the correlators are not periodic.
    :type tpa: integer or ``None``
    :param tpb: If not ``None`` and positive, the ``V->b`` correlator is 
        assumed to be periodic with period ``tpb``. If negative, the
        correlator is periodic with period ``-tpb``. Setting ``tpb=None``
        implies that the correlators are not periodic.
    :type tpb: integer or ``None``
    """
    def __init__(self, datatag, T, tdata, tfit,          #):
                 Vnn, a, b, dEa=None, dEb=None, logdEa=None, logdEb=None, 
                 sa=1., sb=1.,
                 Vno=None, Von=None, Voo=None, transpose_V=False,
                 symmetric_V=False, tpa=None, tpb=None,
                 othertags=[]):
        super(Corr3Test, self).__init__(datatag, othertags)
        self.a = self._param(a)
        self.dEa = self._dE(dEa, logdEa)
        self.sa = self._param(sa, -1.)
        self.b = self._param(b)
        self.dEb = self._dE(dEb, logdEb)
        self.sb = self._param(sb, -1.)
        self.V = [[Vnn, Vno], [Von, Voo]]
        self.transpose_V = transpose_V
        self.symmetric_V = symmetric_V
        self.T = T
        self.tdata = list(tdata)
        self.tpa = tpa
        self.tpb = tpb
        # validate tfit 
        ntfit = []
        for t in tfit:
            if t >= 0 and t <= T:
                ntfit.append(t)
        self.tfit = numpy.array(ntfit)
        self._abscissa = self.tfit
    
    def buildprior(self, prior, nterm):
        """ Create fit prior by extracting relevant pieces of ``prior``. 

        Priors for the fit parameters, as specificied by ``self.a`` etc., 
        are copied from ``prior`` into a new dictionary for use by the
        fitter. If a key ``"XX"`` cannot be found in ``prior``, the
        ``buildprior`` looks for one of ``"logXX"``, ``"log(XX)"``, 
        ``"sqrtXX"``, or ``"sqrt(XX)"`` and includes the corresponding
        prior instead.

        The number of terms kept in each part of the fit can be 
        specified using ``nterm = (n, no)`` where ``n`` is the 
        number of non-oscillating terms and ``no`` is the number 
        of oscillating terms. Setting ``nterm = None`` keeps 
        all terms.
        """
        def resize_sym(Vii, nterm):
            N = int(numpy.round((((8*len(Vii)+1)**0.5 - 1.)/2.)))
            ans = []
            iterV = iter(Vii)
            for i in range(N):
                for j in range(i, N):
                    v = next(iterV)
                    if ((nterm[0] is None or i < nterm[0])
                        and (nterm[1] is None or j < nterm[1])):
                        ans.append(v)
            return numpy.array(ans)
        ans = _gvar.BufferDict()
        for x in [self.a, self.dEa, self.b, self.dEb]:
            for xi, ntermi in zip(x, nterm):
                if xi is not None:
                    xi = self._priorkey(prior, xi)
                    ans[xi] = prior[xi][None:ntermi]
        for i in range(2):
            for j in range(2):
                vij = self.V[i][j]
                if vij is None:
                    continue
                vij = self._priorkey(prior, vij)
                if i == j and self.symmetric_V:
                    ans[vij] = resize_sym(prior[vij], nterm)
                else:
                    ans[vij] = prior[vij][slice(None, nterm[i]), 
                                          slice(None, nterm[j])]
        return ans         
    
    def builddata(self, data):
        """ Assemble fit data from dictionary ``data``. 
            
        Extracts parts of array ``data[self.datatag]`` that are needed for
        the fit, as specified by ``self.tfit``. The entries in the (1-D)
        array ``data[self.datatag]`` are assumed to be |GVar|\s and
        correspond to the ``t``s in ``self.tdata``.
        """
        # tags = [self.datatag]
        # if self.othertags is not None:
        #     tags.extend(self.othertags)
        ans = []
        for tag in self.all_datatags:
            odata = data[tag]
            tdata = self.tdata
            ndata = []
            for t in self.tfit:
                idt = tdata.index(t)
                ndata.append(odata[idt])
            ans.append(ndata)
        return numpy.array(ans[0]) if len(ans) == 1 else lsqfit.wavg(ans)
    
    def fitfcn(self, p, nterm=None, t=None):
        """ Return fit function for parameters ``p``. """
        #stime = time.time()
        # setup
        if t is None:
            t = self.tfit
        ta = t
        tb = self.T - t
        if self.tpa is None:
            tp_ta = None
        elif self.tpa >= 0:
            tp_ta = self.tpa - ta
            pafac = 1
        else:
            tp_ta = -self.tpa - ta
            pafac = -1
        #
        if self.tpb is None:
            tp_tb = None
        elif self.tpb >= 0:
            tp_tb = self.tpb - tb
            pbfac = 1
        else:
            tp_tb = -self.tpb - tb
            pbfac = -1
        if nterm is None:
            nterm = (None, None)

        # initial and final propagators  
        aprop = []  # aprop[i][j] i= n or o; j=excitation level
        ofac = (self.sa[0], (0.0 if self.sa[1] == 0.0 else self.sa[1]*(-1)**ta))
        for _ai, _dEai, ofaci, ntermai in zip(self.a, self.dEa, ofac, nterm):
            if _ai is None:
                aprop.append(None)
                continue
            ans = []
            if ntermai is None:
                ai =  p[_ai] 
                dEai = p[_dEai] 
            else:
                if ntermai <= 0:
                    aprop.append(None)
                    continue
                ai =  p[_ai][:ntermai]
                dEai = p[_dEai][:ntermai] 
            if tp_ta is None:
                exp_ta = _gvar.exp(-ta)
                ans = [
                    ofaci * aij * exp_ta ** sumdE 
                    for aij, sumdE in zip(ai, numpy.cumsum(dEai))
                    ]
            else:
                exp_ta = _gvar.exp(-ta)
                exp_tp_ta = _gvar.exp(-tp_ta)
                ans = [
                    ofaci * aij * (exp_ta ** sumdE + pafac * exp_tp_ta ** sumdE) 
                    for aij, sumdE in zip(ai, numpy.cumsum(dEai))
                    ]
            aprop.append(ans)
        bprop = []
        ofac = (self.sb[0], (0.0 if self.sb[1] == 0.0 else self.sb[1]*(-1)**tb))
        for _bi, _dEbi, ofaci, ntermbi in zip(self.b, self.dEb, ofac, nterm):
            if _bi is None:
                bprop.append(None)
                continue
            ans = []
            if ntermbi is None:
                bi = p[_bi] 
                dEbi = p[_dEbi]
            else:
                if ntermbi <= 0:
                    bprop.append(None)
                    continue
                bi = p[_bi][:ntermbi] 
                dEbi = p[_dEbi][:ntermbi] 
            if tp_tb is None:
                exp_tb = _gvar.exp(-tb)
                ans = [
                    ofaci * bij * exp_tb ** sumdE 
                    for bij, sumdE in zip(bi, numpy.cumsum(dEbi))
                    ]
            else:
                exp_tb = _gvar.exp(-tb)
                exp_tp_tb = _gvar.exp(-tp_tb)
                ans = [
                    ofaci * bij * (exp_tb ** sumdE + pbfac * exp_tp_tb ** sumdE) 
                    for bij, sumdE in zip(bi, numpy.cumsum(dEbi))
                    ]
            bprop.append(ans)
        
        # combine propagators with vertices 
        ans = 0.0
        for i, (apropi, Vi) in enumerate(zip(aprop, self.V)):
            if apropi is None:
                continue
            for j, (bpropj, Vij) in enumerate(zip(bprop, Vi)):
                if bpropj is None or Vij is None:
                    continue
                V = p[Vij]
                if i == j and self.symmetric_V:
                    # unpack symmetric matrix V 
                    na = len(apropi)
                    nb = len(bpropj)
                    assert na == nb, \
                        "Vnn and Voo must be square matrices if symmetric"
                    iterV = iter(V)
                    V = numpy.empty((na, nb), dtype=V.dtype)
                    for k in range(na):
                        for l in range(k, nb):
                            V[k, l] = next(iterV)
                            if k != l:
                                V[l, k] = V[k, l]
                    
                if self.transpose_V or (i>j and self.symmetric_V):
                    V = V.T
                for ak, Vk in zip(apropi, V):
                    acc = 0.0
                    for bl, Vkl in zip(bpropj, Vk):
                        acc += Vkl*bl
                    ans += ak*acc
        #print "iteration time 3pt: ",time.time()-stime
        return ans                

## -- 
class Corr2Adv(BaseModel):
    """
    Implementation of Corr2 to work with same priors as Corr3Adv
    #
    Two-point correlators ``Gab(t) = <b(t) a(0)>``.
    |Corr2| models the ``t`` dependence of a 2-point correlator ``Gab(t)``
    using ::
        Gab(t) = sn * sum_i an[i]*bn[i] * fn(En[i], t)
               + so * sum_i ao[i]*bo[i] * fo(Eo[i], t)
    where ``sn`` and ``so`` are typically ``-1``, ``0``, or ``1`` and ::
        fn(E, t) =  exp(-E*t) + exp(-E*(tp-t)) # tp>0 -- periodic
               or   exp(-E*t) - exp(-E*(-tp-t))# tp<0 -- anti-periodic
               or   exp(-E*t)                  # if tp is None (nonperiodic)
        fo(E, t) = (-1)**t * fn(E, t)
    """
    def __init__(
        self, datatag, tdata, tfit, a, b, dE=None,
        s=1.0, tp=None, othertags=[]
        ):
        super(Corr2Adv, self).__init__(datatag, othertags)
        self.a = self._param(a)
        self.b = self._param(b)
        self.dE = self._param(dE)
        self.esufx = []
        self.tdata = list(tdata)
        self.tp = tp
        self.s = self._param(s, -1.)
        # verify and compress tfit
        ntfit = []
        for t in tfit:
            if tp is None:
                assert t in tdata, ("tfit incompatible with tdata: "
                                  +str(tfit)+" "+str(tdata))
                ntfit.append(t)
            else:
                t1, t2 = sorted([t, abs(tp)-t])
                if t1 in ntfit or t2 in ntfit:
                    continue
                assert (t >= 0 and t < abs(tp)), "illegal t in tfit: "+str(t)
                if t1 in tdata:
                    ntfit.append(t1)
                elif t2 in tdata:
                    ntfit.append(t2)
                else:
                    raise ValueError("tfit incompatible with tdata: "
                                      +str(tfit)+" "+str(tdata))

        self.tfit = numpy.array(ntfit)
        self._abscissa = self.tfit


    #def __str__(self):
    #    ans = "{c.datatag}[a={c.a}"
    #    for f in ['b', 'dE', 's', 'tp']:
    #        ans += ', ' + f + '={c.' + f +'}'
    #    ans += ', tfit=[{t1}...{t2}]]'
    #    return ans.format(c=self, t1=self.tfit[0], t2=self.tfit[-1])

    def buildprior(self, prior, nterm=None):
        """
        """
        ##
        if nterm is None:
            nterm = (None, None)

        ## -- truncate priors based on number of energies available
        ntermx = [[],[]] ## -- store number of terms in each block
        #nidxx  = [[],[]] ## -- store indices of blocks being used
        for i in range(2):
            dEi = self.dE[i]
            ekl = retrieve_block_keys(prior,dEi)
            #print ekl
            self.esufx.append([])
            for eik in ekl:
              eik = self._priorkey(prior,eik) ## -- this will change when gvar updated
              #print 'prior',prior
              #print 'test',len(prior[eik]),eik,prior[eik]
              if prior[eik] is None:
               continue
              ntermx[i].append(len(prior[eik]))
              newsuf = '_'+eik.split('_')[1]
              if not(newsuf in self.esufx[i]):
                self.esufx[i].append(newsuf) ## -- store suffices for faster lookup

        newprior = _gvar.BufferDict()
        for i, (ai, bi, dEi) in enumerate(zip(self.a, self.b, self.dE)):
            for x in [ai, bi, dEi]:
                xkl = retrieve_block_keys(prior,x)
                for xk in xkl:
                 if prior[xk] is None:
                  continue
                 k = int(xk.split('_')[1])
                 xk = self._priorkey(prior,xk) ## -- this will change when gvar updated
                 #xk = self.basekey(prior, xk)
                 #print i,k
                 if k < len(ntermx[i]):
                  newprior[xk] = prior[xk][None:ntermx[i][k]]
                 else:
                  newprior[xk] = []
        return newprior

    def builddata(self, data):
        """ Assemble fit data from dictionary ``data``.
        Extracts parts of array ``data[self.datatag]`` that are needed for
        the fit, as specified by ``self.tp`` and ``self.tfit``. The entries
        in the (1-D) array ``data[self.datatag]`` are assumed to be
        |GVar|\s and correspond to the ``t``s in ``self.tdata``.
        """
        # tags = self.all_datatags
        # if self.othertags is not None:
        #     tags.extend(self.othertags)
        tdata = self.tdata
        tp = self.tp
        if tp is not None:
            pfac = math.copysign(1,tp)
            tp = abs(tp)
        ans = []
        for tag in self.all_datatags:
            odata = data[tag]
            ndata = []
            for t in self.tfit:
                idt = tdata.index(t)
                if tp is None or tp-t not in tdata or t == tp-t:
                    ndata.append(odata[idt])
                else:
                    idt_r = tdata.index(tp-t)
                    ndata.append(lsqfit.wavg([odata[idt], pfac*odata[idt_r]]))
            ans.append(ndata)
        fdata = numpy.array(ans[0]) if len(ans) == 1 else lsqfit.wavg(ans)
        return fdata

    def fitfcn(self, p, nterm=None, t=None):
        """ Return fit function for parameters ``p``. """
        #stime = time.time()
        if t is None:
            t = self.tfit
        if self.tp is None:
            tp_t = None
        elif self.tp >= 0:
            tp_t = self.tp - t
            pfac = 1
        else:
            tp_t = -self.tp - t
            pfac = -1
        if nterm is None:
            nterm = (None, None)
        ofac = (None if self.s[0] == 0.0 else self.s[0],
                (None if self.s[1] == 0.0 else self.s[1]*(-1)**t))
        ans = 0.0
        for _ai, _bi, _dEi, ofaci, esuf in zip(
            self.a, self.b, self.dE, ofac, self.esufx
            ):
            if _ai is None or _bi is None or _dEi is None or ofaci is None:
                continue
            einc = 0
            for sfx in esuf:
              ai = p[_ai+sfx]
              bi = p[_bi+sfx]
              dEi = p[_dEi+sfx]
              Ei = [x for x in dEi]
              einc += dEi[0]
              Ei[0] = einc
              #print numpy.cumsum(Ei)
              if tp_t is None:
                  exp_t = _gvar.exp(-t)
                  for aij, bij, sumdE in zip(ai, bi, numpy.cumsum(Ei)):
                      ans += ofaci * aij * bij * exp_t ** sumdE
              else:
                  exp_t = _gvar.exp(-t)
                  exp_tp_t = _gvar.exp(-tp_t)
                  for aij, bij, sumdE in zip(ai, bi, numpy.cumsum(Ei)):
                      ans += ofaci * aij * bij * (exp_t ** sumdE + pfac * exp_tp_t ** sumdE)
        #print "iteration time: ",time.time()-stime
        #if self.datatag == 's11' and random.randint(0,20) == 0:
        # print "parameters: "
        # for key in sorted(p):
        #  if not('aiai' in key):
        #   print key,p[key]
        # #print "datatag   : ",self.datatag
        # print "answer    : ",ans
        # if random.randint(0,100) == 100:
        #  raise ValueError("test stop")
        return ans

#    def testfitfcn(self, p, nterm=None, t=None):
#        """ Return fit function for parameters ``p``. """
#        if t is None:
#            t = self.tfit
#        if self.tp is None:
#            tp_t = None
#        elif self.tp >= 0:
#            tp_t = self.tp - t
#            pfac = 1
#        else:
#            tp_t = -self.tp - t
#            pfac = -1
#        if nterm is None:
#            nterm = (None, None)
#        ofac = (None if self.s[0] == 0.0 else self.s[0],
#                (None if self.s[1] == 0.0 else self.s[1]*(-1)**t))
#        ans = 0.0
#        for _ai, _bi, _dEi, ofaci in zip(
#            self.a, self.b, self.dE, ofac
#            ):
#            if _ai is None or _bi is None or _dEi is None or ofaci is None:
#                continue
#            #if ntermi is not None:
#            #    if ntermi == 0:
#            #        continue
#            #    ai = p[_ai][:ntermi]
#            #    bi = p[_bi][:ntermi]
#            #    dEi = p[_dEi][:ntermi]
#            #else:
#            _aikl = retrieve_block_keys(p, _ai) ## -- assume prior already trimmed, use all
#            _bikl = retrieve_block_keys(p, _bi)
#            _dEakl = retrieve_block_keys(p, _dEi)
#            for ak,bk,ek in zip(_aikl,_bikl,_dEakl):
#              ai = p[ak]
#              bi = p[bk]
#              dEi = p[ek]
#              #print 'a ',ak,ai
#              #print 'b ',bk,bi
#              #print 'dE',ek,dEi
#              if tp_t is None:
#                  exp_t = _gvar.exp(-t)
#                  for aij, bij, sumdE in zip(ai, bi, numpy.cumsum(dEi)):
#                      ans += ofaci * aij * bij * exp_t ** sumdE
#              else:
#                  exp_t = _gvar.exp(-t)
#                  exp_tp_t = _gvar.exp(-tp_t)
#                  #print "ofaci   ",ofaci
#                  #print "exp_t   ",exp_t
#                  #print "exp_tp_t",exp_tp_t
#                  #print "cumsum  ",numpy.cumsum(dEi)
#                  #print "pfac    ",pfac
#                  for aij, bij, sumdE in zip(ai, bi, numpy.cumsum(dEi)):
#                      #print aij,bij,sumdE
#                      #print exp_t ** sumdE
#                      #print pfac * exp_tp_t ** sumdE
#                      print ofaci * aij * bij * (exp_t ** sumdE + pfac * exp_tp_t ** sumdE)
#                  for aij, bij, sumdE in zip(ai, bi, numpy.cumsum(dEi)):
#                      ans += ofaci * aij * bij * (exp_t ** sumdE + pfac * exp_tp_t ** sumdE)
#        return ans

## -- 
class Corr3Adv(BaseModel):
    """
    Copy of Lepage's Corr3 with more specific functionality
    #
    Advanced Three-point correlators ``Gavb(t, T) = <b(T) V(t) a(0)>``.
    Correlations of diagonal elements more explicitly handled than generic case.
    |Corr3Adv| models the ``t`` dependence of a 3-point correlator
    ``Gavb(t, T)`` using ::
        Gavb(t, T) =
         sum_i,j san*an[i]*fn(Ean[i],t)*Vnn[i,j]*sbn*bn[j]*fn(Ebn[j],T-t)
        +sum_i,j san*an[i]*fn(Ean[i],t)*Vno[i,j]*sbo*bo[j]*fo(Ebo[j],T-t)
        +sum_i,j sao*ao[i]*fo(Eao[i],t)*Von[i,j]*sbn*bn[j]*fn(Ebn[j],T-t)
        +sum_i,j sao*ao[i]*fo(Eao[i],t)*Voo[i,j]*sbo*bo[j]*fo(Ebo[j],T-t)
    where ::
        fn(E, t) =  exp(-E*t) + exp(-E*(tp-t)) # tp>0 -- periodic
               or   exp(-E*t) - exp(-E*(-tp-t))# tp<0 -- anti-periodic
               or   exp(-E*t)                  # if tp is None (nonperiodic)
        fo(E, t) = (-1)**t * fn(E, t)
    """
    def __init__(
        self, datatag, T, tdata, tfit,
        gn, Vnn, a, b, dEa=None, dEb=None, sa=1., sb=1.,
        Vno=None, Von=None, go=None, Voo=None, transpose_V=False, symmetric_V=False,
        tpa=None, tpb=None,
        othertags=[]
        ):
        super(Corr3Adv, self).__init__(datatag, othertags)
        self.a = self._param(a)
        self.dEa = self._param(dEa)
        self.sa = self._param(sa, -1.)
        self.b = self._param(b)
        self.dEb = self._param(dEb)
        self.sb = self._param(sb, -1.)
        self.g = [gn, go]
        self.V = [[Vnn, Vno], [Von, Voo]]
        self.easufx = [[],[]]
        self.ebsufx = [[],[]]
        self.transpose_V = transpose_V
        self.symmetric_V = symmetric_V
        self.T = T
        self.tdata = list(tdata)
        self.tpa = tpa
        self.tpb = tpb
        # validate tfit
        ntfit = []
        for t in tfit:
            if t >= 0 and t <= T:
                ntfit.append(t)
        self.tfit = numpy.array(ntfit)
        self._abscissa = self.tfit

    def buildprior(self, prior, nterm=None):
        """
        turn priors into blocks based on input key
        keys blocked based on integer suffices following '_'s in prior key names
        states with missing gii block key will be ignored
        nterm argument is ignored but required for compatibility
        #
        Create fit prior by extracting relevant pieces of ``prior``.
        This routine does two things: 1) discard parts of ``prior``
        that are not needed in the fit; and 2) determine whether
        any of the parameters has a log-normal/sqrt-normal prior,
        in which case the logarithm/sqrt of the parameter appears in
        prior, rather than the parameter itself.
        The number of terms kept in each part of the fit is
        specified using ``nterm = (n, no)`` where ``n`` is the
        number of non-oscillating terms and ``no`` is the number
        of oscillating terms. Setting ``nterm = None`` keeps
        all terms.
        """
        ## -- resize from n(n-1)/2 rather than n(n+1)/2, but otherwise mostly same
        ##    matrix nesting must be indexed before passing
        def resize_sym(Vii, nterm, nblockk):
            if Vii is None:
              return None
            N = int(numpy.round((((8*len(Vii)+1)**0.5 - 1.)/2.)))
            #print "resize ",len(Vii),N,nterm[0][nblockk],nterm[1][nblockk]
            ans = []
            iterV = iter(Vii)
            for i in range(N):
                for j in range(i, N):
                    v = next(iterV)
                    #if ((nterm[0] is None or i < (nterm[0][nblockk]*(nterm[0][nblockk]-1))/2)
                    #    and (nterm[1] is None or j < (nterm[1][nblockk]*(nterm[1][nblockk]-1))/2)):
                    ans.append(v) ## -- no truncation at this time
            return numpy.array(ans)
        ans = _gvar.BufferDict()
        ntermx = [[],[]] ## -- store number of terms in each block
        nidxx  = [[],[]] ## -- store indices of blocks being used
        #nblockx = [] ## -- store total number of blocks for even/odd
        ## -- determined the number of blocks and terms within blocks to use
        for i in range(2):
            gii = self.g[i]
            gkl = retrieve_block_keys(prior,gii)
            #nblockx.append(len(gkl))
            for giik in gkl:
              if prior[giik] is None:
               continue
              #print giik,prior[giik]
              #print "ntermx",len(prior[giik])
              ntermx[i].append(len(prior[giik]))
              nidxx[i].append(int(giik.split('_')[1]))
        for i in range(2):
            ## -- diagonal elements separately
            gii = self.g[i]
            gkl = retrieve_block_keys(prior,gii)
            for giik in gkl:
             if prior[giik] is None:
              continue
             giik = self._priorkey(prior, giik)
             #giik = self.basekey(prior, giik)
             k = int(giik.split('_')[1])
             ans[giik] = prior[giik][slice(None, ntermx[i][k])]
            ## -- off diagonals
            for j in range(2):
                vij = self.V[i][j]
                if vij is None:
                    continue
                if self.symmetric_V and i < j:
                    continue ## -- ignore repeats for symmetric matrix
                vkl = retrieve_block_keys(prior,vij)
                #print 'vij',vij,vkl
                for vklk in vkl:
                 k = int(vklk.split('_')[1])
                 l = int(vklk.split('_')[2])
                 if not(k in nidxx[i]) or not(l in nidxx[j]):
                  continue
                 ## -- offdiagonal blocks should still be matrices
                 if k == l and i == j and self.symmetric_V:
                     ans[vklk] = resize_sym(prior[vklk], ntermx, k)
                 else:
                     ## -- be explicit, because Vij set to whatever if symmetric
                     if   vklk.split('_')[0][-2:] == 'no': 
                      nx = ntermx[0][k]
                      ny = ntermx[1][l]
                     elif vklk.split('_')[0][-2:] == 'on':
                      nx = ntermx[1][k]
                      ny = ntermx[0][l]
                     else:
                      nx = ntermx[i][k]
                      ny = ntermx[j][l]
                     ans[vklk] = prior[vklk][slice(None, nx), slice(None, ny)]
        for x in [self.a, self.dEa, self.b, self.dEb]:
            if (x is self.dEa) or (x is self.dEb):
             for i, xi in enumerate(x):
              xkl = retrieve_block_keys(prior, xi)
              for xk in xkl:
                 if prior[xk] is None:
                  continue
                 newsuf = '_'+xk.split('_')[1] ## -- store suffices for faster lookup
                 if   (x is self.dEa) and not(newsuf in self.easufx[i]):
                   self.easufx[i].append(newsuf)
                 elif (x is self.dEb) and not(newsuf in self.ebsufx[i]):
                   self.ebsufx[i].append(newsuf)
            for i, xi  in enumerate(x):
             if xi is not None:
              xkl = retrieve_block_keys(prior, xi)
              for xk in xkl:
                 if prior[xk] is None:
                  continue
                 xk = self._priorkey(prior, xk)
                 #xk = self.basekey(prior, xk)
                 k = int(xk.split('_')[1])
                 if not(k in nidxx[i]):
                  continue
                 ## -- here?
                 #print xk,ntermx[i][k],prior[xk][None:ntermx[i][k]]
                 #try:
                 # print 
                 # print ans
                 #except:
                 # pass
                 #ans[xk] = prior[xk][None:ntermx[i][k]]
                 ans[xk] = prior[xk]
        #print "build prior",ans
        return ans

    def builddata(self, data):
        """
        No change from version in Corr3
        #
        Assemble fit data from dictionary ``data``.
        Extracts parts of array ``data[self.datatag]`` that are needed for
        the fit, as specified by ``self.tfit``. The entries in the (1-D)
        array ``data[self.datatag]`` are assumed to be |GVar|\s and
        correspond to the ``t``s in ``self.tdata``.
        """
        # tags = [self.datatag]
        # if self.othertags is not None:
        #     tags.extend(self.othertags)
        ans = []
        for tag in self.all_datatags:
            odata = data[tag]
            tdata = self.tdata
            ndata = []
            for t in self.tfit:
                idt = tdata.index(t)
                ndata.append(odata[idt])
            ans.append(ndata)
        return numpy.array(ans[0]) if len(ans) == 1 else lsqfit.wavg(ans)

    def fitfcn(self, p, nterm=None, t=None):
        """ Return fit function for parameters ``p``. """
        #stime = time.time()
        # setup
        #print "iteration parameters: ",p
        #print "variables: ",p['logEo_0'],p['aiaigo_0']
        if t is None:
            t = self.tfit
        ta = t
        tb = self.T - t
        if self.tpa is None:
            tp_ta = None
        elif self.tpa >= 0:
            tp_ta = self.tpa - ta
            pafac = 1
        else:
            tp_ta = -self.tpa - ta
            pafac = -1
        #
        if self.tpb is None:
            tp_tb = None
        elif self.tpb >= 0:
            tp_tb = self.tpb - tb
            pbfac = 1
        else:
            tp_tb = -self.tpb - tb
            pbfac = -1
        nidxx = [[],[]]

        # initial and final propagators
        aprop = []  # aprop[i][k][l] i= n or o; k=block; l=excitation level
        ofac = (self.sa[0], (0.0 if self.sa[1] == 0.0 else self.sa[1]*(-1)**ta))
        for i, (_ai, _dEai, ofaci, easuf) in enumerate(zip(self.a, self.dEa, ofac, self.easufx)):
            if _ai is None:
                aprop.append(None)
                continue
            aprop.append([])
            eainc = 0
            for asuf in easuf:
              k = int(asuf.split('_')[1])
              nidxx[i].append(k) ## -- store for later
              ans = []
              ai =  p[_ai+asuf]
              dEai = p[_dEai+asuf]
              Eai = [x for x in dEai]
              eainc += dEai[0]
              Eai[0] = eainc
              if tp_ta is None:
                  exp_ta = _gvar.exp(-ta)
                  ans = [
                      ofaci * aij * exp_ta ** sumdE
                      for aij, sumdE in zip(ai, numpy.cumsum(Eai))
                      ]
              else:
                  exp_ta = _gvar.exp(-ta)
                  exp_tp_ta = _gvar.exp(-tp_ta)
                  ans = [
                      ofaci * aij * (exp_ta ** sumdE + pafac * exp_tp_ta ** sumdE)
                      for aij, sumdE in zip(ai, numpy.cumsum(Eai))
                      ]
              aprop[i].append(ans)
        bprop = []
        ofac = (self.sb[0], (0.0 if self.sb[1] == 0.0 else self.sb[1]*(-1)**tb))
        for i, (_bi, _dEbi, ofaci, ebsuf) in enumerate(zip(self.b, self.dEb, ofac, self.ebsufx)):
            if _bi is None:
                bprop.append(None)
                continue
            bprop.append([])
            ebinc = 0
            for bsuf in ebsuf:
              ans = []
              bi = p[_bi+bsuf]
              dEbi = p[_dEbi+bsuf]
              Ebi = [x for x in dEbi]
              ebinc += dEbi[0]
              Ebi[0] = ebinc
              if tp_tb is None:
                  exp_tb = _gvar.exp(-tb)
                  ans = [
                      ofaci * bij * exp_tb ** sumdE
                      for bij, sumdE in zip(bi, numpy.cumsum(Ebi))
                      ]
              else:
                  exp_tb = _gvar.exp(-tb)
                  exp_tp_tb = _gvar.exp(-tp_tb)
                  ans = [
                      ofaci * bij * (exp_tb ** sumdE + pbfac * exp_tp_tb ** sumdE)
                      for bij, sumdE in zip(bi, numpy.cumsum(Ebi))
                      ]
              bprop[i].append(ans)

        # combine propagators with vertices
        ans = 0.0
        for i, (apropi, Vi, easuf) in enumerate(zip(aprop, self.V, self.easufx)):
            if apropi is None:
                continue
            for j, (bpropj, Vij, ebsuf) in enumerate(zip(bprop, Vi, self.ebsufx)):
              if bpropj is None or Vij is None:
                continue
              if self.symmetric_V and i > j:
                eaxsuf = ebsuf
                ebxsuf = easuf
              else:
                eaxsuf = easuf
                ebxsuf = ebsuf
              for ix,(asuf,ak) in enumerate(zip(eaxsuf,apropi)):
               for jx,(bsuf,bl) in enumerate(zip(ebxsuf,bpropj)):
                try:
                 if self.symmetric_V and i > j:
                  V = numpy.transpose(p[Vij+bsuf+asuf])
                 else:
                  V = p[Vij+asuf+bsuf]
                except KeyError:
                 ## -- probably truncated away
                 #print "keyerror: ",Vij+asuf+bsuf
                 continue
                if asuf == bsuf and i == j and self.symmetric_V:
                    # unpack symmetric matrix V
                    gii = self.g[i] +asuf
                    if not(gii in p):
                     continue ## -- number of 3pt states != number of 2pt states
                    g = p[gii]
                    k = int(asuf.split('_')[1])
                    Vsz = int(numpy.round(numpy.sqrt(1+8*len(V)))-1)/2 +1
                    na = min(len(apropi[k]),Vsz)
                    nb = min(len(bpropj[k]),Vsz)
                    assert na == nb, \
                        "Vnn/Voo must be square matrix if symmetric"
                    iterV = iter(V)
                    V = numpy.empty((na, nb), dtype=V.dtype)
                    for m in range(na):
                        for n in range(m, nb):
                            if m == n:
                              if m == 0:
                                V[m, m] = g[0]
                              else:
                                V[m, m] = g[0] + g[m]
                            else:
                              V[m, n] = next(iterV)
                              V[n, m] = V[m, n]

                for akm, Vkm in zip(ak, V):
                    acc = 0.0
                    for bln, Vln in zip(bl, Vkm):
                        acc += Vln*bln
                    ans += akm*acc
        #print "iteration time: ",time.time()-stime
        return ans

## -- 
class Corr3Static(BaseModel):
    """
    #
    Three-point correlators ``Gavb(t, T) = <b(T) V(t) a(0)>`` with mostly fixed spectrum.
    Correlations of diagonal elements more explicitly handled than generic case.
    |Corr3Adv| models the ``t`` dependence of a 3-point correlator
    ``Gavb(t, T)`` using ::
        Gavb(t, T) =
         sum_i,j san*an[i]*fn(Ean[i],t)*Vnn[i,j]*sbn*bn[j]*fn(Ebn[j],T-t)
        +sum_i,j san*an[i]*fn(Ean[i],t)*Vno[i,j]*sbo*bo[j]*fo(Ebo[j],T-t)
        +sum_i,j sao*ao[i]*fo(Eao[i],t)*Von[i,j]*sbn*bn[j]*fn(Ebn[j],T-t)
        +sum_i,j sao*ao[i]*fo(Eao[i],t)*Voo[i,j]*sbo*bo[j]*fo(Ebo[j],T-t)
    where ::
        fn(E, t) =  exp(-E*t) + exp(-E*(tp-t)) # tp>0 -- periodic
               or   exp(-E*t) - exp(-E*(-tp-t))# tp<0 -- anti-periodic
               or   exp(-E*t)                  # if tp is None (nonperiodic)
        fo(E, t) = (-1)**t * fn(E, t)
    """
    def __init__(
        self, datatag, T, tdata, tfit,
        gn, Vnn, a, b, dEa=None, dEb=None, sa=1., sb=1.,
        Vno=None, Von=None, go=None, Voo=None, transpose_V=False, symmetric_V=False,
        tpa=None, tpb=None,
        othertags=[]
        ):
        super(Corr3Adv, self).__init__(datatag, othertags)
        self.a = self._param(a)
        self.dEa = self._param(dEa)
        self.sa = self._param(sa, -1.)
        self.b = self._param(b)
        self.dEb = self._param(dEb)
        self.sb = self._param(sb, -1.)
        self.g = [gn, go]
        self.V = [[Vnn, Vno], [Von, Voo]]
        self.easufx = [[],[]]
        self.ebsufx = [[],[]]
        self.transpose_V = transpose_V
        self.symmetric_V = symmetric_V
        self.T = T
        self.tdata = list(tdata)
        self.tpa = tpa
        self.tpb = tpb
        # validate tfit
        ntfit = []
        for t in tfit:
            if t >= 0 and t <= T:
                ntfit.append(t)
        self.tfit = numpy.array(ntfit)
        self._abscissa = self.tfit

    def buildprior(self, prior, nterm=None):
        """
        turn priors into blocks based on input key
        keys blocked based on integer suffices following '_'s in prior key names
        states with missing gii block key will be ignored
        nterm argument is ignored but required for compatibility
        #
        Create fit prior by extracting relevant pieces of ``prior``.
        This routine does two things: 1) discard parts of ``prior``
        that are not needed in the fit; and 2) determine whether
        any of the parameters has a log-normal/sqrt-normal prior,
        in which case the logarithm/sqrt of the parameter appears in
        prior, rather than the parameter itself.
        The number of terms kept in each part of the fit is
        specified using ``nterm = (n, no)`` where ``n`` is the
        number of non-oscillating terms and ``no`` is the number
        of oscillating terms. Setting ``nterm = None`` keeps
        all terms.
        """
        ## -- resize from n(n-1)/2 rather than n(n+1)/2, but otherwise mostly same
        ##    matrix nesting must be indexed before passing
        def resize_sym(Vii, nterm, nblockk):
            if Vii is None:
              return None
            N = int(numpy.round((((8*len(Vii)+1)**0.5 - 1.)/2.)))
            #print "resize ",len(Vii),N,nterm[0][nblockk],nterm[1][nblockk]
            ans = []
            iterV = iter(Vii)
            for i in range(N):
                for j in range(i, N):
                    v = next(iterV)
                    #if ((nterm[0] is None or i < (nterm[0][nblockk]*(nterm[0][nblockk]-1))/2)
                    #    and (nterm[1] is None or j < (nterm[1][nblockk]*(nterm[1][nblockk]-1))/2)):
                    ans.append(v) ## -- no truncation at this time
            return numpy.array(ans)
        ans = _gvar.BufferDict()
        ntermx = [[],[]] ## -- store number of terms in each block
        nidxx  = [[],[]] ## -- store indices of blocks being used
        #nblockx = [] ## -- store total number of blocks for even/odd
        ## -- determined the number of blocks and terms within blocks to use
        for i in range(2):
            gii = self.g[i]
            gkl = retrieve_block_keys(prior,gii)
            #nblockx.append(len(gkl))
            for giik in gkl:
              if prior[giik] is None:
               continue
              #print giik,prior[giik]
              #print "ntermx",len(prior[giik])
              ntermx[i].append(len(prior[giik]))
              nidxx[i].append(int(giik.split('_')[1]))
        for i in range(2):
            ## -- diagonal elements separately
            gii = self.g[i]
            gkl = retrieve_block_keys(prior,gii)
            for giik in gkl:
             if prior[giik] is None:
              continue
             giik = self._priorkey(prior, giik)
             #giik = self.basekey(prior, giik)
             k = int(giik.split('_')[1])
             ans[giik] = prior[giik][slice(None, ntermx[i][k])]
            ## -- off diagonals
            for j in range(2):
                vij = self.V[i][j]
                if vij is None:
                    continue
                if self.symmetric_V and i < j:
                    continue ## -- ignore repeats for symmetric matrix
                vkl = retrieve_block_keys(prior,vij)
                #print 'vij',vij,vkl
                for vklk in vkl:
                 k = int(vklk.split('_')[1])
                 l = int(vklk.split('_')[2])
                 if not(k in nidxx[i]) or not(l in nidxx[j]):
                  continue
                 ## -- offdiagonal blocks should still be matrices
                 if k == l and i == j and self.symmetric_V:
                     ans[vklk] = resize_sym(prior[vklk], ntermx, k)
                 else:
                     ## -- be explicit, because Vij set to whatever if symmetric
                     if   vklk.split('_')[0][-2:] == 'no': 
                      nx = ntermx[0][k]
                      ny = ntermx[1][l]
                     elif vklk.split('_')[0][-2:] == 'on':
                      nx = ntermx[1][k]
                      ny = ntermx[0][l]
                     else:
                      nx = ntermx[i][k]
                      ny = ntermx[j][l]
                     ans[vklk] = prior[vklk][slice(None, nx), slice(None, ny)]
        for x in [self.a, self.dEa, self.b, self.dEb]:
            if (x is self.dEa) or (x is self.dEb):
             for i, xi in enumerate(x):
              xkl = retrieve_block_keys(prior, xi)
              for xk in xkl:
                 if prior[xk] is None:
                  continue
                 newsuf = '_'+xk.split('_')[1] ## -- store suffices for faster lookup
                 if   (x is self.dEa) and not(newsuf in self.easufx[i]):
                   self.easufx[i].append(newsuf)
                 elif (x is self.dEb) and not(newsuf in self.ebsufx[i]):
                   self.ebsufx[i].append(newsuf)
            for i, xi  in enumerate(x):
             if xi is not None:
              xkl = retrieve_block_keys(prior, xi)
              for xk in xkl:
                 if prior[xk] is None:
                  continue
                 xk = self._priorkey(prior, xk)
                 #xk = self.basekey(prior, xk)
                 k = int(xk.split('_')[1])
                 if not(k in nidxx[i]):
                  continue
                 ## -- here?
                 #print xk,ntermx[i][k],prior[xk][None:ntermx[i][k]]
                 #try:
                 # print 
                 # print ans
                 #except:
                 # pass
                 #ans[xk] = prior[xk][None:ntermx[i][k]]
                 ans[xk] = prior[xk]
        #print "build prior",ans
        return ans

    def builddata(self, data):
        """
        No change from version in Corr3
        #
        Assemble fit data from dictionary ``data``.
        Extracts parts of array ``data[self.datatag]`` that are needed for
        the fit, as specified by ``self.tfit``. The entries in the (1-D)
        array ``data[self.datatag]`` are assumed to be |GVar|\s and
        correspond to the ``t``s in ``self.tdata``.
        """
        # tags = [self.datatag]
        # if self.othertags is not None:
        #     tags.extend(self.othertags)
        ans = []
        for tag in self.all_datatags:
            odata = data[tag]
            tdata = self.tdata
            ndata = []
            for t in self.tfit:
                idt = tdata.index(t)
                ndata.append(odata[idt])
            ans.append(ndata)
        return numpy.array(ans[0]) if len(ans) == 1 else lsqfit.wavg(ans)

    def fitfcn(self, p, nterm=None, t=None):
        """ Return fit function for parameters ``p``. """
        #stime = time.time()
        # setup
        #print "iteration parameters: ",p
        #print "variables: ",p['logEo_0'],p['aiaigo_0']
        if t is None:
            t = self.tfit
        ta = t
        tb = self.T - t
        if self.tpa is None:
            tp_ta = None
        elif self.tpa >= 0:
            tp_ta = self.tpa - ta
            pafac = 1
        else:
            tp_ta = -self.tpa - ta
            pafac = -1
        #
        if self.tpb is None:
            tp_tb = None
        elif self.tpb >= 0:
            tp_tb = self.tpb - tb
            pbfac = 1
        else:
            tp_tb = -self.tpb - tb
            pbfac = -1
        nidxx = [[],[]]

        # initial and final propagators
        aprop = []  # aprop[i][k][l] i= n or o; k=block; l=excitation level
        ofac = (self.sa[0], (0.0 if self.sa[1] == 0.0 else self.sa[1]*(-1)**ta))
        for i, (_ai, _dEai, ofaci, easuf) in enumerate(zip(self.a, self.dEa, ofac, self.easufx)):
            if _ai is None:
                aprop.append(None)
                continue
            aprop.append([])
            eainc = 0
            for asuf in easuf:
              k = int(asuf.split('_')[1])
              nidxx[i].append(k) ## -- store for later
              ans = []
              ai =  p[_ai+asuf]
              dEai = p[_dEai+asuf]
              Eai = [x for x in dEai]
              eainc += dEai[0]
              Eai[0] = eainc
              if tp_ta is None:
                  exp_ta = _gvar.exp(-ta)
                  ans = [
                      ofaci * aij * exp_ta ** sumdE
                      for aij, sumdE in zip(ai, numpy.cumsum(Eai))
                      ]
              else:
                  exp_ta = _gvar.exp(-ta)
                  exp_tp_ta = _gvar.exp(-tp_ta)
                  ans = [
                      ofaci * aij * (exp_ta ** sumdE + pafac * exp_tp_ta ** sumdE)
                      for aij, sumdE in zip(ai, numpy.cumsum(Eai))
                      ]
              aprop[i].append(ans)
        bprop = []
        ofac = (self.sb[0], (0.0 if self.sb[1] == 0.0 else self.sb[1]*(-1)**tb))
        for i, (_bi, _dEbi, ofaci, ebsuf) in enumerate(zip(self.b, self.dEb, ofac, self.ebsufx)):
            if _bi is None:
                bprop.append(None)
                continue
            bprop.append([])
            ebinc = 0
            for bsuf in ebsuf:
              ans = []
              bi = p[_bi+bsuf]
              dEbi = p[_dEbi+bsuf]
              Ebi = [x for x in dEbi]
              ebinc += dEbi[0]
              Ebi[0] = ebinc
              if tp_tb is None:
                  exp_tb = _gvar.exp(-tb)
                  ans = [
                      ofaci * bij * exp_tb ** sumdE
                      for bij, sumdE in zip(bi, numpy.cumsum(Ebi))
                      ]
              else:
                  exp_tb = _gvar.exp(-tb)
                  exp_tp_tb = _gvar.exp(-tp_tb)
                  ans = [
                      ofaci * bij * (exp_tb ** sumdE + pbfac * exp_tp_tb ** sumdE)
                      for bij, sumdE in zip(bi, numpy.cumsum(Ebi))
                      ]
              bprop[i].append(ans)

        # combine propagators with vertices
        ans = 0.0
        for i, (apropi, Vi, easuf) in enumerate(zip(aprop, self.V, self.easufx)):
            if apropi is None:
                continue
            for j, (bpropj, Vij, ebsuf) in enumerate(zip(bprop, Vi, self.ebsufx)):
              if bpropj is None or Vij is None:
                continue
              if self.symmetric_V and i > j:
                eaxsuf = ebsuf
                ebxsuf = easuf
              else:
                eaxsuf = easuf
                ebxsuf = ebsuf
              for ix,(asuf,ak) in enumerate(zip(eaxsuf,apropi)):
               for jx,(bsuf,bl) in enumerate(zip(ebxsuf,bpropj)):
                try:
                 if self.symmetric_V and i > j:
                  V = numpy.transpose(p[Vij+bsuf+asuf])
                 else:
                  V = p[Vij+asuf+bsuf]
                except KeyError:
                 ## -- probably truncated away
                 #print "keyerror: ",Vij+asuf+bsuf
                 continue
                if asuf == bsuf and i == j and self.symmetric_V:
                    # unpack symmetric matrix V
                    gii = self.g[i] +asuf
                    if not(gii in p):
                     continue ## -- number of 3pt states != number of 2pt states
                    g = p[gii]
                    k = int(asuf.split('_')[1])
                    Vsz = int(numpy.round(numpy.sqrt(1+8*len(V)))-1)/2 +1
                    na = min(len(apropi[k]),Vsz)
                    nb = min(len(bpropj[k]),Vsz)
                    assert na == nb, \
                        "Vnn/Voo must be square matrix if symmetric"
                    iterV = iter(V)
                    V = numpy.empty((na, nb), dtype=V.dtype)
                    for m in range(na):
                        for n in range(m, nb):
                            if m == n:
                              if m == 0:
                                V[m, m] = g[0]
                              else:
                                V[m, m] = g[0] + g[m]
                            else:
                              V[m, n] = next(iterV)
                              V[n, m] = V[m, n]

                for akm, Vkm in zip(ak, V):
                    acc = 0.0
                    for bln, Vln in zip(bl, Vkm):
                        acc += Vln*bln
                    ans += akm*acc
        #print "iteration time: ",time.time()-stime
        return ans
