# -*- coding: utf-8 -*-

import math
import numpy
import pandas
import operator
import scipy.stats as stats
import matplotlib.pyplot as plt
import statsmodels.stats.multicomp as multi

from numeric import isint

class Statistics(object):
    
    def __init__(self, K):
       self.K = K
     
############################# STATISTICAL METHODS #############################
       
    def get_mean_std(self, num_dict, is_total=False):

       if is_total == True:
           total_list = list()
           for i in range(1, self.K+1):
              total_list += num_dict[str(i)]
           mean = numpy.mean(total_list)
           std = numpy.std(total_list)
       else: # compute cluster mean and standard deviation    
           mean = dict()
           std = dict()
           if len(num_dict) != self.K:
               print ('Error in computing mean')
           for i in range(1, self.K+1):
               num_list = num_dict[str(i)]
#               print (num_list)
               mean[str(i)] = round(numpy.mean(num_list), 2)
               std[str(i)] = round(numpy.std(num_list), 2)
       return mean, std
       
       
    def get_chisquare(self, pat_var, pat_cls, name=None, state=None):
       # delete patient in pat_cls without pat_val
       pat_cls_new = dict()
       for pat, cls in pat_cls.items():
           if pat in pat_var:
               pat_cls_new[pat] = cls
#       print (len(pat_cls_new))
       # deal with negative value 
       min_fval = min(pat_var.values()) 
#       print (min_fval)
       if isint(min_fval) and min_fval < 0:
           for pat, fval in pat_var.items():
               pat_var[pat] = int(fval + math.fabs(min_fval))
       # construct table    
       pats = pandas.DataFrame({'variable': pat_var, 
                       'cluster':pat_cls_new})
       pat_tab = pandas.crosstab(pats.variable, pats.cluster, margins = True)
       pat_tab.column = ['subtype I', 'subtype II', 'subtype III', 'row_totals']
       pat_tab.index = list(set([v for v in pat_var.values()])) + ['col_totals']
#       print (pat_tab)
       # testing
       observed = pat_tab.ix[0:len(pat_var),0:self.K]
       ch2, p, dof, expected = stats.chi2_contingency(observed= observed) 
       print ("%s: The p-value of %s is: %f" %(state, name, p))
       return p
    
       
    def get_fisher_exact(self, pat_var, pat_cls, name=None, state=None):
       # delete patient in pat_cls without pat_val
       pat_cls_new = dict()
       for pat, cls in pat_cls.items():
           if pat in pat_var:
               pat_cls_new[pat] = cls
#       print (len(pat_cls_new))
       # construct table    
       pats = pandas.DataFrame({'variable': pat_var, 
                       'cluster':pat_cls_new})
       
       pat_tab = pandas.crosstab(pats.variable, pats.cluster, margins = True)
       pat_tab.column = ['subtype I', 'subtype II', 'subtype III', 'row_totals']
       pat_tab.index = list(set([v for v in pat_var.values()])) + ['col_totals']
#       print (pat_tab)
       # testing
       observed = pat_tab.ix[0:len(pat_var),0:self.K]
       ch2, p, dof, expected = stats.chi2_contingency(observed= observed) 
       print ("%s: The p-value of %s is: %f" %(state, name, p))
       return p          
       
       
    def get_f_oneway(self, pat_var, pat_cls, name=None, state=None):
       # delete patient in pat_cls without pat_val
       pat_cls_new = dict()
       for pat, cls in pat_cls.items():
           if pat in pat_var:
               pat_cls_new[pat] = cls   
#       print (len(pat_cls_new))
       # testing
       #pats_array = [[values for cluster 1], [values for cluster 2], ... ,[values for cluster n]]
       pats_array = list()
       for i in range(1, self.K+1):
           pa = list()
           for pat, cls in pat_cls_new.items():
               if cls == str(i):
                   pa.append(int(pat_var[pat]))
           pats_array.append(pa)
#       print (pats_array)
       pats_array = numpy.array(pats_array)
       # for three clusters
       if self.K == 2:
           fval, p = stats.f_oneway(pats_array[0], pats_array[1])
       elif self.K == 3:
           fval, p = stats.f_oneway(pats_array[0], pats_array[1], pats_array[2]) 
       print ("%s: The p-value of %s is: %f" %(state, name, p))
       return p
       
       
    def get_kruskal(self, pat_var, pat_cls, name=None, state=None):
       # delete patient in pat_cls without pat_val
       pat_cls_new = dict()
       for pat, cls in pat_cls.items():
           if pat in pat_var:
               pat_cls_new[pat] = cls   
#       print (len(pat_cls_new))
       # testing
       #pats_array = [[values for cluster 1], [values for cluster 2], ... ,[values for cluster n]]
       pats_array = list()
       for i in range(1, self.K+1):
           pa = list()
           for pat, cls in pat_cls_new.items():
               if cls == str(i):
                   pa.append(int(pat_var[pat]))
           pats_array.append(pa)
       pats_array = numpy.array(pats_array)
       # for three clusters
       if self.K == 2:
           fval, p = stats.kruskal(pats_array[0], pats_array[1]) 
       elif self.K == 3:
           fval, p = stats.kruskal(pats_array[0], pats_array[1], pats_array[2]) 
       print ("%s: The p-value of %s is: %f" %(state, name, p))
       return p
       
       
    def get_mannwhitneyu(self, pat_var, pat_cls, name=None, state=None):
       # delete patient in pat_cls without pat_val
       pat_cls_new = dict()
       for pat, cls in pat_cls.items():
           if pat in pat_var:
               pat_cls_new[pat] = cls   
       # testing
       #pats_array = [[values for cluster 1], [values for cluster 2], ... ,[values for cluster n]]
       pats_array = list()
       for i in range(1, self.K+1):
           pa = list()
           for pat, cls in pat_cls_new.items():
               if cls == str(i):
                   pa.append(int(pat_var[pat]))
           pats_array.append(pa)
       pats_array = numpy.array(pats_array)
       # for three clusters
       fval, p = stats.mannwhitneyu(pats_array[0], pats_array[1], pats_array[2]) 
       print ("%s: The p-value of %s is: %f" %(state, name, p))
       return p
       
       
    def get_tukeyhsd(self, pat_var, pat_cls, name=None, state=None):
        pat_cls_new = dict()
        for pat, cls in pat_cls.items():
            if pat in pat_var:
                pat_cls_new[pat] = int(cls)
        pats = pandas.DataFrame({'variable': pat_var, 
                       'cluster':pat_cls_new})
#        print (pats['cluster'])
#        pats['cluster']=pats['cluster'].astype('category')
#        print (pats['cluster'])
#        print (pats['variable'])
        mc1=multi.MultiComparison(pats['variable'], pats['cluster'])
        res1=mc1.tukeyhsd()
        print ("The summary of %s state for %s are:" %(state, name))
        print (res1.summary())
     
        
    def get_distribution(self, pat_var, is_num=True, is_discretization=False):
        dstrb = dict()
        if is_discretization == True:
            if numpy.mean([v for v in pat_var.values()]) > 1000:
                discrete_type = 'l_intval' # large interval
            elif numpy.mean([v for v in pat_var.values()]) > 100:
                discrete_type = 'm_intval'  # middle interval
            else:
                discrete_type = 's_intval' # small interval
            
        for pat, var in pat_var.items():
            if is_discretization == True:
                if discrete_type == 'l_intval':
                    var = math.floor(var/100)
                elif discrete_type == 'm_intval': 
                    var = math.floor(var/10)
                else:
                    var = int(var)
                    
            if var in dstrb:
                dstrb[var] += 1
            else:
                dstrb[var] = 1

        if is_num == False:
            X = numpy.arange(len(dstrb))
            Y = numpy.array([d for d in dstrb.values()])
            plt.bar(X, Y, facecolor='#9999ff', edgecolor='white')
            plt.show()
        else:
            dstrb = sorted(dstrb.items(), key=operator.itemgetter(1))
            X = numpy.array([d[0] for d in dstrb])
            Y = numpy.array([d[1] for d in dstrb])
            plt.bar(X, Y, facecolor='#9999ff', edgecolor='white')
            plt.show()

       
       
  
       
   
   

       
       

    
    
  
        
        
    