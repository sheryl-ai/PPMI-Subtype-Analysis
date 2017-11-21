#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy
import pandas 
import matplotlib.pyplot as plt

from numeric import isfloat


class Display(object):

    def __init__(self, var):
        self.var = var
        

    def heatmap(self, figurename, is_progress=False, is_rotate=True):
        
        mean_std = self.var.mean
        if is_progress == True:
            mean_std_first = self.var.mean_first
        else:
            mean_total = self.var.mean_total
            
        p_value = dict()
        for fp_list in self.var.p_value:
            p_value[fp_list[0]] = fp_list[1::]

        fn_mean_cls = dict()
        for i in range(1, self.var.K+1):
            fn_mean_cls[str(i)] = dict()

        fval = list()
        for fn, ms_list in mean_std.items():
            mval = [ms[0] for ms in ms_list]
                                 
            is_nan_list = numpy.isnan(mval)
            is_nan = 0 
            for n in is_nan_list:
                if n == True:
                    is_nan += 1
            if is_nan > 0:
                continue
            
            if is_progress==False:
                if p_value[fn][2]>0.05:
                    continue
                mt = mean_total[fn][0]
            else:
                if p_value[fn][3] == None:
                    continue
                else:
                    if p_value[fn][3]>0.05:
                        continue   
                msf_list = [msf for msf in mean_std_first[fn]]
         
            if fn == 'CSF-CSF Alpha-synuclein':
                fn = 'CSF Alpha-synuclein'
               
            if fn == 'MDS UPDRS PartIII-H&Y':
                fn = 'H&Y'
               
            if fn == 'MDS UPDRS PartIII-MDS-UPDRS':
                fn = 'MDS UPDRS PartIII'
            
            if is_progress==False:
                for i in range(1, self.var.K+1):
                    fn_mean_cls[str(i)][fn] = ms_list[i-1][0]-mt
                    if fn_mean_cls[str(i)][fn] >= 0: 
                        fn_mean_cls[str(i)][fn] = -math.log1p(math.fabs(fn_mean_cls[str(i)][fn])+1)
                    else:
                        fn_mean_cls[str(i)][fn] = math.log1p(math.fabs(fn_mean_cls[str(i)][fn])+1)
                    fval.append(fn_mean_cls[str(i)][fn])          
            else:           
                for i in range(1, self.var.K+1):
                    fn_mean_cls[str(i)][fn] = ms_list[i-1][0]-msf_list[i-1][0]
                    if fn_mean_cls[str(i)][fn] >= 0: 
                        fn_mean_cls[str(i)][fn] = -math.log1p(math.fabs(fn_mean_cls[str(i)][fn])+1)
                    else:
                        fn_mean_cls[str(i)][fn] = math.log1p(math.fabs(fn_mean_cls[str(i)][fn])+1)
                    fval.append(fn_mean_cls[str(i)][fn])     
         
        # plot heatmap
        z_min, z_max = -numpy.abs(fval).max(), numpy.abs(fval).max()
        if is_rotate == False:
            if self.var.K == 3:
                mean_tab = pandas.DataFrame({'Subtype I': fn_mean_cls['1'], 
                                         'Subtype II': fn_mean_cls['2'],
                                         'Subtype III': fn_mean_cls['3']})
                subtype_list = ['Subtype I', 'Subtype II', 'Subtype III']
           
            elif self.var.K == 2:
                mean_tab = pandas.DataFrame({'Subtype I': fn_mean_cls['1'], 
                                             'Subtype II': fn_mean_cls['2']})
                subtype_list = ['Subtype I', 'Subtype II']
        else:
            sig_fn_dict, fn_list = self.dict_rotate(fn_mean_cls)
            mean_tab = pandas.DataFrame(sig_fn_dict)
            
        print (mean_tab)
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(mean_tab, cmap=plt.cm.RdBu, alpha=0.8, vmin=z_min, vmax=z_max)
       
        fig = plt.gcf()
        fig.set_size_inches(6,10)
        ax.set_frame_on(False) # turn off the frame
        
        # put the major ticks at the middle of each cell
        ax.set_yticks(numpy.arange(mean_tab.shape[0])+0.5, minor=False)
        ax.set_xticks(numpy.arange(mean_tab.shape[1])+0.5, minor=False)

        # want a more natural, table-like display
        ax.invert_yaxis()
        ax.xaxis.tick_top()
       
        if is_rotate == False:
            if self.var.K == 3:
                ax.set_xticklabels(subtype_list, minor=False) 
            elif self.var.K == 2:
                ax.set_xticklabels(subtype_list, minor=False)
            ax.set_yticklabels(mean_tab.index, minor=False)
        else:
            ax.set_xticklabels(mean_tab.axes[1], minor=False)
            ax.set_yticklabels(mean_tab.index, minor=False)
        # rotate the axis x
#        plt.xticks(rotation=90)
        
        plt.savefig(figurename, bbox_inches='tight', 
                transparent=True,
                pad_inches=0)
        # check the abnormal clusters
        print ('-----------------------')
        if is_progress==True:
            self.check_progress(fn_mean_cls)
       
            
    def dict_rotate(self, fn_mean_cls):
        sig_fn_dict = dict()
        fn_list = list()
        for cls, fn_val in fn_mean_cls.items():
            for fn, val in fn_val.items():
                if fn not in sig_fn_dict:
                    sig_fn_dict[fn] = dict()
                if cls == '1':
                    subtype = 'Subtype I'
                elif cls == '2':
                    subtype = 'Subtype II'
                elif cls == '3':
                    subtype = 'Subtype III'
                sig_fn_dict[fn][subtype] = val 
        fn_list = [fn for fn in sig_fn_dict.keys()]
        return sig_fn_dict, fn_list
        
        
    def check_progress(self, fn_mean_cls):
        '''the conditions is in reverse of the interpretation,
        since the values have been taken negative before'''
        abnormal_cls = dict() # fname:class list
        fname = set(['HVLT', 'MoCA', 'SDM', 'BJLO', 'SF', 'ESS', 'RBD', 'GDS',
                     'QUIP', 'SCOPA-AUT', 'LNN', 'STAI'])
        for fn in fname:
            abnormal_cls[fn] = list()
        for cls, fn_val in fn_mean_cls.items():
            for fn, val in fn_val.items():
                if fn == 'HVLT' and fn_mean_cls[cls][fn]<0:
                    abnormal_cls['HVLT'].append(cls)
                if fn == 'MoCA' and fn_mean_cls[cls][fn]>0:
                    abnormal_cls['MoCA'].append(cls)
                if fn == 'SDM' and fn_mean_cls[cls][fn]<0:
                    abnormal_cls['SDM'].append(cls)
                if fn == 'BJLO' and fn_mean_cls[cls][fn]<0:
                    abnormal_cls['BJLO'].append(cls)
                if fn == 'SF' and fn_mean_cls[cls][fn]<0:
                    abnormal_cls['SF'].append(cls)
                if fn == 'ESS' and fn_mean_cls[cls][fn]>0:
                    abnormal_cls['ESS'].append(cls)
                if fn == 'RBD' and fn_mean_cls[cls][fn]>0:
                    abnormal_cls['RBD'].append(cls)
                if fn == 'GDS' and fn_mean_cls[cls][fn]>0:
                    abnormal_cls['GDS'].append(cls)
                if fn == 'QUIP' and fn_mean_cls[cls][fn]>0:
                    abnormal_cls['QUIP'].append(cls)
                if fn == 'SCOPA-AUT' and fn_mean_cls[cls][fn]>0:
                    abnormal_cls['SCOPA-AUT'].append(cls)
                if fn == 'LNN' and fn_mean_cls[cls][fn]<0:
                    abnormal_cls['LNN'].append(cls)
                if fn == 'STAI' and fn_mean_cls[cls][fn]>0:
                    abnormal_cls['STAI'].append(cls)
        for fn, cls_list in abnormal_cls.items():
            if len(cls_list) == 0:
                continue
            print ('the abnormal progress of %s is cluster: ' %fn)
            for cls in cls_list:
                print (cls)
                