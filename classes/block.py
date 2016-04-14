#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import random

__author__ = 'ociepkam'


class Block:
    def __init__(self, number_of_trials):
        self.number_of_trials = number_of_trials
        self.list_of_trials = []

    def add_general_trial(self, trial):
        trial_json = trial.prepare_general()
        if len(self.list_of_trials) < self.number_of_trials:
            self.list_of_trials.append(trial_json)
        else:
            raise Exception('To many trials')

    def add_concrete_trial(self, trial):
        trial_json = trial.prepare_concrete()
        if len(self.list_of_trials) < self.number_of_trials:
            self.list_of_trials.append(trial_json)
        else:
            raise Exception('To many trials')

    def randomize(self):
        trainig_trials = []
        experiment_trials = []
        instructions = []
        for trial in self.list_of_trials:
            if trial.type != 'instruction':
                if trial.sample_type == 'trial':
                    experiment_trials.append(trial)
                else:
                    trainig_trials.append(trial)
            else:
                instructions.append(trial)

        random.shuffle(trainig_trials)
        random.shuffle(experiment_trials)

        self.list_of_trials = instructions + trainig_trials + experiment_trials

    def prepare_concrete(self):
        elements_list = []
        for element in self.list_of_trials:
            elements_list.append(element.prepare_concrete())

        block_info = {
            "experiment_elements": elements_list
        }
        return block_info

    def save_to_yaml(self, filename):
        with open(filename + '.yaml', 'w') as yamlfile:
            yamlfile.write(yaml.dump(self.list_of_trials))

