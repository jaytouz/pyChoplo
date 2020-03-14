#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la
segmentation du mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import pandas as pd

from droplets import DropletsCpVd2017, DropletsCpJcEval, \
    DropletsCpJcMultiSenso
from player import Player


class PlayerChildVd(Player):
    COL_KINECT_VD_2017 = ["TimeOfGame", "DropletAvailable", "VasqueInZone", "wiifit_lat_x", "wiifit_poid_appuis", "ac",
                          "bc", "COF", "Pos_COP_k_rel", "angle_voulu", "SpineBase_x", "SpineBase_y", "SpineBase_z",
                          "SpineShoulder_x", "SpineShoulder_y", "SpineShoulder_z", "FootLeft_x", "FootLeft_y",
                          "FootLeft_z", "FootRight_x", "FootRight_y", "FootRight_z", "AnkleLeft_x", "AnkleLeft_y",
                          "AnkleLeft_z", "AnkleRight_x", "AnkleRight_y", "AnkleRight_z", "KneeLeft_x", "KneeLeft_y",
                          "KneeLeft_z", "KneeRight_x", "KneeRight_y", "KneeRight_z", "HipLeft_x", "HipLeft_y",
                          "HipLeft_z", "HipRight_x", "HipRight_y", "HipRight_z", "SpineMid_x", "SpineMid_y",
                          "SpineMid_z", "ShoulderLeft_x", "ShoulderLeft_y", "ShoulderLeft_z", "ShoulderRight_x",
                          "ShoulderRight_y", "ShoulderRight_z", "ElbowLeft_x", "ElbowLeft_y", "ElbowLeft_z",
                          "ElbowRight_x", "ElbowRight_y", "ElbowRight_z", "WristLeft_x", "WristLeft_y", "WristLeft_z",
                          "WristRight_x", "WristRight_y", "WristRight_z", "HandLeft_x", "HandLeft_y", "HandLeft_z",
                          "HandRight_x", "HandRight_y", "HandRight_z", "ThumbLeft_x", "ThumbLeft_y", "ThumbLeft_z",
                          "ThumbRight_x", "ThumbRight_y", "ThumbRight_z", "HandTipLeft_x", "HandTipLeft_y",
                          "HandTipLeft_z", "HandTipRight_x", "HandTipRight_y", "HandTipRight_z", "Neck_x", "Neck_y",
                          "Neck_z", "Head_x", "Head_y", "Head_z", "playerScore", "nbrGouttesGauche", "nbrGouttesDroite"]

    def __init__(self, child_vd_path):
        droplets = DropletsCpVd2017(child_vd_path.condition)
        raw = self.load_raw_data(child_vd_path)
        Player.__init__(self, raw, droplets, child_vd_path)

    def load_raw_data(self, dir_):
        df = pd.read_csv(dir_.path, sep=' ', header=None, names=self.COL_KINECT_VD_2017)
        df.rename(columns={'SpineBase_x': 'COM', "SpineShoulder_x": "C7"}, inplace=True)
        df.rename(columns={'SpineBase_y': 'COM_y', "SpineShoulder_y": "C7_y"}, inplace=True)

        df.rename(columns={'AnkleLeft_x': 'ankle_l', 'AnkleRight_x': 'ankle_r'}, inplace=True)
        df.rename(columns={'AnkleLeft_y': 'ankle_l_y', 'AnkleRight_y': 'ankle_r_y'}, inplace=True)

        df.rename(columns={"DropletAvailable": "DropIn", "VasqueInZone": "VasqueStart"}, inplace=True)
        return df


class PlayerCpJcEval(Player):
    def __init__(self, jc_eval_path):
        droplets = DropletsCpJcEval("amp")
        raw = self.load_raw_data(jc_eval_path)
        Player.__init__(self, raw, droplets, jc_eval_path)

    def load_raw_data(self, dir_):
        #TODO change csv output in choplo unity, for now, call correct_format function to correct format

        dir_.data_type = "Kinect"
        dir_.update_path()

        kinect_df = pd.read_csv(dir_.path, sep=' ', header=0)

        dir_.data_type = "Wii"
        dir_.update_path()
        wii_df = pd.read_csv(dir_.path, sep=' ', header=0)

        dir_.data_type = "GameInformation"
        dir_.update_path()
        game_info_df = pd.read_csv(dir_.path, sep=' ', header=0)
        game_info_df["DropletInScreen"] = Player.change_value_in_df(game_info_df, "DropletInScreen", 0, 1)
        game_info_df["DropletInScreen"] = Player.change_value_in_df(game_info_df, "DropletInScreen", '\\N', 0)
        game_info_df["DropletInScreen"] = Player.change_value_in_df(game_info_df, "DropletInScreen", 999, 0)
        df = pd.concat(
            [kinect_df["AnkleLeft_x"], kinect_df["AnkleRight_x"], kinect_df["AnkleLeft_y"], kinect_df["AnkleRight_y"],
             wii_df["Pos_COP_k"], kinect_df["SpineBase_x"], kinect_df["SpineShoulder_x"], kinect_df["SpineBase_y"],
             kinect_df["SpineShoulder_y"], game_info_df["DropletInScreen"], game_info_df["PlayerInCenterZone"]], axis=1)

        df.rename(columns={'AnkleLeft_x': 'ankle_l', 'AnkleRight_x': 'ankle_r'}, inplace=True)
        df.rename(columns={'AnkleLeft_y': 'ankle_l_y', 'AnkleRight_y': 'ankle_r_y'}, inplace=True)
        df.rename(columns={'Pos_COP_k': 'COF', 'SpineBase_x': 'COM', "SpineShoulder_x": "C7"}, inplace=True)
        df.rename(columns={'SpineBase_y': 'COM_y', "SpineShoulder_y": "C7_y"}, inplace=True)
        df.rename(columns={"DropletInScreen": "DropIn", "PlayerInCenterZone": "VasqueStart"}, inplace=True)
        return df


class PlayerCpJcMultiSenso(Player):
    def __init__(self, jc_multi_senso_path):
        droplets = DropletsCpJcMultiSenso(jc_multi_senso_path.repetition)
        raw = self.load_raw_data(jc_multi_senso_path)
        Player.__init__(self, raw, droplets, jc_multi_senso_path)

    def load_raw_data(self, dir_):
        #TODO change csv output in choplo unity, for now, call correct_format function to correct format.py in repo

        dir_.data_type = "Kinect"
        dir_.update_path()

        kinect_df = pd.read_csv(dir_.path, sep=' ', header=0)
        dir_.data_type = "Wii"
        dir_.update_path()
        wii_df = pd.read_csv(dir_.path, sep=' ', header=0)

        dir_.data_type = "GameInformation"
        dir_.update_path()
        game_info_df = pd.read_csv(dir_.path, sep=' ', header=0)
        game_info_df["DropletInScreen"] = Player.change_value_in_df(game_info_df, "DropletInScreen", 0, 1)
        game_info_df["DropletInScreen"] = Player.change_value_in_df(game_info_df, "DropletInScreen", '\\N', 0)
        game_info_df["DropletInScreen"] = Player.change_value_in_df(game_info_df, "DropletInScreen", 999, 0)
        df = pd.concat(
            [kinect_df["AnkleLeft_x"], kinect_df["AnkleRight_x"], kinect_df["AnkleLeft_y"], kinect_df["AnkleRight_y"],
             wii_df["Pos_COP_k"], wii_df["Pos_COP_k_rel"], kinect_df["SpineBase_x"], kinect_df["SpineShoulder_x"], kinect_df["SpineBase_y"],
             kinect_df["SpineShoulder_y"], game_info_df["DropletInScreen"], game_info_df["PlayerInCenterZone"],
             kinect_df["Head_x"], kinect_df["Head_y"], kinect_df["HipLeft_x"], kinect_df["HipLeft_y"],
             kinect_df["HipRight_x"], kinect_df["HipRight_y"]], axis=1)


        df.rename(columns={'AnkleLeft_x': 'ankle_l', 'AnkleRight_x': 'ankle_r'}, inplace=True)
        df.rename(columns={'AnkleLeft_y': 'ankle_l_y', 'AnkleRight_y': 'ankle_r_y'}, inplace=True)
        df.rename(columns={'Pos_COP_k': 'COF', 'Pos_COP_k_rel': "COF_REL", 'SpineBase_x': 'COM', "SpineShoulder_x": "C7"}, inplace=True)
        df.rename(columns={'SpineBase_y': 'COM_y', "SpineShoulder_y": "C7_y"}, inplace=True)
        df.rename(columns={"DropletInScreen": "DropIn", "PlayerInCenterZone": "VasqueStart"}, inplace=True)

        return df


