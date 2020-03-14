#!/usr/bin/python
# -*- coding: utf-8 -*-

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import numpy as np

def derive(p2, p1, t2, t1):
    """ derive la position pour avoir la vitesse"""
    return (p2 - p1) / (t2 - t1)


def get_derivative(y, fs=50):
    """ derive relative to time ((p2-p1)/(t2-t1))"""
    y = np.array(y)
    der = np.diff(y)
    return der


def get_total_distance(arr: np.array):
    dist = 0
    for i in range(1, len(arr)):
        dist += abs(arr[i] - arr[i - 1])
    return dist


def get_range(arr: np.array):
    min_val = arr.min()
    max_val = arr.max()
    return min_val - max_val


def get_max_vel(data):
    pos = data
    vel = np.array(np.diff(pos))
    max_vel = vel.max()
    return max_vel


def get_max_acc(data):
    """from pos in fct of time """
    pos = data
    vel = np.array(np.diff(pos))
    acc = np.array(np.diff(vel))
    acc_max = acc.max()
    return acc_max
