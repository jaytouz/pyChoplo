#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires
 pour la segmentation du mouvement selon 5 différents GAMEMODE """

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from copy import deepcopy

from eventbaseclass import Event


class ReactionTime(Event):
    """this class takes the COF (x_arr) as input to define the counter movement"""

    def __init__(self, x_arr, pre_drop_mean_data, pre_drop_std_data, dtype=None, fs=50):
        y = deepcopy(x_arr)  # copy of numpy array
        # y = ReactionTime.translate_start_to(y, go_to_val=pre_drop_mean_data["COF"])
        reaction_time_index = 0
        index = 0
        look_for_exit_static = False
        self.threshold_mean = pre_drop_mean_data["cof"]
        self.upper_threshold = pre_drop_mean_data["cof"] + (pre_drop_std_data["cof"] * 1.96)  # creation of 5% confidence int
        self.lower_threshold = pre_drop_mean_data["cof"] - (pre_drop_std_data["cof"] * 1.96)  # creation of 5% confidence int

        # print(self.upper_threshold, pre_drop_mean_data["cof"], self.lower_threshold)

        self.state_array = None
        self.static_to_dynamic_event = []
        self.dynamic_to_static_event = []
        self.upper_to_static = []
        self.lower_to_static = []
        self.static_to_lower = []
        self.static_to_upper = []

        self.get_state_array(y, self.upper_threshold, self.lower_threshold)
        self.get_event_array(y)

        try:
            reaction_time_index = self.static_to_dynamic_event[0]
        except IndexError:
            reaction_time_index = 0




        #  # # print(y[index], self.upper_threshold, self.lower_threshold)  # if y[index] > self.upper_threshold or y[index] < self.lower_threshold:  #     reaction_time_index = index  #     search = False  # else:  #     if index == len(y) - 1:  #         search = False  #         reaction_time_index = len(y) - 1  #     else:  #         index += 1

        Event.__init__(self, data=x_arr, index=reaction_time_index, full_name="start move " + dtype)

    def plot(self, color='k', patch_name=['St']):
        import matplotlib.pyplot as plt
        from plot import add_patch
        ax = plt.subplot()
        ax.plot(self.data, color=color, label=self.full_name)

        ax.hlines(self.threshold_mean, xmin=0, xmax=len(self.data) - 1, alpha=0.5, color='#212F3C')
        ax.hlines(self.upper_threshold, linestyles="--", xmin=0, xmax=len(self.data) - 1, alpha=0.5, color='#3498DB')
        ax.hlines(self.lower_threshold, linestyles="--", xmin=0, xmax=len(self.data) - 1, alpha=0.5, color='#3498DB')
        add_patch(ax, self.index, self.val, patch_name[0])
        ax.legend(loc="best")

    def get_state_array(self, y, upperthresold, lowerthreshold):
        """you can be either in the static zone (mean +- 1.96std), higher than upperthreshold or lower than
        lowerthreshold which are both out of the static zone"""

        state = []
        for i in range(0, len(y)):
            if y[i] > upperthresold:
                state.append(1)
            elif y[i] < lowerthreshold:
                state.append(-1)
            elif y[i] <= upperthresold and y[i] >= lowerthreshold:
                state.append(0)
        self.state_array = state

    def get_event_array(self, y):
        for i in range(1, len(y)):
            last_state = self.state_array[i - 1]
            current_state = self.state_array[i]
            if last_state == 0 and current_state == 1:
                # print("static to dynamic upper bound", i)
                self.static_to_dynamic_event.append(i-1)
                self.static_to_upper.append(i-1)
            elif last_state == 0 and current_state == -1:
                # print("static to dynamic lower bound", i-1)
                self.static_to_dynamic_event.append(i-1)
                self.static_to_lower.append(i-1)
            elif last_state == -1 and current_state == 0:
                # print("dynamic to static lower to static", i)
                self.dynamic_to_static_event.append(i-1)
                self.lower_to_static.append(i-1)
            elif last_state == 1 and current_state == 0:
                # print("dynamic to static upper to static", i)
                self.dynamic_to_static_event.append(i-1)
                self.upper_to_static.append(i-1)

    @staticmethod
    def translate_start_to(y, go_to_val=0):
        start = y[0]
        translate_of = go_to_val - start
        y -= translate_of
        return y

    #  # @staticmethod  # def start_from_pos(y, lag=5, threshold=4, influence=0, cm_instance=None, plot=True, color='k', patch_label="s",  #                    plot_label="start_from_pos"):  #     """From the 'y' data arr and the index of the minimum point, find the start of the CM which is based on the  #     thresholding algorithm.  #  #     Parameter  #     -------  #     y : np.array, data of the COF in a move  #     lag : int, the lag of the moving window  #     threshold : the z-score at which the algorithm signals  #     influence : the influence (between 0 and 1) of new signals on the mean and standard deviation  #  #     For example, a lag of 5  #     will use the last 5 observations to smooth the data.  #     A threshold of 3.5 will signal if a datapoint is 3.5 standard  #     deviations away from the moving mean. And an influence of 0.5  #     gives signals half of the influence that normal datapoints  #     have. Likewise, an influence of 0 ignores signals completely  #     for recalculating the new threshold: an influence of 0 is  #     therefore the most robust option; 1 is the least.  #     """  #     pos = y  #  #     filt_signal = thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)  #     signal = filt_signal['signals']  #     search = True  #     index = 0  #     stopper = len(y)  #  #     if cm_instance is not None:  #         release_point_index = cm_instance.release_point_index  #         start_cm_index = cm_instance.drop_in_index  #         if start_cm_index == 0:  #             stopper = release_point_index  #         else:  #             stopper = start_cm_index  #  #     while search:  #  #         if index == stopper:  #             start = stopper  #             search = False  #             if start == len(y):  #                 "ERROR, signal seems broken"  #                 start = 0  #  #         else:  #             start = signal[index]  #             if start == 1 or start == -1:  #                 if index <= stopper:  #                     search = False  #                     start = index  #             else:  #                 index += 1  #     if plot:  #         import matplotlib.pyplot as plt  #         from chopfunction.visualisation.plot import add_patch  #  #         ax = plt.subplot()  #         ax.plot(pos, color=color, label=plot_label)  #         ax.plot(filt_signal['avgFilter'], color='g')  #         ax.plot(signal * 0.05, color='m')  #         add_patch(ax, start, pos[start], patch_label)  #         ax.legend(loc="best")  #         plt.show()  #         print(input("enter to continue..."))  #  #     return start  #  # @staticmethod  # def start_from_vel(y, lag=5, threshold=4, influence=0, cm_instance=None, plot=True, color='b', patch_label="s",  #                    plot_label="start_from_vel"):  #     """From the 'y' data arr and the index of the minimum point, find the start of the CM which is based on the  #     thresholding algorithm.  #  #     Parameter  #     -------  #     y : np.array, data of the COF in a move  #     lag : int, the lag of the moving window  #     threshold : the z-score at which the algorithm signals  #     influence : the influence (between 0 and 1) of new signals on the mean and standard deviation  #  #     For example, a lag of 5  #     will use the last 5 observations to smooth the data.  #     A threshold of 3.5 will signal if a datapoint is 3.5 standard  #     deviations away from the moving mean. And an influence of 0.5  #     gives signals half of the influence that normal datapoints  #     have. Likewise, an influence of 0 ignores signals completely  #     for recalculating the new threshold: an influence of 0 is  #     therefore the most robust option; 1 is the least.  #     """  #     vel = np.diff(y)  #  #     filt_signal = thresholding_algo(vel, lag=lag, threshold=threshold, influence=influence)  #     signal = filt_signal['signals']  #     search = True  #     index = 0  #     stopper = len(y) - 1  # because its vel (1 time diff)  #  #     if cm_instance is not None:  #         release_point_index = cm_instance.release_point_index  #         start_cm_index = cm_instance.drop_in_index  #         if start_cm_index == 0:  #             stopper = release_point_index  #         else:  #             stopper = start_cm_index  #  #     while search:  #  #         if index == stopper:  #             start = stopper  #             search = False  #             if start == len(y) - 1:  #                 "ERROR, signal seems broken"  #                 start = 0  #  #         else:  #             start = signal[index]  #             if start == 1 or start == -1:  #                 if index <= stopper:  #                     search = False  #                     start = index  #             else:  #                 index += 1  #  #     if plot:  #         import matplotlib.pyplot as plt  #         from chopfunction.visualisation.plot import add_patch  #  #         ax = plt.subplot()  #         ax.plot(y, color=color, label='pos')  #         ax.plot(vel, color='r', label="velocity")  #         ax.plot(filt_signal['avgFilter'], color='g')  #         ax.plot(signal * 0.05, color='m')  #         add_patch(ax, start, np.diff(y)[start], "s_v")  #         add_patch(ax, start, y[start], patch_label)  #         ax.legend(loc="best")  #         plt.show()  #         print(input("enter to continue..."))  #  #     return start  #  # @staticmethod  # def start_from_accel(y, lag=5, threshold=4, influence=0, cm_instance=None, plot=True, color='m', patch_label="s",  #                      plot_label="start_from_accel"):  #     """From the 'y' data arr and the index of the minimum point, find the start of the CM which is based on the  #     thresholding algorithm.  #  #     Parameter  #     -------  #     y : np.array, data of the COF in a move  #     lag : int, the lag of the moving window  #     threshold : the z-score at which the algorithm signals  #     influence : the influence (between 0 and 1) of new signals on the mean and standard deviation  #  #     For example, a lag of 5  #     will use the last 5 observations to smooth the data.  #     A threshold of 3.5 will signal if a datapoint is 3.5 standard  #     deviations away from the moving mean. And an influence of 0.5  #     gives signals half of the influence that normal datapoints  #     have. Likewise, an influence of 0 ignores signals completely  #     for recalculating the new threshold: an influence of 0 is  #     therefore the most robust option; 1 is the least.  #     """  #     accel = np.diff(np.diff(y))  #  #     filt_signal = thresholding_algo(accel, lag=lag, threshold=threshold, influence=influence)  #     signal = filt_signal['signals']  #     search = True  #     index = 0  #     stopper = len(y) - 2  # because its accel (2 times diff)  #  #     if cm_instance is not None:  #         release_point_index = cm_instance.release_point_index  #         start_cm_index = cm_instance.drop_in_index  #         if start_cm_index == 0:  #             stopper = release_point_index  #         else:  #             stopper = start_cm_index  #  #     while search:  #  #         if index == stopper:  #             start = stopper  #             search = False  #             if start == len(y) - 2:  #                 "ERROR, signal seems broken"  #                 start = 0  #  #         else:  #             start = signal[index]  #             if start == 1 or start == -1:  #                 if index <= stopper:  #                     search = False  #                     start = index  #             else:  #                 index += 1  #     if plot:  #         import matplotlib.pyplot as plt  #         from chopfunction.visualisation.plot import add_patch  #  #         ax = plt.subplot()  #         ax.plot(y, color=color, label=plot_label)  #         ax.plot(np.diff(y), color='b', label="vel")  #         ax.plot(accel, color='r', label="accel")  #         ax.plot(filt_signal['avgFilter'], color='g')  #         ax.plot(signal * 0.05, color='c')  #         add_patch(ax, start, accel[start], "s_a")  #         add_patch(ax, start, y[start], patch_label)  #         ax.legend(loc="best")  #         plt.show()  #         print(input("enter to continue..."))  #  #     return start
