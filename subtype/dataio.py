# -*- coding: utf-8 -*-

import sys
import math
import csv, codecs
import numpy
import operator
from patient import Patient
from feature import Feature
from numeric import isfloat, isint
from time_converter import convert_int

class DataIO(object):
    
    def __init__(self, K, middle_state=None):
        self.K = K
        self.middle_state = middle_state
        self.patient_cluster = dict() # pat_id: cluster index
        self.patient_info = dict() # pat_id: Patient
        self.patient_id = list() # pat_id
        self.feature = Feature() # store 
    

    def load_clustering_result(self, file):
        f = codecs.open(file, 'r', 'utf-8')
        reader = csv.reader(f)
        line_ctr = 0
        for row in reader:
            # table title
            if line_ctr < 1:
                table_ttl = dict(zip(row, range(len(row))))
                line_ctr += 1
                continue
            
            pid = row[table_ttl['PATNO']]
            cluster_idx = row[table_ttl['CLUSTER_IDX']]
            self.patient_cluster[pid] = cluster_idx
            line_ctr += 1
        f.close()
        print (self.patient_cluster)

        
    def load_patient_id(self, file):
        f = codecs.open(file, 'r', 'utf-8')
        reader = csv.reader(f)
        line_ctr = 0
        for row in reader:
            # table title
            if line_ctr < 1:
                table_ttl = dict(zip(row, range(len(row))))
                line_ctr += 1
                continue
            
            pid = row[table_ttl['PATNO']]
            self.patient_id.append(pid)
            line_ctr += 1
        f.close()

    def load_subtype(self, subtype_method, timestamp = 'baseline'):
        if subtype_method == 'Motor Subtype':
            self.feature.motor.load_subtype(self.patient_id, self.patient_cluster, timestamp)
        elif subtype_method == 'Cognitive Subtype':
            self.feature.nonmotor.load_subtype(self.patient_id, self.patient_cluster, subtype_method, timestamp)
        elif subtype_method == 'Mood Subtype':
            self.feature.nonmotor.load_subtype(self.patient_id, self.patient_cluster, subtype_method, timestamp)
                 
    def load_demographics(self, file):
        f = codecs.open(file, 'r', 'utf-8')
        reader = csv.reader(f)
        line_ctr = 0
        for row in reader:
            # table title
            if line_ctr < 1:
                table_ttl = dict(zip(row, range(len(row))))
                line_ctr += 1
                continue
            if len(row) == 0:
                continue
            pval = Patient()
            pid = row[table_ttl['ID']]
            pval.age = row[table_ttl['AGE']]
            pval.gender = row[table_ttl['GENDER']]
            pval.edu_year = row[table_ttl['EDUCATION YEAR']]
            pval.duration = row[table_ttl['DURATION(MONTH)']]
            self.patient_info[pid] = pval
            line_ctr += 1
        f.close()
 
    def load_feature(self, ftype=None, fname=None,  featname=None):
        self.feature.load_feature(ftype, fname, featname)
        
    def save_result(self, var, filename):
        
        # save pvalue of each feature
        file = open(filename, 'w')
        writer = csv.writer(file)
        if self.K == 2:
            titleline = ['Feature', 'Initial P-Value', 'Median P-Value', 'Final P-Value', 'Difference P-Value', 'Initial Cluster1 Mean',  'Final Cluster1 Mean', 'Initial Cluster2 Mean', 'Final Cluster2 Mean']
        elif self.K == 3:
            titleline = ['Feature', 'Initial P-Value', 'Median P-Value', 'Final P-Value', 'Difference P-Value', 'Initial Cluster1 Mean', 'Median Cluster1 Mean', 'Final Cluster1 Mean', 
            'Initial Cluster2 Mean', 'Median Cluster2 Mean', 'Final Cluster2 Mean',
            'Initial Cluster3 Mean', 'Median Cluster3 Mean', 'Final Cluster3 Mean']
        writer.writerow(titleline)
        
        stats_info = list()
        p_value = var.p_value # feature name, p value tuple (first, median, final) 
        print (p_value)
        mean_std = var.mean # feature name : [(cluster1_mean, cluster1_std), ...]
#        mean_std_median = var.mean_median  # feature name: [(cluster1_mean, cluster1_std), ...]
        mean_std_first = var.mean_first # feature name: [(cluster1_mean, cluster1_std), ...]
        for line in p_value:
            fn = line[0]
            if fn in mean_std:
                ms = mean_std[fn]
                if fn in mean_std_first:
                    msf = mean_std_first[fn]
#                if fn in mean_std_median:
#                    msm = mean_std_median[fn]
                for i in range(var.K):
                    if fn in mean_std_first:
                        line.extend([str(msf[i][0]) + '(' + str(msf[i][1]) + ')'])
                    else:
                        line.extend([None])
                        
#                    if fn in mean_std_median:
#                        line.extend([str(msm[i][0]) + '(' + str(msm[i][1]) + ')'])
#                    else:
#                        line.extend([None])
                    line.extend([str(ms[i][0]) + '(' + str(ms[i][1]) + ')'])
            
            if line[0] == 'CSF-CSF Alpha-synuclein':
                line[0] = 'CSF Alpha-synuclein'
                
            if fn == 'MDS UPDRS PartIII-H&Y':
                fn = 'H&Y'
               
            if fn == 'MDS UPDRS PartIII-MDS-UPDRS':
                fn = 'MDS UPDRS PartIII'
                
            stats_info.append(line)
                        
        writer.writerows(stats_info)   
        file.close()
        
 
 