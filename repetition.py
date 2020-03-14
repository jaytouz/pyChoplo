#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la
segmentation du mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import numpy as np
from angle import AngleLower, AngleTrunk
from joint import Joint
from center_of_force import CenterOfForce
from segment import TotalLeg, HAT
from center_of_mass import CenterOfMasse
from splitterdata import SplitterInfo
from vectorcoding import GammaAngle
from copy import deepcopy


class Repetition:
    """
    A repetition instance stores the data of Choplo from the start of the game to
    the disappearance of the last drop.

    Parameters
    ----------
    raw = raw is a DataFrame with all the variable of interest for analysis but untreated.
    """

    def __init__(self, raw, data_type=['cof', 'cof_rel', 'c7', 'pelvis', 'com','ankle_l','ankle_r', 'angle_lower', 'angle_trunk', 'ddot_com'], low_pass_cutoff = 10): #TODO add parameter data_type [cof, c7, pelvis, com, phase, angle]
        # print("creating rep")
        self.raw = raw
        self.joints = []
        self.derived_dt = []
        self.angles = []
        self.data_type = data_type
        self.P0 = None

        self.ankle_l = None
        self.ankle_r = None

        self.c7 = None
        self.pelvis = None
        self.cof = None
        self.cof_rel = None

        self.hip_left = None
        self.hip_right = None
        self.left_leg = None
        self.right_leg = None
        self.hat = None
        self.com = None
        self.ddot_com =None

        self.angle_lower = None
        self.angle_trunk = None
        self.gamma_angle = None

        self.splitter_info = SplitterInfo(raw["DropIn"], raw["VasqueStart"])

        self.load_model()

        for dt in self.data_type:
            if dt == 'cof':
                self.joints.append(self.cof)
                self.joints.append(self.cof_rel)

            elif dt == 'pelvis':
                self.joints.append(self.pelvis)

            elif dt == 'c7':
                self.joints.append(self.c7)

            elif dt == 'com':
                self.joints.append(self.hip_left)
                self.joints.append(self.hip_right)

                self.joints.append(self.com)
                self.derived_dt.append(self.ddot_com)

        self.angles.append(self.angle_lower)
        self.angles.append(self.angle_trunk)
        self.angles.append(self.gamma_angle)
        self.main_data = [self.joints + self.angles + self.derived_dt]

        self.splitter_info = SplitterInfo(raw["DropIn"], raw["VasqueStart"])

        if low_pass_cutoff is not None:
            self.apply_filter(low_pass_cutoff)

        self.angle_lower = AngleLower(self.pelvis, self.P0) #NEW
        # self.angle_lower.apply_rolling_mean()

        self.angle_trunk = AngleTrunk(self.c7, self.pelvis, self.angle_lower.rel) # NEW
        # self.angle_trunk.apply_rolling_mean()


    @property
    def mid_dist_btw_ankle_x(self):
        """gets the mid distance in the x axis between the two ankle joints"""
        x_ankle_l = self.ankle_l.x_arr
        x_ankle_r = self.ankle_r.x_arr
        if x_ankle_l.mean() < x_ankle_r.mean():
            mid_dist = (x_ankle_r - x_ankle_l)/2
        else:
            mid_dist = (x_ankle_l - x_ankle_r)/2

        result = (x_ankle_l + x_ankle_r) / 2
        return mid_dist

    @property
    def mid_dist_x_coordinate(self):
        x_ankle_l = self.ankle_l.x_arr
        x_ankle_r = self.ankle_r.x_arr
        result = (x_ankle_l + x_ankle_r) / 2
        return result


    def __len__(self):
        return len(self.raw)

    def translate_joint(self, value=None):
        """translate data in the x axis by value.

            Parameters
            ----------
            value = None (if None, default translate by mid_dist_btw_ankle_x)
        """
        if value is None:
            value = self.mid_dist_btw_ankle_x
        for dt in ['cof','pelvis','c7','com','ankle_l','ankle_r']:
            if dt == 'com':
                #Assumption that initial value of COM is close to zero
                com_val = self.__dict__['com'].x_arr[0:30].mean()
                self.__dict__['com'].x_arr -=  com_val
            else:
                # print(dt, "translating by", value.mean())
                self.__dict__[dt].x_arr = self.__dict__[dt].x_arr - value


    def apply_filter(self, cutoff):
        for dt in self.data_type:
            if dt in ['cof', 'cof_rel']:
                self.__dict__[dt].apply_low_pass(cutoff)
            if dt in ['c7', 'pelvis', 'com']:
                self.__dict__[dt].apply_rolling_mean()
                self.__dict__[dt].apply_low_pass(cutoff) #NEW

    def load_model(self):
        n = len(self)
        x_mid_cheville = (np.ones(n) * (self.raw.ankle_r + self.raw.ankle_l)/2)
        y_mid_cheville = (np.ones(n) * (self.raw.ankle_r_y + self.raw.ankle_l_y)/2)

        t0 = Joint(x_mid_cheville, y_mid_cheville, 'translation vector') #vector de translation vers l'origine du model

        self.P0 = Joint(x_mid_cheville, y_mid_cheville, 'P0') - t0


        self.ankle_l = Joint(self.raw.ankle_l, self.raw.ankle_l_y, 'ankle_l') - t0
        self.ankle_r = Joint(self.raw.ankle_r, self.raw.ankle_r_y, 'ankle_r') - t0

        self.c7 = Joint(self.raw["C7"], self.raw["C7_y"], "C7") - t0
        self.pelvis = Joint(self.raw["COM"], self.raw["COM_y"], "COM") - t0

        self.cof = Joint(self.raw["COF"], np.zeros(n), "COF") - t0
        self.cof_rel = CenterOfForce(self.raw["COF_REL"], None, "COF_REL")
        self.cof_rel.x_arr *= 2  # THIS CORRECTS THE ERROR IN COP_K_REL. the problem is in Unity, in the choplo project. gameManager line 295.

        self.hip_left = Joint(self.raw['HipLeft_y'], self.raw['HipLeft_z'], 'hip_l') - t0
        self.hip_right = Joint(self.raw['HipRight_y'], self.raw['HipRight_z'], 'hip_r') - t0
        self.left_leg = TotalLeg(self.hip_left, self.ankle_l, "left")
        self.right_leg = TotalLeg(self.hip_right, self.ankle_r, "right")
        self.hat = HAT(self.pelvis, self.c7)

        self.com = CenterOfMasse("center_of_mass_legsANDhat", segments=[self.hat, self.left_leg, self.right_leg]).to_joint()
        self.ddot_com = Joint(self.cof.x_arr - self.com.x_arr, np.zeros(len(self.raw)), "ddot_com")

        #OLD
        #OLD
        # self.angle_lower = AngleLower(self.pelvis, self.P0)
        # self.angle_lower.apply_rolling_mean()
        # 
        # self.angle_trunk = AngleTrunk(self.c7, self.pelvis, self.angle_lower.rel)
        # self.angle_trunk.apply_rolling_mean()
        # self.gamma_angle = GammaAngle(self.angle_lower.rel_arr, self.angle_trunk.rel_arr)









