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


class GammaAngle(BaseDataClass):
    slots = ["gamma"]

    def __init__(self, teta1=None, teta2=None, gamma = None, name="gamma", data_type="gamma", fs=50):
        BaseDataClass.__init__(self, name, data_type, fs)
        if gamma is not None:
            self.gamma = gamma
        else:
            if teta1 is not None and teta2 is not None:
                self.calculate_gamma(teta1, teta2)
            else:
                self.gamma = None

    def __len__(self):
        return len(self.gamma)

    def __getitem__(self, item):
        if isinstance(item, slice):
            data = self.gamma[item.start:item.stop]
            return GammaAngle(gamma=data)
        else:
            return self
    @staticmethod
    def calculate_gamma(teta1, teta2):
        """based on research methods in biomechanics page 311"""
        gamma = np.rad2deg(np.arctan2(teta2, teta1)) # defini de -180 a 180
        gamma = np.where(gamma <0, gamma+360, gamma) #defini de 0 a 360

        return gamma



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
                self.gamma = arr + self.gamma
            else:
                self.gamma = self.gamma[0:length]
        except ModeError as e:
            print(e.message)

    @classmethod
    def from_moves(cls, moves, norm = False):
        def add_arr(a1,a2):
            if len(a1) < len(a2):
                c = a2.copy()
                c[:len(a1)] += a1
            else:
                c = a1.copy()
                c[:len(a2)] += a2
            return c

        n = len(moves)

        x = np.zeros(1)
        y = np.zeros(1)
        for m in moves:
            gamma = cls.calculate_gamma(m.angle_lower.rel_arr, m.angle_trunk.rel_arr)
            m.gamma = gamma
            xi = np.cos(np.deg2rad(gamma))
            x = add_arr(x,xi)

            yi = np.sin(np.deg2rad(gamma))
            y = add_arr(y,yi)

        x /= n
        y /= n

        gamma = np.rad2deg(np.arctan2(y, x)) # defini de -180 a 180
        gamma = np.where(gamma <0, gamma+360, gamma) #defini de 0 a 360

        return GammaAngle(gamma = gamma)

    def plot_gamma(self):
        import matplotlib.pyplot as plt

        bin_size = 5
        degrees = self.gamma
        a , b=np.histogram(degrees, bins=np.arange(0, 360+bin_size, bin_size))
        centers = np.deg2rad(np.ediff1d(b)//2 + b[:-1])

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='polar')
        ax.bar(centers, a, width=np.deg2rad(bin_size), bottom=0.0, color='.8', edgecolor='k')
        ax.set_theta_zero_location("E")
        ax.set_theta_direction(1)
        plt.show()

    def plot(self):
        import matplotlib.pyplot as plt

        ax = plt.subplot()
        time = np.linspace(0,100,len(self.gamma))
        ax.scatter(time, self.gamma)







