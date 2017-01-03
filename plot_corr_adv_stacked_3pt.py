import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines as df

import matplotlib as mpl
mpl.use('TkAgg')

print_quality = True
#plotLimit = [-0.2,0.6,0.2]
plotLimit = [-0.2,1.2,0.2]

def plot_corr_adv_stacked_3pt(models,data,fit,req=None,**kwargs):
 """
 Get all data ready so that it can be plotted on command
 Allows for dynamic cycling through plots
 """
 _p3NMod = len(models)
 _p3NTsp = 0  ## -- number of source/sink separations
 _p3Tsp = []  ## -- list of source/sink separations used
 _p3Key = []  ## -- list of keys used, to search for different source/sink separations
 _p3Idx = [0] ## -- index of plotted function, in array so it can be modified in functions
 _p3ColorList = ['r','#1e90ff','g','b']
 ## -- objects to hold all plot data
 ##  - Dat/Fit refers to the correlator data or the fit function
 ##  - Central/Error are the central value and errors
 _p3DatCentral = []
 _p3DatError   = []
 _p3FitCentral = []
 _p3FitError   = []
 #
 ## -- timeslice objects
 _p3TData = []
 _p3TFit  = []
 _p3TDataSub = []
 _p3TFitSub  = []
 fig,axp = plt.subplots(1,figsize=(10,8))
 if print_quality:
  plt.subplots_adjust(bottom=0.18,left=0.18,right=0.97,top=0.95)
 else:
  plt.subplots_adjust(bottom=0.15,left=0.15,right=0.97,top=0.95)
 #
 ## -- setup plot function
 def do_plot_3pt(idx,fig=fig):
   fig.clear()
   axp = fig.add_subplot(111)
   handles = list() ## -- handles for legend
   key = _p3Key[idx[0]]

   tbd = np.max([x[-1] for x in _p3TData[idx[0]]])
   axp.set_xlim([-float(tbd)/2-1,float(tbd)/2+1])
   #axp.set_ylim(utp.get_option("y_scale",[-2,2],**kwargs[key]))
   axp.set_ylim(utp.get_option("y_scale",[plotLimit[0],plotLimit[1]],**kwargs[key]))
   #
   ## -- plot fit
   if utp.get_option("p3_do_fit",True,**kwargs[key]):
    for i,tsub,fitcn in zip(range(len(_p3TFitSub[idx[0]])),
      _p3TFitSub[idx[0]],_p3FitCentral[idx[0]]):
     axp.plot(tsub,fitcn,color=_p3ColorList[i])
    for i,tsub,fiter in zip(range(len(_p3TFitSub[idx[0]])),_p3TFitSub[idx[0]],_p3FitError[idx[0]]):
     axp.plot(tsub,fiter[0],color=_p3ColorList[i],
      ls=utp.get_option("linestyle2",'--',**kwargs[key]))
     axp.plot(tsub,fiter[1],color=_p3ColorList[i],
      ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   ## -- plot correlator data
   for i,tsub,datcn,dater in zip(range(len(_p3TFitSub[idx[0]])),_p3TDataSub[idx[0]],
     _p3DatCentral[idx[0]],_p3DatError[idx[0]]):
    (_,caps,_) = axp.errorbar(tsub,datcn,dater,
     mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
     mec=_p3ColorList[i],
     color=_p3ColorList[i],
     #mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
     #color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
     ls=utp.get_option("linestyle1",'None',**kwargs[key]),
     marker=utp.get_option("marker1",'o',**kwargs[key]),
     ms=utp.get_option("markersize",9,**kwargs[key]),
     ecolor=_p3ColorList[i],
     capsize=6,elinewidth=2)
    for cap in caps:
     cap.set_markeredgewidth(1)
   for i,tfit,tsub,datcn in zip(range(len(_p3TFit[idx[0]])),_p3TFit[idx[0]],
     _p3TFitSub[idx[0]],_p3DatCentral[idx[0]]):
    handle = axp.scatter(tsub,[datcn[t] for t in tfit],color=_p3ColorList[i],
     marker=utp.get_option("marker",'o',**kwargs[key]),
     s=utp.get_option("markersize",81,**kwargs[key]))
    handles.append(handle)
   fig.suptitle(utp.get_option("plottitlep3",str(idx[0])+" default title "+str(key),**kwargs[key]),
    fontsize=utp.get_option("titlesize",20,**kwargs[key]))
   if print_quality:
    axp.set_xlabel(r'$t-\frac{T}{2}$',fontsize=40)
    axp.set_ylabel(utp.get_option("yaxistitle",r"$C(t,T)$",**kwargs[key]),
     #fontsize=30,rotation=0,position=(0.05,0.98))
     fontsize=40,rotation='vertical')
    axp.yaxis.set_label_coords(-0.10,0.5)
    axp.tick_params(axis='both', which='major', labelsize=30)
    plt.yticks(list(np.arange(plotLimit[0],plotLimit[1]+1e-8,plotLimit[2])),
     fontsize=30)
   else:
    axp.set_xlabel(r'$t-\frac{T}{2}$',fontsize=30)
    axp.set_ylabel(utp.get_option("yaxistitle",r"$C(t,T)$",**kwargs[key]),
     #fontsize=30,rotation=0,position=(0.05,0.98))
     fontsize=30,rotation=0)
    #axp.yaxis.set_label_coords(-0.02,0.28)
    axp.yaxis.set_label_coords(0.0,1.03)
    axp.tick_params(axis='both', which='major', labelsize=24)
   ## -- modify some options 
   #for item in ([axp.xaxis.label,axp.yaxis.label]):
   # # must be after setting label content (LaTeX ruins it)
   # item.set_fontsize(fontsize=utp.get_option("fontsize",36,**kwargs[key]))
   plt.legend(handles,["T = "+str(t) for t in _p3Tsp],fontsize=30)
   rect =fig.patch
   rect.set_facecolor('white')
   
   if utp.get_option("to_file",False,**kwargs[key]):
    #print "key",key,"saved to file",save_dir+'/'+save_name
    save_dir  = utp.get_option("p3_save_dir","./plotdump",**kwargs[key])
    save_name = utp.get_option("p3_save_name","p3plot-"+key+".pdf",**kwargs[key])
    plt.savefig(save_dir+'/'+save_name)
   if utp.get_option("to_terminal",True,**kwargs[key]):
    plt.draw()
   pass

 #
 ## -- setup button press action function
 def press_3pt(event,idx=_p3Idx):
   try:
     ## -- manually indicate index
     idx[0] = int(event.key) + (idx[0])*10
   except ValueError:
     if event.key==' ': ## -- space
       ## -- allows for replotting when changing index by typing number keys
       idx[0] = idx[0] % len(_p3Key)
       do_plot_3pt(idx)
     elif event.key=='left':
       idx[0] = (idx[0] - 1) % len(_p3Key)
       do_plot_3pt(idx)
     elif event.key=='right':
       idx[0] = (idx[0] + 1) % len(_p3Key)
       do_plot_3pt(idx)
     elif event.key=='backspace':
       ## -- reset index so can manually flip through using number keys
       idx[0] = 0
     elif event.key=='d':
       ## -- dump plots into ./plotdump directory
       for ix,key in zip(range(len(_p3Key)),_p3Key):
         save_dir  = utp.get_option("p3_save_dir","./plotdump",**kwargs[key])
         save_name = utp.get_option("p3_save_name","p3plot-"+key+".pdf",**kwargs[key])
         do_plot_3pt([ix])
         plt.savefig(save_dir+'/'+save_name)
       do_plot_3pt(idx)
 #
 ## -- 
 fig.canvas.mpl_connect('key_press_event',press_3pt)
 ## -- save plot data
 for idx,model in zip(range(len(models)),models):
   key = model.datatag
   tsep = int(key.split('t')[-1]) # tsep
   tkey = 't'.join(key.split('t')[:-1]) # rest of tag
   if not(tsep in _p3Tsp):
    _p3Tsp.append(tsep)
    _p3NTsp += 1
   if not(tkey in _p3Key): ## -- append a list to everything for this new key
    _p3Key.append(tkey)
    _p3TFit.append(list())
    _p3TData.append(list())
    _p3TFitSub.append(list())
    _p3TDataSub.append(list())
    _p3FitCentral.append(list())
    _p3FitError.append(list())
    _p3DatCentral.append(list())
    _p3DatError.append(list())
   tidx = _p3Key.index(tkey)
   _p3TFit[tidx].append(list(model.tfit))
   _p3TData[tidx].append(model.tdata[:len(_p3TFit[tidx][-1])+2])
   _p3TFitSub[tidx].append([t-float(len(_p3TFit[tidx][-1])+1)/2 for t in _p3TFit[tidx][-1]])
   _p3TDataSub[tidx].append([t-float(len(_p3TFit[tidx][-1])+1)/2 for t in _p3TData[tidx][-1]])
   ## -- fit
   #if False:
   #_p3FitFunc = utp.create_fit_func_3pt(model,fit)
   if req is None:
    _p3FitFunc = utp.mask_fit_fcn(model,fit,invert=True)
   else:
    _p3FitFunc = utp.mask_fit_fcn(model,fit,req=req,invert=False)
   _p3FitMean = gv.mean(_p3FitFunc(np.array(_p3TFit[tidx][-1])))
   _p3FitSdev = gv.sdev(_p3FitFunc(np.array(_p3TFit[tidx][-1])))
   _p3FitCentral[tidx].append(_p3FitMean)
   _p3FitError[tidx].append([
     np.array(_p3FitMean)-np.array(_p3FitSdev),
     np.array(_p3FitMean)+np.array(_p3FitSdev)])
   ## -- data
   if req is None:
    _p3SubFunc = utp.mask_fit_fcn(model,fit,invert=False)
   else:
    _p3SubFunc = utp.mask_fit_fcn(model,fit,req=req,invert=True)
   _dfSub = _p3SubFunc(np.array(_p3TData[tidx][-1]))
   #print _p3TData[tidx][-1]
   #print _p3TFit[tidx][-1]
   #print _dfSub,data[key]
   #_p3DatMean = gv.mean([data[key][t] for t in _p3TData[tidx][-1]])
   #_p3DatSdev = gv.sdev([data[key][t] for t in _p3TData[tidx][-1]])
   _p3DatMean = gv.mean(np.array([data[key][t] for t in _p3TData[tidx][-1]])-_dfSub)
   _p3DatSdev = gv.sdev(np.array([data[key][t] for t in _p3TData[tidx][-1]])-_dfSub)
   _p3DatCentral[tidx].append( _p3DatMean )
   _p3DatError[tidx].append([list(_p3DatSdev),list(_p3DatSdev)])
 ## -- done saving data
 
 if not(utp.get_option("to_terminal",True,**kwargs[key])) and\
    utp.get_option("to_file",False,**kwargs[key]):
  for ix in range(len(_p3Key)):
    ## -- loops and saves all without creating window
    do_plot_3pt([ix])
 else:
  do_plot_3pt(_p3Idx)
