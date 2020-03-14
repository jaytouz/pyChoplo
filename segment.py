#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Gère la construction de segment.py """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from basedataclass import BaseDataClass


class Segment(BaseDataClass):
    #TODO change principal variable to dist and prox joint aswell as pos_com. There should be three main array in seg.
    """Structure de donnees pour stocker les donnees des segments"""
    slots = ["x_arr", "y_arr"]

    def __init__(self, name, x=None, y=None, data_type = "Segment", fs=50):
        self.x_arr = x if x is not None else self.x_arr
        self.y_arr = y if y is not None else self.y_arr
        BaseDataClass.__init__(self, name, data_type, fs)

    def __len__(self):
        return len(self.pos_com)

    def __getitem__(self, item):
        if isinstance(item, slice):
            x_arr = self.x_arr[item.start:item.stop]
            y_arr = self.y_arr[item.start:item.stop]
            return Segment(self.name, x=x_arr, y=y_arr)
    #
    # @property
    # def move_id(self):
    #     return self.move_id
    #
    # @move_id.setter
    # def move_id(self, val):
    #     self.move_id = val
    #
    # @move_id.deleter
    # def move_id(self):
    #     self.move_id = None
    #
    # def split(self, start, end, move_id):
    #     """Return a new instance with data[start:end] in abs and rel """
    #     _a = Segment(self.abs[start:end], self.rel[start:end], self.name)
    #     _a.move_id = move_id
    #     return _a

    # def equalise_length(self, length, mode):
    #     try:
    #         if mode not in ["min", "max"]:
    #             raise ModeError(mode)
    #         if mode == 'max':
    #             arr = np.zeros(len(length))
    #             self.abs = arr + self.abs
    #             self.rel = arr + self.rel
    #         else:
    #             self.abs = self.abs[0:length]
    #             self.rel = self.rel[0:length]
    #     except ModeError as e:
    #         print(e.message)


class TotalLeg(Segment):
    mass_coeff = 0.161
    prox_coeff = 0.447
    dist_coeff = 0.553

    def __init__(self, joint_prox, joint_dist, side, name="_TotalLeg", ref='prox'):
        name = side + name

        self.length = joint_dist-joint_prox
        pos_coeff = TotalLeg.prox_coeff if ref == 'prox' else TotalLeg.dist_coeff
        self.pos_com = joint_prox + (self.length*pos_coeff)
        self.mass_coeff = TotalLeg.mass_coeff
        self.x_arr = self.pos_com.x_arr
        self.y_arr = self.pos_com.y_arr
        Segment.__init__(self, name)

class HAT(Segment):
    mass_coeff = 0.678
    prox_coeff = 0.626
    dist_coeff = 0.374

    def __init__(self, joint_prox, joint_dist, name="HAT", ref='prox'):
        self.length = joint_dist-joint_prox
        pos_coeff = HAT.prox_coeff if ref == 'prox' else HAT.dist_coeff
        self.pos_com = joint_prox + (self.length*pos_coeff)
        self.mass_coeff = HAT.mass_coeff

        self.x_arr = self.pos_com.x_arr
        self.y_arr = self.pos_com.y_arr
        Segment.__init__(self, name)