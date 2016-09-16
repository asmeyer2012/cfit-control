import lsqfit as lsq
import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines as df

def plot_corr_effective_mass(models,data,fit=None,**kwargs):
 """
 Get all data ready so that it can be plotted on command
 Allows for dynamic cycling through plots
 """
 _emNMod = len(models)
 _emIdx = [0] ## -- index of plotted function, in array so it can be modified in functions
 ## -- objects to hold all plot data
 ##  - Dat/Fit refers to the correlator data or the fit function
 ##  - Central/Error are the central value and errors
 _emLogRatio        = []
 _emLogRatioCentral = []
 _emLogRatioError   = []
 _emLogRatioFit     = []
 _emFoldRatio       = []
 _emFoldRatioCentral= []
 _emFoldRatioError  = []
 _emFoldRatioFit    = []
 _emRatioFit        = []
 _emRatioFitNonZero = []
 _emFitCentral      = []
 _emFitError        = []
 ## -- timeslice objects
 _emTPosRatio    = []
 _emTPosFit      = []
 _emTPosFold     = []
 _emTPosFoldFit  = []
 #
 ## -- fitting options
 _emFitMin = 0
 _emFitMax = 0
 _emSep    = 0
 fig,ax = plt.subplots(1)
 #
 ## -- setup plot function
 def do_plot_corr_effective_mass(idx,fig=fig):
   fig.clear()
   ax = fig.add_subplot(111)
   key = models[idx[0]].datatag
   ax.set_ylim(utp.get_option("y_limit",[0.0,2.0],**kwargs[key]))
   #
   # -- plot correlator data
   if utp.get_option("meff_do_fold",False,**kwargs[key]):
    ## -- plot fit
    ax.plot([t for t in _emTPosFit[idx[0]] if t < len(_emTData)/2],_emFitCentral[idx[0]],
     color=utp.get_option("color3",'b',**kwargs[key]))
    ax.plot([t for t in _emTPosFit[idx[0]] if t < len(_emTData)/2],_emFitError[idx[0]][0],
     color=utp.get_option("color3",'b',**kwargs[key]),
     ls=utp.get_option("linestyle2",'--',**kwargs[key]))
    ax.plot([t for t in _emTPosFit[idx[0]] if t < len(_emTData)/2],_emFitError[idx[0]][1],
     color=utp.get_option("color3",'b',**kwargs[key]),
     ls=utp.get_option("linestyle2",'--',**kwargs[key]))
    ## -- _emTPosRatio not necessarily symmetric, get times correct
    ax.errorbar(_emTPosFold[idx[0]],_emFoldRatioCentral[idx[0]],yerr=_emFoldRatioError[idx[0]],
     mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
     mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
     color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
     ls=utp.get_option("linestyle1",'None',**kwargs[key]),
     marker=utp.get_option("marker1",'o',**kwargs[key]),
     ms=utp.get_option("markersize",6,**kwargs[key]))
    ax.scatter(_emTPosFoldFit[idx[0]],gv.mean(_emFoldRatioFit[idx[0]]),
     color=utp.get_option("color1",'r',**kwargs[key]),
     marker=utp.get_option("marker",'o',**kwargs[key]),
     s=utp.get_option("markersize",36,**kwargs[key]))
   else:
    ## -- plot fit
    ax.plot(_emTPosFit[idx[0]],_emFitCentral[idx[0]],
     color=utp.get_option("color3",'b',**kwargs[key]))
    ax.plot(_emTPosFit[idx[0]],_emFitError[idx[0]][0],
     color=utp.get_option("color3",'b',**kwargs[key]),
     ls=utp.get_option("linestyle2",'--',**kwargs[key]))
    ax.plot(_emTPosFit[idx[0]],_emFitError[idx[0]][1],
     color=utp.get_option("color3",'b',**kwargs[key]),
     ls=utp.get_option("linestyle2",'--',**kwargs[key]))
    ## -- 
    ax.errorbar(_emTPosRatio[idx[0]],_emLogRatioCentral[idx[0]],yerr=_emLogRatioError[idx[0]],
     mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
     mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
     color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
     ls=utp.get_option("linestyle1",'None',**kwargs[key]),
     marker=utp.get_option("marker1",'o',**kwargs[key]),
     ms=utp.get_option("markersize",6,**kwargs[key]))
    ax.scatter(_emTPosFit[idx[0]],gv.mean(_emLogRatioFit[idx[0]]),
     color=utp.get_option("color1",'r',**kwargs[key]),
     marker=utp.get_option("marker",'o',**kwargs[key]),
     s=utp.get_option("markersize",36,**kwargs[key]))
   fig.suptitle(utp.get_option("plottitleem",str(idx[0])+" default title "+str(key),**kwargs[key]),
    fontsize=utp.get_option("titlesize",20,**kwargs[key]))
   # -- modify some options 
   ax.set_xlabel(r'$t$')
   ax.set_ylabel(utp.get_option("yaxistitle",
    r"$-\frac{1}{"+str(_emSep)+r"}\,log\frac{C(t+"+str(_emSep)+r")}{C(t)}$",**kwargs[key]))
   for item in ([ax.xaxis.label,ax.yaxis.label]):
    # must be after setting label content (LaTeX ruins it)
    item.set_fontsize(fontsize=utp.get_option("fontsize",20,**kwargs[key]))
   rect =fig.patch
   rect.set_facecolor('white')
   if utp.get_option("to_file",False,**kwargs[key]):
    save_dir  = utp.get_option("em_save_dir","./plotdump",**kwargs[key])
    save_name = utp.get_option("em_save_name","emplot-"+key+".pdf",**kwargs[key])
    plt.savefig(save_dir+'/'+save_name)
   if utp.get_option("to_terminal",True,**kwargs[key]):
    plt.draw()
   pass
 #
 ## -- setup button press action function
 def press_effective_mass(event,idx=_emIdx):
   #print('press_effective_mass', event.key)
   try:
     ## -- manually indicate index
     idx[0] = int(event.key) + (idx[0])*10
   except ValueError:
     if event.key==' ': ## -- space
       ## -- allows for replotting when changing index by typing number keys
       idx[0] = idx[0] % _emNMod
       do_plot_corr_effective_mass(idx)
     elif event.key=='left':
       idx[0] = (idx[0] - 1) % _emNMod
       do_plot_corr_effective_mass(idx)
     elif event.key=='right':
       idx[0] = (idx[0] + 1) % _emNMod
       do_plot_corr_effective_mass(idx)
     elif event.key=='backspace':
       ## -- reset index so can manually flip through using number keys
       idx[0] = 0
     elif event.key=='d':
       ## -- dump plots into ./plotdump directory
       for ix,model in zip(range(len(models)),models):
         key = model.datatag
         save_dir  = utp.get_option("em_save_dir","./plotdump",**kwargs[key])
         save_name = utp.get_option("em_save_name","emplot-"+key+".png",**kwargs[key])
         do_plot_corr_effective_mass([ix])
         plt.savefig(save_dir+'/'+save_name)
       do_plot_corr_effective_mass(idx)
 #
 ## -- 
 fig.canvas.mpl_connect('key_press_event',press_effective_mass)
 ## -- save plot data
 for idx,model in zip(range(len(models)),models):
   key = model.datatag
   ## -- parameters used in fitting
   ##    default = 2
   _emSep    = utp.get_option("meff_sep",2,**kwargs[key])
   ##    default = smallest t not included in fit
   _emFitMin = utp.get_option("meff_fit_min",model.tfit[-1]+1,**kwargs[key])
   ##    default = midpoint - sep
   _emFitMax = utp.get_option("meff_fit_max",
     model.tdata[-1]/2-_emSep-int(model.tdata[-1]/12),**kwargs[key])
   _emTData = model.tdata
   _emTFit = range(_emFitMin,_emFitMax)
   _emTFit = np.append(_emTFit,list(sorted([len(_emTData) - t for t in _emTFit])))
   _emTDataNonZero = [t for t in _emTData if np.abs(gv.mean(data[key])[t]) > 1e-20]
   #
   ## -- data
   _emTDataRatio =\
    [t for t in _emTData
    if (t in _emTDataNonZero) and (t <= _emTData[-1]/2 +1 - _emSep) ]   # first half
   _emTDataRatio = np.append(_emTDataRatio,
    [t for t in _emTData
    if (t in _emTDataNonZero) and (t >= _emTData[-1]/2 +1 + _emSep) ] ) # second half
   _emRatio =\
    [data[key][t+_emSep]/data[key][t] for t in _emTData
    if (t in _emTDataNonZero) and (t <= _emTData[-1]/2 +1 - _emSep) ]   # first half
   _emRatio = np.append(_emRatio,
    [data[key][t-_emSep]/data[key][t] for t in _emTData
    if (t in _emTDataNonZero) and (t >= _emTData[-1]/2 +1 + _emSep) ] ) # second half
   ## -- times
   _emTPosRatio.append(
    [_emTDataRatio[t] for t in range(len(_emTDataRatio)) if _emRatio[t] > 0] )
   _emTPosFit.append(
    [_emTDataRatio[t] for t in range(len(_emTDataRatio))
    if _emRatio[t] > 0 and _emTDataRatio[t] in _emTFit] )
   ## -- ratios 
   _emLogRatio.append(
    [-gv.log(_emRatio[t])/_emSep for t in range(len(_emTDataRatio)) if _emRatio[t] > 0] )
   _emLogRatioFit.append(
    [-gv.log(_emRatio[t])/_emSep for t in range(len(_emTDataRatio))
    if (gv.mean(_emRatio[t]) > 0) and (_emTDataRatio[t] in _emTPosFit[-1])] )
   # -- folding
   _emFoldRatio.append(list())
   _emFoldRatioFit.append(list())
   _emTPosFold.append(list())
   _emTPosFoldFit.append(list())
   for t in range(1,len(_emTData)/2):
    if not(t in _emTPosRatio[-1]) or not(len(_emTData)-t in _emTPosRatio[-1]):
     continue
    _emFoldRatio[-1].append((_emLogRatio[-1][list(_emTPosRatio[-1]).index(t)]
      +_emLogRatio[-1][list(_emTPosRatio[-1]).index(len(_emTData)-t)])/2)
    _emTPosFold[-1].append(t)
    if not(t in _emTPosFit[-1]) or not(len(_emTData)-t in _emTPosFit[-1]):
     continue
    _emFoldRatioFit[-1].append((_emLogRatio[-1][list(_emTPosRatio[-1]).index(t)]
      +_emLogRatio[-1][list(_emTPosRatio[-1]).index(len(_emTData)-t)])/2)
    _emTPosFoldFit[-1].append(t)
   for t in range(len(_emTPosFold[-1])):
    print t,_emTPosFold[-1][t],_emFoldRatio[-1][t]
   for t in range(len(_emTPosFoldFit[-1])):
    print t,_emTPosFoldFit[-1][t],_emFoldRatioFit[-1][t]
   _emLogRatioCentral.append(gv.mean(_emLogRatio[-1]))
   _emLogRatioError.append([ list(gv.sdev(_emLogRatio[-1])), list(gv.sdev(_emLogRatio[-1])) ])
   _emFoldRatioCentral.append(gv.mean(_emFoldRatio[-1]))
   _emFoldRatioError.append([ list(gv.sdev(_emFoldRatio[-1])), list(gv.sdev(_emFoldRatio[-1])) ])
   ## -- fit
   _emRatioFit.append(lsq.wavg(_emLogRatioFit[-1]))
   if utp.get_option("meff_do_fold",False,**kwargs[key]):
    _emFitCentral.append([gv.mean(_emRatioFit[-1]) for t in _emTPosFit[-1] if t < len(_emTData)/2])
    _emFitError.append(
     [list(np.array(_emFitCentral[-1])-np.array([gv.sdev(_emRatioFit[-1])
       for t in _emTPosFit[-1] if t < len(_emTData)/2])),
      list(np.array(_emFitCentral[-1])+np.array([gv.sdev(_emRatioFit[-1])
        for t in _emTPosFit[-1] if t < len(_emTData)/2]))])
   else:
    _emFitCentral.append([gv.mean(_emRatioFit[-1]) for t in _emTPosFit[-1]])
    _emFitError.append(
     [list(np.array(_emFitCentral[-1])-np.array([gv.sdev(_emRatioFit[-1])
       for t in _emTPosFit[-1]])),
      list(np.array(_emFitCentral[-1])+np.array([gv.sdev(_emRatioFit[-1])
        for t in _emTPosFit[-1]]))])
 print "Best plateau fits: "
 for key,rfit in zip([model.datatag for model in models],_emRatioFit):
  print "  ",key," : ",rfit
 print "   ----------------- "
 _emRatioFitNonZero = [x for x in _emRatioFit if not(x is None)]
 print "   avg  : ",lsq.wavg(_emRatioFitNonZero)

 ## -- done saving data
 if not(utp.get_option("to_terminal",True,**kwargs[key])) and\
    utp.get_option("to_file",False,**kwargs[key]):
  for ix in range(len(models)):
    ## -- loops and saves all without creating window
    do_plot_corr_effective_mass([ix])
 else:
  do_plot_corr_effective_mass(_emIdx)
