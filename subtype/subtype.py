# -*- coding: utf-8 -*-

import copy                                                                          
from dataio import DataIO
from variable import Variable
from display import Display
from comparable import Comparable

def main():

    result_path = 'results/'
    subtype_method = "Algorithm"
    K = 3 # number of subtypes(clusters)
############################## LOAD DATA ######################################
    print ('patients loading...')
    dataio = DataIO(K)
    dataio.load_demographics('../ufm/patient.csv')
    dataio.load_feature('Motor', 'MDS UPDRS PartI')
    dataio.load_feature('Motor', 'MDS UPDRS PartII')
    dataio.load_feature('Motor', 'MDS UPDRS PartIII')
    dataio.load_feature('Motor', 'MDS UPDRS PartIV')
    
    dataio.load_feature('Non-Motor', 'BJLO')
    dataio.load_feature('Non-Motor', 'ESS')
    dataio.load_feature('Non-Motor', 'GDS')
    dataio.load_feature('Non-Motor', 'HVLT')
    dataio.load_feature('Non-Motor', 'LNS')
    dataio.load_feature('Non-Motor', 'MoCA')
    dataio.load_feature('Non-Motor', 'QUIP')
    dataio.load_feature('Non-Motor', 'RBD')
    dataio.load_feature('Non-Motor', 'SCOPA-AUT')
    dataio.load_feature('Non-Motor', 'SF')
    dataio.load_feature('Non-Motor', 'STAI')
    dataio.load_feature('Non-Motor', 'SDM')
    dataio.load_feature('Non-Motor', 'MCI')
    
    dataio.load_feature('Biospecimen', 'DNA')
    dataio.load_feature('Biospecimen', 'CSF', 'Total tau')
    dataio.load_feature('Biospecimen', 'CSF', 'Abeta 42')
    dataio.load_feature('Biospecimen', 'CSF', 'p-Tau181P')
    dataio.load_feature('Biospecimen', 'CSF', 'CSF Alpha-synuclein')
            
    dataio.load_feature('Image', 'DaTScan SBR')
    dataio.load_feature('Image', 'MRI')
    dataio.load_feature('Medication', 'MED USE')
    suffix =  'normalized_clusters_Deep'
    dataio.load_clustering_result('input/clustering_by_lstm.csv')
    
############################# STATISTICS ######################################
    print ('-----------------------')
    print ('statistics analyzing...')
    var = Variable(K)
    ftype = 'demographics'
    p = var.get_variables(dataio, ftype)
    var.p_value.extend(p) 
    
    ftype = 'motor'
    _ = var.get_variables(dataio, ftype, 'MDS UPDRS PartI')
    _ = var.get_variables(dataio, ftype, 'MDS UPDRS PartII')
    _ = var.get_variables(dataio, ftype, 'MDS UPDRS PartIII', 'MDS-UPDRS')
    _ = var.get_variables(dataio, ftype, 'MDS UPDRS PartIII', 'H&Y')
    p = var.get_variables(dataio, ftype, 'MDS UPDRS PartIV')
    var.p_value.extend(p)
    
    ftype = 'nonmotor'
    _ = var.get_variables(dataio, ftype, 'BJLO')
    _ = var.get_variables(dataio, ftype, 'ESS')
    _ = var.get_variables(dataio, ftype, 'GDS')
    _ = var.get_variables(dataio, ftype, 'HVLT', 'Immediate Recall')
    _ = var.get_variables(dataio, ftype, 'HVLT', 'Discrimination Recognition')
    _ = var.get_variables(dataio, ftype, 'HVLT', 'Retention')
    _ = var.get_variables(dataio, ftype, 'LNS')
    print (var.pat_edu)
    _ = var.get_variables(dataio, ftype, 'MoCA', pat_edu=var.pat_edu)
    _ = var.get_variables(dataio, ftype, 'QUIP')
    _ = var.get_variables(dataio, ftype, 'RBD')
    _ = var.get_variables(dataio, ftype, 'SCOPA-AUT')
    _ = var.get_variables(dataio, ftype, 'SF')
    _ = var.get_variables(dataio, ftype, 'STAI')  
    _ = var.get_variables(dataio, ftype, 'SDM')
    p = var.get_variables(dataio, ftype, 'MCI')
    var.p_value.extend(p)
    
    ftype = 'biospecimen'
    var.get_variables(dataio, ftype, 'DNA')
    _ = var.get_variables(dataio, ftype, 'CSF', 'Total tau')
    _ = var.get_variables(dataio, ftype, 'CSF', 'Abeta 42')
    _ = var.get_variables(dataio, ftype, 'CSF', 'p-Tau181P')
    p = var.get_variables(dataio, ftype, 'CSF', 'CSF Alpha-synuclein')
    var.p_value.extend(p)
    
    ftype = 'image'
    _ = var.get_variables(dataio, ftype, 'DaTScan SBR', 'CAUDATE RIGHT')
    _ = var.get_variables(dataio, ftype, 'DaTScan SBR', 'CAUDATE LEFT')
    _ = var.get_variables(dataio, ftype, 'DaTScan SBR', 'PUTAMEN RIGHT')
    _ = var.get_variables(dataio, ftype, 'DaTScan SBR', 'PUTAMEN LEFT')
    p = var.get_variables(dataio, ftype, 'MRI')
    var.p_value.extend(p)
    
    ftype = 'medication'
    p = var.get_variables(dataio, ftype, 'MED USE')
    var.p_value.extend(p)
    
################################# DISPLAY ######################################
    print ('-----------------------')
    print ('value displaying...')
    ds = Display(var)
    print ('heatmap of the final mean value')
    figurename = 'results/heatmap_clustering_by_' + subtype_method.lower() +'_'+suffix+'.pdf'
    ds.heatmap(figurename, is_progress=False, is_rotate=False)
    print ('heatmap of the first order difference mean value')
    figurename = 'results/heatmap_clustering_by_' + subtype_method.lower() + '_progression_'+suffix+'.pdf'
    ds.heatmap(figurename, is_progress=True, is_rotate=False)
    
############################## SAVE RESULTS ####################################   
    print ('-----------------------')
    filename = result_path+'statistics_clustering_by_' + subtype_method.lower() + '_'+suffix+'.csv'
    dataio.save_result(var, filename)
    print ('done!')    
    
if __name__ == '__main__':
    main ()
 