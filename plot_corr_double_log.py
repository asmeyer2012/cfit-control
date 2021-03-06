import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines as df

import matplotlib as mpl
mpl.use('TkAgg')

#def plot_corr_double_log(models,data,fit,fig,**kwargs):
def plot_corr_double_log(models,data,fit,**kwargs):
 """
 Get all data ready so that it can be plotted on command
 Allows for dynamic cycling through plots
 """
 _dlNMod = len(models)
 _dlIdx = [0] ## -- index of plotted function, in array so it can be modified in functions
 ## -- objects to hold all plot data
 ##  - Dat/Fit refers to the correlator data or the fit function
 ##  - Hi/Lo corresponds to the positive/negative half of the fit plot
 ##  - Central/Error are the central value and errors
 _dlDatHiCentral = []
 _dlDatHiError   = []
 _dlDatLoCentral = []
 _dlDatLoError   = []
 _dlFitHiCentral = []
 _dlFitHiError   = []
 _dlFitLoCentral = []
 _dlFitLoError   = []
 #
 ## -- other objects
 _dlTData = []
 _dlTFit  = []
 fig,(axp,axm) = plt.subplots(2,sharex=True,figsize=(8,16))
 #
 ## -- setup plot function
 def do_plot_double_log(idx,fig=fig):
   fig.clear()
   axp = fig.add_subplot(211)
   axm = fig.add_subplot(212,sharex=axp)
   fig.subplots_adjust(hspace=0)
   key = models[idx[0]].datatag

   axp.set_yscale('log')
   axm.set_yscale('log')
   axp.set_xlim([-1,len(_dlTData[idx[0]])])
   axm.set_xlim([-1,len(_dlTData[idx[0]])])
   axp.set_ylim(utp.get_option("y_pos_limit",[1e-8,1e0],**kwargs[key]))
   axm.set_ylim(utp.get_option("y_neg_limit",[1e-8,1e0],**kwargs[key]))
   axm.set_ylim(axm.get_ylim()[::-1])
   plt.sca(axp)
   expp = [int(np.floor(np.log10(np.abs(x)))) for x in plt.yticks()[0][2:]]
   expp = ['$10^{'+str(x)+'}$' for x in expp]
   plt.yticks(plt.yticks()[0][2:],expp)
   plt.sca(axm)
   expm = [int(np.floor(np.log10(np.abs(x)))) for x in plt.yticks()[0][2:]]
   expm = ['$-10^{'+str(x)+'}$' for x in expm]
   plt.yticks(plt.yticks()[0][2:],expm)
   #
   ## -- plot fit
   axp.plot(_dlTData[idx[0]],_dlFitHiCentral[idx[0]],
    color=utp.get_option("color2",'b',**kwargs[key]))
   axm.plot(_dlTData[idx[0]],_dlFitLoCentral[idx[0]],
    color=utp.get_option("color2",'b',**kwargs[key]))
   axp.plot(_dlTData[idx[0]],_dlFitHiError[idx[0]][0],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   axm.plot(_dlTData[idx[0]],_dlFitLoError[idx[0]][0],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   axp.plot(_dlTData[idx[0]],_dlFitHiError[idx[0]][1],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   axm.plot(_dlTData[idx[0]],_dlFitLoError[idx[0]][1],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   ## -- plot correlator data
   axp.errorbar(_dlTData[idx[0]],_dlDatHiCentral[idx[0]],yerr=_dlDatHiError[idx[0]],
    mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
    mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    ls=utp.get_option("linestyle1",'None',**kwargs[key]),
    marker=utp.get_option("marker1",'o',**kwargs[key]),
    ms=utp.get_option("markersize",6,**kwargs[key]))
   axm.errorbar(_dlTData[idx[0]],_dlDatLoCentral[idx[0]],yerr=_dlDatLoError[idx[0]],
    mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
    mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    ls=utp.get_option("linestyle1",'None',**kwargs[key]),
    marker=utp.get_option("marker1",'o',**kwargs[key]),
    ms=utp.get_option("markersize",6,**kwargs[key]))
   axp.scatter(_dlTFit[idx[0]],[_dlDatHiCentral[idx[0]][t] for t in _dlTFit[idx[0]]],
    color=utp.get_option("color1",'r',**kwargs[key]),
    marker=utp.get_option("marker",'o',**kwargs[key]),
    s=utp.get_option("markersize",36,**kwargs[key]))
   axm.scatter(_dlTFit[idx[0]],[_dlDatLoCentral[idx[0]][t] for t in _dlTFit[idx[0]]],
    color=utp.get_option("color1",'r',**kwargs[key]),
    marker=utp.get_option("marker",'o',**kwargs[key]),
    s=utp.get_option("markersize",36,**kwargs[key]))
   fig.suptitle(utp.get_option("plottitledl",str(idx[0])+" default title "+str(key),**kwargs[key]),
    fontsize=utp.get_option("titlesize",20,**kwargs[key]))
   ## -- modify some options 
   axm.set_xlabel(r'$t$')
   axm.set_ylabel(utp.get_option("yaxistitle",r"$C(t)$",**kwargs[key]),
    fontsize=30,rotation=0,position=(0.05,0.98))
   for item in ([axm.xaxis.label,axm.yaxis.label]):
    # must be after setting label content (LaTeX ruins it)
    item.set_fontsize(fontsize=utp.get_option("fontsize",20,**kwargs[key]))
   rect =fig.patch
   rect.set_facecolor('white')
   if utp.get_option("to_file",False,**kwargs[key]):
    save_dir  = utp.get_option("dl_save_dir","./plotdump",**kwargs[key])
    save_name = utp.get_option("dl_save_name","dlplot-"+key+".pdf",**kwargs[key])
    plt.savefig(save_dir+'/'+save_name)
    #mng = plt.get_current_fig_manager()
    #mng.resize(*mng.window.maxsize())
    #fig.set_size_inches(5,12)
    #save_dir  = utp.get_option("dl_save_dir","./plotdump",**kwargs[key])
    #save_name = utp.get_option("dl_save_name","dlplot-"+key+".pdf",**kwargs[key])
    #fig.savefig(save_dir+'/'+save_name)
   if utp.get_option("to_terminal",True,**kwargs[key]):
    plt.draw()
   pass
 #
 ## -- setup button press action function
 def press_double_log(event,idx=_dlIdx):
   #print('press_double_log', event.key)
   try:
     ## -- manually indicate index
     idx[0] = int(event.key) + (idx[0])*10
   except ValueError:
     if event.key==' ': ## -- space
       ## -- allows for replotting when changing index by typing number keys
       idx[0] = idx[0] % _dlNMod
       do_plot_double_log(idx)
     elif event.key=='left':
       idx[0] = (idx[0] - 1) % _dlNMod
       do_plot_double_log(idx)
     elif event.key=='right':
       idx[0] = (idx[0] + 1) % _dlNMod
       do_plot_double_log(idx)
     elif event.key=='backspace':
       ## -- reset index so can manually flip through using number keys
       idx[0] = 0
     elif event.key=='d':
       ## -- dump plots into ./plotdump directory
       for ix,model in zip(range(len(models)),models):
         key = model.datatag
         save_dir  = utp.get_option("dl_save_dir","./plotdump",**kwargs[key])
         save_name = utp.get_option("dl_save_name","dlplot-"+key+".pdf",**kwargs[key])
         do_plot_double_log([ix])
         plt.savefig(save_dir+'/'+save_name)
       do_plot_double_log(idx)
 #
 ## -- 
 fig.canvas.mpl_connect('key_press_event',press_double_log)
 ## -- save plot data
 for idx,model in zip(range(len(models)),models):
   key = model.datatag
   _dlTData.append(model.tdata)
   _dlTFit.append(model.tfit)
   _dlTFit[-1] = np.append(_dlTFit[-1],list(sorted([len(_dlTData[-1]) - t for t in _dlTFit[-1]])))
   ## -- fit
   _dlFitFunc = utp.create_fit_func(model,fit)
   _dlFitMean = gv.mean(_dlFitFunc(_dlTData[-1]))
   _dlFitSdev = gv.sdev(_dlFitFunc(_dlTData[-1]))
   _dlFitHiCentral.append(
     utf.pos_arr(_dlFitMean,utp.get_option("y_pos_limit",[1e-8,1e0],**kwargs[key])[0]/100) )
   _dlFitLoCentral.append(
     utf.neg_arr(_dlFitMean,utp.get_option("y_neg_limit",[1e-8,1e0],**kwargs[key])[0]/100) )
   _dlFitHiError.append([
     utf.pos_arr(np.array(_dlFitMean)-np.array(_dlFitSdev),
     utp.get_option("y_pos_limit",[1e-8,1e0],**kwargs[key])[0]/1000),
     utf.pos_arr(np.array(_dlFitMean)+np.array(_dlFitSdev),
     utp.get_option("y_pos_limit",[1e-8,1e0],**kwargs[key])[0]/1000) ])
   _dlFitLoError.append([
     utf.neg_arr(np.array(_dlFitMean)-np.array(_dlFitSdev),
     utp.get_option("y_neg_limit",[1e-8,1e0],**kwargs[key])[0]/1000),
     utf.neg_arr(np.array(_dlFitMean)+np.array(_dlFitSdev),
     utp.get_option("y_neg_limit",[1e-8,1e0],**kwargs[key])[0]/1000) ])
   ## -- data
   _dlDatMean = gv.mean(data[key])
   _dlDatSdev = gv.sdev(data[key])
   _dlDatHiCentral.append( utf.pos_arr(_dlDatMean) )
   _dlDatLoCentral.append( utf.neg_arr(_dlDatMean) )
   _dlDatHiError.append(utf.pos_err(_dlDatMean,_dlDatSdev))
   _dlDatLoError.append(utf.neg_err(_dlDatMean,_dlDatSdev))
 ## -- done saving data
 
 if not(utp.get_option("to_terminal",True,**kwargs[key])) and\
    utp.get_option("to_file",False,**kwargs[key]):
  for ix in range(len(models)):
    ## -- loops and saves all without creating window
    do_plot_double_log([ix])
 else:
  do_plot_double_log(_dlIdx)
