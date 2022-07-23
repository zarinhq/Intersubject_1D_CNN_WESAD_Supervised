import pickle
import numpy as np
import os
import datetime
import tensorflow as tf
from pathlib import Path
class DataManager:
    # Path to the WESAD dataset
    ROOT_PATH = '/content/gdrive/MyDrive/WESAD/'
    #ROOT_PATH = r'C:\WESAD'
    
    # pickle file extension for importing
    FILE_EXT = '.pkl'

    # IDs of the subjects
    SUBJECTS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17]

    # Label values defined in the WESAD readme
    BASELINE = 1
    STRESS = 2
    AMUSEMENT = 3

    RAW_SENSOR_VALUES = ['ECG']

    # Dictionaries to store the two sets of data
    BASELINE_DATA = []
    STRESS_DATA = []
    AMUSEMENT_DATA = []


    def __init__(self, ignore_empatica=True, ignore_additional_signals=True):
        # denotes that we will be excluding the empatica data 
        # after loading those measurements
        self.ignore_empatica = ignore_empatica

    def get_subject_path(self, subject):
        """ 
        Parameters:
        subject (int): id of the subject
        
        Returns:
        str: path to the pickle file for the given subject number
             iff the path exists 
        """
        
        # subjects path looks like data_set + '<subject>/<subject>.pkl'
        path = os.path.join(DataManager.ROOT_PATH, 'S'+ str(subject), 'S' + str(subject) + DataManager.FILE_EXT)
        print('Loading data for S'+ str(subject))
        #print('Path=' + path)
        if os.path.isfile(path):
            return path
        else:
            print(path)
            raise Exception('Invalid subject: ' + str(subject))

    def load(self, subject):
        """ 
        Loads and saves the data from the pkl file for the provided subject
        
        Parameters:
        subject (int): id of the subject
        
        Returns: Baseline and stress data
        dict: {{'EDA': [###, ..], ..}, 
               {'EDA': [###, ..], ..} }
        """
       
        # change the encoding because the data appears to have been
        # pickled with py2 and we are in py3
        with open(self.get_subject_path(subject), 'rb') as file:
            data = pickle.load(file, encoding='latin1')
            return self.extract_and_reform(data, subject)

    def extract_and_reform(self, data, subject):
        """ 
        Extracts and shapes the data from the pkl file
        for the provided subject.
        
        Parameters:
        data (dict): as loaded from the pickle file
        
        Returns: Baseline and stress data
        dict: {{'EDA': [###, ..], ..}, 
               {'EDA': [###, ..], ..} }
        """
                
        if self.ignore_empatica:
            del data['signal']['wrist']
        
        baseline_indices = np.nonzero(data['label']==DataManager.BASELINE)[0]   
        stress_indices = np.nonzero(data['label']==DataManager.STRESS)[0]
        amusement_indices = np.nonzero(data['label']==DataManager.AMUSEMENT)[0]   

#         base = dict()
#         stress = dict()
#         amusement = dict()
#         base_label = dict()
        
        
        for value in DataManager.RAW_SENSOR_VALUES: 
            base = data['signal']['chest'][value][baseline_indices]
            stress= data['signal']['chest'][value][stress_indices]
            amusement = data['signal']['chest'][value][amusement_indices]
            
            base_label = data['label'][baseline_indices]
            stress_label = data['label'][stress_indices]
            amusement_label = data['label'][amusement_indices]


            
        
        DataManager.BASELINE_DATA.append(base)
        DataManager.STRESS_DATA.append(stress)
        DataManager.AMUSEMENT_DATA.append(amusement)
        
        
        return base, stress, amusement, base_label, stress_label, amusement_label