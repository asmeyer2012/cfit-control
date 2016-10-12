import matplotlib.pyplot as plt
import numpy as np
import gvar as gv
import util_funcs as utf
import util_plots as utp
import defines as df
from extract_3pt_info import *

import matplotlib as mpl
mpl.use('TkAgg')

def plot_corr_diagonalized(models,data,fit,idx,**kwargs):
 """
 Plot a set of correlators on the same axis to compare
 """
 _dgIdx = idx ## -- set of c,k indices to plot on the same axis
 ## -- objects to hold all plot data
 ##  - Dat/Fit refers to the correlator data or the fit function
 ##  - Hi/Lo corresponds to the positive/negative half of the fit plot
 ##  - Central/Error are the central value and errors
 _dgDatHiCentral = []
 _dgDatHiError   = []
 _dgDatLoCentral = []
 _dgDatLoError   = []
 _dgFitHiCentral = []
 _dgFitHiError   = []
 _dgFitLoCentral = []
 _dgFitLoError   = []
 _dgSrcMatrix = []
 _dgSnkMatrix = []
 _dgCorMatrix = []
 #
 ## -- other objects
 _dgTData = []
 _dgTFit  = []
 fig,(axp,axm) = plt.subplots(2,sharex=True,figsize=(8,16))
 #
 ## -- setup plot function
 ## -- do all arrangement of correlators, fit functions, then do diagonalization
 def do_plot_diagonalized(fig=fig):
   fig.clear()
   axp = fig.add_subplot(211)
   axm = fig.add_subplot(212,sharex=axp)
   fig.subplots_adjust(hspace=0)
   key = models[idx[0]].datatag

   axp.set_yscale('log')
   axm.set_yscale('log')
   axp.set_xlim([-1,len(_dgTData[idx[0]])])
   axm.set_xlim([-1,len(_dgTData[idx[0]])])
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
   axp.plot(_dgTData[idx[0]],_dgFitHiCentral[idx[0]],
    color=utp.get_option("color2",'b',**kwargs[key]))
   axm.plot(_dgTData[idx[0]],_dgFitLoCentral[idx[0]],
    color=utp.get_option("color2",'b',**kwargs[key]))
   axp.plot(_dgTData[idx[0]],_dgFitHiError[idx[0]][0],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   axm.plot(_dgTData[idx[0]],_dgFitLoError[idx[0]][0],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   axp.plot(_dgTData[idx[0]],_dgFitHiError[idx[0]][1],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   axm.plot(_dgTData[idx[0]],_dgFitLoError[idx[0]][1],
    color=utp.get_option("color2",'g',**kwargs[key]),
    ls=utp.get_option("linestyle2",'--',**kwargs[key]))
   ## -- plot correlator data
   axp.errorbar(_dgTData[idx[0]],_dgDatHiCentral[idx[0]],yerr=_dgDatHiError[idx[0]],
    mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
    mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    ls=utp.get_option("linestyle1",'None',**kwargs[key]),
    marker=utp.get_option("marker1",'o',**kwargs[key]),
    ms=utp.get_option("markersize",6,**kwargs[key]))
   axm.errorbar(_dgTData[idx[0]],_dgDatLoCentral[idx[0]],yerr=_dgDatLoError[idx[0]],
    mfc=utp.get_option("markerfacecolor1",'None',**kwargs[key]),
    mec=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    color=utp.get_option("markeredgecolor1",'k',**kwargs[key]),
    ls=utp.get_option("linestyle1",'None',**kwargs[key]),
    marker=utp.get_option("marker1",'o',**kwargs[key]),
    ms=utp.get_option("markersize",6,**kwargs[key]))
   axp.scatter(_dgTFit[idx[0]],[_dgDatHiCentral[idx[0]][t] for t in _dgTFit[idx[0]]],
    color=utp.get_option("color1",'r',**kwargs[key]),
    marker=utp.get_option("marker",'o',**kwargs[key]),
    s=utp.get_option("markersize",36,**kwargs[key]))
   axm.scatter(_dgTFit[idx[0]],[_dgDatLoCentral[idx[0]][t] for t in _dgTFit[idx[0]]],
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
   plt.draw()
   pass
 #
 ## -- setup button press action function
 ## -- disabled by commenting out invokation
 def press_diagonalized(event,idx=_dgIdx):
   #print('press_diagonalized', event.key)
   try:
     ## -- manually indicate index
     idx[0] = int(event.key) + (idx[0])*10
   except ValueError:
     if event.key==' ': ## -- space
       ## -- allows for replotting when changing index by typing number keys
       idx[0] = idx[0] % _dgNMod
       do_plot_diagonalized(idx)
     elif event.key=='left':
       idx[0] = (idx[0] - 1) % _dgNMod
       do_plot_diagonalized(idx)
     elif event.key=='right':
       idx[0] = (idx[0] + 1) % _dgNMod
       do_plot_diagonalized(idx)
     elif event.key=='backspace':
       ## -- reset index so can manually flip through using number keys
       idx[0] = 0
     elif event.key=='d':
       ## -- dump plots into ./plotdump directory
       for ix,model in zip(range(len(models)),models):
         key = model.datatag
         save_dir  = utp.get_option("dl_save_dir","./plotdump",**kwargs[key])
         save_name = utp.get_option("dl_save_name","dlplot-"+key+".png",**kwargs[key])
         do_plot_diagonalized([ix])
         plt.savefig(save_dir+'/'+save_name)
       do_plot_diagonalized(idx)
 #
 ## -- disabled by commenting out
 #fig.canvas.mpl_connect('key_press_event',press_diagonalized)
 #
 ## -- save plot data
 for idx,model in zip(range(len(models)),models):
   key = model.datatag
   _dgTData.append(model.tdata)
   _dgTFit.append(model.tfit)
   _dgTFit[-1] = np.append(_dgTFit[-1],list(sorted([len(_dgTData[-1]) - t for t in _dgTFit[-1]])))
   ## -- fit
   _dgFitFunc = utp.create_fit_func(model,fit)
   _dgFitMean = gv.mean(_dgFitFunc(_dgTData[-1]))
   _dgFitSdev = gv.sdev(_dgFitFunc(_dgTData[-1]))
   _dgFitHiCentral.append(
     utf.pos_arr(_dgFitMean,utp.get_option("y_pos_limit",[1e-8,1e0],**kwargs[key])[0]/100) )
   _dgFitLoCentral.append(
     utf.neg_arr(_dgFitMean,utp.get_option("y_neg_limit",[1e-8,1e0],**kwargs[key])[0]/100) )
   _dgFitHiError.append([
     utf.pos_arr(np.array(_dgFitMean)-np.array(_dgFitSdev),
     utp.get_option("y_pos_limit",[1e-8,1e0],**kwargs[key])[0]/1000),
     utf.pos_arr(np.array(_dgFitMean)+np.array(_dgFitSdev),
     utp.get_option("y_pos_limit",[1e-8,1e0],**kwargs[key])[0]/1000) ])
   _dgFitLoError.append([
     utf.neg_arr(np.array(_dgFitMean)-np.array(_dgFitSdev),
     utp.get_option("y_neg_limit",[1e-8,1e0],**kwargs[key])[0]/1000),
     utf.neg_arr(np.array(_dgFitMean)+np.array(_dgFitSdev),
     utp.get_option("y_neg_limit",[1e-8,1e0],**kwargs[key])[0]/1000) ])
   ## -- data
   _dgDatMean = gv.mean(data[key])
   _dgDatSdev = gv.sdev(data[key])
   _dgDatHiCentral.append( utf.pos_arr(_dgDatMean) )
   _dgDatLoCentral.append( utf.neg_arr(_dgDatMean) )
   _dgDatHiError.append(utf.pos_err(_dgDatMean,_dgDatSdev))
   _dgDatLoError.append(utf.neg_err(_dgDatMean,_dgDatSdev))
 ## -- done saving data, organize
 if df.do_irrep == "8":
  classList = [1,2,3,5,6]
 elif df.do_irrep == "8'":
  classList = [4,7]
 elif df.do_irrep == "16":
  classList = [2,3,4,6]
 ckey,kkey = get_overlap_keys(fit)
 for c in classList:
 _dgCorMatrix.append([data[
 
 do_plot_diagonalized(_dgIdx)
