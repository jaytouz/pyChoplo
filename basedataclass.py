#!/usr/bin/python
# -*- coding: utf-8 -*-
""" """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


from copy import deepcopy

import matplotlib.pyplot as plt

from amplitude import MaxAmplitude, PourcMovement, PourcDisplacement
from chopsummary import Summary
from filter import butter_lowpass_filter, butter_highpass_filter, butter_bandpass_filter, rolling_mean
from start import ReactionTime
from velocity import MaxVelocity


class BaseDataClass(object):
    def __init__(self, name, data_type, fs=50):
        self.name = name
        self.data_type = data_type
        self.fs = fs
        self.cm = None
        self.reaction_time_from_player = None
        self.reaction_time_from_move = None
        self.max_amp = None
        self.max_vel = None  # self.t_norm = None  # self.t_sec = None

    def __str__(self):
        message = "{} est de type {}".format(self.name, self.data_type)
        return message

    def plot(self, color='k', move_id=None, drop_end=None):
        import numpy as np
        time = np.arange(len(self))
        vline_exist = False

        try:
            if "x_arr" in self.__dict__.keys():
                arr = self.x_arr
            elif "rel_arr" in self.__dict__.keys():
                arr = self.rel_arr
            elif "gamma" in self.__dict__.keys():
                arr = self.gamma
            ax = plt.subplot()
            ax.plot(time, arr, color=color, label="{} - {} - {}".format(self.data_type, self.name, move_id))
            if not vline_exist and drop_end is not None:
                ax.vlines(drop_end, -0.08, 0.1, color='m')
                vline_exist = True
            ax.legend(loc="best")
        except AttributeError:
            print("unable to plot data. No attribute rel or xarr")

    def plot_state(self, color='k', s=100, move_id=None, drop_end_time=None):
        import numpy as np
        ax = plt.subplot()
        try:
            if "x_arr" in self.__dict__.keys():
                x = self.x_arr
                y = self.y_arr
                ax.scatter(x, y, color=color, label="{} - {} - {}".format(self.data_type, self.name, move_id))
            elif "rel_arr" in self.__dict__.keys():
                teta = self.rel_arr
                t = np.linspace(0, len(teta), len(teta))
                ax.scatter(t, teta, s=s, color=color, label="{} - {} - {}".format(self.data_type, self.name, move_id))
            ax.legend(loc="best")
        except AttributeError:
            print("unable to plot data. No attribute rel or xarr")

    def get_summary(self, arr):
        summary = Summary(arr)
        return summary

    def set_counter_movement(self, max_amp_index, drop_end_index, method=1):
        from counter_movement import CounterMovement1, CounterMovement
        if self.name not in ["COF", "COF_REL"]:
            print("This is not a center of force object, Can't set counter movement")
            return
        else:
            if method == 1:
                arr = deepcopy(self.x_arr)
                self.cm = CounterMovement1(arr, max_amp_index, drop_end_index)

    def set_reaction_time_from_player_mean(self, player_threshold_mean, player_threshold_std):
        if self.name not in ["COF", "COF_REL"]:
            print("This is not a center of force object, Can't set reaction time")
            return
        else:
            self.reaction_time_from_player = ReactionTime(self.x_arr, player_threshold_mean, player_threshold_std,
                                                          dtype=self.data_type)

    def set_reaction_time_from_move_mean(self, move_threshold_mean, move_threshold_std):
        if self.name not in ["COF", "COF_REL"]:
            print("This is not a center of force object, Can't set reaction time")
            return
        else:
            self.reaction_time_from_move = ReactionTime(self.x_arr, move_threshold_mean, move_threshold_std,
                                                        dtype=self.data_type)

    def add_max_amp(self, drop_end_index):
        self.max_amp = MaxAmplitude(self.x_arr, dtype=self.data_type, drop_end_index=drop_end_index, delay=100)

    def add_max_vel(self, drop_end_index):
        self.max_vel = MaxVelocity(self.x_arr, lim_inf=15, lim_sup=drop_end_index, dtype=self.data_type)

    def set_cof_rel_event(self, drop_amp):
        drop_amp = abs(drop_amp)
        arr = self.x_arr

        self.tm5 = PourcMovement(arr, self.max_amp.index, pourc=5, target=drop_amp)
        self.tm10 = PourcMovement(arr, self.max_amp.index, pourc=10, target=drop_amp)
        self.tm25 = PourcMovement(arr, self.max_amp.index, pourc=25, target=drop_amp)
        self.tm50 = PourcMovement(arr, self.max_amp.index, pourc=50, target=drop_amp)
        self.tm75 = PourcMovement(arr, self.max_amp.index, pourc=75, target=drop_amp)
        self.tm100 = PourcMovement(arr, self.max_amp.index, pourc=100, target=drop_amp)

        self.pdispl_5 = PourcDisplacement(arr, self.max_amp.val, pourc=5, target=drop_amp)
        self.pdispl_10 = PourcDisplacement(arr, self.max_amp.val, pourc=10, target=drop_amp)
        self.pdispl_25 = PourcDisplacement(arr, self.max_amp.val, pourc=25, target=drop_amp)
        self.pdispl_50 = PourcDisplacement(arr, self.max_amp.val, pourc=50, target=drop_amp)
        self.pdispl_75 = PourcDisplacement(arr, self.max_amp.val, pourc=75, target=drop_amp)
        self.pdispl_100 = PourcDisplacement(arr, self.max_amp.val, pourc=100, target=drop_amp)

        self.pdispl_target = PourcDisplacement(arr, self.max_amp.val, target=drop_amp, error=0.1)

    # def add_time_pourc_move(self, drop_end_index, n):
    #     import numpy as np
    #     self.t_norm = np.arange(n)/drop_end_index * 100
    #
    # def add_time_sec(self, n, fs = 50):
    #     import numpy as np
    #     self.t_sec = np.arange(n)/fs

    def apply_low_pass(self, cutoff):
        """apply a buttherworth filter low pass using forward and reverse method on data in self.slots

            parameter
            --------------------
            cutoff (float)
            fs (float or int)
            order (int) : is double because of fillfill method.
            """

        for att in self.slots:
            data = self.__dict__[att]
            if data is not None:
                filt_data = butter_lowpass_filter(data, cutoff, self.fs)
                self.__dict__[att] = filt_data

    def apply_high_pass(self, cutoff):
        """apply a buttherworth filter high pass using forward and reverse method on data in self.slots

            parameter
            --------------------
            cutoff (float)
            fs (float or int)
            order (int) : is double because of fillfill method.
            """

        for att in self.slots:
            data = self.__dict__[att]
            if data is not None:
                filt_data = butter_highpass_filter(data, cutoff, self.fs)
                self.__dict__[att] = filt_data

    def apply_band_pass(self, lowcut, highcut):
        """apply a buttherworth filter bandpass using forward and reverse method on data in self.slots

            parameter
            --------------------
            cutoff (float)
            fs (float or int)
            order (int) : is double because of fillfill method.
            """

        for att in self.slots:
            data = deepcopy(self.__dict__[att])
            if data is not None:
                filt_data = butter_bandpass_filter(data, lowcut, highcut, self.fs)
                self.__dict__[att] = filt_data

    def apply_rolling_mean(self, window=10):
        for att in self.slots:
            data = deepcopy(self.__dict__[att])
            if data is not None:
                filt_data = rolling_mean(data, window, center=True)
                self.__dict__[att] = deepcopy(filt_data)
