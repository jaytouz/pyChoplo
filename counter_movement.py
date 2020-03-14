#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires
 pour la segmentation du mouvement selon 5 différents GAMEMODE """

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

from peaks import detect_peaks, find_max_peak, find_min_valley, find_start_cm, find_release_point, find_next_peak
from zerocrossing import find_zero_crossing
from eventbaseclass import Event

# TODO every choplo class in this project should inherit from a specification class which could contain self.fs etc.
class CounterMovement:
    """this class takes the COF (x_arr) as input to define the counter movement"""
    min_reaction_time = 0.3
    def __init__(self, x_arr, max_amp_index, fs=50):
        self.data = deepcopy(x_arr)
        min_reaction_time_index = int(self.min_reaction_time/(1/fs)) #converts min_reaction_time in seconds to index
        self.fs = fs
        self.have_cm = False
        self.first_absement = None
        self.second_absement = None
        self.total_absement = None
        self.start_cm = None
        self.end_cm = None
        self.rel_pt = None
        self.min_index, self.max_index = min_reaction_time_index, max_amp_index
        self.valleys, self.peaks = CounterMovement.find_valley_peaks(self.data, min_index=self.min_index, max_index=self.max_index)


    @staticmethod
    def find_end_cm(y, rel_pt, end_threshold = 0):
        """from the release point index, finds the end of the counter movement. The function only works if there
        is a counter movement.

        end point definition : from the translated to zero data, the en of a cm is define by the zero crossing
        (last negative value) after the release point.

        :parameter
        -------
        rel_pt : int, index of the minimum point in the counter movement.
        y : np.array, data of interest.
        end_threshold: countermovement ends when it passes zero.

        :return
        ------
        end_index : int, index of the end point"""

        index = rel_pt
        search = True

        while search:
            if index == len(y):
                search = False
                try:
                    end_index = find_zero_crossing(y, start_pos=rel_pt - 1, forward=True)[0]
                except IndexError:
                    # print("NO END CM, the movement was in the wrong direction")
                    end_index = len(y) - 1
            else:
                if y[index] >= 0:
                    # print(y[index], y[start_index], y[start_index-1], y[start_index+1])
                    search = False
                    end_index = index
                else:
                    # print("END SEARCH", index)
                    index += 1

        return end_index

    #
    # @staticmethod
    # def find_start(y, lag=5, threshold=4, influence=0, plot=True, from_vel_signal=True, color='k', patch_label="s",
    #                plot_label="start_from_pos"):
    #     """From the 'y' data arr and the index of the minimum point, find the start of the CM which is based on the
    #     thresholding algorithm.
    #
    #     Parameter
    #     -------
    #     y : np.array, data of the COF in a move
    #     lag : int, the lag of the moving window
    #     threshold : the z-score at which the algorithm signals
    #     influence : the influence (between 0 and 1) of new signals on the mean and standard deviation
    #
    #     For example, a lag of 5
    #     will use the last 5 observations to smooth the data.
    #     A threshold of 3.5 will signal if a datapoint is 3.5 standard
    #     deviations away from the moving mean. And an influence of 0.5
    #     gives signals half of the influence that normal datapoints
    #     have. Likewise, an influence of 0 ignores signals completely
    #     for recalculating the new threshold: an influence of 0 is
    #     therefore the most robust option; 1 is the least.
    #     """
    #     pos = y
    #     if from_vel_signal:
    #         y = np.diff(y)
    #     filt_signal = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)
    #     signal = filt_signal['signals']
    #     search = True
    #     index = 0
    #
    #     while search:
    #         if index == len(y):
    #             start = 0
    #             search = False
    #         else:
    #             start = signal[index]
    #             if start == 1:
    #                 search = False
    #                 start = index
    #             else:
    #                 index += 1
    #
    #     if plot:
    #         import matplotlib.pyplot as plt
    #         from chopfunction.visualisation.plot import add_patch
    #
    #         ax = plt.subplot()
    #         ax.plot(pos, color=color, label=plot_label)
    #         ax.plot(np.diff(pos), color='r', label="velocity")
    #         ax.plot(filt_signal['avgFilter'], color='g')
    #         ax.plot(signal * 0.05, color='m')
    #         add_patch(ax, start, np.diff(pos)[start], "s_v")
    #         add_patch(ax, start, pos[start], patch_label)
    #         ax.legend(loc="best")
    #         plt.show()
    #         print(input("enter to continue..."))
    #
    #     return start

    @staticmethod
    def find_start_cm(y, peaks, min_index):
        """From the 'y' data arr and the index of the minimum point, find the start of the CM"""

        start_index = find_max_peak(y, peaks, search_start=min_index, look_left=True)

        return start_index

    @staticmethod
    def translate_start_to(y, go_to_val=0):
        start = y[0]
        translate_of = go_to_val - start
        y -= translate_of
        return y

    @staticmethod
    def find_valley_peaks(y, min_index, max_index):
        """find indices of valley and peaks

        Returns
        -------
        valley : 1D array_like
        indeces of the peaks in 'y'.

        peaks : 1D array_like indeces of the peaks in 'y'
        """
        if min_index is None:
            min_index = 0
        if max_index is None:
            max_index = len(y)

        valley = detect_peaks(y, mph=None, mpd=15, threshold=0, edge='rising', kpsh=False, valley=True, show=False,
                              ax=None)
        peaks = detect_peaks(y, mph=None, mpd=15, threshold=0, edge='rising', kpsh=False, valley=False, show=False,
                             ax=None)

        return valley, peaks

    @staticmethod
    def find_min_max(y, valleys, peaks):
        """find the index of the minimum valley before the maximum peaks and the maximum peaks

        Parameter
        -------
        y : array of COF to extract counter movement from

        Returns
        -------
        minimum : None if no minimum under 0 before maximum's index
        maximum : index of the maximum"""

        maximum_index = find_max_peak(y, peaks)
        minimum_index = find_min_valley(y, valleys)

        return minimum_index, maximum_index

    @staticmethod
    def check_for_valid_min(y, min_index, reaction_time_pos):
        """Check if the minimum found is actually part of a negative phase (counter movement). Returns False otherwise
            limits the search between index of min_reaction_time and index_of_peak_amp

            Parameter
            -------
            y : array of COF to extract counter movement from
            min_index : index of the minimum

            Returns
            -------
            have_cm : bool """
        have_cm = False
        max_amp = max(y)
        max_amp_index = np.where(y == max_amp)[0][0]
        if min_index is not None:
            if y[min_index] <= reaction_time_pos and min_index < max_amp_index:
                # if minimum is inf or equal to 0, there is a CM
                have_cm = True
        return have_cm


class CounterMovement1(CounterMovement):
    """method 1
    steps:
    1) define region of interest (done in main class : CounterMovement)
    2) check for cm : if data[t0] > data[min_valley_index]
    3) find start cm : look for all peaks from min_valley_index to min_reaction_time_index (sliding window to the left)
        define start cm as the first peak with positive value or the peak closest to zero if none is positive.
    4) find end of cm : define as the first zero crossing from min_valley_index to max peak index (sliding to the right)
    5) get impulse (negative (from start_cm to min_valley); positive (from min_valley to end_cm))

    """
    def __init__(self, x_arr, max_amp_index, drop_end_index, fs=50):
        # step 1 : define data
        # print("MAX AMP", max_amp_index)
        self.drop_end_index = drop_end_index
        CounterMovement.__init__(self,x_arr, max_amp_index, fs=fs)
        self.full_data = deepcopy(x_arr)
        self.v0 = x_arr[0]

        min_valley_idx = find_min_valley(x_arr, self.valleys, min_index_threshold=self.min_index, max_index_threshold=self.max_index, search_start_index=self.max_index,look_left=True)
        if min_valley_idx is None:
            m = min(x_arr[self.min_index:self.max_index])
            min_valley_idx = np.where(x_arr==m)[0][0]
        rel_pt_idx, self.c1, self.c2 = find_release_point(x_arr,self.valleys,self.peaks,min_index_threshold=self.min_index, max_index_threshold=self.max_index,search_start_index=self.max_index)
        self.rel_pt = Event(x_arr, rel_pt_idx, 'rel_pt')
        # print(min_valley_idx, self.rel_pt.val)
        #step 2 : check for cm
        self.have_cm = self.check_for_cm()

        if self.have_cm:
            #step 3 find start
            start_cm_idx = find_start_cm(self.data, self.peaks, max_index_threshold=self.max_index, search_start=self.rel_pt.index)
            if start_cm_idx is None:
                # didn't find start cm > 0
                "no start cm > to zero, just take max_peak in interval"
                start_cm_idx = find_max_peak(self.data, self.peaks, max_index_threshold=self.max_index, search_start=self.rel_pt.index)
                if start_cm_idx > self.rel_pt.index:
                    #means that starts comes after ends... no peaks between zero and rel_pt.index
                    start_cm_idx = np.where(max(self.data[0:self.rel_pt.index]))[0][0]

            if self.data[start_cm_idx] < 0:
                try:
                    start_cm_idx = find_zero_crossing(self.data, start_cm_idx, forward=False)[0]
                except IndexError:
                    pass
                    # print("No zero crossing between last found start cm and index 0")
            if start_cm_idx < self.min_index or start_cm_idx > rel_pt_idx:
                # print("START_CM WAS : ", start_cm_idx)
                start_cm_idx = self.min_index
            self.start_cm = Event(self.data, start_cm_idx, "start_cm")
            #step 4 find end
            end_cm_idx = self.find_end_cm(self.data, self.rel_pt.index)
            self.end_cm = Event(self.data, end_cm_idx, "end_cm")

            #step 5 : find negative impulse and positive impulse
            first_absement = self.data[self.start_cm.index:self.rel_pt.index]
            self.first_absement = np.trapz(first_absement,dx=1/self.fs) #from start to min_valley
            second_absement = self.data[self.rel_pt.index:self.end_cm.index]
            self.second_absement = np.trapz(second_absement,dx=1/self.fs) #from min_valley to first z_c
            self.total_absement = self.first_absement + self.second_absement

    def check_for_cm(self):
        # print(self.v0, self.min_valley.val)
        self.c1 = self.rel_pt.val < 0
        self.c2 = self.v0 > 0 and self.rel_pt.val > 0
        self.c3 = self.rel_pt.index > self.min_index + 10
        if self.c1 and not self.c2 and  self.c3:
            return True
        else:
            return False

    def get_min_valley_index(self):
        min_v = self.data[self.valleys[0]]
        min_v_idx = self.valleys[0]
        for v in self.valleys:
            if self.data[v] < min_v:
                min_v = self.data[v]
                min_v_idx = v
        # except IndexError:
        #     min_v_idx = np.where(self.data == min(self.data))[0][0]
        return Event(self.data, min_v_idx, "min_valley")

    def plot(self, color='k', save=False, title='', path=None):
        from plot import add_patch
        if save:
            fig = plt.figure(figsize=(19, 10.8))
        ax = plt.subplot()
        if self.have_cm:
            ax.plot(self.data, color=color, label="COF_CM")
            add_patch(ax, self.start_cm.index, self.start_cm.val, "s")
            add_patch(ax, self.rel_pt.index, self.rel_pt.val, "r")
            add_patch(ax, self.end_cm.index, self.end_cm.val, "e")
        else:
            ax.plot(self.data, color=color, label="COF_CM", alpha=0.4)
        ax.legend(loc="best")

        if save and path is not None:
            plt.savefig(path + title + '.png')
            plt.close()

    #
    # def calculate_counter_mouvement(self, x, rt_index):
    #     x = deepcopy(x)  # copy of numpy array
    #     self.reaction_time_index = reaction_time_index
    #     self.reaction_time_pos = x[reaction_time_index]
    #
    #     y = CounterMovement.translate_start_to(x, go_to_val=x[reaction_time_index])
    #
    #     valleys, peaks = CounterMovement.find_valley_peaks(y)
    #     min_index, max_index = CounterMovement.find_min_max(y, valleys, peaks)
    #
    #     self.fs = fs
    #     self.have_cm = False
    #     self._absement = None
    #     self.data = deepcopy(x_arr)
    #
    #     # check for counter movement
    #     if CounterMovement.check_for_valid_min(y, min_index, self.reaction_time_pos):
    #         self.have_cm = True
    #         # means that min_index is not None and min is inf or equal to zero
    #         # define the start of the counter movement
    #         self.start_index = CounterMovement.find_start_cm(y, peaks, min_index)
    #         self.start_val = self.data[self.start_index]
    #
    #         self.release_point_index = min_index
    #         self.release_point_val = self.data[self.release_point_index]
    #
    #         self.end_index = CounterMovement.find_end_cm(y, self.release_point_index, self.start_index)
    #         self.end_val = self.data[self.end_index]
    #
    #         self.end_val = self.data[self.end_index]
    #         self.cm_data = self.data[self.start_index: self.end_index]
    #         self.absement = np.trapz(self.cm_data, dx=1 / self.fs)