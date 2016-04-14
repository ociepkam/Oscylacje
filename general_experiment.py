#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gooey import Gooey, GooeyParser
from classes.trial import SampleTypes
from openpyxl import Workbook

__author__ = 'ociepkam'


def save_to_xlsx(tab, filename):
    verification = "=IF(AND(OR(B{0} =\"letters\",B{0} =\"figures\",B{0} =\"NamesHeightRelations\", B{0} =\"NamesAgeRelations\"),OR(C{0} = 2,C{0} = 3,C{0} = 4),OR(E{0} = 0,E{0} = 1),OR(F{0} = 0,F{0} = 1),OR(J{0} = 0,J{0} = 1),OR(L{0} = 0,L{0} = 1),OR(M{0} = 0,M{0} = 1),OR(O{0} = 0,O{0} = 1),OR(P{0} = 0,P{0} = 1)),1, 0)"
    global_verification = "=SUM(S2: S500)"

    wb = Workbook()

    # grab the active worksheet
    ws = wb.active

    # Data can be assigned directly to cells
    ws.append(
        ['BLOCK_NUMBER', 'SAMPLE_TYPE', 'N', 'NR', 'MEMORY', 'INTEGR', 'SHOW_TIME', 'RESP_TIME', 'MAXTIME', 'FEEDB',
         'FEEDB_TIME', 'WAIT', 'EXP', 'FIXTIME', 'EEG', 'LIST_VIEW', 'INSTRUCTION', '', 1])

    for idx, trial in enumerate(tab):
        if trial[1] == "instruction":
            trial_with_verification = trial[0:2] + ['']*4 + [trial[2]] + ['']*9 + [trial[-1]] + ['', verification.format(idx + 2)]
        else:
            trial_with_verification = trial + ['', '', verification.format(idx + 2)]
        ws.append(trial_with_verification)

    # Save the file
    wb.save(filename + ".xlsx")


@Gooey(language='english',  # Translations configurable via json
       default_size=(650, 600),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def generate_trials_gui():
    # General information
    parser = GooeyParser(description='Create_general_experiment')
    parser.add_argument('Number_of_blocks', default=1, action='store', type=int, help='Number')
    parser.add_argument('Number_of_training_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('Number_of_experiment_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('File_name', default='experiment', type=str, help='Name of file with not personalized data')
    parser.add_argument('EEG_connected', default='1', choices=['1', '0'], help='Choice')

    parser.add_argument('--Instruction', widget='FileChooser', help='Choose instruction file')
    parser.add_argument('--Instruction_show_time', default=5, action='store', type=int, help='Number')

    # Information about training
    parser.add_argument('--Training_task', default=SampleTypes.letters,
                        choices=[SampleTypes.letters, SampleTypes.figures, SampleTypes.NamesAgeRelations,
                                 SampleTypes.NamesHeightRelations], help='Choose trial type')
    parser.add_argument('--Training_number', default=1, action='store', type=int, help='Number of relations')
    parser.add_argument('--Training_memory', default='1', choices=['1', '0'], help='Choice')
    parser.add_argument('--Training_integration', default='1', choices=['1', '0'], help='Choice')
    parser.add_argument('--Training_show_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_resp_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_maxtime', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_feedback', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_feedback_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_wait', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_fixtime', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_list_view', default='1', choices=['1', '0'], help='Choose view type')

    # Information about experiment
    parser.add_argument('--Experiment_task', default=SampleTypes.letters,
                        choices=[SampleTypes.letters, SampleTypes.figures, SampleTypes.NamesAgeRelations,
                                 SampleTypes.NamesHeightRelations], help='Choose trial type')
    parser.add_argument('--Experiment_number', default=1, action='store', type=int, help='Number of relations')
    parser.add_argument('--Experiment_memory', default='1', choices=['1', '0'], help='Choice')
    parser.add_argument('--Experiment_integration', default='1', choices=['1', '0'], help='Choice')
    parser.add_argument('--Experiment_show_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_resp_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_maxtime', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_feedback', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_feedback_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_wait', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_fixtime', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_list_view', default='1', choices=['1', '0'], help='Choose view type')

    args = parser.parse_args()
    experiment = []

    name = args.Instruction.split('/')[-1]

    for block in range(args.Number_of_blocks):
        instruction = [block+1, 'instruction', args.Instruction_show_time, name]
        experiment.append(instruction)
        for idx in range(0, args.Number_of_training_trials):
            trial = [block+1, args.Training_task, args.Training_number, idx + 1, int(args.Training_memory),
                          int(args.Training_integration), args.Training_show_time, args.Training_resp_time,
                          args.Training_maxtime, args.Training_feedback, args.Training_feedback_time,
                          args.Training_wait, 0, args.Training_fixtime, int(args.EEG_connected),
                          int(args.Training_list_view)]
            experiment.append(trial)
        for idx in range(0, args.Number_of_experiment_trials):
            trial = [block+1, args.Experiment_task, args.Experiment_number, idx + 1, int(args.Experiment_memory),
                          int(args.Experiment_integration), args.Experiment_show_time, args.Experiment_resp_time,
                          args.Experiment_maxtime, args.Experiment_feedback, args.Experiment_feedback_time,
                          args.Experiment_wait, 1, args.Experiment_fixtime, int(args.EEG_connected),
                          int(args.Experiment_list_view)]
            experiment.append(trial)

    save_to_xlsx(experiment, args.File_name)


def main():
    generate_trials_gui()


if __name__ == '__main__':
    main()
