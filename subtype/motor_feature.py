# -*- coding: utf-8 -*-

import sys
import math
import csv, codecs
import operator 

from statistics import Statistics
from numeric import isint, isfloat
from time_converter import convert_time, convert_int


class MotorFeature(object):
    
    def __init__(self):
        self.feature_info = dict() # feature name: list(pat_id, timestamp, feature_val)
        
        # motor, non-motor, biospecimen, image, medication
        # the dictionaries store the last state feature values
        self.MOTOR = dict() # cluster: motor feature value
        # the dictionaries store the first state feature values 
        self.MOTOR_first = dict() # cluster: motor fature value
        # the dictionaries store the median state feature values 
        self.MOTOR_median = dict() # cluster: motor fature value
        
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
            if fname == 'MDS UPDRS PartI':
                self.read_feature('MDS_UPDRS_Part_I.csv', date_key='INFODT')
                self.read_feature('MDS_UPDRS_Part_I__Patient_Questionnaire.csv', date_key='INFODT')
            elif fname == 'MDS UPDRS PartII':
                self.read_feature('MDS_UPDRS_Part_II__Patient_Questionnaire.csv', date_key='INFODT')
            elif fname == 'MDS UPDRS PartIII':
                self.read_feature('MDS_UPDRS_Part_III__Post_Dose_.csv', featname, date_key='INFODT')
            elif fname == 'MDS UPDRS PartIV':
                self.read_feature('MDS_UPDRS_Part_IV.csv', date_key='INFODT')
        except ValueError:
            print ('please enter correct file name!')
        
    def read_feature(self, filename, featname=None, time_convert=False, date_key=None, pid_name='PATNO'):
        fname = self.get_feature_name(filename, featname=None)
        f = codecs.open('../motor/' + filename, 'r', 'utf-8')
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
            if filename == 'MDS_UPDRS_Part_I.csv':
                fname = ['NP1COG', 'NP1HALL',	'NP1DPRS', 'NP1ANXS', 'NP1APAT',	'NP1DDS']

            if filename == 'MDS_UPDRS_Part_I__Patient_Questionnaire.csv':   
                fname = ['NP1SLPN',	'NP1SLPD',	'NP1PAIN',	'NP1URIN',	'NP1CNST',	'NP1LTHD',	'NP1FATG']
            
            if filename == 'MDS_UPDRS_Part_II__Patient_Questionnaire.csv':
                fname = ['NP2SPCH', 'NP2SALV', 'NP2SWAL', 'NP2EAT', 'NP2DRES',
                     'NP2HYGN',	'NP2HWRT',	'NP2HOBB',	'NP2TURN',	'NP2TRMR',	
                     'NP2RISE',	'NP2WALK',	'NP2FREZ']

            if filename == 'MDS_UPDRS_Part_III__Post_Dose_.csv':
                if featname == 'MDS-UPDRS':
                    fname = ['NP3SPCH',	'NP3FACXP',	'NP3RIGN',	
                     'NP3RIGRU',	'NP3RIGLU',	'PN3RIGRL',	'NP3RIGLL',	'NP3FTAPR',
                     'NP3FTAPL',	'NP3HMOVR',	'NP3HMOVL',	'NP3PRSPR',	'NP3PRSPL',
                     'NP3TTAPR',	'NP3TTAPL',	'NP3LGAGR',	'NP3LGAGL',	'NP3RISNG',	
                     'NP3GAIT',	'NP3FRZGT',	'NP3PSTBL',	'NP3POSTR',	'NP3BRADY',
                     'NP3PTRMR',	'NP3PTRML',	'NP3KTRMR',	'NP3KTRML',	'NP3RTARU',
                     'NP3RTALU',	'NP3RTARL',	'NP3RTALL',	'NP3RTALJ',	'NP3RTCON']
                if featname == 'H&Y':
                    fname = ['NHY']
                if featname == None:
                    fname = ['NP3SPCH',	'NP3FACXP',	'NP3RIGN',	
                     'NP3RIGRU',	'NP3RIGLU',	'PN3RIGRL',	'NP3RIGLL',	'NP3FTAPR',
                     'NP3FTAPL',	'NP3HMOVR',	'NP3HMOVL',	'NP3PRSPR',	'NP3PRSPL',
                     'NP3TTAPR',	'NP3TTAPL',	'NP3LGAGR',	'NP3LGAGL',	'NP3RISNG',	
                     'NP3GAIT',	'NP3FRZGT',	'NP3PSTBL',	'NP3POSTR',	'NP3BRADY',
                     'NP3PTRMR',	'NP3PTRML',	'NP3KTRMR',	'NP3KTRML',	'NP3RTARU',
                     'NP3RTALU',	'NP3RTARL',	'NP3RTALL',	'NP3RTALJ',	'NP3RTCON',
                     'NHY']
         
            if filename == 'MDS_UPDRS_Part_IV.csv':
                fname = ['NP4WDYSK',	'NP4DYSKI',	'NP4OFF', 'NP4FLCTI', 'NP4FLCTX',	 'NP4DYSTN']

        except ValueError:
            print ('please enter correct file name or feature name!')
            
        return fname
        
        
    def get_feature_set(self, fname=None, featname=None):
        feature_set = set()
        try:
            if fname == 'MDS UPDRS PartI':
                feature_set = set(['NP1COG', 'NP1HALL',	'NP1DPRS', 'NP1ANXS', 'NP1APAT',	'NP1DDS',
                                   'NP1SLPN',	'NP1SLPD',	'NP1PAIN',	'NP1URIN',	'NP1CNST',	'NP1LTHD',	'NP1FATG'])
                
            if fname == 'MDS UPDRS PartII':
                feature_set = set(['NP2SPCH', 'NP2SALV', 'NP2SWAL', 'NP2EAT', 'NP2DRES',
                                   'NP2HYGN',	'NP2HWRT',	'NP2HOBB',	'NP2TURN',	'NP2TRMR',	
                                   'NP2RISE',	'NP2WALK',	'NP2FREZ'])
                
            if fname == 'MDS UPDRS PartIII':
                if featname == 'MDS-UPDRS':
                    feature_set = set(['NP3SPCH',	'NP3FACXP',	'NP3RIGN',	
                     'NP3RIGRU',	'NP3RIGLU',	'PN3RIGRL',	'NP3RIGLL',	'NP3FTAPR',
                     'NP3FTAPL',	'NP3HMOVR',	'NP3HMOVL',	'NP3PRSPR',	'NP3PRSPL',
                     'NP3TTAPR',	'NP3TTAPL',	'NP3LGAGR',	'NP3LGAGL',	'NP3RISNG',	
                     'NP3GAIT',	'NP3FRZGT',	'NP3PSTBL',	'NP3POSTR',	'NP3BRADY',
                     'NP3PTRMR',	'NP3PTRML',	'NP3KTRMR',	'NP3KTRML',	'NP3RTARU',
                     'NP3RTALU',	'NP3RTARL',	'NP3RTALL',	'NP3RTALJ',	'NP3RTCON'])
                if featname == 'H&Y':
                    feature_set = set(['NHY'])
                if featname == None:
                    feature_set = set (['NP3SPCH',	'NP3FACXP',	'NP3RIGN',	
                     'NP3RIGRU',	'NP3RIGLU',	'PN3RIGRL',	'NP3RIGLL',	'NP3FTAPR',
                     'NP3FTAPL',	'NP3HMOVR',	'NP3HMOVL',	'NP3PRSPR',	'NP3PRSPL',
                     'NP3TTAPR',	'NP3TTAPL',	'NP3LGAGR',	'NP3LGAGL',	'NP3RISNG',	
                     'NP3GAIT',	'NP3FRZGT',	'NP3PSTBL',	'NP3POSTR',	'NP3BRADY',
                     'NP3PTRMR',	'NP3PTRML',	'NP3KTRMR',	'NP3KTRML',	'NP3RTARU',
                     'NP3RTALU',	'NP3RTARL',	'NP3RTALL',	'NP3RTALJ',	'NP3RTCON',
                     'NHY'])
                    
            if fname == 'MDS UPDRS PartIV':
                feature_set = set(['NP4WDYSK','NP4DYSKI','NP4OFF', 'NP4FLCTI', 'NP4FLCTX',	'NP4DYSTN'])
        
            if fname == 'Motor Subtype':
                feature_set = set(['NP2TRMR', 'NP3PTRMR',	'NP3PTRML',	'NP3KTRMR',	'NP3KTRML',	'NP3RTARU',
                     'NP3RTALU',	'NP3RTARL',	'NP3RTALL',	'NP3RTALJ',	'NP3RTCON', 'NP2WALK',	'NP2FREZ',
                     'NP3GAIT',	'NP3FRZGT',	'NP3PSTBL'])
        except ValueError:
            print ('please enter correct feature name!')
            
        return feature_set
        
    def load_subtype(self, patient_id, patient_cluster, timestamp = 'baseline'):
        epsilon = sys.float_info.epsilon
        feat_info = self.feature_info 
        fname = 'Motor Subtype'
        pat_TD_mean = dict() # pid: mean feature value related with TD
        pat_PIGD_mean = dict() # pid: mean feature value related with PIGD
        PIGD_set = set(['NP2WALK', 'NP2FREZ', 'NP3GAIT',	'NP3FRZGT', 'NP3PSTBL'])
        for fn, tpl_list in feat_info.items():
            if fn not in self.get_feature_set(fname):
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
                 
                if pat not in patient_id:
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
           
            # store first values 
            for pat, tf_list in pat_new_record.items():  
                if timestamp == 'baseline':
                    time_idx = 0
                    pat_fval = tf_list[time_idx][1]
                elif timestamp == 'follow-up':
                    time_idx = -1
                    pat_fval = tf_list[time_idx][1]
                elif timestamp == 'median':
#                    print ('--------')
                    if len(tf_list) % 2 == 1:
                        time_idx = math.floor(len(tf_list)/2)
                        pat_fval = tf_list[time_idx][1]
#                        print (time_idx)
                    else:
                        time_idx1 = math.floor(len(tf_list)/2)
                        time_idx2 = time_idx1-1
#                        print (time_idx1)
#                        print (time_idx2)
                        pat_fval = (tf_list[time_idx1][1] + tf_list[time_idx2][1])/2
                    print (len(tf_list))
                
                if fn in PIGD_set:
                    if pat not in pat_PIGD_mean:
                        pat_PIGD_mean[pat] = 0
                    pat_PIGD_mean[pat] += pat_fval
                else: 
                    if pat not in pat_TD_mean:
                        pat_TD_mean[pat] = 0
                    pat_TD_mean[pat] += pat_fval
        # categorization according to motor subtypes
        for pat in patient_id:
            if pat in pat_PIGD_mean and pat in pat_TD_mean:
                pat_TD_mean[pat] /= 11
                pat_PIGD_mean[pat] /= 5
                motor_ratio = pat_TD_mean[pat]/(pat_PIGD_mean[pat]+epsilon)
                if motor_ratio >= 1.15:
                    patient_cluster[pat] = '1' # TD Subtype
                elif motor_ratio <= 0.90:
                    patient_cluster[pat] = '2' # PIGD Subtype
                else:
                    patient_cluster[pat] = '3' # indetermine Subtype        
        print (patient_cluster)

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
        
    def get_motor(self, dataio, K, fname=None, featname=None):
        pat_cluster = dataio.patient_cluster
        feat_info = dataio.feature.motor.feature_info
       
        # initialization for each cluster
        for i in range(1, K+1):
           self.MOTOR[str(i)] = list()
           self.MOTOR_first[str(i)] = list()
           self.MOTOR_median[str(i)] = list()
       
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
                self.MOTOR[str(cls)].append(pat_fval_last[pat])
            if pat in pat_fval_median:
                self.MOTOR_median[str(cls)].append(pat_fval_median[pat])
            if pat in pat_fval_first:
                self.MOTOR_first[str(cls)].append(pat_fval_first[pat])
        # compute statistics
        # mean , std
        stats = Statistics(K)
        mean_MOTOR, std_MOTOR=stats.get_mean_std(self.MOTOR, is_total=False)
        mean_MOTOR_median, std_MOTOR_median=stats.get_mean_std(self.MOTOR_median, is_total=False)
        mean_MOTOR_first, std_MOTOR_first=stats.get_mean_std(self.MOTOR_first, is_total=False)
        mean_total_MOTOR, std_total_MOTOR = stats.get_mean_std(self.MOTOR, is_total=True)   
        mean_total_MOTOR_median, std_total_MOTOR_median = stats.get_mean_std(self.MOTOR_median, is_total=True)   
        mean_total_MOTOR_first, std_total_MOTOR_first = stats.get_mean_std(self.MOTOR_first, is_total=True)   
        
        if featname != None:
            fname_ = fname + '-' + featname
        else:
            fname_ = fname
        self.mean[fname_] = list()
        self.mean_first[fname_] = list()
        self.mean_median[fname_] = list()
        for i in range(1, K+1):
           self.mean[fname_].append((mean_MOTOR[str(i)], std_MOTOR[str(i)]))
           self.mean_first[fname_].append((mean_MOTOR_first[str(i)], std_MOTOR_first[str(i)]))
           self.mean_median[fname_].append((mean_MOTOR_median[str(i)], std_MOTOR_median[str(i)]))
        # display  
        if featname != None:
            print ('feature name: %s' %featname)
        else:
            print ('feature name: %s' %fname)
        for i in range(1, K+1):
            print ('### CLUSTER %d ####' %i)
            print ("The average value in the %d-th clusters at follow-up is: %f (%f)" %(i, mean_MOTOR[str(i)], std_MOTOR[str(i)]))
            print ("The average value in the %d-th clusters at baseline is: %f (%f)" %(i, mean_MOTOR_first[str(i)], std_MOTOR_first[str(i)]))
            print ("The average value in the %d-th clusters at median is: %f (%f)" %(i, mean_MOTOR_median[str(i)], std_MOTOR_median[str(i)]))
        print ("The total average %s at follow-up is: %f (%f)" %(fname, mean_total_MOTOR, std_total_MOTOR))
        print ("The total average %s at median is: %f (%f)" %(fname, mean_total_MOTOR_median, std_total_MOTOR_median))
        print ("The total average %s at baseline is: %f (%f)" %(fname, mean_total_MOTOR_first, std_total_MOTOR_first))
        print ("##########")
              
        # hypothesis testing
        print ("hypothesis testing...")
        if fname == 'MDS UPDRS PartIV':
            if featname != None:
                fname = fname + '-' + featname
            # fisher exact
#            stats.get_distribution(pat_fval_first, is_num=True)
            p_first = stats.get_fisher_exact(pat_fval_first, pat_cluster, fname, 'FIRST')
#            stats.get_distribution(pat_fval_median, is_num=True)
            p_median = stats.get_fisher_exact(pat_fval_median, pat_cluster, fname, 'MEDIAN')
#            stats.get_distribution(pat_fval_last, is_num=True)
            p_last = stats.get_fisher_exact(pat_fval_last, pat_cluster, fname, 'LAST')
#            stats.get_distribution(pat_fval_diff, is_num=True)
            p_diff = stats.get_fisher_exact(pat_fval_diff, pat_cluster, fname, 'DIFFERENCE')
            self.p_value.append([fname, p_first, p_median, p_last, p_diff])
        else:
            if featname != None:
                fname = fname + '-' + featname
            # chi-square
#            stats.get_distribution(pat_fval_first, is_num=True)
            p_first = stats.get_chisquare(pat_fval_first, pat_cluster, fname, 'FIRST')
#            stats.get_distribution(pat_fval_median, is_num=True)
            p_median = stats.get_chisquare(pat_fval_median, pat_cluster, fname, 'MEDIAN')
#            stats.get_distribution(pat_fval_last, is_num=True)
            p_last = stats.get_chisquare(pat_fval_last, pat_cluster, fname, 'LAST')
#            stats.get_distribution(pat_fval_diff, is_num=True)
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
            
        self.mean_total[fname] = (mean_total_MOTOR, std_total_MOTOR)
        print ('-----------------------')
   