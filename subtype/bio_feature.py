# -*- coding: utf-8 -*-
import math
import csv, codecs
import operator

from statistics import Statistics
from time_converter import convert_time, convert_int
from numeric import isfloat, isint

class BioFeature(object):
    
    def __init__(self):
        self.feature_info = dict() # feature name: list(pat_id, timestamp, feature_val)
        # biospecimen
        # the dictionaries store the last state feature values
        self.BIO = dict() # cluster: biospecimen feature value
        # the dictionaries store the first state feature values 
        self.BIO_first = dict() # cluster: biospecimen feature value
        # the dictionaries store the median state feature values 
        self.BIO_median = dict() # cluster: biospecimen feature value
     
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
        if fname == 'CSF':
            self.read_feature('Biospecimen_Analysis_Results1.csv', featname, date_key='RUNDATE')
        elif fname == 'Blood':
            self.read_feature('Blood_Chemistry___Hematology.csv', date_key='LCOLLDT')
        elif fname == 'ClinicalLab':
            self.read_feature('Clinical_Labs.csv',date_key='INFODT')
        elif fname == 'DNA':
            self.read_feature('DNA_Sample_Collection.csv', date_key='INFODT')
        elif fname == 'LUMBAR':
            self.read_feature('Lumbar_Puncture_Sample_Collection.csv', date_key='INFODT')
        elif fname == 'GENETIC':
            self.read_feature('Genetic_Testing_Results.csv', date_key='INFODT')
#        elif fname == 'SBE':
#            self.read_feature('Skin_Biopsy_Eligibility.csv')
        elif fname == 'SKIN':
            self.read_feature('Skin_Biopsy.csv', date_key='INFODT')
        elif fname == 'WholeBlood':
            self.read_feature('Whole_Blood_Sample_Collection.csv', date_key='INFODT')
        else:
            pass
        
    def read_feature(self, filename, featname=None, time_convert=False, date_key=None, pid_name='PATNO'):
        fname = self.get_feature_name(filename)
        f = codecs.open('../biospecimen/' + filename, 'r', 'utf-8')
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
            if filename == 'Biospecimen_Analysis_Results1.csv':
                if row[table_ttl['TESTNAME']] != featname:
                    continue
                else:
                    if row[table_ttl['CLINICAL_EVENT']] == 'Baseline Collection':
                        fval = row[table_ttl['TESTVALUE']]
                        if featname not in self.feature_info:
                            self.feature_info[featname] = list()
                        self.feature_info[featname].append([pat_id, info_date, fval])
                    continue
            
            for fn in fname:                   
                fval = row[table_ttl[fn]]
                self.feature_info[fn].append((pat_id, info_date, fval))        
            line_ctr +=1 
        f.close()
        return self.feature_info
        
    
    def get_feature_name(self, filename):
       
        if filename == 'Biospecimen_Analysis_Results1.csv':
            fname = ["DIAGNOSIS","CLINICAL_EVENT","TYPE","TESTNAME","TESTVALUE","UNITS","RUNDATE",
            "PROJECTID","PI_NAME","PI_INSTITUTION","update_stamp"]

        if filename == 'Blood_Chemistry___Hematology.csv':
            fname = ["LCOLLDT","COLLTM","LRECDT","RECTM","LRPTDT","RPTTM","LABCODE","LGROUP","LTSTCODE","LTSTNAME",
            "LVISTYPE","LSIRES","LSIUNIT","LSILORNG","LSIHIRNG","LUSRES","LUSUNIT","LUSLORNG","LUSHIRNG","LRESFLG","LTSTCOMM"]
            
        if filename == 'Clinical_Labs.csv':
            fname = ["BLDLAB", "BLDSHPDT"]

        if filename == 'DNA_Sample_Collection.csv':
#            fname = ["BLDDNA","BLDDNADT","BLDVOLML","DNASHPDT"]
            fname = ["BLDVOLML"]

        if filename == 'Genetic_Testing_Results.csv':
            fname = ["GENECAT","LRRKCD","MUTRSLT"]

        if filename == 'Laboratory_Procedures1.csv':
            fname = ['LMDT','LMTM','FASTSTAT','PDMEDYN','PDMEDDT','PDMEDTM','UASPEC','UASPECDT','UT1TM','UT1SPNTM','UT1SPNRT',
                     'UT1SPNDR','UT1CFRG','UT1FTM','BLDDRDT','BLDRNA','BLDRNATM','RNAFDT','RNAFTM',
                     'RNASTTMP','BLDPLAS','PLASTM','PLASPNTM','PLASPNRT','PLASPNDR','PLASCFRG','PLASVAFT',
                     'PLAALQN','PLASFTM','PLASTTMP','BLDSER','BLDSERTM','BSSPNTM','BSSPNRT','BSSPNDR','BSCFRG','BSVAFT',
                     'BSALQN','BSFTM','BSSTTMP','PLASBFCT']

        if filename == 'Lumbar_Puncture_Sample_Collection.csv':
            fname = ["LMDT","LMTM","FASTSTAT","PDMEDYN","PDMEDDT","PDMEDTM","CSFCOLL","CSFDT","CSFNEEDL","CSFMETHD",
            "LPSITE","LPPOSITN","CSFTM","CSFVPRI","CSFSPNTM","CSFSPNRT","CSFSPNDR","CSFCFRG","CSFALQTM","CSFVAFT",
            "CSFALQN","SMPDSCRD","CSFFFTM","CSFSTTMP","SMPLOCAL","WBCRSLT","WBCUNITB","WBCOTHCM","RBCRSLT","RBCUNITB",
            "RBCOTHCM","TOPRRSLT","TOPRUNIT","TGLCRSLT","TGLCUNIT","FLUORO","FLUORODT","SPFI","SPFIDT","LPNDRSN"]

        if filename == 'Skin_Biopsy_Eligibility.csv':
            fname = ["SIGNCNST","SKBICNDT","INEX1","INEX2","INEX3","INEX4","INEX5","INEX6","INEX7","INEX8"]

        if filename == 'Skin_Biopsy.csv':
            fname = ["SKBIOCMP","ANSTHADM","SKBIOLOC","SBIOLCCM","SKBIOSID","BIOCMPLC",
            "WOUNDCLS","WNDCLSCM","BIOCOLTM","BIOFRGTM","SHIPDT"]

        if filename == 'Whole_Blood_Sample_Collection.csv':
            fname = ["BLDCOLL","BLDCLLDT"]    
        
        return fname

        
    def get_feature_set(self, fname=None, featname=None):
        feature_set = set()
        try:
            if fname == 'DNA':
                feature_set = set(["BLDVOLML"])
                                
            if fname == 'CSF':
                if featname == 'Total tau':
                    feature_set = set(['Total tau'])
                if featname == 'Abeta 42':
                    feature_set = set(['Abeta 42'])
                if featname == 'p-Tau181P':
                    feature_set = set(['p-Tau181P'])
                if featname == 'CSF Alpha-synuclein':
                    feature_set = set(['CSF Alpha-synuclein'])
                if featname == None:
                    feature_set = set (['Total tau', 'Abeta 42', 'p-Tau181P', 'CSF Alpha-synuclein'])   
        
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

    def get_biospecimen(self, dataio, K, fname=None, featname=None):
        pat_cluster = dataio.patient_cluster
        feat_info = dataio.feature.biospecimen.feature_info
       
        # initialization for each cluster
        for i in range(1, K+1):
           self.BIO[str(i)] = list()
           self.BIO_first[str(i)] = list()
           self.BIO_median[str(i)] = list()
           
        # intialization for patient and the corresponding feature value
        pat_fval_first = dict() # patient id : first feature value
        pat_fval_median = dict() # patient id : median feature value
        pat_fval_last = dict() # patient id : last feature value
        pat_fval_diff = dict() # patient id : first-order difference 
                                   # between last and first feature value 
      
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
                self.BIO[str(cls)].append(pat_fval_last[pat])
            if pat in pat_fval_first:
                self.BIO_first[str(cls)].append(pat_fval_first[pat])
            if pat in pat_fval_median:
                self.BIO_median[str(cls)].append(pat_fval_median[pat])

        # compute statistics
        # mean , std
        stats = Statistics(K)
        mean_BIO, std_BIO=stats.get_mean_std(self.BIO, is_total=False)
        mean_total_BIO, std_total_BIO = stats.get_mean_std(self.BIO, is_total=True) 
        mean_BIO_first, std_BIO_first=stats.get_mean_std(self.BIO_first, is_total=False)
        mean_total_BIO_first, std_total_BIO_first = stats.get_mean_std(self.BIO_first, is_total=True)   
        mean_BIO_median, std_BIO_median=stats.get_mean_std(self.BIO_median, is_total=False)
        mean_total_BIO_median, std_total_BIO_median = stats.get_mean_std(self.BIO_median, is_total=True)   
        if featname != None:
            fname_ = fname + '-' + featname
        else:
            fname_ = fname
        self.mean[fname_] = list()
        self.mean_first[fname_] = list()
        self.mean_median[fname_] = list()
        for i in range(1, K+1):
           self.mean[fname_].append((mean_BIO[str(i)], std_BIO[str(i)]))
           self.mean_first[fname_].append((mean_BIO_first[str(i)], std_BIO_first[str(i)]))
           self.mean_median[fname_].append((mean_BIO_median[str(i)], std_BIO_median[str(i)]))
        # display  
        for i in range(1, K+1):
            print ('### CLUSTER %d ####' %i)
            print ("The average %s value in the %d-th clusters at follow-up is: %f (%f)" %(fname, i, mean_BIO[str(i)], std_BIO[str(i)]))
            print ("The average value in the %d-th clusters at baseline is: %f (%f)" %(i, mean_BIO_first[str(i)], std_BIO_first[str(i)]))
            print ("The average value in the %d-th clusters at median is: %f (%f)" %(i, mean_BIO_median[str(i)], std_BIO_median[str(i)]))
        print ("The total average %s at follow-up is: %f (%f)" %(fname, mean_total_BIO, std_total_BIO))
        print ("The total average %s at baseline is: %f (%f)" %(fname, mean_total_BIO_first, std_total_BIO_first))
        print ("The total average %s at median is: %f (%f)" %(fname, mean_total_BIO_median, std_total_BIO_median))
        print ("##########")
              
        # hypothesis testing
        print ("hypothesis testing...")
        if fname == 'CSF':
            if featname != None:
                fname = fname + '-' + featname
#            stats.get_distribution(pat_fval_last, is_num=True, is_discretization=True)
            if featname == 'Total tau' or featname == 'Abeta 42':
                p_last = stats.get_f_oneway(pat_fval_last, pat_cluster, fname, 'STATIC')
            if featname == 'p-Tau181P' or featname == 'CSF Alpha-synuclein':
                p_last = stats.get_kruskal(pat_fval_last, pat_cluster, fname, 'STATIC')
            self.p_value.append([fname, None, None, p_last, None])   
        else:
            if featname != None:
                fname = fname + '-' + featname
#            stats.get_distribution(pat_fval_first, is_num=True)
            p_first = stats.get_chisquare(pat_fval_first, pat_cluster, fname, 'FIRST')
#            stats.get_distribution(pat_fval_median, is_num=True)
            p_median = stats.get_chisquare(pat_fval_median, pat_cluster, fname, 'MEDIAN')
#            stats.get_distribution(pat_fval_last, is_num=True)
            p_last = stats.get_chisquare(pat_fval_last, pat_cluster, fname, 'LAST')
#            stats.get_distribution(pat_fval_diff, is_num=True)
            p_diff = stats.get_chisquare(pat_fval_diff, pat_cluster, fname, 'DIFFERENCE')
            # store into self.p_value
            self.p_value.append([fname, p_first, p_median, p_last, p_diff])
            
        # post hoc test    
#        if p_first <= 0.05:
#            stats.get_tukeyhsd(pat_fval_first, pat_cluster, fname, 'FIRST')
#        if p_median <= 0.05:
#            stats.get_tukeyhsd(pat_fval_median, pat_cluster, fname, 'MEDIAN')
        if p_last <= 0.05:
            stats.get_tukeyhsd(pat_fval_last, pat_cluster, fname, 'LAST')
#        if p_diff <= 0.05:
#            stats.get_tukeyhsd(pat_fval_diff, pat_cluster, fname, 'DIFFERENCE')
            
        self.mean_total[fname] = (mean_total_BIO, std_total_BIO)
        print ('-----------------------')