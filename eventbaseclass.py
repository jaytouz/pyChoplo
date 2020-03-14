#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires
 pour la segmentation du mouvement selon 5 différents GAMEMODE """

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import matplotlib.pyplot as plt


class Event:
    def __init__(self, data, index, full_name=None):
        self.full_name = full_name

        self.index = index
        self.data = data
        self.val = data[index]

    def plot(self, color='k', patch_name=['X']):
        from plot import add_patch
        ax = plt.subplot()
        ax.plot(self.data, color=color, label=self.full_name)
        add_patch(ax, self.index, self.val, patch_name[0])
        ax.legend(loc="best")


