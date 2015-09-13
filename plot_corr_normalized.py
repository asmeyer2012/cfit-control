import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines as df

def plot_corr_normalized(models,data,fit,**kwargs):
 """
 Get all data ready so that it can be plotted on command
 Allows for dynamic cycling through plots
 """
 _fnNMod = len(models)
 _fnIdx = [0] ## -- index of plotted function, in array so it can be modified in functions
 ## -- objects to hold all plot data
 ##  - Dat/Fit refers to the correlator data or the fit function
 ##  - Central/Error are the central value and errors
 _fnDatCentral = []
 _fnDatError   = []
 _fnFitOnes    = []
 _fnFitError   = []
 #
 ## -- other objects
 _fnTDataNonZero = []
 _fnTFitNonZero  = []
 _fnTData        = []
 _fnTFit         = []
 _fnTRem         = [] # number of previous timeslices removed
 fig,ax = plt.subplots(1)
 #
 ## -- setup plot function
 def do_plot_normalized(idx,fig=fig):
   fig.clear()
   ax = fig.add_subplot(111)
   key = models[idx[0]].datatag

   ax.set_ylim(utp.get_option("y_limit",[0.2,1.8],**kwargs[key]))
   #
   ## -- plot fit
   ax.plot(_fnTDataNonZero[idx[0]],_fnFitOnes[idx[0]],
    color=utp.get_option("color2",'b',**kwargs[key]))
   ax.plot(_fnTDataNonZero[idx[0]],_fnFitError[idx[0]][0],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   ax.plot(_fnTDataNonZero[idx[0]],_fnFitError[idx[0]][1],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   ## -- plot correlator data
   ax.errorbar(_fnTDataNonZero[idx[0]],_fnDatCentral[idx[0]],yerr=_fnDatError[idx[0]],
    mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
    mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    ls=utp.get_option("linestyle1",'None',**kwargs[key]),
    marker=utp.get_option("marker1",'o',**kwargs[key]),
    ms=utp.get_option("markersize",6,**kwargs[key]))
   ax.scatter(_fnTFitNonZero[idx[0]],
    [ _fnDatCentral[idx[0]][t] for t in
    list(np.array(_fnTFitNonZero[idx[0]])-np.array(_fnTRem[idx[0]])) ],
    color=utp.get_option("color1",'r',**kwargs[key]),
    marker=utp.get_option("marker",'o',**kwargs[key]),
    s=utp.get_option("markersize",36,**kwargs[key]))
   fig.suptitle(utp.get_option("plottitle",str(idx[0])+" default title "+str(key),**kwargs[key]),
    fontsize=utp.get_option("titlesize",20,**kwargs[key]))
   ## -- modify some options 
   ax.set_xlabel(r'$t$ slice')
   ax.set_ylabel(utp.get_option("yaxistitle",r"$C(t)/C_{fit}(t)$",**kwargs[key]))
   for item in ([ax.xaxis.label,ax.yaxis.label]):
    # must be after setting label content (LaTeX ruins it)
    item.set_fontsize(fontsize=utp.get_option("fontsize",20,**kwargs[key]))
   rect =fig.patch
   rect.set_facecolor('white')
   plt.draw()
   pass
 #
 ## -- setup button press action function
 def press_normalized(event,idx=_fnIdx):
   #print('press_normalized', event.key)
   try:
     ## -- manually indicate index
     idx[0] = int(event.key) + (idx[0])*10
   except ValueError:
     if event.key==' ': ## -- space
       ## -- allows for replotting when changing index by typing number keys
       idx[0] = idx[0] % _fnNMod
       do_plot_normalized(idx)
     elif event.key=='left':
       idx[0] = (idx[0] - 1) % _fnNMod
       do_plot_normalized(idx)
     elif event.key=='right':
       idx[0] = (idx[0] + 1) % _fnNMod
       do_plot_normalized(idx)
     elif event.key=='backspace':
       ## -- reset index so can manually flip through using number keys
       idx[0] = 0
 #
 ## -- 
 fig.canvas.mpl_connect('key_press_event',press_normalized)
 ## -- save plot data
 for idx,model in zip(range(len(models)),models):
   key = model.datatag
   _fnTData.append(model.tdata)
   _fnTFit.append(model.tfit)
   _fnTFit[-1] = np.append(_fnTFit[-1],list(sorted([len(_fnTData[-1]) - t for t in _fnTFit[-1]])))
   ## -- fit
   _fnFitFunc = utp.create_fit_func(model,fit)
   _fnFitMean = gv.mean(_fnFitFunc(_fnTData[-1]))
   _fnTDataNonZero.append([t for t in _fnTData[-1] if np.abs(_fnFitMean[t]) > 1e-20])
   _fnTFitNonZero.append([t for t in _fnTFit[-1] if np.abs(_fnFitMean[t]) > 1e-20])
   _fnTRem.append([(0 if np.abs(_fnFitMean[t]) > 1e-20 else 1) for t in model.tdata])
   _fnTRem[-1] = \
     [sum(_fnTRem[-1][:i+1]) for i in range(len(_fnTRem[-1])) if i in _fnTFitNonZero[-1]]
   _fnFitMean = gv.mean(_fnFitFunc(_fnTDataNonZero[-1]))
   _fnFitSdev = list(np.array(gv.sdev(_fnFitFunc(_fnTDataNonZero[-1])))/np.array(_fnFitMean))
   _fnFitOnes.append(list(np.ones(len(_fnTDataNonZero[-1]))))
   _fnFitError.append([ list(np.array(_fnFitOnes[-1])-np.array(_fnFitSdev)),
     list(np.array(_fnFitOnes[-1])+np.array(_fnFitSdev)) ])
   ## -- data
   _fnDatCentral.append( list(np.array([gv.mean(data[key])[t] for t in _fnTDataNonZero[-1]])/
     np.array(_fnFitMean)) )
   _fnDatSdev = ( np.array([gv.sdev(data[key])[t] for t in _fnTDataNonZero[-1]])/
     np.array(_fnFitMean) )
   _fnDatError.append([ list(_fnDatSdev), list(_fnDatSdev) ])
 ## -- done saving data
 
 do_plot_normalized(_fnIdx)
