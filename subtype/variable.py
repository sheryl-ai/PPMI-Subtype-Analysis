# -*- coding: utf-8 -*-


from feature import Feature

class Variable(object):
    
    def __init__(self, K):
       self.K = K
       self.feature = Feature()
       self.pat_edu = dict()
       # p-value: first, median, last
       self.p_value = list() # feature name, p-value tuple (first, median, last, diff)
       self.mean = dict() # feature name : list(cluster1_mean, cluster1_std, ...)}
                          # mean of the last state for temporal features
       self.mean_first = dict() # feature name : list(cluster1_mean, cluster1_std, ...)
                                # mean of the first state for temporal fatures
       self.mean_median = dict()
       self.mean_total = dict() # feature name : (total mean, total std) 
       self.mean_follow_up = dict() # feature name : mean follow-up time in this feature 
       
           
############################ VARIABLES ANALYSIS ###############################
    def get_variables(self, dataio, ftype, fname=None, featname=None, pat_edu=None):
        if ftype == 'demographics':
            self.pat_edu = self.feature.demographics.get_demographics(dataio, self.K)
            self.mean.update(self.feature.demographics.mean)
            self.mean_total.update(self.feature.demographics.mean_total)
            self.mean_first.update(self.feature.demographics.mean_first)
            self.mean_median.update(self.feature.demographics.mean_median)
            self.mean_follow_up.update(self.feature.demographics.mean_follow_up)
            return self.feature.demographics.p_value
        elif ftype == 'motor':
            self.feature.motor.get_motor(dataio, self.K, fname, featname)
            self.mean.update(self.feature.motor.mean)
            self.mean_total.update(self.feature.motor.mean_total)
            self.mean_first.update(self.feature.motor.mean_first)
            self.mean_median.update(self.feature.motor.mean_median)
            self.mean_follow_up.update(self.feature.motor.mean_follow_up)
            return self.feature.motor.p_value
        elif ftype == 'nonmotor':
            self.feature.nonmotor.get_nonmotor(dataio, self.K, fname, featname, pat_edu)
            self.mean.update(self.feature.nonmotor.mean)
            self.mean_total.update(self.feature.nonmotor.mean_total)
            self.mean_first.update(self.feature.nonmotor.mean_first)
            self.mean_median.update(self.feature.nonmotor.mean_median)
            self.mean_follow_up.update(self.feature.nonmotor.mean_follow_up)
            return self.feature.nonmotor.p_value
        elif ftype == 'biospecimen':
            self.feature.biospecimen.get_biospecimen(dataio, self.K, fname, featname)
            self.mean.update(self.feature.biospecimen.mean)
            self.mean_total.update(self.feature.biospecimen.mean_total)
            self.mean_first.update(self.feature.biospecimen.mean_first)
            self.mean_median.update(self.feature.biospecimen.mean_median)
            self.mean_follow_up.update(self.feature.biospecimen.mean_follow_up)
            return self.feature.biospecimen.p_value
        elif ftype == 'image':
            self.feature.image.get_image(dataio, self.K, fname, featname)
            self.mean.update(self.feature.image.mean)
            self.mean_total.update(self.feature.image.mean_total)
            self.mean_first.update(self.feature.image.mean_first)
            self.mean_median.update(self.feature.image.mean_median)
            self.mean_follow_up.update(self.feature.image.mean_follow_up)
            return self.feature.image.p_value
        elif ftype == 'medication':
            self.feature.medication.get_medication(dataio, self.K, fname, featname)
            self.mean.update(self.feature.medication.mean)
            self.mean_total.update(self.feature.medication.mean_total)
            self.mean_first.update(self.feature.medication.mean_first)
            self.mean_median.update(self.feature.medication.mean_median)
            self.mean_follow_up.update(self.feature.medication.mean_follow_up)
            return self.feature.medication.p_value
        else:
            print ("Error!! ftype must be one of {dempraphics, motor, nonmotor, biospecimen, image, and medication}!!")
