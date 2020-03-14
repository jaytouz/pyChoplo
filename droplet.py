#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la segmentation du mouvement selon 5 différents GAMEMODE """


# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


class Droplet(object):
    """format de données qui sera utilisé dans l'analyse."""
    num_droplets = 0

    def __init__(self, amp_val=None, vit_val=None, rep=None, sound_delay_val=None, time_val=None):
        self._amp = amp_val
        self._vit = vit_val
        self._rep = rep
        self._sound_delay = sound_delay_val
        self._time = time_val
        self.droplet_id = Droplet.num_droplets
        Droplet.num_droplets += 1


    @property
    def rep(self):
        return self._rep

    @rep.setter
    def rep(self, val):
        self._rep = val

    @property
    def amp(self):
        return self._amp

    @amp.setter
    def amp(self, val):
        self._amp = val

    @amp.deleter
    def amp(self):
        self._amp = None

    @property
    def vit(self):
        return self._vit

    @vit.setter
    def vit(self, val):
        self._vit = val

    @vit.deleter
    def vit(self):
        self._vit = None

    @property
    def sound_delay(self):
        return self._sound_delay

    @sound_delay.setter
    def sound_delay(self, val):
        self._sound_delay = val

    @sound_delay.deleter
    def sound_delay(self):
        self._sound_delay = None

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, val):
        self._time = val

    @time.deleter
    def time(self):
        self._time = None
