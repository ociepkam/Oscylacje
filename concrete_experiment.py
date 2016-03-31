#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gooey import Gooey, GooeyParser
from openpyxl import load_workbook

from classes.trial import Trial
from classes.trials import Trials

__author__ = 'ociepkam'


def load_info(filename):
    experiment_file = load_workbook(filename)
    sheet = experiment_file.get_active_sheet()

    experiment = []
    for row_idx in range(len(sheet.columns[0]) - 1):
        trial = {}
        for column_idx, column in enumerate(sheet.columns):
            if column_idx == 15:
                break
            if isinstance(column[row_idx + 1].value, (str, unicode)):
                trial.update({str(column[0].value): str(column[row_idx + 1].value)})
            else:
                trial.update({str(column[0].value): int(column[row_idx + 1].value)})

        experiment.append(trial)

    return experiment


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

    experiment = load_info(args.Experiment_file_name)

    trials = Trials(len(experiment))

    for idx in range(0, len(experiment)):
        trial_info = experiment[idx]
        trial = Trial(trial_info['SAMPLE_TYPE'], trial_info['N'], trial_info['NR'], trial_info['MEMORY'],
                      trial_info['INTEGR'], trial_info['SHOW_TIME'], trial_info['RESP_TIME'], trial_info['MAXTIME'],
                      trial_info['FEEDB'], trial_info['FEEDB_TIME'], trial_info['WAIT'], trial_info['EXP'],
                      trial_info['FIXTIME'], trial_info['EEG'], trial_info['LIST_VIEW'])
        trial.create_sample()
        trials.add_concrete_trial(trial)

    if args.Random:
        trials.randomize()
    trials.save_to_yaml(args.Participant_code)


if __name__ == '__main__':
    main()
