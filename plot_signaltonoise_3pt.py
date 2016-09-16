import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines as df

def plot_corr_3pt(models,data,fit,**kwargs):
 """
 Get all data ready so that it can be plotted on command
 Allows for dynamic cycling through plots
 """
 _p3NMod = len(models)
 _p3Idx = [0] ## -- index of plotted function, in array so it can be modified in functions
 ## -- objects to hold all plot data
 ##  - Dat/Fit refers to the correlator data or the fit function
 ##  - Central/Error are the central value and errors
 _p3DatCentral = []
 _p3DatError   = []
 _p3FitCentral = []
 _p3FitError   = []
 #
 ## -- other objects
 _p3TData = []
 _p3TFit  = []
 fig,axp = plt.subplots(1,figsize=(8,8))
 #
 ## -- setup plot function
 def do_plot_3pt(idx,fig=fig):
   fig.clear()
   axp = fig.add_subplot(111)
   #fig.subplots_adjust(hspace=0)
   key = models[idx[0]].datatag

   #axp.set_yscale('log')
   #axp.set_xlim([-1,len(_p3TData[idx[0]])])
   axp.set_xlim([-.5,len(_p3TFit[idx[0]])+1.5])
   axp.set_ylim(utp.get_option("y_scale",[-2,2],**kwargs[key]))
   #plt.sca(axp)
   #expp = [int(np.floor(np.log10(np.abs(x)))) for x in plt.yticks()[0][2:]]
   #expp = ['$10^{'+str(x)+'}$' for x in expp]
   #plt.yticks(plt.yticks()[0][2:],expp)
   #
   ## -- plot fit
   axp.plot(_p3TData[idx[0]],_p3FitCentral[idx[0]],
    color=utp.get_option("color2",'b',**kwargs[key]))
   axp.plot(_p3TData[idx[0]],_p3FitError[idx[0]][0],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   axp.plot(_p3TData[idx[0]],_p3FitError[idx[0]][1],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   ## -- plot correlator data
   axp.errorbar(_p3TData[idx[0]],_p3DatCentral[idx[0]],yerr=_p3DatError[idx[0]],
    mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
    mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    ls=utp.get_option("linestyle1",'None',**kwargs[key]),
    marker=utp.get_option("marker1",'o',**kwargs[key]),
    ms=utp.get_option("markersize",6,**kwargs[key]))
   axp.scatter(_p3TFit[idx[0]],[_p3DatCentral[idx[0]][t] for t in _p3TFit[idx[0]]],
    color=utp.get_option("color1",'r',**kwargs[key]),
    marker=utp.get_option("marker",'o',**kwargs[key]),
    s=utp.get_option("markersize",36,**kwargs[key]))
   fig.suptitle(utp.get_option("plottitlep3",str(idx[0])+" default title "+str(key),**kwargs[key]),
    fontsize=utp.get_option("titlesize",20,**kwargs[key]))
   ## -- modify some options 
   for item in ([axp.xaxis.label,axp.yaxis.label]):
    # must be after setting label content (LaTeX ruins it)
    item.set_fontsize(fontsize=utp.get_option("fontsize",20,**kwargs[key]))
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
       idx[0] = idx[0] % _p3NMod
       do_plot_3pt(idx)
     elif event.key=='left':
       idx[0] = (idx[0] - 1) % _p3NMod
       do_plot_3pt(idx)
     elif event.key=='right':
       idx[0] = (idx[0] + 1) % _p3NMod
       do_plot_3pt(idx)
     elif event.key=='backspace':
       ## -- reset index so can manually flip through using number keys
       idx[0] = 0
     elif event.key=='d':
       ## -- dump plots into ./plotdump directory
       for ix,model in zip(range(len(models)),models):
         key = model.datatag
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
   _p3TData.append(model.tdata)
   _p3TFit.append(model.tfit)
   #_p3TFit[-1] = np.append(_p3TFit[-1],list(sorted([len(_p3TData[-1]) - t for t in _p3TFit[-1]])))
   ## -- fit
   _p3FitFunc = utp.create_fit_func_3pt(model,fit) ## not defined yet!
   _p3FitMean = gv.mean(_p3FitFunc(_p3TData[-1]))
   _p3FitSdev = gv.sdev(_p3FitFunc(_p3TData[-1]))
   _p3FitCentral.append(_p3FitMean)
   _p3FitError.append([
     np.array(_p3FitMean)-np.array(_p3FitSdev),
     np.array(_p3FitMean)+np.array(_p3FitSdev)])
   ## -- data
   _p3DatMean = gv.mean(data[key])
   _p3DatSdev = gv.sdev(data[key])
   _p3DatCentral.append( _p3DatMean )
   _p3DatError.append([list(_p3DatSdev),list(_p3DatSdev)])
 ## -- done saving data
 
 if not(utp.get_option("to_terminal",True,**kwargs[key])) and\
    utp.get_option("to_file",False,**kwargs[key]):
  for ix in range(len(models)):
    ## -- loops and saves all without creating window
    do_plot_3pt([ix])
 else:
  do_plot_3pt(_p3Idx)
