# -*- coding: utf-8 -*-

from feature import Feature

class Patient(object):
    
   def __init__(self):
       # denographic feature
       self.id = int()
       self.prim_diag = str()
       self.birth = int()
       self.age = -1
       self.gender = str()
       self.race = str()
       self.enrol_date = str()
       self.duration = -1
       self.handness = str()
       self.edu_year = -1 # education year
       self.fam_his = list() # family disease history
       self.rec_id = list() # record id
       # all other non-demographic features 
       self.feature = Feature() # feature instance including kinds of features: motor, cognitive...
       
           
   def update(self, fval, fname):
       if fname == 'PRIMDIAG':
           self.prim_diag = fval
           
       if fname == 'GENDER':
           self.get_gender(fval)

       if fname == 'BIRTHDT':
           self.get_birth(fval)
           
       if fname == 'HISPLAT' and fval == '1':
           self.race = 'HISPLAT'
       if fname == 'RAINDALS' and fval == '1':
           self.race = 'RAINDALS'
       if fname == 'RAASIAN'and fval == '1':
           self.race = 'RAASIAN'
       if fname == 'RABLACK' and fval == '1':
           self.race = 'RABLACK'
       if fname == 'RAHAWOPI' and fval == '1':
           self.race = 'RAHAWOPI'
       if fname == 'RAWHITE' and fval == '1':
           self.race = 'RAWHITE'
       if fname == 'RANOS'and fval == '1':
           self.race = 'RANOS'
           
       if fname == 'EDUCYRS':
           self.get_edu_year(fval)  
           
       if fname == 'HANDED' and fval == '1':
           self.handness = 'Right'
       if fname == 'HANDED' and fval == '2':
           self.handness = 'Left'
       if fname == 'HANDED' and fval == '3':
           self.handness = 'Mixed'
           
       if fname == 'ENROLL_DATE':
           self.get_enrol(fval)
           self.get_age()
           
       if fname == 'PDDXDT':
           self.get_duration(fval)
       
   def get_feature(self, pat_id):
       feature = self.feature
       return feature 
       
   def get_birth(self, fval):
       if fval != '':
           self.birth = int(fval)
       
   def get_age(self):
       if self.enrol_date != '':
           year = self.enrol_date[-4::]
           self.age = int(year) - int(self.birth)
   
    
   def get_gender(self, indicator):
       if indicator == '0' or indicator == '1':
           self.gender = 'Female' # with children
       elif indicator == '2':
           self.gender = 'Male'
        
   
   def get_edu_year(self, fval):
       if fval != '':
           self.edu_year = int(fval)
         
           
   def get_enrol(self, fval):
       if fval != '':
           self.enrol_date = fval

           
   def get_duration(self, pdd_date):
       if pdd_date != '' and self.enrol_date != '':
           pdd_month, pdd_year = pdd_date.split('/')
           enrol_month, enrol_year = self.enrol_date.split('/')
           month = int(enrol_month) - int(pdd_month)
           year = int(enrol_year) - int(pdd_year)
           self.duration = year*12 + month
           
   
   def get_fam_his(self):
       pass
   
        

   