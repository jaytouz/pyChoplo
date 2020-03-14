#!/usr/bin/python
# -*- coding: utf-8 -*-

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from copy import deepcopy

import numpy as np

from eventbaseclass import Event


class MaxAmplitude(Event):
    """this class manage the calculation """

    def __init__(self, arr, drop_end_index, inf_idx_lim = 50, delay=100, dtype=None):
        data = deepcopy(arr)  # copy of the original data saved for plot purpose
        name = "MaxAmp"
        limit_idx = drop_end_index + delay

        pos = deepcopy(arr[inf_idx_lim:limit_idx])  # array to work with

        max_amp = max(pos)
        max_amp_index = np.where(pos == max_amp)[0][0] + inf_idx_lim


        Event.__init__(self, data, max_amp_index, full_name=name + " - " + dtype)


class PourcMovement(Event):
    """Create a point corresponding to a pourcentage of the movement 100% = time at maxAmp"""

    def __init__(self, arr, max_amp_index, pourc=None, target=0.4, t0=0, name='TM', dtype=''):
        """from an array gets the value of an instant corresponding to a pourcentage of the movement where 100% of the
        movement is at max_amp_index

        if pourc == None, looks for the of pourc at target == 0.4


        Compare to PourcMovement, PourcDisplacement looks at a normalize y axis, while PourcMovement looks at pourcentage
        of movement on a normalize time axis"""

        if name == 'TM':
            name += str(pourc)

        if pourc is None:
            # looking for pourc of movement where
            pourc_index = self.find_index_closer_to(arr, target)  # get index where arr reach target
            pourc = self.index_to_pourc(pourc_index, max_amp_index, t0)
        else:
            pourc_index = self.pourc_to_index(pourc, max_amp_index, t0)

        self.pourc_index = int(pourc_index)  # corresponds to the index at the pourcentage of the movement
        self.pourc = pourc  # pourcentage of the movement
        self.t100 = max_amp_index  # 100% of the movement
        self.t0 = t0  # start of the movement
        Event.__init__(self, arr, self.pourc_index, full_name='max_amp')

    def pourc_to_index(self, pi, M, m=0):
        i = ((M * pi - m * pi) / 100) + m
        return i

    def index_to_pourc(self, i, M, m=0):
        p = (((M-m) - ((M-m) - (i-m))) / (M - m)) * 100
        return p

    def find_index_closer_to(self, arr, target_val):
        index = 0
        while index <= len(arr):
            if arr[index] <= target_val:
                index += 1
            else:
                break
        return index


class PourcDisplacement(Event):
    """PourcDisplacement is a class to manage event based on the displacement relative to the position at t0 and
    at t100.

    Compare to PourcMovement, PourcDisplacement looks at a normalize y axis, while PourcMovement looks at pourcentage
    of movement on a normalize time axis"""

    def __init__(self, arr, max_amp_val, pourc=None, target=None, error=0.1, t0=0, name='TM', dtype=''):
        if name == 'PDispl':
            name += str(pourc)

        max_val = max_amp_val
        min_val = arr[t0]

        if pourc is None:
            # looking for pourc dist at target
            pourc = self.val_to_pourc(max_val, min_val, target)
            if max_val > abs(target) - error:
                try:
                    index_pourc = self.get_index_of_pourc(arr, target, error)
                except IndexError:
                    # print('index not found')
                    index_pourc = 0
            else:
                index_pourc = 0

        else:
            # looking for dist at pourc
            val = self.pourc_to_val(max_val, min_val, pourc)
            try:
                index_pourc = self.get_index_of_pourc(arr, target, error)
            except IndexError:
                # print('Index not found')
                index_pourc = 0

        self.pourc = pourc  # pourcentage of distance relative to max amp
        self.index_pourc = index_pourc  # index at the pourc of dist
        self.M = max_val  # max distance in move
        self.m = min_val  # distance of cof_rel at t0
        Event.__init__(self,arr, self.index_pourc, full_name=name + " - " + dtype)

    def val_to_pourc(self, M, m, y):
        py = (((M-m) - ((M-m) - (y-m))) / (M - m)) * 100
        return py

    def pourc_to_val(self, M, m, py):
        y = ((M * py - m * py) / 100) + m
        return y

    def get_index_of_pourc(self, arr, target, error):
        i = 0
        while arr[i] < abs(target) - error:
            i+=1
        return i
