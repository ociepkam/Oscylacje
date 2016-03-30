#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ociepkam'

import csv
import yaml
import random
from openpyxl import Workbook


class Trials:
    def __init__(self, number_of_trials):
        self.number_of_trials = number_of_trials
        self.list_of_trials = []

    def add_general_trial(self, trial):
        trial_json = trial.create_general_trial_json()
        if len(self.list_of_trials) < self.number_of_trials:
            self.list_of_trials.append(trial_json)
        else:
            raise Exception('To many trials')

    def add_concrete_trial(self, trial):
        trial_json = trial.create_concrete_trial_json()
        if len(self.list_of_trials) < self.number_of_trials:
            self.list_of_trials.append(trial_json)
        else:
            raise Exception('To many trials')

    def randomize(self):
        trainig_trials = []
        experiment_trials = []
        for trial in self.list_of_trials:
            if trial['EXP']:
                experiment_trials.append(trial)
            else:
                trainig_trials.append(trial)

        random.shuffle(trainig_trials)
        random.shuffle(experiment_trials)

        self.list_of_trials = trainig_trials + experiment_trials

    def save_to_yaml(self, filename):
        with open(filename + '.yaml', 'w') as yamlfile:
            yamlfile.write(yaml.dump(self.list_of_trials))

    def save_to_xlsx(self, filename):
        veryfication = "=IF(AND(OR(A{0} =\"letters\",A{0} =\"figures\",A{0} =\"NamesHeightRelations\", A{0} =\"NamesAgeRelations\"),OR(B{0} = 2,B{0} = 3,B{0} = 4),OR(D{0} = 0,D{0} = 1),OR(E{0} = 0,E{0} = 1),OR(I{0} = 0,I{0} = 1),OR(K{0} = 0,K{0} = 1),OR(L{0} = 0,L{0} = 1),OR(N{0} = 0,N{0} = 1),OR(O{0} = 0,O{0} = 1)),1, 0)"
        global_veryfication = "=SUM(Q2: Q500)"

        wb = Workbook()

        # grab the active worksheet
        ws = wb.active

        # Data can be assigned directly to cells
        ws.append(
            ['SAMPLE_TYPE', 'N', 'NR', 'MEMORY', 'INTEGR', 'SHOW_TIME', 'RESP_TIME', 'MAXTIME', 'FEEDB', 'FEEDB_TIME',
             'WAIT', 'EXP', 'FIXTIME', 'EEG', 'LIST_VIEW', '', global_veryfication])

        for idx, trial_info in enumerate(self.list_of_trials):
            ws.append([trial_info['SAMPLE_TYPE'], trial_info['N'], trial_info['NR'], trial_info['MEMORY'],
                       trial_info['INTEGR'], trial_info['SHOW_TIME'], trial_info['RESP_TIME'], trial_info['MAXTIME'],
                       trial_info['FEEDB'], trial_info['FEEDB_TIME'], trial_info['WAIT'], trial_info['EXP'],
                       trial_info['FIXTIME'], trial_info['EEG'], trial_info['LIST_VIEW'], '' ,veryfication.format(idx+2)])

        # Save the file
        wb.save(filename + ".xlsx")
