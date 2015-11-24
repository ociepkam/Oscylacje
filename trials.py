#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ociepkam'

import csv
import yaml


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

    def save_to_yaml(self, filename):
        with open(filename + '.yml', 'w') as yamlfile:
            yamlfile.write(yaml.dump(self.list_of_trials))

    def save_to_csv(self, filename):
        with open(filename + '.csv', 'w') as csvfile:
            fieldnames = ['NR', 'MEMORY', 'INTEGR', 'TIME', 'MAXTIME', 'FEEDB',
                          'WAIT', 'EXP', 'RELATIONS_LIST', 'TASK', 'ANSWER']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for trial in self.list_of_trials:
                writer.writerow({
                    'NR': trial["NR"],
                    'MEMORY': trial["MEMORY"],
                    'INTEGR': trial['INTEGR'],
                    'TIME': trial['TIME'],
                    'MAXTIME': trial['MAXTIME'],
                    'FEEDB': trial['FEEDB'],
                    'WAIT': trial['WAIT'],
                    'EXP': trial['EXP'],
                    'RELATIONS_LIST': trial['RELATIONS_LIST'],
                    'TASK': trial['TASK'],
                    'ANSWER': trial['ANSWER']
                })
