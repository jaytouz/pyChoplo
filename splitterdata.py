#!/usr/bin/python
# -*- coding: utf-8 -*-

"""POUR AMELIORER CES CLASSES, IL FAUDRAIT UTILISER LE CONCEPT D'HERITAGE.
IL Y A BEAUCOUP DE CHOSES COMMUNES ENTRE CES CLASSES """


# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


class SplitterInfo:
    def __init__(self, drop_in, vasque_start):
        """
        dropIn: array
        vasqueStart: array
         """
        self.vasque_start = vasque_start
        self.drop_in = drop_in

    def __len__(self):
        return len(self.vasque)

    @property
    def vasque(self):
        return self.vasque_start

    @vasque.setter
    def vasque(self, arr):
        self.vasque_start = arr

    @vasque.deleter
    def vasque(self):
        self.vasque_start = None

    @property
    def drop(self):
        return self.drop_in

    @drop.setter
    def drop(self, arr):
        self.drop_in = arr

    @drop.deleter
    def drop(self):
        self.drop_in = None
