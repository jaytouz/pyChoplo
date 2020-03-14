#!/usr/bin/python
# -*- coding: utf-8 -*-

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

from eventbaseclass import Event


class MaxVelocity(Event):
    """this class manage the calculation """

    def __init__(self, arr, lim_inf, lim_sup, dtype=None):
        data = deepcopy(arr)  # copy of the original data saved for plot purpose
        self.name = "MaxVel"
        self.dtype = dtype

        pos = deepcopy(arr)  # array to work with
        vel = np.diff(pos)  # vel array to work with
        self.vel = np.diff(pos)  # copy for plot purpose

        self.max_vel = max(vel[lim_inf:lim_sup]) #dont look after 5 sec.
        max_vel_index = np.where(vel == self.max_vel)[0][0]

        Event.__init__(self, data, max_vel_index, full_name='max_vel')

    def calculate_max_vel_with_boundary(self, inf, sup):
        print(inf, sup)
        m_v = max(self.vel[inf:sup])
        index = np.where(self.vel == m_v)[0][0]
        self.max_vel = m_v
        self.index = index
        self.val = m_v

    @staticmethod
    def correct_max_vel_with_cm(move, dt, arr='x_arr'):
        lim_inf_idx = move.cof.cm.rel_pt.index + 6
        lim_sup_idx = move.end_drop_median

        n = lim_sup_idx - lim_inf_idx

        while n < 6:
            lim_sup_idx +=3
            n = lim_sup_idx - lim_inf_idx

        return MaxVelocity(move.__dict__[dt].__dict__[arr], lim_inf_idx, lim_sup_idx)

    def plot_vel(self, patch=True):
        from plot import add_patch

        ax = plt.subplot()
        ax.plot(self.vel, color="b", label="Vel - " + self.dtype)
        if patch:
            add_patch(ax, self.index, self.val, 'maxV')
        ax.legend(loc="best")
