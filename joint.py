#!/usr/bin/python
# -*- coding: utf-8 -*-
"""POUR AMELIORER CES CLASSES, IL FAUDRAIT UTILISER LE CONCEPT D'HERITAGE.
IL Y A BEAUCOUP DE CHOSES COMMUNES ENTRE CES CLASSES """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


import numpy as np
import matplotlib.pyplot as plt

from copy import deepcopy
from error import ModeError
from basedataclass import BaseDataClass


class Joint(BaseDataClass):
    """Structure de donnees pour les joints de kinect """

    slots = ["x_arr", "y_arr"] #, "vel_x", "vel_y", "accel_x", "accel_y"]

    def __init__(self, x, y, name, data_type='Joint', fs=50):
        self.vel_x = None
        self.vel_y = None
        self.accel_x = None
        self.accel_y = None
        if x is not None:
            self.x_arr = np.array(x)
            # self.add_vel()
            # self.add_accel()
        else:
            self.x_arr = np.array([])

        if y is not None:
            self.y_arr = np.array(y)
            # self.add_vel(axis='y')
            # self.add_accel(axis='y')

        else:
            self.y_arr = np.empty(len(self.x_arr))
            self.y_arr[:] = np.nan

        BaseDataClass.__init__(self, name, data_type, fs)

    def __len__(self):
        return len(self.x_arr)

    def __sub__(self, other):
        if type(other) == type(self):
            x_arr = self.x_arr - other.x_arr
            y_arr = self.y_arr - other.y_arr
        else:
            x_arr = self.x_arr - other
            y_arr = self.y_arr - other
        return Joint(x_arr, y_arr, self.name)

    def __add__(self, other):
        if type(other) == type(self):
            x_arr = self.x_arr + other.x_arr
            y_arr = self.y_arr + other.y_arr
        else:
            x_arr = self.x_arr + other
            y_arr = self.y_arr + other
        return Joint(x_arr, y_arr, self.name)

    def __mul__(self, other):
        if type(other) == type(self):
            x_arr = self.x_arr * other.x_arr
            y_arr = self.y_arr * other.y_arr
        else:
            x_arr = self.x_arr * other
            y_arr = self.y_arr * other
        return Joint(x_arr, y_arr, self.name)

    def __divmod__(self, other):
        if type(other) == type(self):
            x_arr = self.x_arr / other.x_arr
            y_arr = self.y_arr / other.y_arr
        else:
            x_arr = self.x_arr / other
            y_arr = self.y_arr / other

        return Joint(x_arr, y_arr, self.name)


    def __getitem__(self, item):
        if isinstance(item, slice):
            x_arr = None
            y_arr = None
            if self.x_arr is not None:
                x_arr = self.x_arr[item.start:item.stop]
            if self.y_arr is not None:
                y_arr = self.y_arr[item.start:item.stop]
            return Joint(x_arr, y_arr, self.name)

    def equalise_length(self, length, mode, max_length = None):
        if max_length is not None and length > max_length:
            length = max_length
        try:
            if mode not in ["min", "max"]:
                raise ModeError(mode)
            if mode == 'max':
                arr = np.zeros(len(length))
                self.x_arr = arr + self.x_arr
                self.y_arr = arr + self.y_arr
                # if self.vel_x is None or self.vel_y is None:
                #     self.add_vel()
                #     self.add_accel()
                #     self.add_vel(axis='y')
                #     self.add_accel(axis='y')

            else:
                self.x_arr = self.x_arr[0:length]
                self.y_arr = self.y_arr[0:length]
                # if self.vel_x is None or self.vel_y is None:
                #     self.add_vel()
                #     self.add_accel()
                #     self.add_vel(axis='y')
                #     self.add_accel(axis='y')

        except ModeError as e:
            print(e.message)

    def add_vel(self, axis='x'):

        if axis == 'x':
            data = self.x_arr
            self.vel_x = np.diff(deepcopy(data))
            self.vel_x = np.append(self.vel_x, self.vel_x[-1]) #To keep it the same length as x_arr
            # print("vel_x added")
        else:
            data = self.y_arr
            self.vel_y = np.diff(deepcopy(data))
            self.vel_y = np.append(self.vel_y, self.vel_y[-1]) #To keep it the same length as y_arr

            # print("vel_y added")

    def add_accel(self, axis='x'):

        if axis == 'x' and self.vel_x is not None:
            data = self.vel_x
            self.accel_x = np.diff(deepcopy(data))
            self.accel_x = np.append(self.accel_x, self.accel_x[-1]) #To keep it the same length as vel_x

            # print("accel_x added")
        elif axis == 'y' and self.vel_y is not None:
            data = self.vel_y
            self.accel_y = np.diff(deepcopy(data))
            self.accel_y = np.append(self.accel_y, self.accel_y[-1]) #To keep it the same length as vel_y

            # print("accel_y added")
        else:
            print("no accel added, maybe self.vel_x or self.vel_y is None")

    def plot_vel(self, axis='x', with_pos=True):
        if axis == 'x':
            pos = self.x_arr
            vel = self.vel_x
        else:
            pos = self.y_arr
            vel = self.vel_y

        ax = plt.subplot()
        ax.plot(vel, color='b', label="{} - {} - vel".format(self.data_type, self.name))
        if with_pos:
            ax.plot(pos, color='k', label="{} - {} - pos".format(self.data_type, self.name))

        ax.legend(loc="best")

    def plot_accel(self, axis='x', with_pos=True, with_vel=True):
        if axis == 'x':
            pos = self.x_arr
            vel = self.vel_x
            accel = self.accel_x
        else:
            pos = self.y_arr
            vel = self.vel_y
            accel = self.accel_y

        ax = plt.subplot()
        ax.plot(accel, color='r', label="{} - {} - accel".format(self.data_type, self.name))
        if with_pos:
            ax.plot(pos, color='k', label="{} - {} - pos".format(self.data_type, self.name))
        if with_vel:
            ax.plot(vel, color='b', label="{} - {} - vel".format(self.data_type, self.name))

        ax.legend(loc="best")

    # def transpose_to_ref_pivot(self, pivot):
    #     x_to_p = self.x_arr + (pivot.x_arr - self.x_arr)
    #     y_to_p = self.y_arr + (pivot.y_arr - self.y_arr)
    #     self.x_arr = self.x_arr + x_to_p
    #     self.y_arr = self.y_arr + y_to_p
    #     return deepcopy(self)
