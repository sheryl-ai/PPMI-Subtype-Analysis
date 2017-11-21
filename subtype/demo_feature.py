# -*- coding: utf-8 -*-
 
from statistics import Statistics
 
class DemoFeature(object):
    
    def __init__(self):
        self.age = int()
        self.gender = str()
        self.race = str()
        self.handness = str()
        self.edu_year = int() # education year
        self.fam_his = list() # family disease history
        
        ### demo statistics variables:
        self.Male = dict() # cluster : count number
        self.Female = dict() 
        self.Age = dict() # cluster : age list
        self.Duration = dict() # cluster : month list
        self.Education = dict() # cluster : year list
        
        # p-value: first, median, last
        self.p_value = list() # feature name, p-value tuple (first, median, last, diff)
        self.mean = dict() # feature name : list(cluster1_mean, cluster1_std, ...)}
                          # mean of the last state for temporal features
        self.mean_first = dict() # feature name : list(cluster1_mean, cluster1_std, ...)
                                # mean of the first state for temporal fatures
        self.mean_median = dict()
        self.mean_total = dict() # feature name : (total mean, total std)
       
        self.mean_follow_up = dict() # feature name : mean follow-up time in this feature 
       

    def get_feature_name(self, filename):
       
        if filename == 'Primary_Diagnosis.csv':
            fname = ['PRIMDIAG']

        if filename == 'Screening_Demographics.csv':
            fname = ['APPRDX', 'CURRENT_APPRDX', 'BIRTHDT', 'GENDER', 'HISPLAT', 
             'RAINDALS', 'RAASIAN',	'RABLACK',	'RAHAWOPI',	'RAWHITE', 'RANOS', 	
             'PRJENRDT',	'REFERRAL',	'DECLINED',	'RSNDEC', 'EXCLUDED', 'RSNEXC']
            
        if filename == 'Patient_Status.csv':
            fname = ['IMAGING_CAT', 'ENROLL_DATE', 'ENROLL_CAT', 'ENROLL_STATUS']

        if filename == 'PD_Features.csv':
            fname = ['SXMO', 'SXYEAR', 'PDDXDT', 'PDDXEST', 'DXTREMOR',
                     'DXRIGID', 'DXBRADY',	'DXPOSINS',	'DXOTHSX', 'DXOTHCM', 'DOMSIDE']
            
        if filename == 'Family_History_PD_.csv':
            fname = ['BIOMOM', 'BIOMOMPD', 'BIODAD', 'BIODADPD', 'FULSIB', 'FULSIBPD',
                     'HAFSIB', 'HAFSIBPD',	'MAGPAR', 'MAGPARPD', 'PAGPAR', 'PAGPARPD', 
                     'MATAU', 'MATAUPD', 'PATAU', 'PATAUPD',	'KIDSNUM','KIDSPD']
 
        if filename == 'Socio-Economics.csv':
            fname = ['EDUCYRS', 'HANDED']
        return fname
        
        
    def get_demographics(self, dataio, K):
       pat_cluster = dataio.patient_cluster
       pat_info = dataio.patient_info
       
       # initialization for each cluster
       for i in range(1, K+1):
           self.Male[str(i)] = 0
           self.Female[str(i)] = 0
           self.Age[str(i)] = list()
           self.Duration[str(i)] = list()
           self.Education[str(i)] = list()
       
       pat_gender = dict() # patient id : gender
       pat_age = dict() # patient id : age
       pat_duration = dict() # patitent id : duration month
       pat_education = dict() # patient id : education year
       count = 0
       for pat, cls in pat_cluster.items():
           if pat not in pat_info:
               continue
           patient = pat_info[pat] # patient info
           
           if patient.age != '-1':
               self.Age[cls].append(int(patient.age))
               pat_age[pat] = int(patient.age)
           else:
#               print (pat)
               count += 1
               
           if patient.duration != '-1':
               self.Duration[cls].append(int(patient.duration))
               pat_duration[pat] = int(patient.duration)
#           else:
#               count += 1
               
           if patient.edu_year != '-1':
               self.Education[cls].append(int(patient.edu_year))
               pat_education[pat] = int(patient.edu_year)

           if patient.gender == 'Male':
               self.Male[cls] += 1
           elif patient.gender == 'Female':
               self.Female[cls] += 1
           else:
               continue
           
           if len(patient.gender) > 0:
               pat_gender[pat] = patient.gender
           else:
               continue

       # compute statistics
       # mean , std
       stats = Statistics(K)
       mean_Age, std_Age=stats.get_mean_std(self.Age, is_total=False)
       mean_Duration, std_Duration=stats.get_mean_std(self.Duration, is_total=False)
       mean_Education, std_Education=stats.get_mean_std(self.Education, is_total=False)
       mean_total_Age, std_total_Age = stats.get_mean_std(self.Age, is_total=True)
       mean_total_Duration, std_total_Duration = stats.get_mean_std(self.Duration, is_total=True)
       mean_total_Education, std_total_Education = stats.get_mean_std(self.Education, is_total=True)
       self.mean['age'] = list()
       self.mean['duration'] = list()
       self.mean['education'] = list()
       for i in range(1, K+1):
           self.mean['age'].append((mean_Age[str(i)], std_Age[str(i)]))
           self.mean['duration'].append((mean_Duration[str(i)], std_Duration[str(i)]))  
           self.mean['education'].append((mean_Education[str(i)], std_Education[str(i)]))

       self.mean_total['age'] = (mean_total_Age, std_total_Age)
       self.mean_total['duration'] = (mean_total_Duration, std_total_Duration)
       self.mean_total['education'] = (mean_total_Education, std_total_Education)
       # percentage      
       total_Male = 0
       total_Female = 0
       total_cls_Patient = dict()
       percent_cls_Patient = dict()
#       print (pat_cluster)
       for i in range(1, K+1):
           total_Male += self.Male[str(i)]
           total_Female += self.Female[str(i)]
           total_cls_Patient[str(i)] = self.Male[str(i)] + self.Female[str(i)]
           percent_cls_Patient[str(i)] = total_cls_Patient[str(i)]/len(pat_cluster)
       percent_Male = [val/total_Male for val in self.Male.values()]
       percent_Female = [val/total_Female for val in self.Female.values()]      
       
       # display  
       for i in range(1, K+1):
           if i == 2:
               print (self.Age[str(i)])
               print (self.Duration[str(i)])
           print ('### CLUSTER %d ####' %i)
           print ("The total number of Patient in the %d-th clusters is: %d (%f)" %(i, total_cls_Patient[str(i)], percent_cls_Patient[str(i)]))
           print ("The number of Male in the %d-th clusters is: %d (%f) " %(i, self.Male[str(i)], percent_Male[i-1]))
           print ("The number of Female in the %d-th clusters is: %d (%f)" %(i, self.Female[str(i)], percent_Female[i-1]))
           print ("The average Age in the %d-th clusters are: %f (%f)" %(i, mean_Age[str(i)], std_Age[str(i)]))
           print ("The average Duration in the %d-th clusters is: %f (%f)" %(i, mean_Duration[str(i)], std_Duration[str(i)]))
           print ("The average Education in the %d-th clusters is: %f (%f)" %(i, mean_Education[str(i)], std_Education[str(i)]))
       print ("The total average age is: %f (%f)" %(mean_total_Age,std_total_Age))
       print ("The total average duration is: %f (%f)" %(mean_total_Duration,std_total_Duration))
       print ("The total average education is: %f (%f)" %(mean_total_Education,std_total_Education))
       print ("##########")

       # hypothesis testing
       print ("hypothesis testing...")
       # chi-square
#       stats.get_distribution(pat_gender, is_num=False)
       p_last = stats.get_chisquare(pat_gender, pat_cluster, 'gender', 'STATIC')
#       if p_last <= 0.05: # post hoc test  
#           stats.get_tukeyhsd(pat_gender, pat_cluster, 'gender', 'STATIC')
       self.p_value.append(['gender', None, None, p_last, None]) 
       print ('-----------------------')
#       stats.get_distribution(pat_age, is_num=True)
       p_last = stats.get_f_oneway(pat_age, pat_cluster, 'age', 'STATIC')
       if p_last <= 0.05: # post hoc test  
#           print (pat_age)
           stats.get_tukeyhsd(pat_age, pat_cluster, 'age', 'STATIC')
       self.p_value.append(['age', None, None, p_last, None])
       print ('-----------------------')
#       stats.get_distribution(pat_duration, is_num=True)
       p_last = stats.get_f_oneway(pat_duration, pat_cluster, 'duration month', 'STATIC')
       if p_last <= 0.05: # post hoc test  
           stats.get_tukeyhsd(pat_duration, pat_cluster, 'duration month', 'STATIC')
       self.p_value.append(['duration', None, None, p_last, None])
       print ('-----------------------')
#       stats.get_distribution(pat_education, is_num=True)
       p_last = stats.get_f_oneway(pat_education, pat_cluster, 'education year', 'STATIC')
       if p_last <= 0.05: # post hoc test  
           stats.get_tukeyhsd(pat_education, pat_cluster, 'education year', 'STATIC')
       self.p_value.append(['education', None, None, p_last, None])
       print ('-----------------------')
       
          
       return pat_education