#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lab'

import json
import random
from enum import Enum
import string
from gooey import Gooey, GooeyParser
import csv


# All possible sample types in procedure.
class SampleTypes(Enum):
    letters = 'letters'
    figures = 'figures'
    NamesHeightRelations = 'NamesHeightRelations'
    NamesAgeRelations = 'NamesAgeRelations'


# General relations types.
class Relations(Enum):
    major = '>'
    minor = '<'


# Age relations types for name samples.
class NamesAgeRelations(Enum):
    major_M = ' starszy niż '
    major_F = ' starsza niż '
    minor_M = ' młodszy niż '
    minor_F = ' młodsza niż '


# Height relations types for name samples.
class NamesHeightRelations(Enum):
    major_M = ' wyższy niż '
    major_F = ' wyższa niż '
    minor_M = ' niższy niż '
    minor_F = ' niższa niż '

# Dictonary for name samples.
names_types = {
    'NamesAgeRelations': NamesAgeRelations,
    'NamesHeightRelations': NamesHeightRelations
}

names = (
    {'name': 'Tomek', 'sex': 'M'},
    {'name': 'Lech', 'sex': 'M'},
    {'name': 'Jan', 'sex': 'M'},
    {'name': 'Zygmunt', 'sex': 'M'},
    {'name': 'Ewa', 'sex': 'F'},
    {'name': 'Anna', 'sex': 'F'},
    {'name': 'Monika', 'sex': 'F'},
    {'name': 'Magda', 'sex': 'F'},
)

# List of stimulus for letters samples. Only consonants letters.
letters = list(set(string.ascii_uppercase) - set("AEIOUY"))

figures = (
    'square',
    'triangle',
    'circle',
    'trapeze',
    'diamond',
    'ellipse',
    'rectangle',
    'hexagon'
)


class Trial:
    def __init__(self, sample_type, n, nr, memory, integr, time, maxtime, feedb, wait, exp):
        """
        :param sample_type: kind of stimulus. All possibilities in SampleTypes class.
        :param n: number of relations in trial. n+1 number od elements in relation chain
        :param nr: Trial index. Different for each Trial.
        :param memory:
            (memory == True) => Participant can't see stimulus when answering.
            (memory == False) => Participant see all stimulus from Trial when answering.
        :param integr:
            (integr == True) => Question contain first and last element from relation chain.
            (integr == True) => Question contain two random element from relation chain.
                                This element have to be neighbors.
        :param time: how long participant can see each relations.
        :param maxtime: time for answer.
        :param feedb:
            0 - doesn't show result for this Trial.
            1 - show result for this Trial.
            2 - doesn't show result for this Trial but show percent result at the end of test.
        :param wait: break time after Trial. 0 - wait until participant doesn't press button.
        :param exp:
            (exp == True) => Experiment Trial.
            (exp == True) => Test Trail.
        :return:
        """
        self.sample_type = sample_type
        self.n = n
        self.nr = nr
        self.memory = memory
        self.integr = integr
        self.time = time
        self.maxtime = maxtime
        self.feedb = feedb
        self.wait = wait
        self.exp = exp

        self.relations_list, self.task, self.answer = self.create_sample()

    def create_sample_letters(self):
        """
        From n+1 random letters generate chain of pair of relations.
        There are two types of relations "<" and ">"
        :return: Chain of pair of relations.
        """
        stimulus_nr = random.sample(range(0, 8), self.n + 1)
        relations_list = []
        chain_of_letters = []
        for idx in stimulus_nr:
            chain_of_letters.append(letters[idx])

        for idx in range(0, self.n):
            stimulus_type = random.choice([Relations.major, Relations.minor])
            stimulus_1 = chain_of_letters[idx]
            stimulus_2 = chain_of_letters[idx + 1]

            if stimulus_type == Relations.minor:
                relation = stimulus_1 + stimulus_type + stimulus_2
                relations_list.append(relation)
            else:
                relation = stimulus_2 + stimulus_type + stimulus_1
                relations_list.append(relation)

        task, answer = self.create_task(chain_of_letters)

        return relations_list, task, answer

    def create_sample_names(self, sample_type):
        """
        From n+1 random letters generate chain of pair of relations.
        There are two types of relations "<" and ">"
        :param sample_type: decide with of two NamesAgeRelations or NamesHeightRelations we need to generate
        :return: Chain of pair of relations.
        """
        stimulus_nr = random.sample(range(0, 8), self.n + 1)
        relations_list = []

        chain_of_names = []
        for idx in stimulus_nr:
            chain_of_names.append(names[idx])

        for idx in range(0, self.n):
            stimulus_type = random.choice([Relations.major, Relations.minor])
            stimulus_1 = chain_of_names[idx]
            stimulus_2 = chain_of_names[idx + 1]

            if stimulus_type == Relations.minor:
                if stimulus_1['sex'] == 'F':
                    stimulus_type = sample_type.minor_F
                else:
                    stimulus_type = sample_type.minor_M

                relation = stimulus_1['name'] + stimulus_type + stimulus_2['name']
                relations_list.append(relation)
            else:
                if stimulus_2['sex'] == 'F':
                    stimulus_type = sample_type.major_F
                else:
                    stimulus_type = sample_type.major_M

                relation = stimulus_2['name'] + stimulus_type + stimulus_1['name']
                relations_list.append(relation)

        task, answer = self.create_task(chain_of_names)

        return relations_list, task, answer

    def create_sample_figures(self):
        """
        From n+1 random figures generate chain of pair of relations.
        :return: Chain of pair of relations.
        """

        stimulus_nr = random.sample(range(0, 8), self.n + 1)
        chain_of_figures = []
        for idx in stimulus_nr:
            chain_of_figures.append(figures[idx])

        relations_list = []
        for idx in range(0, self.n):
            stimulus_1 = chain_of_figures[idx]
            stimulus_2 = chain_of_figures[idx + 1]
            relations_list.append([stimulus_1, stimulus_2])

        task, answer = self.create_task(chain_of_figures)

        return relations_list, task, answer

    def create_sample(self):
        """
        Allow to choose task type.
        :return: Chain of pair of relations.
        """
        if self.sample_type == "letters":
            relations_list, task, answer = self.create_sample_letters()
        elif self.sample_type == "NamesHeightRelations":
            relations_list, task, answer = self.create_sample_names(names_types["NamesHeightRelations"])
        elif self.sample_type == "NamesAgeRelations":
            relations_list, task, answer = self.create_sample_names(names_types["NamesAgeRelations"])
        else:
            relations_list, task, answer = self.create_sample_figures()

        self.shuffle_sample(relations_list)

        return relations_list, task, answer

    def shuffle_sample(self, relations_list):
        """
        :param relations_list: List of all relations in trial. Generated by create_sample.
        :return: Shuffled list of relations in order with will see participant.

        Firs relation is random. Each next must contain one of the parameters with was show before.
        """
        # choosing first relation
        first_stimulus = random.randint(0, self.n - 1)
        relations_shuffled_list = [relations_list[first_stimulus]]

        next_elem = first_stimulus + 1
        previous_elem = first_stimulus - 1

        # As long as exist relations before or after chose relations find new one before or after already choose.
        while next_elem <= self.n and previous_elem >= -1:
            # No not chose elements at the end of relations chain
            if next_elem == self.n:
                relations_shuffled_list.append(relations_list[previous_elem])
                previous_elem -= 1
            # No not chose elements at the beginning of relations chain
            elif previous_elem == -1:
                relations_shuffled_list.append(relations_list[next_elem])
                next_elem += 1
            # Choose element before or after created chain
            else:
                if random.choice(['next', 'previous']) == next_elem:
                    relations_shuffled_list.append(relations_list[next_elem])
                    next_elem += 1
                else:
                    relations_shuffled_list.append(relations_list[previous_elem])
                    previous_elem -= 1

        return relations_shuffled_list

    def create_task(self, relations_chain):
        """
        :param relations_chain: chain of all samples in trial
        :return: Task and answer for trial
        """

        # Participant have to integrate relations -  task conclude first and last element from chain.
        if self.integr:
            first = 0
            second = self.n
        # Task conclude random pair of neighbors.
        else:
            first = random.randint(0, self.n)
            second = first + 1

        # Creating task and answer
        if self.sample_type == SampleTypes.figures:
            first_task = [relations_chain[first], relations_chain[second]]
            second_task = [relations_chain[second], relations_chain[first]]

        elif self.sample_type == SampleTypes.letters:
            first_task = relations_chain[first] + Relations.minor + relations_chain[second]
            second_task = relations_chain[second] + Relations.minor + relations_chain[first]
        else:
            if self.sample_type == SampleTypes.NamesAgeRelations:
                if relations_chain[first]['sex'] == 'M':
                    first_relation = NamesAgeRelations.minor_M
                else:
                    first_relation = NamesAgeRelations.minor_F
                if relations_chain[second]['sex'] == 'M':
                    second_relation = NamesAgeRelations.minor_M
                else:
                    second_relation = NamesAgeRelations.minor_F
            else:
                if relations_chain[first]['sex'] == 'M':
                    first_relation = NamesHeightRelations.minor_M
                else:
                    first_relation = NamesHeightRelations.minor_F
                if relations_chain[second]['sex'] == 'M':
                    second_relation = NamesHeightRelations.minor_M
                else:
                    second_relation = NamesHeightRelations.minor_F
            first_task = relations_chain[first]['name'] + first_relation + relations_chain[second]['name']
            second_task = relations_chain[second]['name'] + second_relation + relations_chain[first]['name']

        task = [first_task, second_task]
        random.shuffle(task)
        answer = [first_task]

        return task, answer

    def create_json(self):
        trial = {
            'NR': self.nr,
            'MEMORY': self.memory,
            'INTEGR': self.integr,
            'TIME': self.time,
            'MAXTIME': self.maxtime,
            'FEEDB': self.feedb,
            'WAIT': self.wait,
            'EXP': self.exp,
            'RELATIONS_LIST': self.relations_list,
            'TASK': self.task,
            'ANSWER': self.answer
        }

        return trial


class Trials:
    def __init__(self, number_of_trials):
        self.number_of_trials = number_of_trials
        self.list_of_trials = []

    def add_trial(self, trial_json):
        if len(self.list_of_trials) < self.number_of_trials:
            self.list_of_trials.append(trial_json)
        else:
            raise Exception('To many trials')

    def save_to_csv(self):

        with open('names.csv', 'w') as csvfile:
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



@Gooey(language='english',  # Translations configurable via json
       default_size=(650, 600),   # starting size of the GUI
       required_cols=1,           # number of columns in the "Required" section
       optional_cols=3,           # number of columbs in the "Optional" section
       )
def generate_trials_gui():

    parser = GooeyParser(description='Trial')
    parser.add_argument('Number_of_trials', default=4,action='store', type = int, help='Number')
    parser.add_argument("Random",default='True', choices = ['True', 'False'], help="Present trials in random order")

    parser.add_argument('--Exp', default='Trial', choices = ['Experiment', 'Trial'], help = 'Choice')
    parser.add_argument('--Task', default=SampleTypes.letters, choices=[SampleTypes.letters, SampleTypes.figures, SampleTypes.NamesAgeRelations, SampleTypes.NamesHeightRelations], help='Choose trial type')
    parser.add_argument('--Number',default=1, action='store', type = int, help='Number of relations')
    parser.add_argument('--Memory', default='True',choices = ['True', 'False'], help = 'Choice')
    parser.add_argument('--Integration',default='True', choices = ['True', 'False'], help = 'Choice')
    parser.add_argument('--Time',default=1, action='store', type = int, help='Number')
    parser.add_argument('--Maxtime',default=1, action='store', type = int, help='Number')
    parser.add_argument('--Feedback',default=1, action='store', type = int, help='Number')
    parser.add_argument('--Wait',default=1, action='store', type = int, help='Number')

    args = parser.parse_args()

    trials = Trials(args.Number_of_trials)

    for idx in range(0, args.Number_of_trials):
        test = Trial(args.Task, args.Number, idx+1, args.Memory, args.Integration, args.Time, args.Maxtime, args.Feedback, args.Wait, args.Exp)
        trials.add_trial(test.create_json())
        print test.create_json()

    trials.save_to_csv()

def main():

    generate_trials_gui()

if __name__ == '__main__':
    main()