#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Caclul du centre de masse a  """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import numpy as np
from joint import Joint
from copy import deepcopy
import matplotlib.pyplot as plt


from error import ModeError
from basedataclass import BaseDataClass


class CenterOfMasse(Joint):
    """Structure de donnees pour calculer et stocker le centre de masse"""

    slots = ["x_arr", "y_arr"]
    def __init__(self, name, segments:list = [], x=None, y = None, data_type='CenterOfMasse', fs=50):
        """segment.py is composed of left_leg, right_leg and HAT"""
        nb_seg = len(segments)
        nb = len(segments[0]) if x is None else len(x)

        if len(segments)>=1:
            com = Joint(np.zeros(nb), np.zeros(nb), "COM")
            for s in segments:
                com += s.pos_com * s.mass_coeff
            com.x_arr/=nb_seg
            com.y_arr/=nb_seg

        self.x_arr = com.x_arr if x is None else x
        self.y_arr = com.y_arr if y is None else y

        BaseDataClass.__init__(self, name, data_type, fs)

    def __len__(self):
        return len(self.abs_arr)

    def __getitem__(self, item):
        if isinstance(item, slice):
            y = self.x_arr[item.start:item.stop]
            x = self.y_arr[item.start:item.stop]
            return CenterOfMasse(self.name, x=x, y=y)

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
        """Return a new instance with data[start:end] """
        _com = CenterOfMasse(self.name, x=self.x_arr[start:end], y=self.y_arr[start:end])
        _com.move_id = move_id
        return _com

    def equalise_length(self, length, mode, max_length = None):
        if max_length is not None and length > max_length:
            length = max_length
        try:
            if mode not in ["min", "max"]:
                raise ModeError(mode)
            if mode == 'max':
                arr = np.zeros(len(length))
                self.x_arr = arr + self.x_arr
                self.y_arr= arr + self.y_arr
            else:
                self.x_arr = self.x_arr[0:length]
                self.y_arr = self.y_arr[0:length]
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

    @classmethod
    def from_com(cls, x, y):
        return CenterOfMasse("COM", x=x, y=y)


    def to_joint(self):
        return Joint(self.x_arr,self.y_arr,"COM")
