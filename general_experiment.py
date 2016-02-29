#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ociepkam'

from gooey import Gooey, GooeyParser
from trial import Trial, SampleTypes
from trials import Trials


@Gooey(language='english',  # Translations configurable via json
       default_size=(650, 600),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def generate_trials_gui():
    # General information
    parser = GooeyParser(description='Create_general_experiment')
    parser.add_argument('Number_of_training_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('Number_of_experiment_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('File_name', default='experiment', type=str, help='Name of file with not personalized data')

    # Information about training
    parser.add_argument('--Training_task', default=SampleTypes.letters,
                        choices=[SampleTypes.letters, SampleTypes.figures, SampleTypes.NamesAgeRelations,
                                 SampleTypes.NamesHeightRelations], help='Choose trial type')
    parser.add_argument('--Training_number', default=1, action='store', type=int, help='Number of relations')
    parser.add_argument('--Training_memory', default='True', choices=['True', 'False'], help='Choice')
    parser.add_argument('--Training_integration', default='True', choices=['True', 'False'], help='Choice')
    parser.add_argument('--Training_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_maxtime', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_feedback', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_wait', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_fixtime', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_eeg', default='True', choices=['True', 'False'], help='Choice')

    # Information about experiment
    parser.add_argument('--Experiment_task', default=SampleTypes.letters,
                        choices=[SampleTypes.letters, SampleTypes.figures, SampleTypes.NamesAgeRelations,
                                 SampleTypes.NamesHeightRelations], help='Choose trial type')
    parser.add_argument('--Experiment_number', default=1, action='store', type=int, help='Number of relations')
    parser.add_argument('--Experiment_memory', default='True', choices=['True', 'False'], help='Choice')
    parser.add_argument('--Experiment_integration', default='True', choices=['True', 'False'], help='Choice')
    parser.add_argument('--Experiment_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_maxtime', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_feedback', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_wait', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_fixtime', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_eeg', default='True', choices=['True', 'False'], help='Choice')

    args = parser.parse_args()

    number_of_trials = args.Number_of_training_trials + args.Number_of_experiment_trials

    trials = Trials(number_of_trials)

    for idx in range(0, args.Number_of_training_trials):
        trial = Trial(args.Training_task, args.Training_number, idx + 1, args.Training_memory,
                      args.Training_integration, args.Training_time, args.Training_maxtime, args.Training_feedback,
                      args.Training_wait, False, args.Training_fixtime, args.Training_eeg)
        trials.add_general_trial(trial)
    for idx in range(0, args.Number_of_experiment_trials):
        trial = Trial(args.Experiment_task, args.Experiment_number, idx + 1, args.Experiment_memory,
                      args.Experiment_integration, args.Experiment_time, args.Experiment_maxtime,
                      args.Experiment_feedback, args.Experiment_wait, True, args.Experiment_fixtime, args.Experiment_eeg)
        trials.add_general_trial(trial)

    trials.save_to_yaml(args.File_name)


def main():
    generate_trials_gui()


if __name__ == '__main__':
    main()