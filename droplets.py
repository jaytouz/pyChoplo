#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour
la segmentation du mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


from droplet import Droplet


class Droplets(list):
    def __init__(self, lst_g):
        # print("Droplets list INIT")
        Droplet.num_droplets = 0
        self._droplets = lst_g

    def __len__(self):
        return len(self._droplets)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self):
            output = self._droplets[self.i]
            self.i += 1
            return output
        else:
            raise StopIteration

    def __getitem__(self, key):
        # print(key)
        return self._droplets[key]

    def __setitem__(self, key, item):
        if isinstance(item, Droplet):
            self._droplets[key] = item
            # print(len(self), "update")
        else:
            raise TypeError("Item must be Droplet")

    def append(self, item):
        if isinstance(item, Droplet):
            self._droplets.append(item)
            # print(len(self), "update")
        else:
            raise TypeError("Item must be Droplet")

    def __repr__(self):
        lst_droplets = []
        for g in self._droplets:
            lst_droplets.append("g{}".format(g.droplet_id))
        return "Droplets({})".format(str(lst_droplets))

    def __str__(self):
        lst_droplets = []
        for g in self._droplets:
            lst_droplets.append("g{}".format(g.Droplet_id))
        return "Droplets({})".format(str(lst_droplets))


class DropletsAdult2017(Droplets):
    # ADULT_2017
    rand_adult_2017 = {
        'time': [5.0, 19.25, 33.5, 47.75, 62.0, 76.25, 90.5, 104.8, 119.0, 133.2, 147.5, 161.8, 176.0, 190.2, 204.5,
                 218.8, 233.0, 247.2, 261.5, 275.8, 290.0, 304.2, 318.5, 332.8, 347.0, 361.2, 375.5, 389.8, 404.0,
                 418.2],
        'amp': [-0.25, -0.25, 0.25, -0.25, -0.25, 0.25, 0.25, -0.25, 0.25, -0.25, 0.25, 0.25, -0.25, -0.25, 0.25, 0.25,
                0.25, 0.25, 0.25, 0.25, -0.25, 0.25, -0.25, -0.25, 0.25, -0.25, 0.25, -0.25, -0.25, -0.25],
        'vit': [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
                0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        'rep': ['rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand',
                'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand',
                'rand', 'rand', 'rand', 'rand']}

    amp_lvl1_adult_2017 = {
        'time': [5.0, 19.25, 33.5, 47.75, 62.0, 76.25, 90.5, 104.8, 119.0, 133.2, 147.5, 161.8, 176.0, 190.2, 204.5,
                 218.8, 233.0, 247.2, 261.5, 275.8, 290.0, 304.2, 318.5, 332.8, 347.0, 361.2, 375.5, 389.8, 404.0,
                 418.2],
        'amp': [-0.25, -0.25, 0.25, -0.25, -0.25, 0.25, 0.25, -0.25, 0.25, -0.25, 0.25, 0.25, -0.25, -0.25, 0.25, 0.25,
                0.25, 0.25, 0.25, 0.25, -0.25, 0.25, -0.25, -0.25, 0.25, -0.25, 0.25, -0.25, -0.25, -0.25],
        'vit': [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
                0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        'rep': ['amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1',
                'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1', 'amp1',
                'amp1', 'amp1', 'amp1', 'amp1']}

    amp_lvl2_adult_2017 = {
        'time': [5.0, 19.25, 33.5, 47.75, 62.0, 76.25, 90.5, 104.8, 119.0, 133.2, 147.5, 161.8, 176.0, 190.2, 204.5,
                 218.8, 233.0, 247.2, 261.5, 275.8, 290.0, 304.2, 318.5, 332.8, 347.0, 361.2, 375.5, 389.8, 404.0,
                 418.2],
        'amp': [0.5, -0.5, -0.5, 0.5, 0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5, 0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5,
                -0.5, -0.5, -0.5, -0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5, -0.5],
        'vit': [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
                0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        'rep': ['amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2',
                'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2', 'amp2',
                'amp2', 'amp2', 'amp2', 'amp2']}

    amp_lvl3_adult_2017 = {
        'time': [5.0, 19.25, 33.5, 47.75, 62.0, 76.25, 90.5, 104.8, 119.0, 133.2, 147.5, 161.8, 176.0, 190.2, 204.5,
                 218.8, 233.0, 247.2, 261.5, 275.8, 290.0, 304.2, 318.5, 332.8, 347.0, 361.2, 375.5, 389.8, 404.0,
                 418.2],
        'amp': [-0.75, -0.75, 0.75, 0.75, -0.75, 0.75, -0.75, -0.75, -0.75, 0.75, -0.75, -0.75, 0.75, 0.75, 0.75, 0.75,
                0.75, -0.75, -0.75, 0.75, -0.75, -0.75, 0.75, -0.75, 0.75, 0.75, 0.75, 0.75, -0.75, -0.75],
        'vit': [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
                0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        'rep': ['amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3',
                'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3', 'amp3',
                'amp3', 'amp3', 'amp3', 'amp3']}

    amp_lvl4_adult_2017 = {
        'time': [5.0, 19.25, 33.5, 47.75, 62.0, 76.25, 90.5, 104.8, 119.0, 133.2, 147.5, 161.8, 176.0, 190.2, 204.5,
                 218.8, 233.0, 247.2, 261.5, 275.8, 290.0, 304.2, 318.5, 332.8, 347.0, 361.2, 375.5, 389.8, 404.0,
                 418.2],
        'amp': [-1, 1, -1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1,
                -1],
        'vit': [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
                0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        'rep': ['amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4',
                'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4', 'amp4',
                'amp4', 'amp4', 'amp4', 'amp4']}

    vit_lvl1_adult_2017 = {
        'time': [5.0, 15.42, 25.84, 36.27, 46.69, 57.11, 67.53, 77.96, 88.38, 98.8, 109.2, 119.6, 130.1, 140.5, 150.9,
                 161.3, 171.8, 182.2, 192.6, 203.0, 213.4, 223.9, 234.3, 244.7, 255.1, 265.6, 276.0, 286.4, 296.8,
                 307.2],
        'amp': [0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5, -0.5,
                0.5, 0.5, -0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5],
        'vit': [0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062,
                0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062,
                0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062, 0.014062],
        'rep': ['vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1',
                'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1', 'vit1',
                'vit1', 'vit1', 'vit1', 'vit1']}

    vit_lvl2_adult_2017 = {
        'time': [5.0, 12.87, 20.75, 28.62, 36.5, 44.37, 52.24, 60.12, 67.99, 75.87, 83.74, 91.61, 99.49, 107.4, 115.2,
                 123.1, 131.0, 138.9, 146.7, 154.6, 162.5, 170.4, 178.2, 186.1, 194.0, 201.8, 209.7, 217.6, 225.5,
                 233.3],
        'amp': [0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5, -0.5,
                0.5, 0.5, -0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5],
        'vit': [0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193,
                0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193, 0.0193,
                0.0193, 0.0193, 0.0193, 0.0193],
        'rep': ['vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2',
                'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2', 'vit2',
                'vit2', 'vit2', 'vit2', 'vit2']}

    vit_lvl3_adult_2017 = {
        'time': [5.0, 11.73, 18.45, 25.18, 31.91, 38.63, 45.36, 52.09, 58.81, 65.54, 72.27, 78.99, 85.72, 92.45, 99.17,
                 105.9, 112.6, 119.4, 126.1, 132.8, 139.5, 146.3, 153.0, 159.7, 166.4, 173.2, 179.9, 186.6, 193.3,
                 200.1],
        'amp': [0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5, -0.5,
                0.5, 0.5, -0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5],
        'vit': [0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137,
                0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137,
                0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137],
        'rep': ['vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3',
                'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3', 'vit3',
                'vit3', 'vit3', 'vit3', 'vit3']}

    vit_lvl4_adult_2017 = {
        'time': [5.0, 11.73, 18.45, 25.18, 31.91, 38.63, 45.36, 52.09, 58.81, 65.54, 72.27, 78.99, 85.72, 92.45, 99.17,
                 105.9, 112.6, 119.4, 126.1, 132.8, 139.5, 146.3, 153.0, 159.7, 166.4, 173.2, 179.9, 186.6, 193.3,
                 200.1],
        'amp': [0.5, -0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5, -0.5, 0.5, -0.5, 0.5, -0.5, -0.5,
                0.5, 0.5, -0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5],
        'vit': [0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137,
                0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137,
                0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137, 0.023137],
        'rep': ['vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4',
                'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4', 'vit4',
                'vit4', 'vit4', 'vit4', 'vit4']}

    def __init__(self, c, r):
        dict_g = self.get_dict_g(c, r)
        lst_g = self.dict_to_drop(dict_g)
        Droplets.__init__(self, lst_g)

    def get_dict_g(self, c, r):
        dict_g = {}
        if c == "amp":
            if r == 1:
                dict_g = self.amp_lvl1_adult_2017
            elif r == 2:
                dict_g = self.amp_lvl2_adult_2017
            elif r == 3:
                dict_g = self.amp_lvl3_adult_2017
            elif r == 4:
                dict_g = self.amp_lvl4_adult_2017

        elif c == "vit":
            if r == 1:
                dict_g = self.vit_lvl1_adult_2017
            elif r == 2:
                dict_g = self.vit_lvl2_adult_2017
            elif r == 3:
                dict_g = self.vit_lvl3_adult_2017
            elif r == 4:
                dict_g = self.vit_lvl4_adult_2017

        elif c == "rand":
            dict_g = self.rand_adult_2017

        return dict_g

    def dict_to_drop(self, dict_of_droplets):
        """Convertion du dict en haut en un format Droplet.
         C'est la classe Droplet qui sera intégré dans les analyses."""
        lst_g = []
        N = len(dict_of_droplets['amp'])  # length of all key are equal
        for i in range(0, N):
            lst_g.append(Droplet(amp_val=dict_of_droplets["amp"][i], vit_val=dict_of_droplets["vit"][i],
                                 time_val=dict_of_droplets['time'][i], rep=dict_of_droplets['rep'][i]))
        return lst_g


class DropletsChildTD(Droplets):
    # 2017-2018
    rand_TD_2017 = {"amp": [-0.3516, -0.4892, 0.2748, 0.5, -0.4335, 0.9, -0.7, 0.3529, -0.6, 1, -1],
                    "vit": [0.93132, 0.50624, 0.96377, 0.87672, 0.73371, 0.79868, 0.63417, 0.98468, 0.97282, 0.97282,
                            0.97282],
                    'rep':['rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand', 'rand']}

    amp_TD_2017 = {"amp": [-0.5, -0.75, -0.25, 0.5, 0.5, -0.75, 0.25, 0.75, 1, -0.25, 1, 0.25, -1, -1, 0.75, -0.5],
                   "vit": [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6],
                   'rep': ['amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp', 'amp']}

    vit_TD_2017 = {
        "amp": [-0.45, 0.45, -0.45, -0.45, 0.45, 0.45, -0.45, 0.45, 0.45, -0.45, -0.45, -0.45, 0.45, -0.45, 0.45, 0.45],
        "vit": [1.125, 1.125, 0.6, 0.75, 0.75, 1.125, 0.6, 0.75, 1.125, 0.6, 0.75, 1.5, 1.5, 0.75, 0.6, 1.125, 1.5, 1.5,
                0.6],
        'rep': ['vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit', 'vit',
                'vit']}

    def __init__(self, c):
        dict_g = self.get_dict_g(c)
        lst_g = self.dict_to_drop(dict_g)
        Droplets.__init__(self, lst_g)

    def get_dict_g(self, c):
        dict_g = {}
        if c == "amp":
            dict_g = self.amp_TD_2017
        elif c == "vit":
            dict_g = self.vit_TD_2017
        elif c == "rand":
            dict_g = self.rand_TD_2017
        return dict_g

    def dict_to_drop(self, dict_of_droplets):
        """Convertion du dict en haut en un format Droplet.
         C'est la classe Droplet qui sera intégré dans les analyses."""
        lst_g = []
        N = len(dict_of_droplets['amp'])  # length of all key are equal
        for i in range(0, N):
            lst_g.append(Droplet(amp_val=dict_of_droplets["amp"][i], vit_val=dict_of_droplets["vit"][i]))
        return lst_g


class DropletsCpVd2017(Droplets):
    rand_VD_2017 = {"amp": [-0.3516, -0.4892, 0.2748, 0.5, -0.4335, 0.9, -0.7, 0.3529, -0.6, 1, -1],
                    "vit": [0.93132, 0.50624, 0.96377, 0.87672, 0.73371, 0.79868, 0.63417, 0.98468, 0.97282, 0.97282,
                            0.97282]}

    amp_VD_2017 = {"amp": [-0.5, -0.75, -0.25, 0.5, 0.5, -0.75, 0.25, 0.75, 1, -0.25, 1, 0.25, -1, -1, 0.75, -0.5],
                   "vit": [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]}

    def __init__(self, c):
        dict_g = self.get_dict_g(c)
        lst_g = self.dict_to_drop(dict_g)
        Droplets.__init__(self, lst_g)

    def get_dict_g(self, c):
        dict_g = {}
        if c == "Amplitude":
            dict_g = self.amp_VD_2017

        elif c == "Random":
            dict_g = self.rand_VD_2017
        return dict_g

    def dict_to_drop(self, dict_of_droplets):
        """Convertion du dict en haut en un format Droplet.
         C'est la classe Droplet qui sera intégré dans les analyses."""
        lst_g = []
        N = len(dict_of_droplets['amp'])  # length of all key are equal
        for i in range(0, N):
            lst_g.append(Droplet(amp_val=dict_of_droplets["amp"][i], vit_val=dict_of_droplets["vit"][i]))
        return lst_g


class DropletsCpJcEval(Droplets):
    # Choplo evaluation Joseph-Charbonneau CP 2018 Hiv
    rand_JC = {'amp': [-0.3516, -0.4892, 0.2748, 0.5, -0.4335, 0.9, -0.7, 0.3529, -0.6, 1, -1],
               'vit': [0.93132, 0.50624, 0.96377, 0.87672, 0.73371, 0.79868, 0.63417, 0.98468, 0.97282, 0.97282,
                       0.97282]}
    amp_JC = {'amp': [0, -0.25, 0.25, -0.5, 0.5, -0.75, 0.75, 1, -1], 'vit': [1, 1, 1, 1, 1, 1, 1, 1, 1]}

    def __init__(self, c):
        dict_g = self.get_dict_g(c)
        lst_g = self.dict_to_drop(dict_g)
        Droplets.__init__(self, lst_g)

    def get_dict_g(self, c):
        dict_g = {}
        if c == "amp":
            dict_g = self.amp_JC
        elif c == "rand":
            dict_g = self.rand_JC
        return dict_g

    def dict_to_drop(self, dict_of_droplets):
        """Convertion du dict en haut en un format Droplet.
         C'est la classe Droplet qui sera intégré dans les analyses."""
        lst_g = []
        N = len(dict_of_droplets["amp"])  # length of all key are equal
        for i in range(0, N):
            lst_g.append(Droplet(amp_val=dict_of_droplets["amp"][i], vit_val=dict_of_droplets["vit"][i]))
        return lst_g


class DropletsCpJcMultiSenso(Droplets):
    # MultiSenso Joseph-Charbonneau CP 2018 Hiv
    """sound_delay = 999 : No Sounds, sound_delay = 0 : Sounds with 0 ms delay (in theory...)"""
    V_VA_rep1 = {'amp': [0.5, 0.5, -0.5, -0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5],
                 'sound_delay': [999, 0, 0, 999, 999, 0, 999, 999, 0, 999, 0, 0],
                 'rep': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
    V_VA_rep2 = {'amp': [-0.5, 0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, -0.5, 0.5],
                 'sound_delay': [999, 0, 0, 999, 999, 999, 0, 999, 0, 999, 0, 0],
                 'rep': [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]}
    V_VA_rep3 = {'amp': [0.5, 0.5, -0.5, -0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5],
                 'sound_delay': [999, 0, 0, 999, 999, 0, 999, 999, 0, 999, 0, 0],
                 'rep': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]}
    V_VA_rep4 = {'amp': [-0.5, 0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, -0.5, 0.5],
                 'sound_delay': [999, 0, 0, 999, 999, 999, 0, 999, 0, 999, 0, 0],
                 'rep': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]}

    def __init__(self, r):
        dict_g = self.get_dict_g(r)
        lst_g = self.dict_to_drop(dict_g)
        Droplets.__init__(self, lst_g)

    def get_dict_g(self, r):
        dict_g = {}
        if r == 1:
            dict_g = self.V_VA_rep1
        elif r == 2:
            dict_g = self.V_VA_rep2
        elif r == 3:
            dict_g = self.V_VA_rep3
        elif r == 4:
            dict_g = self.V_VA_rep4
        return dict_g

    def dict_to_drop(self, dict_of_droplets):
        """Convertion du dict en haut en un format Droplet.
         C'est la classe Droplet qui sera intégré dans les analyses."""
        lst_g = []
        N = len(dict_of_droplets["amp"])  # length of all key are equal
        for i in range(0, N):
            lst_g.append(Droplet(amp_val=dict_of_droplets["amp"][i], sound_delay_val=dict_of_droplets["sound_delay"][i],
                                 rep=dict_of_droplets["rep"][i]))
        return lst_g
