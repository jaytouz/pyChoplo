#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la segmentation du
 mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from copy import copy

from moves import Moves, LeftMoves, RightMoves, AllMoves
from repetition import Repetition
from vectorcoding import GammaAngle


class Player(object):
    player_num = 0

    def __init__(self, raw, droplets, directory):
        print("player init", Player.player_num)
        self.dir = directory
        self.droplets = droplets
        self.raw = raw
        self.player_id = Player.player_num

        self._rep = None
        self.num_moves = None

        self.left_moves = None
        self.right_moves = None

        self.all_moves = None
        self.all_moves_mean = None
        self.all_moves_std = None
        self.norm_all_moves = None
        self.valid_moves = None
        self.invalid_moves = None

        self.p1_S = None
        self.p2_S = None
        self.p3_S = None
        self.p4_S = None

        self.mean_gamma = None

        self.move_phases = {'reaction_phase': [], 'neg_cm': [], 'shift': [], 'overshoot': []}
        self.move_norm_phases = {'reaction_phase': [], 'neg_cm': [], 'shift': [], 'overshoot': []}

        self.norm_phase_gamma = {'reaction_phase': None, 'neg_cm': None, 'shift': None, 'overshoot': None}

        self.phase_gamma = {'reaction_phase': None, 'neg_cm': None, 'shift': None, 'overshoot': None}

        Player.player_num += 1

    def __len__(self):
        return self.num_moves

    @staticmethod
    def change_value_in_df(df, col_name, old_value, new_value):
        """Cette fonction corrige les valeurs dans GameInformation qui
        sont differents dans certain fichier data.txt en raison de
        modification au travers des versions de choplo"""
        new_col = []
        for i in range(0, len(df)):
            try:
                value = int(df[col_name].iloc[i])
            except ValueError:
                value = df[col_name].iloc[i]
            if value == old_value:
                new_col.append(int(new_value))
            else:
                new_col.append(value)
        return new_col

    @property
    def rep(self):
        return copy(self._rep)

    def load_data(self):
        """
        load the raw csv into a dataFrame then use the dataframe to create the Repetition instance
        """
        # print("ABOUT TO FILT", self.player_id)
        self._rep = Repetition(self.raw,
                               low_pass_cutoff=5)  # For now, all joints are filter with 15Hz lowpass  # self.rep.translate_joint()

    def split_data_in_moves(self, limit, use_droplets=True):
        self.split_moves_by_side(limit, use_droplet=use_droplets)
        self.add_info_to_moves()
        self.add_side_info_to_move()

    def add_side_info_to_move(self):
        for m in self.all_moves:
            right = False
            left = False
            static = False

            if m.move_id in self.all_moves.left_id:
                right = False
                left = True
                static = True

            elif m.move_id in self.all_moves.right_id:
                right = True
                left = False
                static = True

            elif m.move_id in self.all_moves.static_id:
                right = False
                left = False
                static = True

            m.add_side_info(left=left, right=right, static=static)

    def add_phase(self):
        for m in self.valid_moves:
            if m.target_reach:
                if m.cof.cm.have_cm:
                    m.add_phase()

    def check_for_valid_movement(self):
        invalid = []
        valid = []
        for m in self.all_moves:
            c1 = m.cof.cm.have_cm  # has a counter movement
            c2 = m.target_reach  # target reach
            if c1 and c2:
                valid.append(m)
            else:
                print('INVALID --- ', 'c1:', c1, 'c2 ', c2)
                invalid.append(m)
        self.valid_moves = Moves(valid)
        self.invalid_moves = Moves(invalid)

    def quantify_strategy(self):
        from strategy import Strategy
        from copy import deepcopy

        for m in self.valid_moves:
            m.add_strategy()

        self.p1_S = Strategy.from_player(deepcopy(self), 'data1')
        self.p2_S = Strategy.from_player(deepcopy(self), 'data2')
        self.p3_S = Strategy.from_player(deepcopy(self), 'data3')
        self.p4_S = Strategy.from_player(deepcopy(self), 'data4')

    def add_info_to_moves(self):
        i = 0
        for m in self.all_moves:
            droplet = self.droplets[i]

            if droplet.rep is not None:
                m.rep = droplet.rep

            if droplet.amp is not None:
                m.amp = droplet.amp

            if droplet.vit is not None:
                m.vit = droplet.vit

            if droplet.sound_delay is not None:
                m.sound_delay = droplet.sound_delay

    # def split_moves_by_feedback(self):
    #     """creates individual moves in three categories. with sounds left, with sounds right, with sounds all"""
    #     self.left_moves_with_sound = self.left_moves.get_moves_by_sounds(self.droplets, with_sound=True)
    #     self.left_moves_without_sound = self.left_moves.get_moves_by_sounds(self.droplets, with_sound=False)
    #
    #     self.right_moves_with_sound = self.right_moves.get_moves_by_sounds(self.droplets, with_sound=True)
    #     self.right_moves_without_sound = self.right_moves.get_moves_by_sounds(self.droplets, with_sound=False)
    #
    #     self.all_moves_with_sound = self.all_moves.get_moves_by_sounds(self.droplets, with_sound=True)
    #     self.all_moves_without_sound = self.all_moves.get_moves_by_sounds(self.droplets, with_sound=False)

    def split_moves_by_side(self, limit, use_droplet=True):
        """creates individual moves in three categories. Left moves, right moves, both sides moves (all_moves)

        ----

        :param use_droplet: for adult, use False
        :type: bool"""
        moves = Moves.from_repetition(self.rep, limit)
        # print("len drops", len(self.droplets))
        if use_droplet:
            left_moves = LeftMoves.from_list_of_moves(moves, droplets=self.droplets)
            right_moves = RightMoves.from_list_of_moves(moves, droplets=self.droplets)
        else:
            left_moves = LeftMoves.from_list_of_moves(moves)
            right_moves = RightMoves.from_list_of_moves(moves)
        #
        # self.left_moves = left_moves
        # self.right_moves = right_moves
        # print(left_moves.list_id, right_moves.list_id)
        left_moves.flip_moves()
        right_moves.flip_angle()
        self.all_moves = AllMoves.from_list_of_moves(left_moves, right_moves)
        self.num_moves = len(self.all_moves)
        self.all_moves.selection_sort()  # self.left_moves.selection_sort()  # self.right_moves.selection_sort()

    def check_for_target_reach(self, target_dist):
        for m in self.all_moves:
            m.check_for_target_reach(target_dist,
                                     m.end_drop_median)  # USED WITH COF_REL, if not change target_dist  # for m in self.left_moves:  #     m.check_for_target_reach(target_dist) #USED WITH COF_REL, if not change target_dist  # for m in self.right_moves:  #     m.check_for_target_reach(target_dist) #USED WITH COF_REL, if not change target_dist
    def get_full_move_norm_joints_std(self):
        """extract std joints displacement after all valid move from player"""
        import numpy as np
        MEAN = self.get_full_move_norm_joints_mean()
        STD = np.zeros(MEAN.shape)
        for i in range(0, len(self.valid_moves)):
            STD += (MEAN - self.valid_moves[i].get_full_move_norm_joints())**2
        STD/=len(self.valid_moves)
        M_STD = np.sqrt(STD)
        return M_STD

    def get_full_move_norm_joints_mean(self):
        """extract mean joints displacement after all valid move from player"""
        M = self.valid_moves[0].get_full_move_norm_joints()
        for i in range(1, len(self.valid_moves)):
            M+= self.valid_moves[i].get_full_move_norm_joints()
        M/=len(self.valid_moves)
        return M

    def get_full_move_strat_matrix(self):
        """extract mean strat after all valid move from a player"""
        import numpy as np
        M = np.concatenate([self.p1_S.matrix, self.p2_S.matrix, self.p3_S.matrix, self.p4_S.matrix],axis=1)
        return M

    def add_droplet_info_in_move(self):
        end_index = self.median_drop_end()
        for m in self.all_moves:
            if m.move_id < len(self.droplets):
                m.end_drop_median = end_index
                i = m.move_id
                m.amp = self.droplets[i].amp
                m.vit = self.droplets[i].vit
                m.sound_delay = self.droplets[i].sound_delay
                try:
                    if m.sound_delay >= 0 and m.sound_delay < 999:
                        m.with_sound = True
                    else:
                        m.without_sound = False
                except TypeError:
                    m.without_sound = False

                if m.amp > 0:
                    m.right = True
                    m.side = 'right'  # drop is on the right side of screen
                elif m.amp < 0:
                    m.left = True
                    m.side = 'left'  # drop is on the left side of screen
                elif m.amp == 0:
                    m.static = True
                    m.side = 'static'  # drop is center

    def median_drop_end(self):
        import numpy as np
        arr = []
        for m in self.all_moves:
            arr.append(m.drop_end_index)
        # print("MEAN :", int(np.mean(np.array(arr))), "--- MEDIAN : ", int(np.median(np.array(arr))))
        median = int(np.median(np.array(arr)))
        return median

    def add_coupling_angle(self):
        # for m in self.norm_all_moves:
        #     m.gamma_angle = GammaAngle(m.angle_lower.rel_arr, m.angle_trunk.rel_arr)
        # self.mean_gamma_norm = GammaAngle.from_moves(self.norm_all_moves)

        self.norm_phase_gamma = {'reaction_phase': GammaAngle.from_moves(self.move_norm_phases['reaction_phase']),
                                 'neg_cm': GammaAngle.from_moves(self.move_norm_phases['neg_cm']),
                                 'shift': GammaAngle.from_moves(self.move_norm_phases['shift']),
                                 'overshoot': GammaAngle.from_moves(self.move_norm_phases['overshoot'])}

        self.phase_gamma = {'reaction_phase': GammaAngle.from_moves(self.move_phases['reaction_phase']),
                            'neg_cm': GammaAngle.from_moves(self.move_phases['neg_cm']),
                            'shift': GammaAngle.from_moves(self.move_phases['shift']),
                            'overshoot': GammaAngle.from_moves(self.move_phases['overshoot'])}

    def add_describe(self):
        # self.left_moves_mean, self.left_moves_std = self.left_moves.describe()
        # self.right_moves_mean, self.rightmoves_std = self.right_moves.describe()
        self.all_moves_mean, self.all_moves_std = self.all_moves.describe()

        # if self.left_moves_with_sound is not None:  #     self.left_moves_with_sound_mean, self.left_moves_with_sound_std = self.left_moves_with_sound.describe  #     self.left_moves_without_sound_mean, self.left_moves_without_sound_std = self.left_moves_without_sound.describe  #  #     self.right_moves_with_sound_mean, self.right_moves_with_sound_std = self.right_moves_with_sound.describe  #     self.right_moves_without_sound_mean, self.right_moves_without_sound_std = self.right_moves_without_sound.describe  #  #     self.all_moves_with_sound_mean, self.all_moves_with_sound_std = self.all_moves_with_sound.describe  #     self.all_moves_without_sound_mean, self.all_moves_without_sound_std = self.all_moves_without_sound.describe

    def add_event(self):
        for m in self.valid_moves:
            m.add_event()

    def add_max_amp(self):
        for m in self.all_moves:
            m.add_max_amp()

    def add_max_vel(self):
        for m in self.all_moves:
            m.add_max_vel()

    def correct_max_vel(self):
        for m in self.all_moves:
            if m.have_cm:
                m.correct_max_vel()

    def add_cof_rel_event(self):
        for m in self.all_moves:
            m.add_cof_rel_event()

    def add_cm(self):
        for m in self.all_moves:
            m.add_counter_movement()

    def add_pre_drop_data(self):
        for m in self.all_moves:
            m.set_pre_drop_data(self.rep, pre_drop_window=75)

    def add_mean_pre_drop_data(self):
        player_pre_drop_data = {'mean': {}, 'std': {}}

        describe_type = ["mean", "std"]
        keys = self.rep.data_type

        for dt in describe_type:
            for k in keys:
                for m in self.all_moves:
                    if dt == "mean":
                        try:
                            player_pre_drop_data[dt][k] += m.pre_drop_mean_data[k]
                        except KeyError:
                            player_pre_drop_data[dt][k] = 0
                            player_pre_drop_data[dt][k] += m.pre_drop_mean_data[k]

                    elif dt == "std":
                        try:
                            player_pre_drop_data[dt][k] += m.pre_drop_std_data[k]
                        except KeyError:
                            player_pre_drop_data[dt][k] = 0
                            player_pre_drop_data[dt][k] += m.pre_drop_std_data[k]
                player_pre_drop_data[dt][k] /= len(self.all_moves)

        self.player_pre_drop_data = player_pre_drop_data

    def set_threshold_state(self):
        for m in self.all_moves:
            m.set_player_threshold(self.player_pre_drop_data)

    def add_phase_data(self):
        for m in self.all_moves:
            m.set_phase_data()

    def add_velocity(self):
        for m in self.all_moves:
            m.add_velocity()

    def add_acceleration(self):
        for m in self.all_moves:
            m.add_acceleration()

    def add_time_axis(self, unit):
        for m in self.all_moves:
            m.add_time_axis(unit)

    def add_normalize_moves(self):
        self.norm_all_moves = []
        for m in self.all_moves:
            if m.cof.cm.have_cm:
                if m.target_reach:
                    self.norm_all_moves.append(NormalizeMove(m, m.cof.cm.start_cm.index, m.cof.max_amp.index))

    def get_moves_by_phase(self):

        self.delete_norm = []
        self.delete = []
        for m in self.all_moves:
            if m.cof.cm.have_cm:
                if m.target_reach:
                    try:
                        self.move_norm_phases['reaction_phase'].append(NormalizeMove(m, 0, m.cof.cm.start_cm.index))
                        self.move_norm_phases['neg_cm'].append(
                            NormalizeMove(m, m.cof.cm.start_cm.index, m.cof.cm.rel_pt.index))
                        self.move_norm_phases['shift'].append(
                            NormalizeMove(m, m.cof.cm.rel_pt.index, m.cof_rel.pdispl_target.index))
                        self.move_norm_phases['overshoot'].append(
                            NormalizeMove(m, m.cof_rel.pdispl_target.index, m.cof_rel.pdispl_target.index + 50))
                    except Exception:
                        self.delete_norm.append(m)

        for m in self.all_moves:
            if m.cof.cm.have_cm:
                if m.target_reach:
                    try:
                        self.move_phases['reaction_phase'].append(m[0: m.cof.cm.start_cm.index])
                        self.move_phases['neg_cm'].append(m[m.cof.cm.start_cm.index: m.cof.cm.rel_pt.index])
                        self.move_phases['shift'].append(m[m.cof.cm.rel_pt.index:m.cof_rel.pdispl_target.index])
                        self.move_phases['overshoot'].append(
                            m[m.cof_rel.pdispl_target.index:m.cof_rel.pdispl_target.index + 50])
                    except Exception:
                        self.delete.append(m)

    def equalise_length(self, length, mode):
        self.all_moves.equalise_length(length, mode)
        self.all_moves_mean.equalise_length(length, mode)
        self.all_moves_std.equalise_length(length,
                                           mode)  # # self.left_moves_mean.equalise_length(length, mode)  # self.left_moves_std.equalise_length(length, mode)  #  # self.right_moves_mean.equalise_length(length, mode)  # self.rightmoves_std.equalise_length(length, mode)

        # if self.left_moves_with_sound is not None:  #     self.left_moves_with_sound.equalise_length(length, mode)  #     self.left_moves_with_sound_mean.equalise_length(length, mode)  #     self.left_moves_with_sound_std.equalise_length(length, mode)  #  #     self.left_moves_without_sound.equalise_length(length, mode)  #     self.left_moves_without_sound_mean.equalise_length(length, mode)  #     self.left_moves_without_sound_std.equalise_length(length, mode)  #  #     self.right_moves_with_sound.equalise_length(length, mode)  #     self.right_moves_with_sound_mean.equalise_length(length, mode)  #     self.right_moves_with_sound_std.equalise_length(length, mode)  #  #     self.right_moves_without_sound.equalise_length(length, mode)  #     self.right_moves_without_sound_mean.equalise_length(length, mode)  #     self.right_moves_without_sound_std.equalise_length(length, mode)  #  #     self.all_moves_with_sound.equalise_length(length, mode)  #     self.all_moves_with_sound_mean.equalise_length(length, mode)  #     self.all_moves_with_sound_std.equalise_length(length, mode)  #  #     self.all_moves_without_sound.equalise_length(length, mode)  #     self.all_moves_without_sound_mean.equalise_length(length, mode)  #     self.all_moves_without_sound_std.equalise_length(length, mode)

    # def plot(self, left="left_moves", right="right_moves", all_data="all_moves", multisenso=False, mean=False,  #          std=False):  #     # TODO plot 3x3  #  #     if mean:  #         lst_data = [self.__dict__["mean_left"], self.__dict__["mean_right"], self.__dict__["mean_all"]]  #  #     elif multisenso:  #         pass  #     else:  #         lst_data = [self.__dict__[left], self.__dict__[right], self.__dict__[all_data]]  #     pass

    # def vector_coding_player(self):  #     from scipy.stats import circmean, circstd  #     from vectorcoding import GammaAngle  #  #     left_mean, left_std = None, None  #     right_mean, right_std = None, None  #     all_mean, all_std = None, None
