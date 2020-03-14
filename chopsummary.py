#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour
la segmentation du mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import numpy as np
import displacement as dsp


class Summary:
    """from a array of data (position or angle) return the summary of the array
    ----------------------------------------
    distance = total distance travel by the jt  (dist += abs(data[i] + data[i-1]))
    range = max - min
    max_vel = max(single_derivative(data))
    max_acc = max(double_derivative(data))"""

    def __init__(self, arr: np.array):
        self.distance = dsp.displacement.get_total_distance(arr)
        self.range = dsp.get_range(arr)
        self.max_vel = dsp.get_max_vel(arr)
        self.max_acc = dsp.get_max_accel(arr)
