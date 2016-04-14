#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ociepkam'

# All possible sample types in procedure.

import random
from enum import Enum
import string


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
    {'name': 'Roch', 'sex': 'M'},
    {'name': 'Piotr', 'sex': 'M'},
    {'name': 'Adam', 'sex': 'M'},
    {'name': 'Filip', 'sex': 'M'},
    {'name': 'Igor', 'sex': 'M'},
    {'name': 'Jacek', 'sex': 'M'},
    {'name': 'Wit', 'sex': 'M'},

    {'name': 'Ewa', 'sex': 'F'},
    {'name': 'Anna', 'sex': 'F'},
    {'name': 'Iga', 'sex': 'F'},
    {'name': 'Magda', 'sex': 'F'},
    {'name': 'Ada', 'sex': 'F'},
    {'name': 'Ola', 'sex': 'F'},
    {'name': 'Łucja', 'sex': 'F'},
    {'name': 'Maja', 'sex': 'F'},
    {'name': 'Klara', 'sex': 'F'},
    {'name': 'Ida', 'sex': 'F'},
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
    def __init__(self, sample_type, n, nr, memory, integr, show_time, resp_time, maxtime, feedb, feedb_time, wait, exp, fixtime, eeg, view_list):
        """
        :param sample_type: kind of stimulus. All possibilities in SampleTypes class.
        :param n: number of relations in trial. n+1 number od elements in relation chain
        :param nr: Trial index. Different for each Trial.
        :param memory:
            (memory == 1) => Participant can't see stimulus when answering.
            (memory == 0) => Participant see all stimulus from Trial when answering.
        :param integr:
            (integr == 1) => Question contain first and last element from relation chain.
            (integr == 0) => Question contain two random element from relation chain.
                                This element have to be neighbors.
        :param time: how long participant can see each relations.
        :param maxtime: time for answer.
        :param feedb:
            0 - doesn't show result for this Trial.
            1 - show result for this Trial.
            2 - doesn't show result for this Trial but show percent result at the end of test.
        :param wait: break time after Trial. 0 - wait until participant doesn't press button.
        :param exp:
            (exp == 1) => Experiment Trial.
            (exp == 0) => Test Trail.
        :param eeg:
            (eeg == 1) => EEG is connected.
            (eeg == 0) => EEG isn't connected.
        :param view_list:
            (view_list == 1) => Relation under relation - for tablets.
            (view_list == 0) => All relations shown at the same place.
        :return:
        """
        self.sample_type = sample_type
        self.n = n
        self.nr = nr
        self.memory = int(memory)
        self.integr = int(integr)
        self.show_time = show_time
        self.resp_time = resp_time
        self.maxtime = maxtime
        self.feedb = feedb
        self.feedb_time = feedb_time
        self.wait = wait
        self.exp = int(exp)
        self.fixtime = fixtime
        self.relations_list = None
        self.task = None
        self.answer = None
        self.eeg = int(eeg)
        self.view_list = int(view_list)

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
            relations_list, task, [answer] = self.create_sample_figures()

        self.shuffle_sample(relations_list)

        self.relations_list = relations_list
        self.task = task
        self.answer = answer

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
            first = random.randint(0, self.n - 1)
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
        answer = first_task

        return task, answer

    def create_general_trial_json(self):
        trial = {
            'SAMPLE_TYPE': self.sample_type,
            'N': self.n,
            'NR': self.nr,
            'MEMORY': self.memory,
            'INTEGR': self.integr,
            'SHOW_TIME': self.show_time,
            'RESP_TIME': self.resp_time,
            'MAXTIME': self.maxtime,
            'FEEDB': self.feedb,
            'FEEDB_TIME': self.feedb_time,
            'WAIT': self.wait,
            'EXP': self.exp,
            'FIXTIME': self.fixtime,
            'EEG': self.eeg,
            'LIST_VIEW': self.view_list
        }

        return trial

    def create_concrete_trial_json(self):
        trial = self.create_general_trial_json()
        trial['RELATIONS_LIST'] = self.relations_list
        trial['TASK'] = self.task
        trial['ANSWER'] = self.answer

        return trial