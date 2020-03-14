#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la segmentation du
 mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from player import Player
from joint import Joint
from angle import Angle
from old_phase import OLD_PHASE_OUT_PHASE
from move import Move
from moves import Moves
from copy import deepcopy
import numpy as np


class Players(list):

    def __init__(self, lst_players):
        self._players = []
        if isinstance(lst_players, list):
            self._players = lst_players

        else:
            raise TypeError("lst_Players must be a list")

    @property
    def list_of_players(self):
        lst = []
        for p in self._players:
            lst.append(p)
        return lst

    @list_of_players.setter
    def list_of_players(self, lst):
        self._players = lst

    @list_of_players.deleter
    def list_of_players(self):
        self._players = []

    def __len__(self):
        return len(self._players)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self):
            output = self._players[self.i]
            self.i += 1
            return output
        else:
            raise StopIteration

    def __getitem__(self, key):
        return self._players[key]

    def __setitem__(self, key, item):
        if isinstance(item, Player):
            self._players.insert(key, item)
        else:
            raise TypeError("Item must be a Move")

    def append(self, item):
        if isinstance(item, Player):
            self._players.append(item)
            # print("UPDATE - Players now is of length ", len(self))
        else:
            raise TypeError("Can't append item to Players, must be a Move")

    def __repr__(self):
        lst_players = []
        for p in self.list_of_players:
            lst_players.append("p{}".format(p.player_id))
        return "Players({})".format(str(lst_players))

    def __str__(self):
        lst_players = []
        for p in self.list_of_players:
            lst_players.append("p{}".format(p.player_id))
        return "Players({})".format(str(lst_players))

    @property
    def max_length(self):
        max_length = self.list_of_players[0].all_moves.max_length
        for p in self.list_of_players:
            all_move_max_length = p.all_moves.max_length
            if all_move_max_length > max_length:
                max_length = all_move_max_length
        return max_length

    @property
    def min_length(self):
        min_length = self.list_of_players[0].all_moves.min_length
        for p in self.list_of_players:
            all_move_min_length = p.all_moves.min_length
            if all_move_min_length < min_length:
                min_length = all_move_min_length
        return min_length

    def equalise_length(self, mode="min"):
        if mode == "min":
            length = self.min_length
        elif mode == "max":
            length = self.max_length
        # print(length)
        for p in self.list_of_players:
            p.equalise_length(length, mode)

    def selection_sort(self):
        from copy import deepcopy
        "implementation du selection sort algorithm"
        unsorted = deepcopy(self.list_of_players)  # IS IT NECESSARY TO DEEPCOPY?
        _sorted = []
        n_player = len(unsorted)

        for i in range(0, n_player - 1):
            len_unsort = len(unsorted)
            # print(i, "unsorted length = ", len(unsorted), len_unsort)
            # print(i, "sorted length = ", len(_sorted))
            j = 0
            while j < len_unsort:
                if unsorted[j].player_id == i:
                    #       print("j", j, "unsorted.N", unsorted[j].id, "i", i)
                    _sorted.append(unsorted[j])
                    del (unsorted[j])
                    j += 1
                    break
                j += 1

        _sorted.append(unsorted[0])  # last item is surely the last
        # print("unsorted length = ", len(unsorted))
        # print("sorted length = ", len(_sorted))
        self.list_of_players = _sorted


class DescribePlayers:

    def __init__(self, _players, describe_att_name=None,
                 dtype_att=["COF", "COM", "C7", "angle_lower", "angle_trunk", "phase"]):
        """Allows to calculate the mean of a move_id or mean_arr of a group of player

        :parameter _players: an Instance of Players
        :parameter move_id: the id of the move to look at
        :parameter dtype_att: the data instance from maindata to look att
        :parameter mean_att: all the instance of MeanMove to consider if move_id is None

        :type _players: Players
        :type move_id: int
        :type dtype_att: list
        :type mean_att: list
        """
        self._players = deepcopy(_players)
        self._players.equalise_length(mode='min')
        # TODO is taking the id 0 robust? need change?
        self.num_move_per_player = len(_players[0].__dict__[describe_att_name])
        self.dtype_att = dtype_att
        self.describe_att_name = describe_att_name

        self.lst_moves = deepcopy(list(range(0, len(_players[0].__dict__[self.describe_att_name]))))
        # self.lst_moves = self.get_lst_move()
        # print("players list moves", self.lst_moves)
        self._mean = None  # mean de tous les moves pour tous les joueurs pour le move_id
        self._std = None  # mean de tous les moves pour tous les joueurs pour le move_id
        self.moves_mean = Moves([])
        self.moves_std = Moves([])
        self.add_moves_describe(self.lst_moves)
        # mean de tous les joueurs pour le move_id
         # std de tous les joueurs pour le move_id

        self._mean_drop_end_time = None
        self._mean_drop_end_time = self.mean_drop_end
        self._std_drop_end_time = None
        self._std_drop_end_time = self.std_drop_end

    def __len__(self):
        return self.num_move_per_player

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self):
            output = self._moves[self.i]
            self.i += 1
            return output
        else:
            raise StopIteration

    def __getitem__(self, info):
        move_id, describe_type = info[0], info[1]  # must be a tuple or list
        if describe_type == "mean":
            if move_id is not None:
                data = self.moves_mean[move_id]
            else:
                data = self.mean
        elif describe_type == 'std':
            if move_id is not None:
                data = self.moves_std[move_id]
            else:
                data = self.std
        return deepcopy(data)

    @property
    def mean(self):
        if self._mean is None:
            _data = self.create_empty_data_struct()
            self._mean = self.calculate_mean(data_struct=_data)
        return self._mean

    @property
    def std(self):
        if self._std is None:
            _data = self.create_empty_data_struct()
            self._std = self.calculate_std(self.mean, data_struct=_data)
        return self._std

    @property
    def mean_drop_end(self):
        if self._mean_drop_end_time is None:
            mean_time = 0
            for m in self.moves_mean:
                mean_time += m.drop_end
            mean_time /= len(self.moves_mean)
            self._mean_drop_end_time = mean_time
        return self._mean_drop_end_time

    @property
    def std_drop_end(self):
        if self._std_drop_end_time is None:
            std_time = 0
            for m in self.moves_std:
                std_time = 0
            std_time /= len(self.moves_std)
            # this the mean of all the std. It is still std
            self._std_drop_end_time = std_time
        return self._std_drop_end_time

    # def get_lst_move(self):
    #     """extract the move id based on the describe_att_name"""
    #     moves_id_lst = []
    #     for m in self._players[0].__dict__[self.describe_att_name]:
    #         #regarder tous les moves de describe_att_name
    #         moves_id_lst.append(m.move_id)
    #     return moves_id_lst


    def create_empty_data_struct(self):
        COF = Joint(None, None, "COF")
        COM = Joint(None, None, "COF")
        C7 = Joint(None, None, "COF")
        angle_lower = Angle(None, None, "angle_lower")
        angle_trunk = Angle(None, None, "angle_trunk")
        phase = OLD_PHASE_OUT_PHASE(None, None, None, name="phase")
        return Move(cof=COF, com=COM, c7=C7, angle_l=angle_lower, angle_t=angle_trunk, phase=phase)

    def append(self, move_id):
        # print("move_id to get mean", move_id)
        _data = self.create_empty_data_struct()
        _mean = self.calculate_mean(data_struct=_data, move_id=move_id)
        _std = self.calculate_std(_mean, data_struct=_data, move_id=move_id)
        _mean.drop_end = self.calculate_mean_drop_end(move_id=move_id)
        self.moves_mean.append(_mean)
        self.moves_std.append(_std)

    def add_moves_describe(self, lst_moves):
        for i in lst_moves:
            self.append(i)


    def calculate_mean_drop_end(self, move_id=None):
        mean_time_drop_end = 0
        if move_id is not None:
            for p in self._players:
                mean_time_drop_end += p.__dict__[self.describe_att_name][move_id].drop_end_index
            mean_time_drop_end /= len(self._players)
        else:
            raise IndexError
        return mean_time_drop_end

    def calculate_std_drop_end(self, mean_drop_time, move_id=None):
        std_time_drop_end = 0
        if move_id is not None:
            for p in self._players:
                std_time_drop_end += p.__dict__[self.describe_att_name][move_id].drop_end_index
            std_time_drop_end -= mean_drop_time ** 2
            std_time_drop_end /= len(self._players)
            std_time_drop_end = np.sqrt(std_time_drop_end)
        else:
            raise IndexError
        return std_time_drop_end

    def calculate_mean(self, data_struct=None, move_id=None):
        # TODO adapt for players, right now it's a copy of MeanMove.calculate_mean
        for att in self.dtype_att:
            for s in data_struct.__dict__[att].slots:
                # s in slots is either x_arr, y_arr or abs_angle, rel_angle or phase
                # print("attribute of mean_move : ", att, "attribute of maindata in move : ", s)
                # adding all the s, of dtype of att of player and dividing by num of players to get the mean
                # player.describe_att_name.dtypename.slot
                if move_id is not None:
                    # this section manages data strucutre with move_id like player.all_move
                    mean = deepcopy(self._players[0].__dict__[self.describe_att_name][move_id].__dict__[att].__dict__[s])
                    data_struct.__dict__[att].__dict__[s] = mean
                    for i in range(1, len(self._players)):
                        mean = self._players[i].__dict__[self.describe_att_name][move_id].__dict__[att].__dict__[s]
                        data_struct.__dict__[att].__dict__[s] += mean
                    data_struct.__dict__[att].__dict__[s] /= len(self._players)

                else:
                    # this section manages data strucutre with move_id like player.mean_all
                    mean = self._players[0].__dict__[self.describe_att_name + "_mean"].__dict__[att].__dict__[s]
                    data_struct.__dict__[att].__dict__[s] = mean
                    for i in range(1, len(self._players)):
                        mean = self._players[i].__dict__[self.describe_att_name + "_mean"].__dict__[att].__dict__[s]
                        data_struct.__dict__[att].__dict__[s] += mean
                    data_struct.__dict__[att].__dict__[s] /= len(self._players)
        return data_struct

    def calculate_std(self, _mean, data_struct=None, move_id=None):
        for att in self.dtype_att:
            for s in data_struct.__dict__[att].slots:
                if move_id is not None:
                    std = 0
                    for i in range(0, len(self._players)):
                        std += self._players[i].__dict__[self.describe_att_name][move_id].__dict__[att].__dict__[s] ** 2
                    std -= _mean.__dict__[att].__dict__[s] ** 2
                    std /= len(self._players)
                    data_struct.__dict__[att].__dict__[s] = np.sqrt(std)
                else:
                    std = 0
                    for i in range(0, len(self._players)):
                        std += self._players[i].__dict__[self.describe_att_name + "_std"].__dict__[att].__dict__[s] ** 2
                    std -= _mean.__dict__[att].__dict__[s] ** 2
                    std /= len(self._players)
                    data_struct.__dict__[att].__dict__[s] = np.sqrt(std)
        return data_struct
