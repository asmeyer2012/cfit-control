import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines as df

import matplotlib as mpl
mpl.use('TkAgg')

def plot_corr_double_log_folded(models,data,fit,**kwargs):
 """
 Get all data ready so that it can be plotted on command
 Allows for dynamic cycling through plots
 """
 _dfNMod = len(models)
 _dfIdx = [0] ## -- index of plotted function, in array so it can be modified in functions
 ## -- objects to hold all plot data
 ##  - Dat/Fit refers to the correlator data or the fit function
 ##  - Hi/Lo corresponds to the positive/negative half of the fit plot
 ##  - Central/Error are the central value and errors
 _dfDatHiCentral = []
 _dfDatHiError   = []
 _dfDatLoCentral = []
 _dfDatLoError   = []
 _dfFitHiCentral = []
 _dfFitHiError   = []
 _dfFitLoCentral = []
 _dfFitLoError   = []
 #
 ## -- other objects
 _dfTData = []
 _dfTFit  = []
 fig,axp = plt.subplots(1,figsize=(8,8))
 #
 ## -- setup plot function
 def do_plot_double_log_folded(idx,fig=fig):
   fig.clear()
   axp = fig.add_subplot(111)
   key = models[idx[0]].datatag

   axp.set_yscale('log')
   axp.set_xlim([-1,len(_dfTData[idx[0]])])
   axp.set_ylim(utp.get_option("y_pos_limit",[1e-8,1e0],**kwargs[key]))
   plt.sca(axp)
   expp = [int(np.floor(np.log10(np.abs(x)))) for x in plt.yticks()[0][2:]]
   expp = ['$10^{'+str(x)+'}$' for x in expp]
   plt.yticks(plt.yticks()[0][2:],expp)
   axp.tick_params(axis='both', which='major', labelsize=20)
   #
   ## -- plot fit
   axp.plot(_dfTData[idx[0]],_dfFitHiCentral[idx[0]],
    color=utp.get_option("color2",'b',**kwargs[key]))
   axp.plot(_dfTData[idx[0]],_dfFitHiError[idx[0]][0],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   axp.plot(_dfTData[idx[0]],_dfFitHiError[idx[0]][1],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   ## -- plot correlator data
   (_,caps,_) = axp.errorbar(_dfTData[idx[0]],_dfDatHiCentral[idx[0]],yerr=_dfDatHiError[idx[0]],
    mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
    mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    ls=utp.get_option("linestyle1",'None',**kwargs[key]),
    marker=utp.get_option("marker1",'o',**kwargs[key]),
    ms=utp.get_option("markersize",9,**kwargs[key]),
    capsize=6, elinewidth=2)
   for cap in caps:
     cap.set_markeredgewidth(1)
   axp.scatter(_dfTFit[idx[0]],[_dfDatHiCentral[idx[0]][t] for t in _dfTFit[idx[0]]],
    color=utp.get_option("color1",'r',**kwargs[key]),
    marker=utp.get_option("marker",'o',**kwargs[key]),
    s=utp.get_option("markersize",81,**kwargs[key]))
   fig.suptitle(utp.get_option("plottitledf",str(idx[0])+" default title "+str(key),**kwargs[key]),
    fontsize=utp.get_option("titlesize",20,**kwargs[key]))
   ## -- modify some options 
   axp.set_xlabel(r'$t$',fontsize=10)
   axp.set_ylabel(utp.get_option("yaxistitle",r"$C(t)$",**kwargs[key]),
    #fontsize=10,rotation=0,position=(0.01,0.04),labelpad=10)
    fontsize=10,rotation=0)
   axp.yaxis.set_label_coords(-0.07,0.04)
   for item in ([axp.xaxis.label,axp.yaxis.label]):
    # must be after setting label content (LaTeX ruins it)
    item.set_fontsize(fontsize=utp.get_option("fontsize",30,**kwargs[key]))
   rect =fig.patch
   rect.set_facecolor('white')
   if utp.get_option("to_file",False,**kwargs[key]):
    save_dir  = utp.get_option("df_save_dir","./plotdump",**kwargs[key])
    save_name = utp.get_option("df_save_name","dfplot-"+key+".pdf",**kwargs[key])
    plt.savefig(save_dir+'/'+save_name)
    #mng = plt.get_current_fig_manager()
    #mng.resize(*mng.window.maxsize())
    #fig.set_size_inches(5,12)
    #save_dir  = utp.get_option("df_save_dir","./plotdump",**kwargs[key])
    #save_name = utp.get_option("df_save_name","dfplot-"+key+".pdf",**kwargs[key])
    #fig.savefig(save_dir+'/'+save_name)
   if utp.get_option("to_terminal",True,**kwargs[key]):
    plt.draw()
   pass
 #
 ## -- setup button press action function
 def press_double_log_folded(event,idx=_dfIdx):
   #print('press_double_log_folded', event.key)
   try:
     ## -- manually indicate index
     idx[0] = int(event.key) + (idx[0])*10
   except ValueError:
     if event.key==' ': ## -- space
       ## -- allows for replotting when changing index by typing number keys
       idx[0] = idx[0] % _dfNMod
       do_plot_double_log_folded(idx)
     elif event.key=='left':
       idx[0] = (idx[0] - 1) % _dfNMod
       do_plot_double_log_folded(idx)
     elif event.key=='right':
       idx[0] = (idx[0] + 1) % _dfNMod
       do_plot_double_log_folded(idx)
     elif event.key=='backspace':
       ## -- reset index so can manually flip through using number keys
       idx[0] = 0
     elif event.key=='d':
       ## -- dump plots into ./plotdump directory
       for ix,model in zip(range(len(models)),models):
         key = model.datatag
         save_dir  = utp.get_option("df_save_dir","./plotdump",**kwargs[key])
         save_name = utp.get_option("df_save_name","dfplot-"+key+".pdf",**kwargs[key])
         do_plot_double_log_folded([ix])
         plt.savefig(save_dir+'/'+save_name)
       do_plot_double_log_folded(idx)
 #
 ## -- 
 fig.canvas.mpl_connect('key_press_event',press_double_log_folded)
 ## -- save plot data
 for idx,model in zip(range(len(models)),models):
   key = model.datatag
   _dfTData.append([t for t in model.tdata if t < len(model.tdata)/2+1])
   _dfTFit.append([t for t in model.tfit if t < len(model.tdata)/2+1])
   ## -- fit
   _dfFitFunc = utp.create_fit_func(model,fit)
   _dfFitMean = gv.mean(_dfFitFunc(_dfTData[-1]))
   _dfFitSdev = gv.sdev(_dfFitFunc(_dfTData[-1]))
   _dfFitHiCentral.append(
     utf.pos_arr(_dfFitMean,utp.get_option("y_pos_limit",[1e-4,1e0],**kwargs[key])[0]/100) )
   _dfFitHiError.append([
     utf.pos_arr(np.array(_dfFitMean)-np.array(_dfFitSdev),
     utp.get_option("y_pos_limit",[1e-4,1e0],**kwargs[key])[0]/1000),
     utf.pos_arr(np.array(_dfFitMean)+np.array(_dfFitSdev),
     utp.get_option("y_pos_limit",[1e-4,1e0],**kwargs[key])[0]/1000) ])
   ## -- data
   _dfDatMean = [gv.mean(data[key][0])]
   _dfDatSdev = [gv.sdev(data[key][0])]
   for t in range(1,len(_dfTData[-1])-1):
    _dfDatMean.append(gv.mean(data[key][t]))
    _dfDatSdev.append(gv.sdev(data[key][t]))
   _dfDatMean.append(gv.mean(data[key][len(_dfTData[-1])-1]))
   _dfDatSdev.append(gv.sdev(data[key][len(_dfTData[-1])-1]))
   _dfDatHiCentral.append( utf.pos_arr(_dfDatMean) )
   _dfDatHiError.append(utf.pos_err(_dfDatMean,_dfDatSdev))
 ## -- done saving data
 
 if not(utp.get_option("to_terminal",True,**kwargs[key])) and\
    utp.get_option("to_file",False,**kwargs[key]):
  for ix in range(len(models)):
    ## -- loops and saves all without creating window
    do_plot_double_log_folded([ix])
 else:
  do_plot_double_log_folded(_dfIdx)
