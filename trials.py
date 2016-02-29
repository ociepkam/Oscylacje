#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ociepkam'

import csv
import yaml
import random


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
        with open(filename + '.yml', 'w') as yamlfile:
            yamlfile.write(yaml.dump(self.list_of_trials))