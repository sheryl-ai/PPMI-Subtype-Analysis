# -*- coding: utf-8 -*-

from demo_feature import DemoFeature
from motor_feature import MotorFeature
from nonmotor_feature import NonMotorFeature
from bio_feature import BioFeature
from image_feature import ImageFeature
from med_feature import MedFeature


class Feature(object):
    
    def __init__(self):
        self.demographics = DemoFeature()
        self.motor = MotorFeature()
        self.nonmotor = NonMotorFeature()
        self.biospecimen = BioFeature()
        self.image = ImageFeature() # education year
        self.medication = MedFeature() # family disease history
  
       
    def load_feature(self, ftype=None, fname=None, featname=None):
        try:
            if ftype == 'Motor':
                self.motor.load_feature(fname, featname)
            elif ftype == 'Non-Motor':
                self.nonmotor.load_feature(fname, featname)
            elif ftype == 'Biospecimen': 
                self.biospecimen.load_feature(fname, featname)
            elif ftype == 'Image': 
                self.image.load_feature(fname, featname) 
            elif ftype == 'Medication':
                self.medication.load_feature(fname, featname)
        except ValueError:
            print ('the type should be one of Motor, Non-Motor, Biospecimen, and Image!')
     
           
   