#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires
 pour la segmentation du mouvement selon 5 différents GAMEMODE """

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from copy import deepcopy
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

from angle import Angle, AngleTrunk, AngleLower
from center_of_force import CenterOfForce
from center_of_mass import CenterOfMasse
from joint import Joint
from old_phase import OLD_PHASE_OUT_PHASE
from vectorcoding import GammaAngle
from phase import Phase, PhaseData
from strategy import Strategy

from amplitude import PourcDisplacement


class Move(object):
    move_num = 0
    joints = ["cof", "pelvis", "c7", "com", "ddot_com", "ankle_l", "ankle_r"]
    angles = ["angle_lower", "angle_trunk"]
    OLD_PHASE = ["phase"]
    all_data_type = [joints, angles]

    # low_pass_param = {"cutoff": 6, "fs": 50, "order": 1}

    def __init__(self, cof=None, pelvis=None, ddot_com=None, com=None, c7=None, ankle_l=None, ankle_r=None,
                 angle_l=None, angle_t=None, phase=None, cof_rel=None, gamma=None):
        # analyse and player info
        self.player_id = None
        self.analyse_name = None

        self.valid_move = True
        self.comment_on_move = ''
        # time array
        self.t_sec = None
        self.t_norm = None

        # vasque event
        self.vasque_in = None
        self.vasque_out = None

        # drop event
        self.drop_in = None
        self.drop_end = None
        self._end_index = None
        self.end_drop_median = None
        # drop info
        self.rep = None
        self.right = False
        self.left = False
        self.static = False
        self.with_sound = False
        self.without_sound = False
        self.amp = None
        self.vit = None
        self.sound_delay = None
        self.side = None
        self.target_reach = None

        # move data
        self.data_type = None
        self.pre_drop_mean_data = None
        self.pre_drop_std_data = None
        self.player_threshold = None
        self.cm = None
        self.head = None
        self.cof = cof
        self.pelvis = pelvis
        self.c7 = c7
        self.cof_rel = cof_rel
        self.hip_left = None
        self.hip_right = None
        self.ankle_l = ankle_l
        self.ankle_r = ankle_r
        self.gamma_angle = gamma

        self.left_leg = None
        self.right_leg = None
        self.hat = None

        self.com = com
        self.ddot_com = ddot_com

        self.angle_lower = angle_l
        self.angle_trunk = angle_t
        self.OLD_PHASE = phase

        self._move_id = Move.move_num
        Move.move_num += 1  # print(Move.move_num)

    def __len__(self):
        return len(self.cof)

    def __getitem__(self, item):
        if isinstance(item, slice):
            new_move = Move()
            new_move.__dict__ = deepcopy(self.__dict__)
            for dt in self.data_type:
                for s in new_move.__dict__[dt].slots:
                    print(dt,s)
                    new_move.__dict__[dt].__dict__[s] = new_move.__dict__[dt].__dict__[s][item.start:item.stop]
            return new_move

    @property
    def have_cm(self):
        return self.cof.cm.have_cm

    @property
    def max_vel_condition(self):
        v_idx = self.cof.max_vel.index
        if self.have_cm:
            c1 = self.cof.cm.rel_pt.index

        else:
            print("NO CM, CANT CHECK MAX_VEL CONDITION")
            return False
    # def add_player_info(self, **kwargs):
    #     for k in kwargs.keys():
    #         self.__setattr__(k, kwargs[k])

    def set_data_from_splitter(self, repetition, pre_drop_window=75):
        self.data_type = repetition.data_type
        for dt in repetition.data_type:
            self.__dict__[dt] = repetition.__dict__[dt][self.drop_in_index - pre_drop_window:self.end_idx]

    def set_phase_data(self):
        self.OLD_PHASE = OLD_PHASE_OUT_PHASE()
        self.OLD_PHASE.set_phase_data(self.angle_trunk.rel, self.angle_lower.rel, self.player_threshold["mean"],
                                      self.player_threshold["std"])

    def set_player_threshold(self, player_threshold):
        self.player_threshold = player_threshold

    def add_phase(self):
        self.phase = Phase(0, self.cof.cm.start_cm.index, self.cof.cm.start_cm.index, self.cof.cm.rel_pt.index,
                           self.cof.cm.rel_pt.index, self.cof.max_vel.index, self.cof.max_vel.index, self.end_drop_median +100)

        if self.cof.cm.rel_pt.index-self.cof.cm.start_cm.index < 0 :
            self.cof.cm.plot()
        # print('p1_len', self.cof.cm.start_cm.index, 0, self.cof.cm.start_cm.index)
        # print('p2_len', self.cof.cm.rel_pt.index-self.cof.cm.start_cm.index, self.cof.cm.start_cm.index, self.cof.cm.rel_pt.index)
        # print('p3_len', self.cof.max_vel.index- self.cof.cm.rel_pt.index, self.cof.cm.rel_pt.index, self.cof.max_vel.index)
        # print('p4_len', self.cof.max_amp.index- self.cof.max_vel.index, self.cof.max_vel.index, self.cof.max_amp.index)
        if self.cof.cm.have_cm:
            if  self.cof.max_amp.index - self.cof.max_vel.index <= 15:
                # self.cof.max_vel.plot()
                # self.cof.max_amp.plot()
                pass
        self.phase.get_normalize_data_from_move(deepcopy(self))

    def add_strategy(self):
        move = deepcopy(self)
        # print('adding strat to :', move.move_id)
        self.phase.data1.S = Strategy.from_move(move, name_phase='data1')

        self.phase.data2.S = Strategy.from_move(move, name_phase='data2')

        self.phase.data3.S = Strategy.from_move(move, name_phase='data3')

        self.phase.data4.S = Strategy.from_move(move, name_phase='data4')

    def get_full_move_norm_angle(self):
        teta1_1, teta1_2, teta1_3, teta1_4 = self.phase.data1.angle_lower, self.phase.data2.angle_lower, self.phase.data3.angle_lower, self.phase.data4.angle_lower
        teta2_1, teta2_2, teta2_3, teta2_4 = self.phase.data1.angle_trunk, self.phase.data2.angle_trunk, self.phase.data3.angle_trunk, self.phase.data4.angle_trunk
        teta2_v_1, teta2_v_2, teta2_v_3, teta2_v_4 = self.phase.data1.angle_trunk_v, self.phase.data2.angle_trunk_v, self.phase.data3.angle_trunk_v, self.phase.data4.angle_trunk_v

        teta1 = np.concatenate([teta1_1, teta1_2, teta1_3, teta1_4])  # array 0 to 403
        teta2 = np.concatenate([teta2_1, teta2_2, teta2_3, teta2_4])  # array 0 to 403
        teta2_v = np.concatenate([teta2_v_1, teta2_v_2, teta2_v_3, teta2_v_4])  # array 0 to 403

        M = np.array([teta1, teta2, teta2_v])  # creates matrix 2x403

        return M
    def get_full_move_norm_joints(self):
        """Extract norm joints data from a valid move"""
        import numpy as np
        cof1, cof2, cof3, cof4 = self.phase.data1.cof, self.phase.data2.cof, self.phase.data3.cof, self.phase.data4.cof
        pel1, pel2, pel3, pel4= self.phase.data1.pelvis, self.phase.data2.pelvis, self.phase.data3.pelvis, self.phase.data4.pelvis
        c7_1, c7_2, c7_3, c7_4 = self.phase.data1.c7, self.phase.data2.c7, self.phase.data3.c7, self.phase.data4.c7

        cof = np.concatenate([cof1,cof2,cof3,cof4]) #array 0 to 403
        pel = np.concatenate([pel1,pel2,pel3,pel4]) #array 0 to 403
        c7 = np.concatenate([c7_1,c7_2, c7_3, c7_4]) #array 0 to 403

        M = np.array([cof,pel,c7]) # creates matrix 3x403

        return M

    # def get_full_move_norm_ankle(self):
    #     """Extract norm ankle data from a valid move"""
    #     import numpy as np
    #     cof1, cof2, cof3, cof4 = self.phase.data1.cof, self.phase.data2.cof, self.phase.data3.cof, self.phase.data4.cof
    #     pel1, pel2, pel3, pel4= self.phase.data1.pelvis, self.phase.data2.pelvis, self.phase.data3.pelvis, self.phase.data4.pelvis
    #     c7_1, c7_2, c7_3, c7_4 = self.phase.data1.c7, self.phase.data2.c7, self.phase.data3.c7, self.phase.data4.c7
    #
    #     cof = np.concatenate([cof1,cof2,cof3,cof4]) #array 0 to 403
    #     pel = np.concatenate([pel1,pel2,pel3,pel4]) #array 0 to 403
    #     c7 = np.concatenate([c7_1,c7_2, c7_3, c7_4]) #array 0 to 403
    #
    #     M = np.array([cof,pel,c7]) # creates matrix 3x403
    #
    #     return M

    def get_full_move_strat_matrix(self):
        """Extract norm strat data from a valid move"""
        import numpy as np
        M1, M2, M3, M4 = self.phase.data1.S.matrix, self.phase.data2.S.matrix, self.phase.data3.S.matrix, self.phase.data4.S.matrix
        M = np.concatenate([M1,M2,M3,M4],axis=1)
        return M.squeeze()

    def add_max_amp(self):
        self.cof.add_max_amp(self.end_drop_median)
        self.cof_rel.add_max_amp(self.end_drop_median)
        self.pelvis.add_max_amp(self.end_drop_median)
        self.c7.add_max_amp(self.end_drop_median)

    def add_max_vel(self):
        self.cof.add_max_vel(self.end_drop_median)
        self.cof_rel.add_max_vel(self.end_drop_median)
        self.pelvis.add_max_vel(self.end_drop_median)
        self.c7.add_max_vel(self.end_drop_median)

    def correct_max_vel(self):
        from velocity import MaxVelocity
        self.cof.max_vel = MaxVelocity.correct_max_vel_with_cm(deepcopy(self), 'cof')
        self.cof_rel.max_vel = MaxVelocity.correct_max_vel_with_cm(deepcopy(self), 'cof_rel')
        self.c7.max_vel = MaxVelocity.correct_max_vel_with_cm(deepcopy(self), 'c7')
        self.pelvis.max_vel = MaxVelocity.correct_max_vel_with_cm(deepcopy(self), 'pelvis')


    def add_cof_rel_event(self):
        self.cof_rel.set_cof_rel_event(self.amp)

    def add_counter_movement(self):
        self.cof.set_counter_movement(self.cof.max_amp.index, self.end_drop_median)
        self.cof_rel.set_counter_movement(self.cof_rel.max_amp.index, self.end_drop_median)

    def add_event(self):
        self.cof.set_event(self.end_drop_median, drop_amp=abs(self.amp))
        self.cof.set_reaction_time_from_player_mean(self.player_threshold["mean"], self.player_threshold["std"])
        self.cof.set_reaction_time_from_move_mean(self.pre_drop_mean_data, self.pre_drop_std_data)
        # if self.cof.cm.have_cm:
        #     if self.cof.cm.rel_pt.index > self.end_drop_median:
        #         #
        #         self.cof.cm.plot()
        #         self.cof.max_vel.plot()
        #         self.cof.max_vel.calculate_max_vel_with_boundary(self.cof.cm.end_cm.index, self.end_drop_median + 50)
        #     else:
        #         self.cof.max_vel.calculate_max_vel_with_boundary(self.cof.cm.end_cm.index, self.end_drop_median)

        self.cof_rel.set_event(self.drop_end_index, drop_amp=abs(self.amp))
        self.cof_rel.set_reaction_time_from_player_mean(self.player_threshold["mean"], self.player_threshold["std"])
        self.cof_rel.set_reaction_time_from_move_mean(self.pre_drop_mean_data, self.pre_drop_std_data)
        # if self.cof_rel.cm.have_cm:
        #     if self.cof_rel.cm.rel_pt.index > self.end_drop_median:
        #         #
        #         # self.cof_rel.cm.plot()
        #         # self.cof.max_vel.plot()
        #         self.cof_rel.max_vel.calculate_max_vel_with_boundary(self.cof_rel.cm.end_cm.index, self.end_drop_median + 50)
        #     else:
        #         self.cof_rel.max_vel.calculate_max_vel_with_boundary(self.cof_rel.cm.end_cm.index, self.end_drop_median)

        self.pelvis.set_event(self.drop_end_index, drop_amp=abs(self.amp))
        self.c7.set_event(self.drop_end_index, drop_amp=abs(self.amp))
        self.angle_lower.set_event(self.drop_end_index, drop_amp=abs(self.amp))
        self.angle_trunk.set_event(self.drop_end_index, drop_amp=abs(self.amp))

    def check_for_target_reach(self, target_dist, drop_end, dt='cof_rel'):
        error_bol = 0.1  # cof_rel = centre du bol. si attrape a + ou - error = target reach
        data = self.__dict__[dt].x_arr[drop_end]

        self.target_reach = data >= target_dist - error_bol or data <= target_dist - error_bol

    def add_time_axis(self, unit):
        if unit == 'second':
            self.add_time_sec()
        elif unit == 'normalize':
            self.add_time_pourc_move()

    def add_time_pourc_move(self):
        import numpy as np
        if self.cof.cm.have_cm:
            self.t_norm = (np.arange(len(self))-self.cof.cm.start_cm.index) / self.drop_end_index * 100
        else:
            self.t_norm = (np.arange(len(self))-20) / self.drop_end_index * 100

    def add_time_sec(self, fs=50):
        import numpy as np
        self.t_sec = np.arange(len(self)) / fs

    # def add_time_axis(self, unit):
    #     if unit == 'second':
    #         for dt in self.data_type:
    #             self.__dict__[dt].add_time_sec(len(self))
    #     elif unit =='normalize':
    #         for dt in self.data_type:
    #             self.__dict__[dt].add_time_pourc_move(self.drop_end_index, len(self))

    def add_velocity(self):
        self.cof.add_vel()
        self.pelvis.add_vel()
        self.c7.add_vel()  # TODO define for angle class
        self.com.add_vel()

    def add_acceleration(self):
        self.cof.add_accel()
        self.pelvis.add_accel()
        self.c7.add_accel()  # TODO define for angle class
        self.com.add_accel()

    def add_side_info(self, left=False, right=False, static=False):
        self.left = left
        self.right = right
        self.static = static

        if right:
            self.side = "right"
        elif left:
            self.side = "left"
        elif static:
            self.side = "static"

    def set_pre_drop_data(self, repetition, pre_drop_window, min_human_reaction_time=15):
        """min_human_reaction_time=15 or 300 ms, simple reaction time is 200ms, in this complexe task,
        it could be even more"""
        self.pre_drop_mean_data = {}
        self.pre_drop_std_data = {}
        for dt in repetition.data_type:

            if type(repetition.__dict__[dt]) in [Angle, AngleTrunk, AngleLower]:
                self.pre_drop_mean_data[dt] = repetition.__dict__[dt].rel[
                                              self.drop_in - pre_drop_window: self.drop_in + min_human_reaction_time].mean()
                self.pre_drop_std_data[dt] = repetition.__dict__[dt].rel[
                                             self.drop_in - pre_drop_window: self.drop_in + min_human_reaction_time].std()
            elif type(repetition.__dict__[dt]) == GammaAngle:
                # print(dt)
                self.pre_drop_mean_data[dt] = repetition.__dict__[dt].gamma[
                                              self.drop_in - pre_drop_window: self.drop_in + min_human_reaction_time].mean()
                self.pre_drop_std_data[dt] = repetition.__dict__[dt].gamma[
                                             self.drop_in - pre_drop_window: self.drop_in + min_human_reaction_time].std()
            elif type(repetition.__dict__[dt]) in [Joint, CenterOfMasse, CenterOfForce]:
                self.pre_drop_mean_data[dt] = repetition.__dict__[dt].x_arr[
                                              self.drop_in - pre_drop_window: self.drop_in + min_human_reaction_time].mean()
                self.pre_drop_std_data[dt] = repetition.__dict__[dt].x_arr[
                                             self.drop_in - pre_drop_window: self.drop_in + min_human_reaction_time].std()

    @property
    def drop_in_index(self):
        return self.drop_in

    @drop_in_index.setter
    def drop_in_index(self, value):
        self.drop_in = value

    @property
    def end_idx(self):
        return self._end_index

    @end_idx.setter
    def end_idx(self, value):
        self._end_index = value

    @property
    def drop_end_index(self):
        return self.drop_end

    @drop_end_index.setter
    def drop_end_index(self, ind):
        self.drop_end = ind

    @property
    def move_id(self):
        return self._move_id

    @move_id.setter
    def move_id(self, val):
        if val in ["mean", "std"]:
            self._move_id = val

    def flip(self):
        """Multiply x axis data by -1 for all the joints"""
        for dt in self.data_type:
            if type(self.__dict__[dt]) in [Joint, CenterOfForce, CenterOfMasse]:
                # print(dt,'  flipping')
                self.__dict__[dt].x_arr = deepcopy(self.__dict__[dt].x_arr * -1)
    def flip_angle(self):
        self.angle_lower.rel_arr = deepcopy(self.angle_lower.rel_arr) * -1
        self.angle_trunk.rel_arr = deepcopy(self.angle_trunk.rel_arr) * -1

    def equalise_length(self, length, mode):
        for dt in self.data_type:
            self.__dict__[dt].equalise_length(length, mode, max_length=300)

    def plot(self, dtype=['cof', 'pelvis', 'c7'], color=['k', 'b', 'r']):
        """plot the move in list_of_moves in a single figure

        :parameter dtype: name of the att of move to plot
        :parameter plt_colors: index of color map to use
        :parameter single_color: if single_color is used, plt_colors is ignore
        :type dtype: str
        :type plt_colors: int
        :type single_color: char (look in possible color from matplotlib.pyplot.plot doc)
        """


        self.__dict__[dtype[0]].plot(color=color[0])
        self.__dict__[dtype[1]].plot(color=color[1])
        self.__dict__[dtype[2]].plot(color=color[2])

    def plot_angle_angle(self, scatter = True):
        import matplotlib.pyplot as plt

        teta1 = self.angle_lower.rel_arr
        teta2 = self.angle_trunk.rel_arr




        marker_size = np.linspace(1, 50, len(teta1))
        colors = np.linspace(0,1, len(teta1))


        ax = plt.subplot()
        ax.set_xlim([-10,10])
        ax.set_ylim([-10,10])
        if scatter:
            for i in range(0, len(teta1)):
                ax.scatter(teta1[i],teta2[i],s=marker_size[i], edgecolors = 'k', color = colors[i])
        else:
            ax.plot(teta1,teta2)

    def normalize_index(self):
        from eventbaseclass import Event
        from counter_movement import CounterMovement
        drop_end_idx = self.drop_end_index
        if self.cof.cm.have_cm:
            start_cm_idx = self.cof.cm.start_cm.index
        else:
            start_cm_idx = 20 #reaction time of 400ms for healthy adult

        """normalize move de facon a ce que 0 soit start_cm et 100% soit drop_end"""
        normalize = lambda idx, start_cm_idx, drop_end_idx: (idx - start_cm_idx) / drop_end_idx * 100

        new_move = deepcopy(self)
        for dt in self.data_type:  # dt (cof, com, pelvis,etc)
            for dt_att in new_move.__dict__[dt].__dict__.keys():  # dt_att (cm, max_amp, x_arr, etc)
                att = new_move.__dict__[dt].__dict__[dt_att]  # att (cof.cm, cof.max_amp, cof.x_arr, etc)
                if isinstance(att, Event):
                    # traite les cas de max_vel, max_amp, etc sauf ceux dans cm
                    new_move.__dict__[dt].__dict__[dt_att].index = normalize(att.index, start_cm_idx, drop_end_idx)

                if isinstance(att, CounterMovement):
                    if att.have_cm:
                        new_move.__dict__[dt].__dict__[dt_att].start_cm.index = normalize(att.start_cm.index, start_cm_idx, drop_end_idx)
                        new_move.__dict__[dt].__dict__[dt_att].rel_pt.index = normalize(att.rel_pt.index, start_cm_idx, drop_end_idx)
                        new_move.__dict__[dt].__dict__[dt_att].end_cm.index = normalize(att.end_cm.index, start_cm_idx, drop_end_idx)

        return deepcopy(new_move)

    def get_move_norm(self, phase_start_event, phase_end_event):
        """normalize index of every event with normalize index and shorten array of data so it's between 0%
        (start_cm_index) and max_amp_index

        phase_start and phase_end shorten between two phase
        (ex: start_cm_index to rel_pt_index; start_cm and drop_end_index

        phase_start = int (index)
        phase_end = int (index)

        phase_start = [0, self.cof.cm.start_cm.index, self.cof.cm.rel_pt.index, self.cof.cm.end_cm.index, self.cof.max_vel.index, self.cof_rel.pdispl_target.index]
        phase_end =[self.cof.cm.start_cm.index, self.cof.cm.rel_pt.index, self.cof.cm.end_cm.index, self.cof.max_vel.index, self.cof_rel.pdispl_target.index, self.cof.max_amp.index]
"""


        new_move = deepcopy(self)
        if self.cof.cm.have_cm:
            phase_start = [0, self.cof.cm.start_cm.index, self.cof.cm.rel_pt.index, self.cof.cm.end_cm.index, self.cof.max_vel.index, self.cof_rel.pdispl_target.index]
            phase_end =[self.cof.cm.start_cm.index, self.cof.cm.rel_pt.index, self.cof.cm.end_cm.index, self.cof.max_vel.index, self.cof_rel.pdispl_target.index, self.cof.max_amp.index]

            index_start = phase_start[phase_start_event]
            index_end = phase_end[phase_end_event]

            for dt in new_move.data_type:  # dt (cof, com, pelvis,etc)
                for s in new_move.__dict__[dt].slots:  # s (x_arr, y_arr)
                    arr = new_move.__dict__[dt].__dict__[s]  # arr (cof.x_arr, angle_lower.rel_arr, etc)
                    new_move.__dict__[dt].__dict__[s] = arr[index_start:index_end]

        return new_move


