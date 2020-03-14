#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la segmentation du mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import pandas as pd

from droplets import DropletsAdult2017
from player import Player


class PlayerAdult(Player):
    COL_KINECT_2017 = ["TimeOfGame", "DropletAvailable", "VasqueInZone", "wiifit_lat_x", "wiifit_poid_appuis", "ac",
                       "bc", "COF", "pos_ankle_l_x", "pos_ankle_r_x", "pos_COP_k_rel", "angle_voulu", "pos_spine_x",
                       "pos_spine_y", "pos_spine_z", "pos_mid_shoulder_x", "pos_mid_shoulder_y", "pos_mid_shoulder_z",
                       "FootLeft_x", "FootLeft_y", "FootLeft_z", "FootRight_x", "FootRight_y", "FootRight_z",
                       "AnkleLeft_x", "AnkleLeft_y", "AnkleLeft_z", "AnkleRight_x", "AnkleRight_y", "AnkleRight_z",
                       "KneeLeft_x", "KneeLeft_y", "KneeLeft_z", "KneeRight_x", "KneeRight_y", "KneeRight_z",
                       "HipLeft_x", "HipLeft_y", "HipLeft_z", "HipRight_x", "HipRight_y", "HipRight_z", "SpineBase_x",
                       "SpineBase_y", "SpineBase_z", "SpineMid_x", "SpineMid_y", "SpineMid_z", "SpineShoulder_x",
                       "SpineShoulder_y", "SpineShoulder_z", "ShoulderLeft_x", "ShoulderLeft_y", "ShoulderLeft_z",
                       "ShoulderRight_x", "ShoulderRight_y", "ShoulderRight_z", "ElbowLeft_x", "ElbowLeft_y",
                       "ElbowLeft_z", "ElbowRight_x", "ElbowRight_y", "ElbowRight_z", "WristLeft_x", "WristLeft_y",
                       "WristLeft_z", "WristRight_x", "WristRight_y", "WristRight_z", "HandLeft_x", "HandLeft_y",
                       "HandLeft_z", "HandRight_x", "HandRight_y", "HandRight_z", "ThumbLeft_x", "ThumbLeft_y",
                       "ThumbLeft_z", "ThumbRight_x", "ThumbRight_y", "ThumbRight_z", "HandTipLeft_x", "HandTipLeft_y",
                       "HandTipLeft_z", "HandTipRight_x", "HandTipRight_y", "HandTipRight_z", "Neck_x", "Neck_y",
                       "Neck_z", "Head_x", "Head_y", "Head_z", "ScoreManager_score_joueur",
                       "ScoreManager_nbrGouttesGauche", "ScoreManager_nbrGouttesDroite"]

    def __init__(self, path_adult):
        print("PlayerAdult init")

        droplets = DropletsAdult2017(path_adult.condition, path_adult.repetition)
        self._raw = self.load_raw_data(path_adult)
        Player.__init__(self, self.raw, droplets, path_adult)

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, df):
        return df

    def load_raw_data(self, dir_):
        df = pd.read_csv(dir_.path, sep=' ', header=None, names=self.COL_KINECT_2017)
        df.rename(columns={'pos_spine_x': 'COM', "pos_mid_shoulder_x": "C7"}, inplace=True)
        df.rename(columns={'pos_spine_y': 'COM_y', "pos_mid_shoulder_y": "C7_y"}, inplace=True)
        df.rename(columns={'pos_COP_k_rel': 'COF_REL'}, inplace=True)
        df.rename(columns={'pos_ankle_l_x': 'ankle_l', 'pos_ankle_r_x': 'ankle_r'}, inplace=True)
        df.rename(columns={'AnkleLeft_z': 'ankle_l_y', 'AnkleRight_z': 'ankle_r_y'}, inplace=True) #IL Y A UN DÉCALAGE DANS LES DONNÉES DE SORTIE ATTENTION. JE CROIS AVOIR TROUVER LE BON Y APRÈS UNE JOURNÉE DE VISUALISATION DES DONNÉES.... JE CROIS QUE CEST CORRIGÉ POUR LES DONNÉES D'ENFANTS, LE PROBLÈME EST DANS LA VERSION UTILISÉE DU JEU PAS DANS CE SCRIPT

        df.rename(columns={"DropletAvailable": "DropIn", "VasqueInZone": "VasqueStart"}, inplace=True)
        return df
