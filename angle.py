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


class Angle(BaseDataClass):
    """Structure de donnees pour stocker les donnees d'angle"""

    slots = ["abs_arr", "rel_arr"]

    def __init__(self, _abs, rel, name, data_type='Angle', fs=50):
        BaseDataClass.__init__(self, name, data_type, fs)
        if _abs is None:
            self.abs_arr = np.array([])
        else:
            self.abs_arr = _abs
        if rel is None:
            self.rel_arr = np.array([])
        else:
            self.rel_arr = rel

    def __len__(self):
        return len(self.rel_arr)

    def __getitem__(self, item):
        if isinstance(item, slice):
            abs_ = self.abs[item.start:item.stop]
            rel = self.rel[item.start:item.stop]
            return Angle(abs_, rel, self.name)

    @property
    def abs(self):
        return self.abs_arr

    @abs.setter
    def abs(self, arr):
        self.abs_arr = arr

    @abs.deleter
    def abs(self):
        self.abs_arr = None

    @property
    def rel(self):
        return self.rel_arr

    @rel.setter
    def rel(self, arr):
        self.rel_arr = arr

    @rel.deleter
    def rel(self):
        self.rel_arr = None

    @property
    def move_id(self):
        return self.move_id

    @move_id.setter
    def move_id(self, val):
        self.move_id = val

    @move_id.deleter
    def move_id(self):
        self.move_id = None

    def split(self, start, end, move_id):
        """Return a new instance with data[start:end] in abs and rel """
        _a = Angle(self.abs[start:end], self.rel[start:end], self.name)
        _a.move_id = move_id
        return _a

    def equalise_length(self, length, mode, max_length = None):
        if max_length is not None and length > max_length:
            length = max_length
        try:
            if mode not in ["min", "max"]:
                raise ModeError(mode)
            if mode == 'max':
                arr = np.zeros(len(length))
                self.abs = arr + self.abs
                self.rel = arr + self.rel
            else:
                self.abs = self.abs[0:length]
                self.rel = self.rel[0:length]
        except ModeError as e:
            print(e.message)

    @staticmethod
    def angle_abs(joint_dist_x, joint_dist_y, joint_prox_x, joint_prox_y):
        """trouve l'angle abs entre deux points (x,y) a l'aide de arctan2 en degree"""
        return np.rad2deg(np.arctan2(joint_dist_y - joint_prox_y, joint_dist_x - joint_prox_x))

    @staticmethod
    def get_mid_dist_array(ankle_l, ankle_r):
        left = ankle_l.x_arr
        right = ankle_r.x_arr
        mid_dist = (left + right) / 2
        return mid_dist

    @staticmethod
    def angle_btw_2_v(v1_joint_prox, v1_joint_dist, v2_joint_prox, v2_joint_dist):
        n = v1_joint_dist.size
        angle = []
        for i in range(0, n):
            v1_x = v1_joint_dist.x_arr[i] - v1_joint_prox.x_arr[i]
            v1_y = v1_joint_dist.y_arr[i] - v1_joint_prox.y_arr[i]
            v1 = np.array([v1_x, v1_y])

            v2_x = v2_joint_dist.x_arr[i] - v2_joint_prox.x_arr[i]
            v2_y = v2_joint_dist.y_arr[i] - v2_joint_prox.y_arr[i]
            v2 = np.array([v1_x, v1_y])

        pass


class AngleTrunk(Angle):
    def __init__(self, _c7, _com, teta1):
        abs_ = Angle.angle_abs(_c7.x_arr, _c7.y_arr, _com.x_arr, _com.y_arr)
        rel_temp = abs_-90
        rel = rel_temp - teta1

        # rel = np.empty(len(abs_))
        # rel[:] = np.nan
        #
        # v1x = _com.x_arr - pivot.x_arr
        # v1y = _com.y_arr - pivot.y_arr
        # v2x = _c7.x_arr - _com.x_arr
        # v2y = _c7.y_arr - _com.y_arr
        # for i in range(0, v1x.size):
        #     v1 = np.array([v1x[i], v1y[i]])
        #     v2 = np.array([v2x[i], v2y[i]])
        #     v1_u = self.unit_vector(v1)
        #     v2_u = self.unit_vector(v2)
        #     rel[i] = np.degrees(np.arccos(np.clip(np.dot(v1/np.linalg.norm(v1), v2/np.linalg.norm(v2)), -1.0, 1.0)))

        Angle.__init__(self, rel_temp, rel, name="AngleTrunk")

    def unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)
    def angle_between(self, v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

class AngleLower(Angle):
    def __init__(self, _com, pivot):
        abs_ = Angle.angle_abs(_com.x_arr, _com.y_arr, pivot.x_arr, pivot.y_arr)
        rel = abs_-90

        # print("MEAN LOWER ANGLE : ", rel.mean())
        # if abs(rel.mean()) > 100:
        #     """Je crois qu'il y a un référentiel différent dans l'une des deux versions utilisées dans la collecte"""
        #     rel = rel+180
        Angle.__init__(self, abs_, rel, name="AngleLower")




