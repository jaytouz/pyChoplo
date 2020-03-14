#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module gère la séparation en phase du mouvement et la normalization  """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2019

import numpy as np
from scipy.interpolate import interp1d


class Phase:
    slots = ['p1', 'p2', 'p3', 'p4']

    def __init__(self, s_p1=None, e_p1=None, s_p2=None, e_p2=None, s_p3=None, e_p3=None, s_p4=None, e_p4=None,
                 data1=None, data2=None, data3=None, data4=None):
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.data4 = data4

        self.p1_slice = (s_p1, e_p1)
        self.p2_slice = (s_p2, e_p2)
        self.p3_slice = (s_p3, e_p3)
        self.p4_slice = (s_p4, e_p4)

    def get_normalize_data_from_move(self, move):
        self.data1 = PhaseData('p1')
        self.data1.from_move(move, self.p1_slice[0], self.p1_slice[1])

        self.data2 = PhaseData('p2')
        self.data2.from_move(move, self.p2_slice[0], self.p2_slice[1])

        self.data3 = PhaseData('p3')
        self.data3.from_move(move, self.p3_slice[0], self.p3_slice[1])

        self.data4 = PhaseData('p4')
        self.data4.from_move(move, self.p4_slice[0], self.p4_slice[1])

    def plot(self, ):
        pass




class PhaseData:
    slots = ['cof', 'cof_rel', 'angle_lower', 'angle_trunk', 'S']

    def __init__(self, phase_name, cof=None, cof_rel=None, angle_lower=None, angle_trunk=None):
        if cof is not None:
            self.cof = cof
        else:
            self.cof = None

        if cof_rel is not None:
            self.cof_rel = cof_rel
        else:
            self.cof_rel = None

        if angle_lower is not None:
            self.angle_lower = angle_lower
        else:
            self.angle_lower = None

        if angle_trunk is not None:
            self.angle_trunk = angle_trunk
        else:
            self.angle_trunk = None


        self.lim_inf_teta1 = None
        self.lim_sup_teta1 = None
        self.teta1_nul = None
        self.state1 = None

        self.lim_inf_teta2 =None
        self.lim_sup_teta2 = None
        self.teta2_nul = None
        self.state2 = None


        self.phase_name = phase_name
        self.S = None


    def add_strategy(self, S):
        from strategy import Strategy
        if isinstance(S, Strategy):
            self.S = S
        else:
            self.S = None

    def from_move(self, move, start, end):
        # print(0, move.cof.cm.start_cm.index, move.cof.cm.rel_pt.index, move.cof.max_vel.index, move.cof.max_amp.index)
        # print(self.phase_name, start, end)
        self.cof = self.normalize(move.cof.x_arr, start, end)
        self.cof_rel = self.normalize(move.cof_rel.x_arr, start, end)
        self.pelvis = self.normalize(move.pelvis.x_arr, start, end)
        self.c7 = self.normalize(move.c7.x_arr, start, end)
        self.angle_lower = self.normalize(move.angle_lower.rel_arr, start, end)
        self.angle_trunk = self.normalize(move.angle_trunk.rel_arr, start, end)
        self.angle_trunk_v = self.normalize(move.angle_trunk.abs_arr, start, end)

    def normalize(self, data, start, end):
        """modified from https://stackoverflow.com/questions/19117660/how-to-generate-equispaced-interpolating-values"""
        from scipy import interpolate

        y = data[start:end]
        x = np.arange(y.size)
        xd = np.diff(x)
        yd = np.diff(y)
        dist = np.sqrt(xd ** 2 + yd ** 2)
        u = np.cumsum(dist)
        u = np.hstack([[0], u])

        t = np.linspace(0, u.max(), 101)
        xn = interpolate.pchip(u, x)
        yn = interpolate.pchip(u, y)
        norm_data = yn(t)
        return norm_data

    def plot(self):
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        import numpy as np

        fig, ax1 = plt.subplots()

        t = np.arange(101)

        ax1.set_xlabel('normalize time (%)')
        ax1.set_ylabel('angle (degree)', color='navy')

        ax1.plot(t, self.angle_lower, lw = 5,c='turquoise', label='teta1')
        ax1.plot(t, self.angle_trunk, lw = 5, c='teal', label='teta2')
        ax1.legend(loc='upper left')

        ax1.tick_params(axis='y', labelcolor='navy')

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        ax2.set_ylabel('displacement (m)', color='darkblue')  # we already handled the x-label with ax1
        ax2.plot(t, self.cof, lw = 5, c='black', label='cof')
        ax2.plot(t, self.pelvis, lw = 5, c='blue', label='Sb_k')
        ax2.plot(t, self.c7, lw = 5, c='red', label='Ms_k')
        ax2.tick_params(axis='y', labelcolor='darkblue')
        ax2.legend(loc='upper right')


        #add strategy
        scatter_y = min(self.cof.min(), self.pelvis.min(), self.c7.min())
        strats = np.zeros(101)
        strats += self.S.SPI
        strats += self.S.ST * 2
        strats += self.S.DPIp * 3
        strats += self.S.DPIap * 4

        tag = strats
        print(tag)
        cmap = plt.cm.jet
        # extract all colors from the .jet map
        cmaplist = [cmap(i) for i in range(cmap.N)]
        # force the first color entry to be grey
        cmaplist[0] = (.78, .05, .05, 1.0)
        cmaplist[1] = (1.0, .39, .0, 1.0)
        cmaplist[2] = (.0, .75, .125, 1.0)
        cmaplist[3] = (.23, .0, .7, 1.0)
        cmaplist[4] = (.0, .93, .77, 1.0)
        # create the new map
        cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist[:6], 6)
        # define the bins and normalize
        bounds = np.linspace(0,5,6)
        ticks = np.arange(0.5, 6.5, 1)
        norm = mpl.colors.BoundaryNorm(bounds, 5)

        pax = ax2.scatter(t,np.ones(t.size) * scatter_y - 0.04, c=tag, marker='s',
                          s=1000, linewidths=1, cmap=cmap, norm=norm)

        # create a second axes for the colorbar
        ax3 = fig.add_axes([0.6, 0.2, 0.25, 0.02]) # posHori, posVert, longueur, hauteur
        cb = mpl.colorbar.ColorbarBase(ax3, cmap=cmap, norm=norm, spacing ='proportional',orientation = 'horizontal', ticks=bounds, boundaries=bounds, format='%1i')
        cb.set_ticks(ticks)
        cb.set_ticklabels([ 'PS','SPI','ST','SJ','DPIp','DPIap'])
        # pax.set_clim(0, 6)

        plt.rcParams.update({'font.size': 30})
        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        return ax1,ax2,ax3