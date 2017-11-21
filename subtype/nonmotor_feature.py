# -*- coding: utf-8 -*-


import math
import numpy
import csv, codecs
import operator 

from statistics import Statistics
from numeric import isint, isfloat
from time_converter import convert_time, convert_int



class NonMotorFeature(object):
    
    def __init__(self):
        self.feature_info = dict() # feature name: list(pat_id, timestamp, feature_val)
        # non-motor
        # the dictionaries store the last state feature values
        self.NONMOTOR = dict() # cluster: non-motor feature value
        # the dictionaries store the first state feature values 
        self.NONMOTOR_first = dict() # cluster: non-motor feature value
        # the dictionaries store the median state feature values 
        self.NONMOTOR_median = dict() # cluster: non-motor feature value
        
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
            if fname == 'BJLO':
                self.read_feature('Benton_Judgment_of_Line_Orientation.csv', date_key='INFODT')
            elif fname == 'ESS':
                self.read_feature('Epworth_Sleepiness_Scale.csv', date_key='INFODT')
            elif fname == 'GDS':
                self.read_feature('Geriatric_Depression_Scale__Short_.csv', date_key='INFODT')
            elif fname == 'HVLT':
                self.read_feature('Hopkins_Verbal_Learning_Test1.csv', featname, date_key='INFODT')
            elif fname == 'LNS':
                self.read_feature('Letter_-_Number_Sequencing__PD_.csv', date_key='INFODT')
            elif fname == 'MoCA':
                self.read_feature('Montreal_Cognitive_Assessment__MoCA_.csv', date_key='INFODT')
            elif fname == 'UPSIT':
                self.read_feature('Olfactory_UPSIT.csv',  date_key='COMPLT_DATE', pid_name='SUBJECT_ID')
            elif fname == 'QUIP':
                self.read_feature('QUIP_Current_Short.csv', date_key='INFODT')
            elif fname == 'RBD':
                self.read_feature('REM_Sleep_Disorder_Questionnaire.csv', date_key='INFODT')
            elif fname == 'SCOPA-AUT':
                self.read_feature('SCOPA-AUT1.csv',date_key='INFODT')
            elif fname == 'SF':
                self.read_feature('Semantic_Fluency.csv', date_key='INFODT')
            elif fname == 'STAI':
                self.read_feature('State-Trait_Anxiety_Inventory.csv', date_key='INFODT')
            elif fname == 'SDM':
                self.read_feature('Symbol_Digit_Modalities.csv', date_key='INFODT')
            elif fname == 'MCI':
                self.read_feature('Hopkins_Verbal_Learning_Test1.csv', featname, date_key='INFODT')
                self.read_feature('Benton_Judgment_of_Line_Orientation.csv', featname, date_key='INFODT')
                self.read_feature('Letter_-_Number_Sequencing__PD_.csv', featname, date_key='INFODT')
                self.read_feature('Semantic_Fluency.csv', featname, date_key='INFODT')
                self.read_feature('Symbol_Digit_Modalities.csv', featname, date_key='INFODT')
                self.read_feature('Cognitive_Categorization.csv', featname, date_key='INFODT')
                
        except ValueError:
            print('please enter correct file name!')
        
    def read_feature(self, filename, featname=None, time_convert=False, date_key=None, pid_name='PATNO'):
        fname = self.get_feature_name(filename, featname)
        f = codecs.open('../non-motor/' + filename, 'r', 'utf-8')
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
            if filename == 'Benton_Judgment_of_Line_Orientation.csv':
                if featname == 'Mild Cognitive Impairment':
                    fname = ['DVS_JLO_MSSAE']
                if featname == None:
                    fname = ["BJLOT1","BJLOT2","BJLOT3","BJLOT4","BJLOT5","BJLOT6","BJLOT7","BJLOT8","BJLOT9","BJLOT10","BJLOT11",
                    "BJLOT12","BJLOT13","BJLOT14","BJLOT15","BJLOT16","BJLOT17","BJLOT18","BJLOT19","BJLOT20","BJLOT21","BJLOT22",
                    "BJLOT23","BJLOT24","BJLOT25","BJLOT26","BJLOT27","BJLOT28","BJLOT29","BJLOT30"]

            if filename == 'Epworth_Sleepiness_Scale.csv':
                fname = ["ESS1","ESS2","ESS3","ESS4","ESS5","ESS6","ESS7","ESS8"]
            
            if filename == 'Geriatric_Depression_Scale__Short_.csv':
                fname = ["GDSSATIS","GDSDROPD","GDSEMPTY","GDSBORED","GDSGSPIR","GDSAFRAD","GDSHAPPY","GDSHLPLS","GDSHOME",
                "GDSMEMRY","GDSALIVE","GDSWRTLS","GDSENRGY","GDSHOPLS","GDSBETER"]

            if filename == 'Hopkins_Verbal_Learning_Test1.csv':
                if featname == 'Immediate Recall':
                    fname = ["HVLTRT1","HVLTRT2","HVLTRT3"]
                if featname == 'Discrimination Recognition':
                    fname = ["HVLTREC", "HVLTFPRL", "HVLTFPUN"]
                if featname == "Retention":
                    fname = ["HVLTRDLY", "HVLTRT2", "HVLTRT3"]
                if featname == 'Mild Cognitive Impairment':
                    fname = ["DVT_TOTAL_RECALL", "DVT_RECOG_DISC_INDEX"]
                if featname == None:
                    fname = ["HVLTRT1","HVLTRT2","HVLTRT3","HVLTRDLY","HVLTREC","HVLTFPRL","HVLTFPUN"]
    
            if filename == 'Letter_-_Number_Sequencing__PD_.csv':
                if featname == 'Mild Cognitive Impairment':
                    fname = ["DVS_LNS"]
                if featname == None:
                    fname = ["LNS1A","LNS1B","LNS1C","LNS2A","LNS2B","LNS2C","LNS3A","LNS3B","LNS3C","LNS4A","LNS4B",
                    "LNS4C","LNS5A","LNS5B","LNS5C","LNS6A","LNS6B","LNS6C","LNS7A","LNS7B","LNS7C"]

            if filename == 'Montreal_Cognitive_Assessment__MoCA_.csv':
                fname = ["MCAALTTM","MCACUBE","MCACLCKC","MCACLCKN","MCACLCKH","MCALION","MCARHINO","MCACAMEL",
                "MCAFDS","MCABDS","MCAVIGIL","MCASER7","MCASNTNC","MCAVFNUM","MCAVF","MCAABSTR","MCAREC1","MCAREC2",
                "MCAREC3","MCAREC4","MCAREC5", "MCADATE","MCAMONTH","MCAYR","MCADAY","MCAPLACE","MCACITY"]
                fname = ["MCATOT"]

            if filename == 'Olfactory_UPSIT.csv':
                fname = ["SCENT_10_RESPONSE","SCENT_09_RESPONSE","SCENT_08_RESPONSE","SCENT_07_RESPONSE",
                "SCENT_06_RESPONSE","SCENT_05_RESPONSE","SCENT_04_RESPONSE","SCENT_03_RESPONSE","SCENT_02_RESPONSE",
                "SCENT_01_RESPONSE","SCENT_20_RESPONSE","SCENT_19_RESPONSE","SCENT_18_RESPONSE","SCENT_17_RESPONSE",
                "SCENT_16_RESPONSE","SCENT_15_RESPONSE","SCENT_14_RESPONSE","SCENT_13_RESPONSE","SCENT_12_RESPONSE",
                "SCENT_11_RESPONSE","SCENT_30_RESPONSE","SCENT_29_RESPONSE","SCENT_28_RESPONSE","SCENT_27_RESPONSE",
                "SCENT_26_RESPONSE","SCENT_25_RESPONSE","SCENT_24_RESPONSE","SCENT_23_RESPONSE","SCENT_22_RESPONSE",
                "SCENT_21_RESPONSE","SCENT_40_RESPONSE","SCENT_39_RESPONSE","SCENT_38_RESPONSE","SCENT_37_RESPONSE",
                "SCENT_36_RESPONSE","SCENT_35_RESPONSE","SCENT_34_RESPONSE","SCENT_33_RESPONSE","SCENT_32_RESPONSE",
                "SCENT_31_RESPONSE","SCENT_10_CORRECT","SCENT_09_CORRECT","SCENT_08_CORRECT","SCENT_07_CORRECT",
                "SCENT_06_CORRECT","SCENT_05_CORRECT","SCENT_04_CORRECT","SCENT_03_CORRECT","SCENT_02_CORRECT",
                "SCENT_01_CORRECT","SCENT_20_CORRECT","SCENT_19_CORRECT","SCENT_18_CORRECT","SCENT_17_CORRECT",
                "SCENT_16_CORRECT","SCENT_15_CORRECT","SCENT_14_CORRECT","SCENT_13_CORRECT","SCENT_12_CORRECT",
                "SCENT_11_CORRECT","SCENT_30_CORRECT","SCENT_29_CORRECT","SCENT_28_CORRECT","SCENT_27_CORRECT",
                "SCENT_26_CORRECT","SCENT_25_CORRECT","SCENT_24_CORRECT","SCENT_23_CORRECT","SCENT_22_CORRECT",
                "SCENT_21_CORRECT","SCENT_40_CORRECT","SCENT_39_CORRECT","SCENT_38_CORRECT","SCENT_37_CORRECT",
                "SCENT_36_CORRECT","SCENT_35_CORRECT","SCENT_34_CORRECT","SCENT_33_CORRECT","SCENT_32_CORRECT",
                "SCENT_31_CORRECT","TOTAL_CORRECT","UPSIIT_PRCNTGE"]

            if filename == 'QUIP_Current_Short.csv':
                fname = ["TMGAMBLE","CNTRLGMB","TMSEX","CNTRLSEX","TMBUY","CNTRLBUY",
                "TMEAT","CNTRLEAT","TMTORACT","TMTMTACT","TMTRWD"]

            if filename == 'REM_Sleep_Disorder_Questionnaire.csv':
                fname = ["DRMVIVID","DRMAGRAC","DRMNOCTB","SLPLMBMV","SLPINJUR",
                "DRMVERBL","DRMFIGHT","DRMUMV","DRMOBJFL","MVAWAKEN","DRMREMEM","SLPDSTRB",
                "STROKE","HETRA","PARKISM","RLS","NARCLPSY","DEPRS","EPILEPSY","BRNINFM",
                "CNSOTH","CNSOTHCM"]

            if filename == 'SCOPA-AUT1.csv':
                fname = ["SCAU1","SCAU2","SCAU3","SCAU4","SCAU5","SCAU6","SCAU7", 
                "SCAU8","SCAU9","SCAU10","SCAU11","SCAU12","SCAU13","SCAU14","SCAU15","SCAU16",
                "SCAU17","SCAU18","SCAU19","SCAU20","SCAU21","SCAU22","SCAU23","SCAU23A",
                "SCAU23AT","SCAU24","SCAU25","SCAU26A","SCAU26AT","SCAU26B","SCAU26BT",
                "SCAU26C","SCAU26CT","SCAU26D","SCAU26DT"]
            
            if filename == 'Semantic_Fluency.csv':
                if featname == 'Mild Cognitive Impairment':
                    fname = ['DVT_SFTANIM']
                if featname == None:
                    fname = ["VLTANIM","VLTVEG","VLTFRUIT"]
        
            if filename == 'State-Trait_Anxiety_Inventory.csv':
                fname = ["STAIAD1","STAIAD2","STAIAD3","STAIAD4","STAIAD5","STAIAD6","STAIAD7",
                "STAIAD8","STAIAD9","STAIAD10","STAIAD11","STAIAD12","STAIAD13","STAIAD14",
                "STAIAD15","STAIAD16","STAIAD17","STAIAD18","STAIAD19","STAIAD20","STAIAD21",
                "STAIAD22","STAIAD23","STAIAD24","STAIAD25","STAIAD26","STAIAD27","STAIAD28",
                "STAIAD29","STAIAD30","STAIAD31","STAIAD32","STAIAD33","STAIAD34","STAIAD35",
                "STAIAD36","STAIAD37","STAIAD38","STAIAD39","STAIAD40"]
       
            if filename == 'Symbol_Digit_Modalities.csv':
                if featname == 'Mild Cognitive Impairment':
                    fname = ['DVT_SDM']
                if featname == None:
                    fname = ['SDMTOTAL']

            if filename == 'Cognitive_Categorization.csv':
                fname = ['COGDECLN', 'FNCDTCOG', 'COGSTATE']

        except ValueError:
            print('please enter correct file name or feature name!')
            
        return fname

        
    def get_feature_set(self, fname=None, featname=None):
        feature_set = set()
        try:
            if fname == 'BJLO':
                feature_set = set(["BJLOT1","BJLOT2","BJLOT3","BJLOT4","BJLOT5","BJLOT6","BJLOT7","BJLOT8","BJLOT9","BJLOT10","BJLOT11",
                "BJLOT12","BJLOT13","BJLOT14","BJLOT15","BJLOT16","BJLOT17","BJLOT18","BJLOT19","BJLOT20","BJLOT21","BJLOT22",
                "BJLOT23","BJLOT24","BJLOT25","BJLOT26","BJLOT27","BJLOT28","BJLOT29","BJLOT30"])

            if fname == 'ESS':
                feature_set = set(["ESS1","ESS2","ESS3","ESS4","ESS5","ESS6","ESS7","ESS8"])
                
            if fname == 'GDS':
                feature_set = set(["GDSSATIS","GDSDROPD","GDSEMPTY","GDSBORED","GDSGSPIR","GDSAFRAD","GDSHAPPY","GDSHLPLS","GDSHOME",
                                       "GDSMEMRY","GDSALIVE","GDSWRTLS","GDSENRGY","GDSHOPLS","GDSBETER"])
                
            if fname == 'HVLT':
                if featname == 'Immediate Recall':
                    feature_set = set(["HVLTRT1","HVLTRT2","HVLTRT3"])
                if featname == 'Discrimination Recognition':
                    feature_set = set(["HVLTREC", "HVLTFPRL", "HVLTFPUN"])
                if featname == "Retention":
                    feature_set = set(["HVLTRDLY", "HVLTRT2", "HVLTRT3"])
                if featname == None:
                    feature_set = set(["HVLTRT1","HVLTRT2","HVLTRT3","HVLTRDLY","HVLTREC","HVLTFPRL","HVLTFPUN"])
    
            if fname == 'LNS':
                feature_set = set(["LNS1A","LNS1B","LNS1C","LNS2A","LNS2B","LNS2C","LNS3A","LNS3B","LNS3C","LNS4A","LNS4B",
                                   "LNS4C","LNS5A","LNS5B","LNS5C","LNS6A","LNS6B","LNS6C","LNS7A","LNS7B","LNS7C"])
              
            if fname == 'MoCA':
#                feature_set = set(["MCAALTTM","MCACUBE","MCACLCKC","MCACLCKN","MCACLCKH","MCALION","MCARHINO","MCACAMEL",
#                                   "MCAFDS","MCABDS","MCAVIGIL","MCASER7","MCASNTNC","MCAVFNUM","MCAVF","MCAABSTR","MCAREC1","MCAREC2",
#                                   "MCAREC3","MCAREC4","MCAREC5", "MCADATE","MCAMONTH","MCAYR","MCADAY","MCAPLACE","MCACITY"])
                feature_set = set(['MCATOT'])
                
            if fname == 'UPSIT':
                feature_set = set(["SCENT_10_RESPONSE","SCENT_09_RESPONSE","SCENT_08_RESPONSE","SCENT_07_RESPONSE",
                                   "SCENT_06_RESPONSE","SCENT_05_RESPONSE","SCENT_04_RESPONSE","SCENT_03_RESPONSE","SCENT_02_RESPONSE",
                                   "SCENT_01_RESPONSE","SCENT_20_RESPONSE","SCENT_19_RESPONSE","SCENT_18_RESPONSE","SCENT_17_RESPONSE",
                                   "SCENT_16_RESPONSE","SCENT_15_RESPONSE","SCENT_14_RESPONSE","SCENT_13_RESPONSE","SCENT_12_RESPONSE",
                                   "SCENT_11_RESPONSE","SCENT_30_RESPONSE","SCENT_29_RESPONSE","SCENT_28_RESPONSE","SCENT_27_RESPONSE",
                                   "SCENT_26_RESPONSE","SCENT_25_RESPONSE","SCENT_24_RESPONSE","SCENT_23_RESPONSE","SCENT_22_RESPONSE",
                                   "SCENT_21_RESPONSE","SCENT_40_RESPONSE","SCENT_39_RESPONSE","SCENT_38_RESPONSE","SCENT_37_RESPONSE",
                                   "SCENT_36_RESPONSE","SCENT_35_RESPONSE","SCENT_34_RESPONSE","SCENT_33_RESPONSE","SCENT_32_RESPONSE",
                                   "SCENT_31_RESPONSE","SCENT_10_CORRECT","SCENT_09_CORRECT","SCENT_08_CORRECT","SCENT_07_CORRECT",
                                   "SCENT_06_CORRECT","SCENT_05_CORRECT","SCENT_04_CORRECT","SCENT_03_CORRECT","SCENT_02_CORRECT",
                                   "SCENT_01_CORRECT","SCENT_20_CORRECT","SCENT_19_CORRECT","SCENT_18_CORRECT","SCENT_17_CORRECT",
                                   "SCENT_16_CORRECT","SCENT_15_CORRECT","SCENT_14_CORRECT","SCENT_13_CORRECT","SCENT_12_CORRECT",
                                   "SCENT_11_CORRECT","SCENT_30_CORRECT","SCENT_29_CORRECT","SCENT_28_CORRECT","SCENT_27_CORRECT",
                                   "SCENT_26_CORRECT","SCENT_25_CORRECT","SCENT_24_CORRECT","SCENT_23_CORRECT","SCENT_22_CORRECT",
                                   "SCENT_21_CORRECT","SCENT_40_CORRECT","SCENT_39_CORRECT","SCENT_38_CORRECT","SCENT_37_CORRECT",
                                   "SCENT_36_CORRECT","SCENT_35_CORRECT","SCENT_34_CORRECT","SCENT_33_CORRECT","SCENT_32_CORRECT",
                                   "SCENT_31_CORRECT","TOTAL_CORRECT","UPSIIT_PRCNTGE"])
                    
            if fname == 'QUIP':
                feature_set = set(["TMGAMBLE","CNTRLGMB","TMSEX","CNTRLSEX","TMBUY","CNTRLBUY",
                         "TMEAT","CNTRLEAT","TMTORACT","TMTMTACT","TMTRWD"])
                             
            if fname == 'RBD':
                feature_set = set(["DRMVIVID","DRMAGRAC","DRMNOCTB","SLPLMBMV","SLPINJUR",
                                   "DRMVERBL","DRMFIGHT","DRMUMV","DRMOBJFL","MVAWAKEN","DRMREMEM","SLPDSTRB",
                                   "STROKE","HETRA","PARKISM","RLS","NARCLPSY","DEPRS","EPILEPSY","BRNINFM",
                                   "CNSOTH","CNSOTHCM"])
                    
            if fname == 'SCOPA-AUT':
                feature_set = set(["SCAU1","SCAU2","SCAU3","SCAU4","SCAU5","SCAU6","SCAU7", 
                                   "SCAU8","SCAU9","SCAU10","SCAU11","SCAU12","SCAU13","SCAU14","SCAU15","SCAU16",
                                   "SCAU17","SCAU18","SCAU19","SCAU20","SCAU21","SCAU22","SCAU23","SCAU23A",
                                   "SCAU23AT","SCAU24","SCAU25","SCAU26A","SCAU26AT","SCAU26B","SCAU26BT",
                                   "SCAU26C","SCAU26CT","SCAU26D","SCAU26DT"])
                    
            if fname == 'SF':
                feature_set = set(["VLTANIM","VLTVEG","VLTFRUIT"])
        
            if fname == 'STAI':
#                feature_set = set(["STAIAD1","STAIAD2","STAIAD3","STAIAD4","STAIAD5","STAIAD6","STAIAD7",
#                                   "STAIAD8","STAIAD9","STAIAD10","STAIAD11","STAIAD12","STAIAD13","STAIAD14",
#                                   "STAIAD15","STAIAD16","STAIAD17","STAIAD18","STAIAD19","STAIAD20"])
                feature_set = set(["STAIAD1","STAIAD2","STAIAD3","STAIAD4","STAIAD5","STAIAD6","STAIAD7",
                                   "STAIAD8","STAIAD9","STAIAD10","STAIAD11","STAIAD12","STAIAD13","STAIAD14",
                                   "STAIAD15","STAIAD16","STAIAD17","STAIAD18","STAIAD19","STAIAD20","STAIAD21",
                                   "STAIAD22","STAIAD23","STAIAD24","STAIAD25","STAIAD26","STAIAD27","STAIAD28",
                                   "STAIAD29","STAIAD30","STAIAD31","STAIAD32","STAIAD33","STAIAD34","STAIAD35",
                                   "STAIAD36","STAIAD37","STAIAD38","STAIAD39","STAIAD40"])
                    
            if fname == 'SDM':
                feature_set = set(['SDMTOTAL'])
                
            if fname == 'MCI':
                feature_set = set(['DVT_SFTANIM', 'DVS_JLO_MSSAE', 'DVT_SDM', 'DVS_LNS', 'DVT_TOTAL_RECALL', 'DVT_RECOG_DISC_INDEX', 'COGDECLN', 'FNCDTCOG'])
                    
            if fname == 'Cognitive Subtype':
                feature_set = set(['COGSTATE'])
                
            if fname == 'Mood Subtype':
                feature_set = set(["GDSSATIS","GDSDROPD","GDSEMPTY","GDSBORED","GDSGSPIR","GDSAFRAD","GDSHAPPY","GDSHLPLS","GDSHOME",
                                   "GDSMEMRY","GDSALIVE","GDSWRTLS","GDSENRGY","GDSHOPLS","GDSBETER",
                                   "STAIAD1","STAIAD2","STAIAD3","STAIAD4","STAIAD5","STAIAD6","STAIAD7",
                                   "STAIAD8","STAIAD9","STAIAD10","STAIAD11","STAIAD12","STAIAD13","STAIAD14",
                                   "STAIAD15","STAIAD16","STAIAD17","STAIAD18","STAIAD19","STAIAD20"])
                
        except ValueError:
            print ('please enter correct feature name!')
            
        return feature_set

        
    def load_subtype(self, patient_id, patient_cluster, method, timestamp = 'baseline'):
        feat_info = self.feature_info
        fname = method  
        if method == 'Cognitive Subtype':
            self.load_cognitive_subtype(fname, feat_info, patient_id, patient_cluster, timestamp)
        if method == 'Mood Subtype':
            self.load_mood_subtype(fname, feat_info, patient_id, patient_cluster, timestamp)
            
            
    def load_cognitive_subtype(self, fname, feat_info, patient_id, patient_cluster, timestamp = 'baseline'):
        pat_cog_state = dict() # pid: cognitive state
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
#            print (len(pat_record))        
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
                    if len(tf_list) % 2 == 1:
                        time_idx = math.floor(len(tf_list)/2)
                        pat_fval = tf_list[time_idx][1]
                    else:
                        time_idx1 = math.floor(len(tf_list)/2)
                        time_idx2 = time_idx1-1
                        pat_fval = int((tf_list[time_idx1][1] + tf_list[time_idx2][1])/2)
                 
                pat_cog_state[pat] = pat_fval
#            print(len(pat_cog_state))
#            print(pat_cog_state)
#        fname = 'MCI'
#        pat_fn_record = dict()
#        for fn, tpl_list in feat_info.items():
#            if fn not in self.get_feature_set(fname):
#                continue
#            pat_record = dict() # patient id : a list of (time stamp, feature val)
#            for tpl in tpl_list:
#                if isint(tpl[2])==True:
#                    fv = int(tpl[2])
#                elif isfloat(tpl[2])==True:
#                    fv = float(tpl[2])
#                else:
#                    continue
#                pat = tpl[0]
#                time = convert_int(tpl[1])
#             
#                if pat not in patient_id:
#                    continue
#
#                if pat not in pat_fn_record:
#                    pat_fn_record[pat] = list()
#                    pat_fn_record[pat].append((time, fn, fv))
#                else:
#                    pat_fn_record[pat].append((time, fn, fv))
#                continue   
#        pat_fval_first, pat_fval_median, pat_fval_last, _ = \
#        self.get_MCI_value(pat_fn_record)
#        pat_mci = dict() # pid: mci = 1 if it is a mci
#        if timestamp == 'baseline':
#            pat_mci = pat_fval_first
#        elif timestamp == 'follow-up':
#            pat_mci = pat_fval_last
#        elif timestamp == 'median':
#            pat_mci = pat_fval_median  

        # categorization according to cognitive subtypes
        for pat in patient_id:
            if pat in pat_cog_state:
                if pat_cog_state[pat] == 1:
                    patient_cluster[pat] = '1' # no cognitive impairment
                elif pat_cog_state[pat] == 2:
                    patient_cluster[pat] = '2' # Mild Cognitive Impairment 
                elif pat_cog_state[pat] == 3:
                    patient_cluster[pat] = '3' # Dementia      
#            else:
#                if pat in pat_mci:
#                    if pat_mci[str(pat)] == 1:
#                        patient_cluster[pat] = '2'
                        
    def load_mood_subtype(self, fname, feat_info, patient_id, patient_cluster, timestamp = 'baseline'):
        pat_mood_state = dict() # there are four mood state:
                                # depression, anxiety, depression-anxiety, none
                                # are corresponding to '1', '2', '3', '4'
        fname = ['STAI', 'GDS']
        pat_fval = dict()
        for variable in fname:
            # intialization for patient and the corresponding feature value
            pat_fval_first = dict() # patient id : first feature value
            pat_fval_median = dict() # patient id : median feature value
            pat_fval_last = dict() # patient id : last feature value
            for fn, tpl_list in feat_info.items():
                if fn not in self.get_feature_set(variable):
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
           
                # sort for each patient according to time stamp       
                for pat, tf_list in pat_new_record.items():
                    pat_fval_first, pat_fval_median, pat_fval_last = \
                    self.get_feature_value(pat, tf_list, pat_fval_first, pat_fval_median, pat_fval_last, variable, fn)
                
            pat_mood_state = dict() 
            if timestamp == 'baseline':
                for pat, fval in pat_fval_first.items():
                    if pat not in pat_fval:
                        pat_fval[pat] = list()
                    pat_fval[pat].append(fval)
                pat_num_first = len(pat_fval)
#                print (pat_num_first)
            elif timestamp == 'follow-up':
                for pat, fval in pat_fval_last.items():
                    if pat not in pat_fval:
                        pat_fval[pat] = list()
                    pat_fval[pat].append(fval)
                pat_num_last = len(pat_fval)
#                print (pat_num_last)
            elif timestamp == 'median':
                for pat, fval in pat_fval_median.items():
                    if pat not in pat_fval:
                        pat_fval[pat] = list()
                    pat_fval[pat].append(fval) 
                pat_num_median = len(pat_fval)
#                print (pat_num_median)
        
            
        for pat, fval_list in pat_fval.items():
            if fval_list[0] > 55: # ANXIETY
                if fval_list[1] < 5: # only anxiety
                    pat_mood_state[pat] = 1
                else: # depression-anxiety
                    pat_mood_state[pat] = 3
            else:
                if fval_list[1] < 5: #  all good
                    pass
#                    pat_mood_state[pat] = 4
                else: # only depression 
                    pat_mood_state[pat] = 2
         
#        print (pat_mood_state)
        # categorization according to mood subtypes
        count = dict()
        count['1'] = 0
        count['2'] = 0
        count['3'] = 0
#        count['4'] = 0
        for pat in patient_id:
            if pat in pat_mood_state:
                if pat_mood_state[pat] == 1:
                    patient_cluster[pat] = '1' # anxiety
                    count['1'] += 1 
                elif pat_mood_state[pat] == 2: 
                    patient_cluster[pat] = '2' # depression  
                    count['2'] += 1 
                elif pat_mood_state[pat] == 3:
                    patient_cluster[pat] = '3' # depression-anxiety
                    count['3'] += 1 
#                elif pat_mood_state[pat] == 4:
#                    patient_cluster[pat] = '4' # none
#                    count['4'] += 1      
#        print (count)
        
    def get_MCI_value(self, pat_fn_record):
        #DVT_SFTANIM, DVS_JLO_MSSAE, DVT_SDM, DVS_LNS
        #DVT_TOTAL_RECALL, DVT_RECOG_DISC_INDEX, COGDECLN, FNCDTCOG
        pf_first = dict()
        pf_median = dict() 
        pf_last = dict() 
        pf_diff = dict()
        mci_fn = ['DVT_SFTANIM', 'DVS_JLO_MSSAE', 'DVT_SDM', 'DVS_LNS', 'DVT_TOTAL_RECALL', \
                  'DVT_RECOG_DISC_INDEX', 'COGDECLN', 'FNCDTCOG']
        fn_tbl = dict(zip(mci_fn, range(len(mci_fn)))) # fname:idx           
        for pat, tnv_record in pat_fn_record.items():
            mci_flag = [0, 0, 0] # for three timestamps
            feat = dict() # fn:fval list sorting by time
            time_feat = dict()
            for tnv in tnv_record:
                time = tnv[0]
                fn = tnv[1]
                fval = tnv[2]
                if time not in time_feat:
                    time_feat[time] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                time_feat[time][fn_tbl[fn]] = fval
            
            time_feat = sorted(time_feat.items(), key=operator.itemgetter(0))
            time_list = [tf[0] for tf in time_feat]
            feat_list = [tf[1] for tf in time_feat]
            mid_idx = math.floor(len(time_list)/2)-1
            for fn in mci_fn: 
                feat[fn] = [f[fn_tbl[fn]] for f in feat_list]
           
            # use mci_flag to label whether the patient is suffering MCI 
            # if feature satisfied all the conditions 
            for i in range(3): # for the three timestamps
                if i == 0:
                    j = 0
                elif i == 1:
                    j = mid_idx
                elif i == 2:
                    j = -1
                if feat['COGDECLN'][j] == 1:
                    count = 0
                    if feat['DVT_TOTAL_RECALL'][j] <= 35:
                        count += 1
                    if feat['DVT_RECOG_DISC_INDEX'][j] <= 35:
                        count += 1
                    if feat['DVS_JLO_MSSAE'][j] <= 6:
                        count += 1
                    if feat['DVS_LNS'][j] <= 6:
                        count += 1
                    if feat['DVT_SFTANIM'][j] <= 35:
                        count += 1
                    if feat['DVT_SDM'][j] <= 35:
                        count += 1
                    if count >= 2:
                        if feat['FNCDTCOG'][j] == 0:
                            mci_flag[i] = 1
                        else:
                            mci_flag[i] = 0
                    else:
                        mci_flag[i] = 0
                else:
                    mci_flag[i] = 0  
            pf_first[pat] = mci_flag[0]
            pf_median[pat] = mci_flag[1]
            pf_last[pat] = mci_flag[2]
            pf_diff[pat] = pf_last[pat] - pf_first[pat]
        return (pf_first, pf_median, pf_last, pf_diff)
        
    def get_HVLT_value(self, pat_fn_record, featname):
        pf_first = dict()
        pf_median = dict() 
        pf_last = dict() 
        pf_diff = dict()
        if featname == 'Discrimination Recognition':
            for pat, tnv_record in pat_fn_record.items():
                time_feat = dict()
                for tnv in tnv_record:
                    time = tnv[0]
                    fn = tnv[1]
                    fval = tnv[2]
                    if time not in time_feat:
                        time_feat[time] = [0, 0, 0]

                    if fn == 'HVLTREC':
                        time_feat[time][0] = fval
                    elif fn == 'HVLTFPRL':
                        time_feat[time][1] = fval
                    elif fn == 'HVLTFPUN':
                        time_feat[time][2] = fval
                time_feat = sorted(time_feat.items(), key=operator.itemgetter(0))
                time_list = [tf[0] for tf in time_feat]
                feat_list = [tf[1] for tf in time_feat]
                feat_rec = [f[0] for f in feat_list]
                feat_prl = [f[1] for f in feat_list]
                feat_pun = [f[2] for f in feat_list]
                pf_first[pat] = feat_rec[0] - (feat_prl[0] + feat_pun[0])
                pf_last[pat] = feat_rec[-1] - (feat_prl[-1] + feat_pun[-1])
                if len(feat_rec) % 2 == 0:
                    mid_idx1 = math.floor(len(feat_rec)/2)
                    mid_idx2 = mid_idx1-1
                    feat_rec_median = (feat_rec[mid_idx1] + feat_rec[mid_idx2])/2
                    feat_prl_median = (feat_prl[mid_idx1] + feat_prl[mid_idx2])/2
                    feat_pun_median = (feat_pun[mid_idx1] + feat_pun[mid_idx2])/2
                else:
                    mid_idx = math.floor(len(feat_rec)/2)-1
                    feat_rec_median = feat_rec[mid_idx]
                    feat_prl_median = feat_prl[mid_idx]
                    feat_pun_median = feat_pun[mid_idx]
                pf_median[pat] = feat_rec_median - (feat_prl_median + feat_pun_median)
                pf_diff[pat] = pf_last[pat] - pf_first[pat]
           
        elif featname == 'Retention':
             for pat, tnv_record in pat_fn_record.items():
                time_feat = dict()
                for tnv in tnv_record:
                    time = tnv[0]
                    fn = tnv[1]
                    fval = tnv[2]
                    if time not in time_feat:
                        time_feat[time] = [0, 0, 0]

                    if fn == 'HVLTRDLY':
                        time_feat[time][0] = fval
                    elif fn == 'HVLTRT2':
                        time_feat[time][1] = fval
                    elif fn == 'HVLTRT3':
                        time_feat[time][2] = fval
                time_feat = sorted(time_feat.items(), key=operator.itemgetter(0))
                time_list = [tf[0] for tf in time_feat]
                feat_list = [tf[1] for tf in time_feat]
                feat_dly = [f[0] for f in feat_list]
                feat_rt2 = [f[1] for f in feat_list]
                feat_rt3 = [f[2] for f in feat_list]
                pf_first[pat] = feat_dly[0]/max(feat_rt2[0], feat_rt3[0])
                pf_last[pat] = feat_dly[-1]/max(feat_rt2[-1], feat_rt3[-1])
                if len(feat_dly) % 2 == 0:
                    mid_idx1 = math.floor(len(feat_dly)/2)
                    mid_idx2 = mid_idx1-1
                    feat_dly_median = (feat_dly[mid_idx1] + feat_dly[mid_idx2])/2
                    feat_rt2_median = (feat_rt2[mid_idx1] + feat_rt2[mid_idx2])/2
                    feat_rt3_median = (feat_rt3[mid_idx1] + feat_rt3[mid_idx2])/2
                else:
                    mid_idx = math.floor(len(feat_dly)/2)-1
                    feat_dly_median = feat_dly[mid_idx] 
                    feat_rt2_median = feat_rt2[mid_idx]
                    feat_rt3_median = feat_rt3[mid_idx]
                pf_median[pat] = feat_dly_median/max(feat_rt2_median, feat_rt3_median)
                pf_diff[pat] = pf_last[pat] - pf_first[pat]
             
        return (pf_first, pf_median, pf_last, pf_diff)
        
    def get_feature_value(self, pat, tf_list, pf_first, pf_median, pf_last, fname=None, fn=None):

        if fname == 'SCOPA-AUT':
            add_3 = set(["SCAU1","SCAU2","SCAU3","SCAU4","SCAU5","SCAU6","SCAU7", 
                "SCAU8","SCAU9","SCAU10","SCAU11","SCAU12","SCAU13","SCAU14","SCAU15","SCAU16",
                "SCAU17","SCAU18","SCAU19","SCAU20","SCAU21"])
            add_0 = set(["SCAU22","SCAU23","SCAU23A", "SCAU23AT","SCAU24","SCAU25"])
        elif fname == 'STAI':
#             reverse = set(["STAIAD1","STAIAD2","STAIAD5","STAIAD8","STAIAD10","STAIAD11","STAIAD15",
#            "STAIAD16","STAIAD19","STAIAD20"])
            reverse = set(["STAIAD1","STAIAD2","STAIAD5","STAIAD8","STAIAD10","STAIAD11","STAIAD15",
            "STAIAD16","STAIAD19","STAIAD20","STAIAD21","STAIAD23","STAIAD26","STAIAD27","STAIAD30",
            "STAIAD33","STAIAD34","STAIAD36","STAIAD39"])
            
        # first
        fv_first = tf_list[0][1]      
        if fname == 'SCOPA-AUT' and fv_first == 9:
            if fn in add_0:
                fv_first = 0
            elif fn in add_3:
                fv_first = 3
        elif fname == 'STAI':
            if fn in reverse:
                fv_first = 5-fv_first
                     
        if pat not in pf_first:
            pf_first[pat] = fv_first
        else:
            pf_first[pat] += fv_first

        # median
#        if len(tf_list) % 2 == 1:
        mid_idx = math.floor(len(tf_list)/2)
        fv_median = tf_list[mid_idx][1]         
#        else:
#            mid_idx1 = math.floor(len(tf_list)/2)
#            mid_idx2 = mid_idx1-1
#            fv_median = (tf_list[mid_idx1][1] + tf_list[mid_idx2][1])/2
                     
        if fname == 'SCOPA-AUT' and fv_median == 9:
            if fn in add_0:
                fv_median = 0
            elif fn in add_3:
                fv_median = 3
        elif fname == 'STAI':
            if fn in reverse:
                fv_median = 5-fv_median
                     
        if pat not in pf_median:
            pf_median[pat] = fv_median
        else:
            pf_median[pat] += fv_median

        # last
        fv_last = tf_list[-1][1]
        if fname == 'SCOPA-AUT' and fv_last == 9:
            if fn in add_0:
                fv_last = 0
            elif fn in add_3:
                fv_last = 3     
        elif fname == 'STAI':
            if fn in reverse:
                fv_last = 5-fv_last  
                     
        if pat not in pf_last:
            pf_last[pat] = fv_last
        else:
            pf_last[pat] += fv_last
      
        return (pf_first, pf_median, pf_last)
        

    def get_correct_value(self, pat, tf_list, pf_first, pf_median, pf_last, fn, add_for_any):
        
        if fn not in add_for_any: 
            return (pf_first, pf_median, pf_last)
            
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
         
        if fname == 'SCOPA-AUT':
            add_3 = set(["SCAU1","SCAU2","SCAU3","SCAU4","SCAU5","SCAU6","SCAU7", 
                "SCAU8","SCAU9","SCAU10","SCAU11","SCAU12","SCAU13","SCAU14","SCAU15","SCAU16",
                "SCAU17","SCAU18","SCAU19","SCAU20","SCAU21"])
            add_0 = set(["SCAU22","SCAU23","SCAU23A", "SCAU23AT","SCAU24","SCAU25"])
        elif fname == 'STAI':
#            reverse = set(["STAIAD1","STAIAD2","STAIAD5","STAIAD8","STAIAD10","STAIAD11","STAIAD15",
#            "STAIAD16","STAIAD19","STAIAD20"])
            reverse = set(["STAIAD1","STAIAD2","STAIAD5","STAIAD8","STAIAD10","STAIAD11","STAIAD15",
            "STAIAD16","STAIAD19","STAIAD20","STAIAD21","STAIAD23","STAIAD26","STAIAD27","STAIAD30",
            "STAIAD33","STAIAD34","STAIAD36","STAIAD39"])
            
        fv_first = tf_list[0][1] 
        fv_last = tf_list[-1][1]     
        if fname == 'SCOPA-AUT' and fv_first == 9:
            if fn in add_0:
                fv_first = 0
                fv_last = 0
            elif fn in add_3:
                fv_first = 3
                fv_last = 3
        elif fname == 'STAI':
            if fn in reverse:
                fv_first = 5-fv_first
                fv_last = 5-fv_last
  
        fv_diff = fv_last - fv_first
        if pat not in pf_diff:
            pf_diff[pat] = fv_diff
        else:
            pf_diff[pat] += fv_diff

        return pf_diff
        
    def get_nonmotor(self, dataio, K, fname=None, featname=None, pat_edu=None):
        pat_cluster = dataio.patient_cluster
        feat_info = dataio.feature.nonmotor.feature_info
       
        # initialization for each cluster
        for i in range(1, K+1):
           self.NONMOTOR[str(i)] = list()
           self.NONMOTOR_first[str(i)] = list()
           self.NONMOTOR_median[str(i)] = list()
       
        # intialization for patient and the corresponding feature value
        pat_fval_first = dict() # patient id : first feature value
        pat_fval_median = dict() # patient id : median feature value
        pat_fval_last = dict() # patient id : last feature value
        pat_fval_diff = dict() # patient id : first-order difference 
                               # between last and first feature value 
        if fname == 'HVLT' or fname == 'MCI':
            pat_fn_record = dict()
            
        if fname == 'RBD':
            add_for_any = set(["STROKE","HETRA","PARKISM","RLS","NARCLPSY","DEPRS","EPILEPSY","BRNINFM",
                "CNSOTH","CNSOTHCM"])
            pat_correct_first = dict()
            pat_correct_median = dict()
            pat_correct_last = dict()
        elif fname == 'QUIP':
            add_for_any = set(["TMGAMBLE","CNTRLGMB","TMSEX","CNTRLSEX","TMBUY","CNTRLBUY","TMEAT","CNTRLEAT"])
            pat_correct_first = dict()
            pat_correct_median = dict()
            pat_correct_last = dict()
              
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
                
                if fname == 'HVLT':
                    if featname == 'Discrimination Recognition' or featname == 'Retention':
                        if pat not in pat_fn_record:
                            pat_fn_record[pat] = list()
                            pat_fn_record[pat].append((time, fn, fv))
                        else:
                            pat_fn_record[pat].append((time, fn, fv))
                        continue
                    
                if fname == 'MCI':
                    if pat not in pat_fn_record:
                        pat_fn_record[pat] = list()
                        pat_fn_record[pat].append((time, fn, fv))
                    else:
                        pat_fn_record[pat].append((time, fn, fv))
                    continue
                            
                if pat not in pat_record:
                    pat_record[pat] = list()
                    pat_record[pat].append((time, fv))
                else:
                    pat_record[pat].append((time, fv))
            
            if fname == 'HVLT':
                if featname == 'Discrimination Recognition' or featname == 'Retention':
                    continue
            
            if fname == 'MCI':
                continue
            # sort for each patient according to time stamp       
            pat_new_record = dict()
            for pat, tf_list in pat_record.items():
                pat_new_record[pat] = sorted(tf_list, key=operator.itemgetter(0))
           
            # store last, (first, median) values 
            for pat, tf_list in pat_new_record.items():
                pat_fval_first, pat_fval_median, pat_fval_last = \
                self.get_feature_value(pat, tf_list, pat_fval_first, pat_fval_median, pat_fval_last, fname, fn)
                pat_fval_diff = self.get_feature_diff(pat, tf_list, pat_fval_diff)
                if fname == 'RBD' or fname == 'QUIP':
                    pat_correct_first, pat_correct_median, pat_correct_last = \
                    self.get_correct_value(pat, tf_list, pat_correct_first, pat_correct_median, pat_correct_last, fn, add_for_any)
                    
                    
        if fname == 'HVLT':
            if featname == 'Discrimination Recognition' or featname == 'Retention':
                 pat_fval_first, pat_fval_median, pat_fval_last, pat_fval_diff = \
                 self.get_HVLT_value(pat_fn_record, featname)
       
        if fname == 'MCI':
            pat_fval_first, pat_fval_median, pat_fval_last, pat_fval_diff = \
            self.get_MCI_value(pat_fn_record)
            
        if fname == 'RBD' or fname == 'QUIP':
            
            for pat, fval in pat_fval_first.items():
                if pat_correct_first[pat] >= 1:
                    pat_fval_first[pat] -= pat_correct_first[pat]  
            for pat, fval in pat_fval_median.items():
                if pat_correct_median[pat] >= 1:
                    pat_fval_median[pat] -= pat_correct_median[pat]
            for pat, fval in pat_fval_last.items():
                if pat_correct_last[pat] >= 1:
                    pat_fval_last[pat] -= pat_correct_last[pat]
            for pat, fval in pat_fval_diff.items():
                if pat_correct_last[pat] >= 1 or pat_correct_first[pat] >=1:
                    pat_fval_diff[pat] -= (pat_correct_last[pat]-pat_correct_first[pat])
           
        if fname == 'MoCA':

            for pat, fval in pat_fval_first.items():
                if pat_edu[pat] <= 12 and fval < 30:
                    pat_fval_first[pat] += 1
            for pat, fval in pat_fval_median.items():
                if pat_edu[pat] <= 12 and fval < 30:
                    pat_fval_median[pat] += 1
            for pat, fval in pat_fval_last.items():
                if pat_edu[pat] <= 12 and fval < 30:
                    pat_fval_last[pat] += 1

        pat_num_first = dict()
        pat_num_median = dict()
        pat_num_last = dict()
        for pat, cls in pat_cluster.items():
            if pat in pat_fval_last:
                self.NONMOTOR[str(cls)].append(pat_fval_last[pat])
                if cls not in pat_num_last:
                    pat_num_last[cls] = 0
                pat_num_last[cls] += 1
            if pat in pat_fval_first:
                self.NONMOTOR_first[str(cls)].append(pat_fval_first[pat])
                if cls not in pat_num_first:
                    pat_num_first[cls] = 0
                pat_num_first[cls] += 1
            if pat in pat_fval_median:
                self.NONMOTOR_median[str(cls)].append(pat_fval_median[pat])
                if cls not in pat_num_median:
                    pat_num_median[cls] = 0
                pat_num_median[cls] += 1
        print (pat_num_first)
        print (pat_num_median)
        print (pat_num_last)
        
        # compute statistics
        # mean , std
        stats = Statistics(K)
        mean_NONMOTOR, std_NONMOTOR = stats.get_mean_std(self.NONMOTOR, is_total=False)
        mean_total_NONMOTOR, std_total_NONMOTOR = stats.get_mean_std(self.NONMOTOR, is_total=True)      
        mean_NONMOTOR_first, std_NONMOTOR_first = stats.get_mean_std(self.NONMOTOR_first, is_total=False)
        mean_total_NONMOTOR_first, std_total_NONMOTOR_first = stats.get_mean_std(self.NONMOTOR_first, is_total=True)   
        mean_NONMOTOR_median, std_NONMOTOR_median = stats.get_mean_std(self.NONMOTOR_median, is_total=False)
        mean_total_NONMOTOR_median, std_total_NONMOTOR_median = stats.get_mean_std(self.NONMOTOR_median, is_total=True)  
        if featname != None:
            fname_ = fname + '-' + featname
        else:
            fname_ = fname
        self.mean[fname_] = list()
        self.mean_first[fname_] = list()
        self.mean_median[fname_] = list()
        for i in range(1, K+1):
           self.mean[fname_].append((mean_NONMOTOR[str(i)], std_NONMOTOR[str(i)]))
           self.mean_first[fname_].append((mean_NONMOTOR_first[str(i)], std_NONMOTOR_first[str(i)]))
           self.mean_median[fname_].append((mean_NONMOTOR_median[str(i)], std_NONMOTOR_median[str(i)]))
        # display  
        for i in range(1, K+1):
            print ('### CLUSTER %d ####' %i)
            print ("The average %s value in the %d-th clusters at follow-up is: %f (%f)" %(fname, i, mean_NONMOTOR[str(i)], std_NONMOTOR[str(i)]))
            print ("The average value in the %d-th clusters at baseline is: %f (%f)" %(i, mean_NONMOTOR_first[str(i)], std_NONMOTOR_first[str(i)]))
            print ("The average value in the %d-th clusters at median is: %f (%f)" %(i, mean_NONMOTOR_median[str(i)], std_NONMOTOR_median[str(i)]))
        print ("The total average %s at follow-up is: %f (%f)" %(fname, mean_total_NONMOTOR, std_total_NONMOTOR))
        print ("The total average %s at baseline is: %f (%f)" %(fname, mean_total_NONMOTOR_first, std_total_NONMOTOR_first))
        print ("The total average %s at median is: %f (%f)" %(fname, mean_total_NONMOTOR_median, std_total_NONMOTOR_median))
        print ("##########")
              
        # hypothesis testing
        print ("hypothesis testing...")
        if featname != None:
            fname = fname + '-' + featname
        else:
            fname_ = fname
        # chi-square
#        stats.get_distribution(pat_fval_first, is_num=True)
        p_first = stats.get_chisquare(pat_fval_first, pat_cluster, fname, 'FIRST')
#        stats.get_distribution(pat_fval_median, is_num=True)
        p_median = stats.get_chisquare(pat_fval_median, pat_cluster, fname, 'MEDIAN')
#        stats.get_distribution(pat_fval_last, is_num=True)
        p_last = stats.get_chisquare(pat_fval_last, pat_cluster, fname, 'LAST')
#        stats.get_distribution(pat_fval_diff, is_num=True)
        p_diff = stats.get_chisquare(pat_fval_diff, pat_cluster, fname, 'DIFFERENCE')
        
        # post hoc test    
        if p_first <= 0.05:
            stats.get_tukeyhsd(pat_fval_first, pat_cluster, fname, 'FIRST')
        if p_median <= 0.05:
            stats.get_tukeyhsd(pat_fval_median, pat_cluster, fname, 'MEDIAN')
        if p_last <= 0.05:
            stats.get_tukeyhsd(pat_fval_last, pat_cluster, fname, 'LAST')
        if p_diff <= 0.05:
            stats.get_tukeyhsd(pat_fval_diff, pat_cluster, fname, 'DIFFERENCE')
            
       # store into self.p_value
        self.p_value.append([fname, p_first, p_median, p_last, p_diff])
        self.mean_total[fname] = (mean_total_NONMOTOR, std_total_NONMOTOR)
        print ('-----------------------')