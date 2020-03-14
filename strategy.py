#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module gère le calcule des strategies pour un modele à deux segments lors d'un tML """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2019

import numpy as np


class Strategy:
    """class qui gère la création de la matrix de stratégie où chaque colonne est un vecteur unitaire.  """
    states = [-1, 0, 1]  # -1: teta_opp, 0: teta_null, 1:teta_tML
    strategy = [0, 1, 2, 3, 4]  # PS, SPI, ST DPIp, DPIap
    strategy_name = {0: 'PS', 1: 'SPI', 2: 'ST', 3: 'DPIp', 4: 'DPIap'}

    def __init__(self, M=None):
        if M is not None:
            self.S = M
        else:
            self.S = None

    @property
    def PS(self):
        return self.S[0]

    @property
    def PS_CS(self):
        sum = 0
        for data in self.PS:
            sum += data
        return sum

    @property
    def SPI(self):
        return self.S[1]

    @property
    def SPI_CS(self):
        sum = 0
        for data in self.SPI:
            sum += data
        return sum

    @property
    def ST(self):
        return self.S[2]

    @property
    def ST_CS(self):
        sum = 0
        for data in self.ST:
            sum += data
        return sum

    @property
    def SJ(self):
        return self.S[3]

    @property
    def SJ_CS(self):
        sum = 0
        for data in self.SJ:
            sum += data
        return sum

    @property
    def DPIp(self):
        return self.S[4]

    @property
    def PIp_CS(self):
        sum = 0
        for data in self.PIp:
            sum += data
        return sum

    @property
    def DPIap(self):
        return self.S[5]

    @property
    def DPIap_CS(self):
        sum = 0
        for data in self.DPIap:
            sum += data
        return sum

    @property
    def matrix(self):
        return self.S

    @matrix.setter
    def matrix(self, M):
        self.S = M

    def plot(self, strat_id=[0, 1, 2, 3, 4]):
        import matplotlib.pyplot as plt
        import matplotlib.pylab as pl

        ax = plt.subplot()
        colors = pl.cm.jet(np.linspace(0, 1, len(strat_id)))
        t = np.arange(101)

        for i in strat_id:
            plt.plot(t, self.S[i], label=self.strategy_name[i])
        plt.legend(loc='best')
        plt.ylim([-0.5, 1.5])

    def normalize_columns(self):
        unit_vector = lambda vector: vector / sum(vector)
        matrix = self.matrix
        for c in range(0, matrix.shape[1]):
            matrix[:, c] = unit_vector(matrix[:, c])
        self.S = matrix

    @staticmethod
    def get_teta_state(teta, lim_inf_teta, lim_sup_teta):
        state = np.empty((1, 101))
        state[:] = np.nan

        c_nul = np.logical_and(teta >= lim_inf_teta, teta <= lim_sup_teta)
        state = np.where(c_nul, 0, state)  # teta nul
        state = np.where(teta < lim_inf_teta, -1, state)  # teta opp
        state = np.where(teta > lim_sup_teta, 1, state)  # teta tML

        return state

    @staticmethod
    def calcule_strategy(state1, state2):
        strategy = np.empty((5, 101))
        strategy[:] = np.nan

        # static : 0 0
        c1 = np.logical_and(state1 == 0, state2 == 0)
        strategy[0] = np.where(c1, 1, 0)

        # SPI : 1 0
        c2 = np.logical_and(state1 == 1, state2 == 0)
        c3 = np.logical_and(state1 == -1, state2 == 0)
        c_spi = np.logical_or(c2 == True, c3 == True)
        strategy[1] = np.where(c_spi, 1, 0)

        # ST : 0 1
        c4 = np.logical_and(state1 == 0, state2 == 1)
        c5 = np.logical_and(state1 == 0, state2 == -1)
        c_st = np.logical_or(c4 == True, c5 == True)
        strategy[2] = np.where(c_st, 1, 0)

        # DPIp 1 1
        c6 = np.logical_and(state1 == 1, state2 == 1)
        c7 = np.logical_and(state1 == -1, state2 == -1)
        c_dpip = np.logical_or(c6 == True, c7 == True)
        strategy[3] = np.where(c_dpip, 1, 0)

        # DPIap -1 1
        c8 = np.logical_and(state1 == -1, state2 == 1)
        c9 = np.logical_and(state1 == 1, state2 == -1)
        c_dpiap = np.logical_or(c8 == True, c9 == True)
        strategy[4] = np.where(c_dpiap, 1, 0)

        return strategy

    @classmethod
    def from_move(cls, move, name_phase=None):
        phase_data = move.phase.__dict__[name_phase]
        lim_inf_teta1 = move.player_threshold['mean']['angle_lower'] - (
                1.96 * move.player_threshold['std']['angle_lower'])

        lim_sup_teta1 = move.player_threshold['mean']['angle_lower'] + (
                    1.96 * move.player_threshold['std']['angle_lower'])

        teta1 = phase_data.angle_lower
        state1 = cls.get_teta_state(teta1, lim_inf_teta1, lim_sup_teta1)

        # assign to phase class
        phase_data.teta1_nul, phase_data.lim_inf_teta1, phase_data.lim_sup_teta1, phase_data.state1 = \
            move.player_threshold['mean']['angle_lower'], move.player_threshold['mean']['angle_lower'] - (
                    1.96 * move.player_threshold['std']['angle_lower']), move.player_threshold['mean'][
                'angle_lower'] + (1.96 * move.player_threshold['std']['angle_lower']), state1

        lim_inf_teta2 = move.player_threshold['mean']['angle_trunk'] - (
                1.96 * move.player_threshold['std']['angle_trunk'])
        lim_sup_teta2 = move.player_threshold['mean']['angle_trunk'] + (
                    1.96 * move.player_threshold['std']['angle_trunk'])
        teta2 = phase_data.angle_trunk
        state2 = cls.get_teta_state(teta2, lim_inf_teta2, lim_sup_teta2)

        # assign to phase class
        phase_data.teta2_nul, phase_data.lim_inf_teta2, phase_data.lim_sup_teta2, phase_data.state2 = \
            move.player_threshold['mean']['angle_trunk'], move.player_threshold['mean']['angle_trunk'] - (
                    1.96 * move.player_threshold['std']['angle_trunk']), move.player_threshold['mean'][
                'angle_trunk'] + (1.96 * move.player_threshold['std']['angle_trunk']), state2

        # print('teta1 - INF: ', lim_inf_teta1, " SUP : ", lim_sup_teta1, 'teta2 - INF: ', lim_inf_teta2, " SUP : ",
        #       lim_sup_teta2)

        S_m = cls.calcule_strategy(state1, state2)

        return Strategy(S_m)

    @classmethod
    def from_player(cls, player, name_phase=None):
        S_p = np.empty((5, 101))
        S_p[:] = np.nan
        first = True
        for m in player.valid_moves:
            if m.target_reach:
                if m.cof.cm.have_cm:
                    if first:
                        S_p = m.phase.__dict__[name_phase].S.S
                        first = False
                    else:
                        S_p += m.phase.__dict__[name_phase].S.S
        strategy = Strategy(M=S_p)
        strategy.normalize_columns()
        return strategy

    @classmethod
    def from_analyse(cls, analyse, name_phase=None):
        S = np.empty((5, 101))
        S[:] = np.nan
        first = True
        for p in analyse.players:
            if first:
                S = p.__dict__[name_phase].S
                first = False
            else:
                S += p.__dict__[name_phase].S
        strategy = Strategy(M=S)
        strategy.normalize_columns()
        return strategy
