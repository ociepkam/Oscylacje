#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ociepkam'

from gooey import Gooey, GooeyParser
import yaml
from trial import Trial, SampleTypes
from trials import Trials


@Gooey(language='english',  # Translations configurable via json
       default_size=(450, 500),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def main():
    parser = GooeyParser(description='Create_concrete_experiment')
    parser.add_argument('Experiment_file_name', widget='FileChooser', help='Choose experiment file with general info')
    parser.add_argument('Participant_code', type=str, help='Name of file with personalized data')
    parser.add_argument('Random', default='True', choices=['True', 'False'], help="Present trials in random order")
    args = parser.parse_args()

    with open(args.Experiment_file_name, 'r') as experimentfile:
        experiment = yaml.load(experimentfile)

    trials = Trials(len(experiment))

    for idx in range(0, len(experiment)):
        trial_info = experiment[idx]
        trial = Trial(trial_info['SAMPLE_TYPE'], trial_info['N'], trial_info['NR'], trial_info['MEMORY'],
                      trial_info['INTEGR'], trial_info['TIME'], trial_info['MAXTIME'], trial_info['FEEDB'],
                      trial_info['WAIT'], trial_info['EXP'], trial_info['FIXTIME'])
        trial.create_sample()
        trials.add_concrete_trial(trial)

    if args.Random:
        trials.randomize()
    trials.save_to_yaml(args.Participant_code)

if __name__ == '__main__':
    main()
