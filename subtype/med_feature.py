# -*- coding: utf-8 -*-

import math
import csv, codecs
import operator

from statistics import Statistics
from time_converter import convert_time, convert_int
from numeric import isfloat, isint


class MedFeature(object):
    
    def __init__(self):
        self.feature_info = dict() # feature name: list(pat_id, timestamp, feature_val)
        # medication
        # the dictionaries store the last state feature values
        self.MED = dict() # cluster: medication use state
        # the dictionaries store the first state feature values 
        self.MED_first = dict() # cluster: medication feature value
        # the dictionaries store the median state feature values 
        self.MED_median = dict() # cluster: medication feature value
        
        # p-value: first, median, last
        self.p_value = list() # feature name, p-value tuple (first, median, last, diff)
        self.mean = dict() # feature name : list(cluster1_mean, cluster1_std, ...)}
                          # mean of the last state for temporal features
        self.mean_first = dict() # feature name : list(cluster1_mean, cluster1_std, ...)
                                # mean of the first state for temporal fatures
        self.mean_median = dict()
        self.mean_total = dict() # feature name : (total mean, total std)
       
        self.mean_follow_up = dict() # feature name : mean follow-up time in this feature 
        
    
    def load_feature(self, fname=None, featname=None):
        try:
            if fname == 'MED USE':
                self.read_feature('MDS_UPDRS_Part_III__Post_Dose_.csv', featname, date_key='INFODT')
       
        except ValueError:
            print ('please enter correct file name!')
        
            
    def read_feature(self, filename, featname=None, time_convert=False, date_key=None, pid_name='PATNO'):
        fname = self.get_feature_name(filename, featname=None)
        f = codecs.open('../medication/' + filename, 'r', 'utf-8')
        reader = csv.reader(f)
        line_ctr = 0
        for row in reader:

            # table title
            if line_ctr < 1:
                table_ttl = dict(zip(row, range(len(row))))
                for fn in fname:
                    self.feature_info[fn] = list()
                line_ctr += 1
                continue
            
            # table content
            if date_key != None:
                if time_convert:
                    info_date = convert_time(row[table_ttl[date_key]])
                else:
                    info_date = row[table_ttl[date_key]]
            else:
                info_date = 'static'
                    

            # update feature info
            pat_id = row[table_ttl[pid_name]]
            for fn in fname:
                fval = row[table_ttl[fn]]
                self.feature_info[fn].append((pat_id, info_date, fval))        
            line_ctr +=1 
        f.close()
        return self.feature_info
        
    
    def get_feature_name(self, filename=None, featname=None):
        try:
            if filename == 'MDS_UPDRS_Part_III__Post_Dose_.csv':
                fname = ['PD_MED_USE']
       
        except ValueError:
            print ('please enter correct file name or feature name!')
            
        return fname
        
        
    def get_feature_set(self, fname=None, featname=None):
        feature_set = set()
        try:
            if fname == 'MED USE':
                feature_set = set(['PD_MED_USE'])	
               
        except ValueError:
            print ('please enter correct feature name!')
            
        return feature_set
        
    def get_feature_value(self, pat, tf_list, pf_first, pf_median, pf_last, fname=None, fn=None):

        # first
        fv_first = tf_list[0][1]      
                     
        if pat not in pf_first:
            pf_first[pat] = fv_first
        else:
            pf_first[pat] += fv_first

        # median
        if len(tf_list) % 2 == 1:
            mid_idx = math.floor(len(tf_list)/2)
            fv_median = tf_list[mid_idx][1]         
        else:
            mid_idx1 = math.floor(len(tf_list)/2)
            mid_idx2 = mid_idx1-1
            fv_median = (tf_list[mid_idx1][1] + tf_list[mid_idx2][1])/2
                     
        if pat not in pf_median:
            pf_median[pat] = fv_median
        else:
            pf_median[pat] += fv_median

        # last
        fv_last = tf_list[-1][1]
                     
        if pat not in pf_last:
            pf_last[pat] = fv_last
        else:
            pf_last[pat] += fv_last
      
        return (pf_first, pf_median, pf_last)
         
        
    def get_feature_diff(self, pat, tf_list, pf_diff, fname=None, fn=None):
         
        fv_first = tf_list[0][1] 
        fv_last = tf_list[-1][1]     
       
        fv_diff = fv_last - fv_first
        if pat not in pf_diff:
            pf_diff[pat] = fv_diff
        else:
            pf_diff[pat] += fv_diff

        return pf_diff
        
    def get_medication(self, dataio, K, fname=None, featname=None):
        pat_cluster = dataio.patient_cluster
        feat_info = dataio.feature.medication.feature_info
       
        # initialization for each cluster
        for i in range(1, K+1):
           self.MED[str(i)] = list()
           self.MED_first[str(i)] = list()
           self.MED_median[str(i)] = list()
       
        # intialization for patient and the corresponding feature value
        pat_fval_first = dict() # patient id : first feature value
        pat_fval_median = dict()# patient id : median feature value
        pat_fval_last = dict() # patient id : last feature value
        pat_fval_diff = dict() # patient id : first-order difference 
                                   # between last and first feature value 
        # read and store
        for fn, tpl_list in feat_info.items():
            if fn not in self.get_feature_set(fname, featname):
                continue
           
            pat_record = dict() # patient id : a list of (time stamp, feature val)
           
            for tpl in tpl_list:
                if isint(tpl[2])==True:
                    fv = int(tpl[2])
                elif isfloat(tpl[2])==True:
                    fv = float(tpl[2])
                else:
                    continue
                pat = tpl[0]
                time = convert_int(tpl[1])
             
                if pat not in pat_cluster:
                    continue
            
                if pat not in pat_record:
                    pat_record[pat] = list()
                    pat_record[pat].append((time, fv))
                else:
                    pat_record[pat].append((time, fv))
                   
            # sort for each patient according to time stamp       
            pat_new_record = dict()
            for pat, tf_list in pat_record.items():
                pat_new_record[pat] = sorted(tf_list, key=operator.itemgetter(0))
           
            # store last, (first, median) values 
            for pat, tf_list in pat_new_record.items():
                pat_fval_first, pat_fval_median, pat_fval_last = \
                self.get_feature_value(pat, tf_list, pat_fval_first, pat_fval_median, pat_fval_last)
                pat_fval_diff = self.get_feature_diff(pat, tf_list, pat_fval_diff)
                
        # store feature values according to subtypes 
        for pat, cls in pat_cluster.items():
            if pat in pat_fval_last:
                self.MED[str(cls)].append(pat_fval_last[pat])
            if pat in pat_fval_first:
                self.MED_first[str(cls)].append(pat_fval_first[pat])
            if pat in pat_fval_median:
                self.MED_median[str(cls)].append(pat_fval_median[pat])
                
        # compute statistics
        # mean , std
        stats=Statistics(K)
        mean_MED, std_MED=stats.get_mean_std(self.MED, is_total=False)
        mean_MED_first, std_MED_first=stats.get_mean_std(self.MED_first, is_total=False)
        mean_MED_median, std_MED_median=stats.get_mean_std(self.MED_median, is_total=False)
        mean_total_MED, std_total_MED = stats.get_mean_std(self.MED, is_total=True)   
        mean_total_MED_first, std_total_MED_first = stats.get_mean_std(self.MED_first, is_total=True)   
        mean_total_MED_median, std_total_MED_median = stats.get_mean_std(self.MED_median, is_total=True)   
        if featname != None:
            fname_ = fname + '-' + featname
        else:
            fname_ = fname
        self.mean[fname_] = list()
        self.mean_first[fname_] = list()
        self.mean_median[fname_] = list()
        for i in range(1, K+1):
           self.mean[fname_].append((mean_MED[str(i)], std_MED[str(i)]))
           self.mean_first[fname_].append((mean_MED_first[str(i)], std_MED_first[str(i)]))
           self.mean_median[fname_].append((mean_MED_median[str(i)], std_MED_median[str(i)]))
        # display  
        if featname != None:
            print ('feature name: %s' %featname)
        else:
            print ('feature name: %s' %fname)
        for i in range(1, K+1):
            print ('### CLUSTER %d ####' %i)
            print ("The average value in the %d-th clusters at follow-up is: %f (%f)" %(i, mean_MED[str(i)], std_MED[str(i)]))
            print ("The average value in the %d-th clusters at baseline is: %f (%f)" %(i, mean_MED_first[str(i)], std_MED_first[str(i)]))
            print ("The average value in the %d-th clusters at median is: %f (%f)" %(i, mean_MED_median[str(i)], std_MED_median[str(i)]))
        print ("The total average %s at follow-up is: %f (%f)" %(fname, mean_total_MED, std_total_MED))
        print ("The total average %s at baseline is: %f (%f)" %(fname, mean_total_MED_first, std_total_MED_first))
        print ("The total average %s at median is: %f (%f)" %(fname, mean_total_MED_median, std_total_MED_median))
        print ("##########")
              
        # hypothesis testing
        print ("hypothesis testing...")
        if featname != None:
            fname = fname + '-' + featname
        # fisher exact
#        stats.get_distribution(pat_fval_first, is_num=True)
        p_first = stats.get_chisquare(pat_fval_first, pat_cluster, fname, 'FIRST')
#        stats.get_distribution(pat_fval_median, is_num=True)
        p_median = stats.get_chisquare(pat_fval_median, pat_cluster, fname, 'MEDIAN')
#        stats.get_distribution(pat_fval_last, is_num=True)
        p_last = stats.get_chisquare(pat_fval_last, pat_cluster, fname, 'LAST')
#        stats.get_distribution(pat_fval_diff, is_num=True)
        p_diff = stats.get_chisquare(pat_fval_diff, pat_cluster, fname, 'DIFFERENCE')
        self.p_value.append([fname, p_first, p_median, p_last, p_diff])
        
        # post hoc test    
        if p_first <= 0.05:
            stats.get_tukeyhsd(pat_fval_first, pat_cluster, fname, 'FIRST')
        if p_median <= 0.05:
            stats.get_tukeyhsd(pat_fval_median, pat_cluster, fname, 'MEDIAN')
        if p_last <= 0.05:
            stats.get_tukeyhsd(pat_fval_last, pat_cluster, fname, 'LAST')
        if p_diff <= 0.05:
            stats.get_tukeyhsd(pat_fval_diff, pat_cluster, fname, 'DIFFERENCE')
            
        self.mean_total[fname] = (mean_total_MED, std_total_MED)
        print ('-----------------------')