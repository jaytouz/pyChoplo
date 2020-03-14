# !/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la segmentation du mouvement selon 5 différents GAMEMODE """


# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


class ModeError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the choploerror occurred
        message -- explanation of the choploerror
    """

    def __init__(self, mode):
        self.message = "{} : is not a valid input for mode... use 'min' or 'max'".format(mode)
