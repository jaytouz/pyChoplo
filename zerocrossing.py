#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Les classes de choppath permet de gerer le chemin vers les données d'intérêts """


# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


def find_zero_crossing(arr, start_pos=0, forward=True):
    """finds all the zero crossing event in the signal

    :parameter

    arr: np.array, data of interest
    forward : Bool, direction of the window
    start_pos : Int, index to start from, 0 if not specified

    :return

    zc : np.array, indices of the zero crossing event
    """

    zero_cross_index = []

    if forward:
        for i in range(start_pos+1, len(arr)):
            last = arr[i-1]
            current = arr[i]

            if last < 0 and current > 0:
                zero_cross_index.append(i)

            elif last > 0 and current < 0:
                zero_cross_index.append(i)

            elif current == 0:
                zero_cross_index.append(i)

    else:
        for i in range(start_pos-1, 0, -1):
            last = arr[i]
            current = arr[i-1]

            #TODO Verifier si la logique est aussi bonne en backward, j'ai seulement copy paste forward.
            if last < 0 and current >= 0:
                #ascendent
                zero_cross_index.append(i)

            elif last > 0 and current <= 0:
                #descendent
                zero_cross_index.append(i)

    return zero_cross_index


