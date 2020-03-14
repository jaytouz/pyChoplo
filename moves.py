#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires
 pour la segmentation du mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from copy import deepcopy

import numpy as np
from matplotlib.pyplot import cm

from move import Move
from splitter import Splitter
from angle import Angle
from joint import Joint
from old_phase import OLD_PHASE_OUT_PHASE


class Moves(list):
    def __init__(self, lst_moves):
        # print("moves init")
        self._moves = []
        if isinstance(lst_moves, list):
            # print(type(lst_moves))
            self._moves = lst_moves  # print("UPDATE - Moves now is of length ", len(self))
        else:
            raise TypeError("lst_moves must be a list")

    @property
    def list_of_moves(self):
        lst = []
        for m in self._moves:
            lst.append(m)
        return lst

    @list_of_moves.setter
    def list_of_moves(self, lst):
        # print("UPDATE - Moves now is of length ", len(self))
        self._moves = lst

    @list_of_moves.deleter
    def list_of_moves(self):
        self._moves = []

    @property
    def list_id(self):
        lst = []
        for m in self.list_of_moves:
            lst.append(m.move_id)
        return lst

    def __len__(self):
        return len(self._moves)

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

    def __getitem__(self, key):
        return self._moves[key]

    def __setitem__(self, key, item):
        if isinstance(item, Move):
            self._moves.insert(key, item)  # print("UPDATE - Moves now is of length ", len(self))
        else:
            raise TypeError("Item must be a Move")

    def append(self, item):
        if isinstance(item, Move):
            self._moves.append(item)  # print("UPDATE - Moves now is of length ", len(self))
        else:
            raise TypeError("Can't append item to moves, must be a Move")

    def __repr__(self):
        lst_moves = []
        for m in self.list_of_moves:
            lst_moves.append("m{}".format(m.move_id))
        return "Moves({})".format(str(lst_moves))

    def __str__(self):
        lst_moves = []
        for m in self.list_of_moves:
            lst_moves.append("m{}".format(m.move_id))
        return "Moves({})".format(str(lst_moves))

    @property
    def max_length(self):
        max_length = len(self.list_of_moves[0])
        for m in self.list_of_moves:
            if len(m) > max_length:
                max_length = len(m)
        return max_length

    @property
    def min_length(self):
        min_length = len(self.list_of_moves[0])
        for m in self.list_of_moves:
            if len(m) < min_length:
                min_length = len(m)
        return min_length

    @property
    def drop_end_time(self):
        fs = self.list_of_moves[0].cof.fs
        drop_end = 0
        for m in self.list_of_moves:
            drop_end += m.drop_end
        drop_end /= len(self)
        # print(drop_end)
        return drop_end


    def describe(self):
        _moves = deepcopy(self)
        _mean = MeanMove(_moves)
        _std = StdMove(_moves, _mean)
        return _mean, _std

    def equalise_length(self, length=None, mode="min"):
        """allows to equilize the length of all array in all the move based on the shortest or longuest
        array of data

        :parameter mode: "min" or "max"
        :type mode: str
        """
        # TODO possible error if user enter something else then 'min' or 'max'
        if length is None:
            if mode == "min":
                length = self.min_length
            elif mode == "max":
                length = self.max_length
        for m in self.list_of_moves:
            m.equalise_length(length, mode)

    def selection_sort(self):
        from copy import deepcopy
        "implementation du selection sort algorithm"
        unsorted = deepcopy(self.list_of_moves)  # IS IT NECESSARY TO DEEPCOPY?
        _sorted = []
        n_move = len(unsorted)
        # print(n_move)
        for i in range(0, n_move):
            len_unsort = len(unsorted)
            # print(i, "unsorted length = ", len(unsorted), len_unsort)
            # print(i, "sorted length = ", len(_sorted))
            j = 0
            while j < len_unsort:
                if unsorted[j].move_id == i:
                    #       print("j", j, "unsorted.N", unsorted[j].id, "i", i)
                    _sorted.append(unsorted[j])
                    del (unsorted[j])
                    j += 1
                    break
                j += 1

        # _sorted.append(unsorted[0])  # last item is surely the last
        # print("unsorted length = ", len(unsorted))
        # print("sorted length = ", len(_sorted))
        self.list_of_moves = _sorted

    def flip_moves(self):
        for i in range(0, len(self)):
            self.list_of_moves[i] = self.list_of_moves[i].flip()
    def flip_angle(self):
        for i in range(0, len(self)):
            self.list_of_moves[i] = self.list_of_moves[i].flip_angle()

    def plot_3x3(self):
        lst_data = []
        lst_legend = []

    def plot(self, dtype="cof", plt_colors=0, single_color=None):
        """plot the move in list_of_moves in a single figure

        :parameter dtype: name of the att of move to plot
        :parameter plt_colors: index of color map to use
        :parameter single_color: if single_color is used, plt_colors is ignore
        :type dtype: str
        :type plt_colors: int
        :type single_color: char (look in possible color from matplotlib.pyplot.plot doc)
        """
        lst_colors = [cm.rainbow, cm.winter, cm.autumn, cm.summer, cm.spring, cm.PRGn, cm.bone]
        colors = iter(lst_colors[plt_colors](np.linspace(0, 1, len(self))))
        for m in self.list_of_moves:
            if single_color is None:
                c = next(colors)
                m.__dict__[dtype].plot(color=c, move_id=m.move_id, drop_end_time=self.drop_end_time)
            else:
                c = single_color
                m.__dict__[dtype].plot(color=c, move_id=m.move_id, drop_end_time=self.drop_end_time)

    def get_moves_by_sounds(self, droplets, with_sound=True):
        """with the help of droplet attributes, split moves that used sounds or only visual stimuli

        :return Moves: the list object countain the moves of interest
        :return type: Moves"""

        moves = []
        for m in self.list_of_moves:
            if with_sound:
                if droplets[m.move_id].sound_delay != 999:
                    moves.append(m)
            if not with_sound:
                if droplets[m.move_id].sound_delay == 999:
                    moves.append(m)

        return Moves.from_list_of_moves(moves)

    def get_moves_normalize_index(self):
        list_moves = []
        for m in self.list_of_moves:
            copy_m = deepcopy(m.normalize_index())
            list_moves.append(copy_m)
        return Moves(list_moves)

    def get_norm_moves(self, start_event = 1, end_event = -1):
        list_moves = []
        for m in self.list_of_moves:
            copy_m = deepcopy(m.get_move_norm(phase_start_event=start_event, phase_end_event=end_event))
            list_moves.append(copy_m)
        return Moves(list_moves)



    @classmethod
    def from_list_of_moves(cls, moves):
        new_lst = deepcopy(moves)
        return cls(new_lst)

    @classmethod
    def from_repetition(cls, repetition, limit):
        splitter = Splitter(repetition)
        splitter.create_moves()
        moves = splitter.get_moves(limit)
        return cls(moves)

    @classmethod
    def from_analysis(cls, list_of_analysis):
        list_moves = []
        for a in list_of_analysis:
            for p in a.players:
                for m in p.all_moves:
                    list_moves.append(deepcopy(m))
        return cls(list_moves)


class LeftMoves(Moves):
    def __init__(self, lst_moves, droplets=None):
        moves = []
        for m in lst_moves:
            if droplets is None:
                if m.cof.x_arr.cumsum().mean() < 0:  # cumsum().mean() more robust for lvl with small displacement.
                    moves.append(m)
            else:
                if droplets[m.move_id].amp < 0:
                    moves.append(m)
        Moves.__init__(self, moves)

    @classmethod
    def from_list_of_moves(cls, _moves, droplets=None):
        new_lst = deepcopy(_moves.list_of_moves)
        return cls(new_lst, droplets)


class RightMoves(Moves):
    def __init__(self, lst_moves, droplets=None):
        moves = []
        for m in lst_moves:
            if droplets is None:
                if m.cof.x_arr.cumsum().mean() > 0:  # cumsum().mean() more robust for lvl with small displacement.
                    moves.append(m)
            else:
                if droplets[m.move_id].amp > 0:
                    moves.append(m)
        Moves.__init__(self, moves)

    @classmethod
    def from_list_of_moves(cls, _moves, droplets=None):
        new_lst = deepcopy(_moves.list_of_moves)
        return cls(new_lst, droplets)


class StaticMoves(Moves):

    def __init__(self, lst_moves, droplets=None):
        moves = []
        for m in lst_moves:
            if droplets is not None:
                if droplets[m.move_id].amp == 0:
                    moves.append(m)
        Moves.__init__(self, moves)

    @classmethod
    def from_list_of_moves(cls, _moves, droplets=None):
        cls.static_id = _moves.list_id
        cls.static_n = len(cls.static_id)
        new_lst = deepcopy(_moves.list_of_moves)
        return cls(new_lst, droplets)


class AllMoves(Moves):

    def __init__(self, left_lst_moves, right_lst_moves):
        moves = []

        for m in left_lst_moves:
            moves.append(m)
        for m in right_lst_moves:
            moves.append(m)

        Moves.__init__(self, moves)

    @classmethod
    def from_list_of_moves(cls, left_lst_moves, right_lst_moves):
        cls.left_id = left_lst_moves.list_id
        cls.left_n = len(cls.left_id)

        cls.right_id = right_lst_moves.list_id
        cls.right_n = len(cls.right_id)

        left_lst = deepcopy(left_lst_moves.list_of_moves)
        right_lst = deepcopy(right_lst_moves.list_of_moves)
        return cls(left_lst, right_lst)


class DescribeMove(Move):
    dtype_att = ["cof", "pelvis", "c7", "com",'ankle_l', 'ankle_r',"angle_lower", "angle_trunk"]

    def __init__(self):

        cof = Joint(None, None, "COF")
        pelvis = Joint(None, None, "pelvis")
        c7 = Joint(None, None, "c7")
        com = Joint(None, None, "COM")
        ankle_l = Joint(None, None, "ankle_l")
        ankle_r = Joint(None, None, "ankle_r")
        angle_lower = Angle(None, None, "angle_lower")
        angle_trunk = Angle(None, None, "angle_trunk")
        phase = OLD_PHASE_OUT_PHASE()
        Move.__init__(self, cof=cof, pelvis=pelvis, c7=c7, com=com, ankle_l=ankle_l, ankle_r=ankle_r,
                      angle_l=angle_lower, angle_t=angle_trunk,phase=phase)


class MeanMove(DescribeMove):

    def __init__(self, _moves):
        DescribeMove.__init__(self)
        self.calculate_mean(_moves)
        self.move_id = 'mean'

    def calculate_mean(self, _moves, normalise_length_mode="min"):
        _moves.equalise_length(length=None, mode=normalise_length_mode)
        for att in DescribeMove.dtype_att:
            # iter in att to get mean of in a move
            mean_move_att = self.__dict__[att]
            for s in mean_move_att.slots:
                # getting mean of a single att of every move in _moves
                mean_move_att.__dict__[s] = deepcopy(_moves[0].__dict__[att].__dict__[s])
                for i in range(1, len(_moves)):
                    mean_move_att.__dict__[s] += _moves[i].__dict__[att].__dict__[s]
                mean_move_att.__dict__[s] /= len(_moves)


class StdMove(DescribeMove):

    def __init__(self, _moves, _mean):
        self.mean_instance = _mean
        DescribeMove.__init__(self)
        self.move_id = 'std'
        for att in DescribeMove.dtype_att:
            # iter in att to get std of in a move
            std_move_att = self.__dict__[att]
            for s in std_move_att.slots:
                std_move_att.__dict__[s] = self.calculate_std(_moves, s, att)

    def calculate_std(self, _moves, s, att):
        """This fonction uses the mean to calculate the std of all the moves for a
        dtype (att) and an axis of that dtype (s)

        :parameter _moves: the moves used to calculate the mean and the std
        :parameter s: name of attribute of a child of basedataclass (ex: x_arr)
        :parameter att: name of the dtype (ex: COF)

        :type _moves: Moves
        :type s : str
        :type att: "str",

        :return std : the std of moves.dtype.slot"""
        # std = 0
        # for move in _moves:
        #     std += move.__dict__[att].__dict__[s] ** 2
        # std -= self.mean_instance.__dict__[att].__dict__[s] ** 2
        # std /= len(_moves)
        # std = np.sqrt(std)
        move_array = []
        for move in _moves:
            move_array.append(move.__dict__[att].__dict__[s])
        move_array = np.array(move_array)
        std = move_array.std(axis=0)
        return std


class NormalizeMoves(Moves):

    def __init__(self):
        pass

