#!/usr/bin/python
# -*- coding: utf-8 -*-
"""POUR AMELIORER CES CLASSES, IL FAUDRAIT UTILISER LE CONCEPT D'HERITAGE.
IL Y A BEAUCOUP DE CHOSES COMMUNES ENTRE CES CLASSES """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import numpy as np

from error import ModeError
from basedataclass import BaseDataClass


class OLD_PHASE_OUT_PHASE(BaseDataClass):
    slots = ["data"]

    def __init__(self, data=None, name="phase", data_type="Phase", fs=50):
        BaseDataClass.__init__(self, name, data_type, fs)
        if data is not None:
            self.data = data
        else:
            self.data = None

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        if isinstance(item, slice):
            data = self.data[item.start:item.stop]
            return OLD_PHASE_OUT_PHASE(data)

    def set_phase_data(self, trunk, lower, pre_drop_mean, pre_drop_std):
        """calculate if the patient is in phase or not based on the lower body and trunk angle and a threshold defined
        when the patient is in static condition before the appearance of the drop.

        trunk lower and threshold must be relative angle."""
        top_threshold_trunk = pre_drop_mean["angle_trunk"] + (1.96 * pre_drop_std["angle_trunk"])
        low_threshold_trunk = pre_drop_mean["angle_trunk"] - (1.96 * pre_drop_std["angle_trunk"])
        top_threshold_lower = pre_drop_mean["angle_lower"] + (1.96 * pre_drop_std["angle_lower"])
        low_threshold_lower = pre_drop_mean["angle_lower"] - (1.96 * pre_drop_std["angle_lower"])

        # print("threshold", top_threshold_trunk, low_threshold_trunk, top_threshold_lower, low_threshold_lower)

        threshold_trunk = np.logical_or(trunk > top_threshold_trunk, trunk < low_threshold_trunk)
        threshold_lower = np.logical_or(lower > top_threshold_lower, lower < low_threshold_lower)
        threshold_condition = np.logical_and(threshold_lower, threshold_trunk)
        # print("condtion")

        in_phase_right_side = np.logical_and(np.logical_and(trunk > 0, lower > 0), threshold_condition)
        in_phase_left_side = np.logical_and(np.logical_and(trunk < 0, lower < 0), threshold_condition)
        in_phase = np.where(np.logical_or(in_phase_left_side, in_phase_right_side), 1, 0)
        # print("inphase")

        out_of_phase_right_side = np.logical_and(np.logical_and(trunk > 0, lower < 0), threshold_condition)
        out_of_phase_left_side = np.logical_and(np.logical_and(trunk < 0, lower > 0), threshold_condition)
        out_phase = np.where(np.logical_or(out_of_phase_left_side, out_of_phase_right_side), -1, 0)
        # print("out_phase")

        phase = np.zeros(len(trunk))
        phase += (in_phase + out_phase)
        # print("phase_done")

        self.data = phase

    @property
    def move_id(self):
        return self.move_id

    @move_id.setter
    def move_id(self, val):
        self.move_id = val

    @move_id.deleter
    def move_id(self):
        self.move_id = None

    def equalise_length(self, length, mode, max_length = None):
        if max_length is not None and length > max_length:
            length = max_length
        try:
            if mode not in ["min", "max"]:
                raise ModeError(mode)
            if mode == 'max':
                arr = np.zeros(len(length))
                self.data = arr + self.data
            else:
                self.data = self.data[0:length]
        except ModeError as e:
            print(e.message)
