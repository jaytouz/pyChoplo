# !/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la segmentation du
 mouvement selon 5 différents GAMEMODE """

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018
from moves import Moves


class GraphExporter:
    def __init__(self, moves: Moves, output_path=None, plot_fonction=None):
        if plot_fonction is None:
            from plot import graph_move
            plot_fonction = graph_move

        if output_path is None:
            import os
            import datetime
            directory = "C:/Users/tousi/Documents/Labo_Laurent_Ballaz/Projet_ChopLo/pyChoplo_output/"
            year = str(datetime.datetime.today().year)
            month = str(datetime.datetime.today().month)
            day = str(datetime.datetime.today().day)
            index = 0
            folder = "{}_{}_{}_{}".format(year, month, day, index)
            output_path = directory + folder
            while os.path.exists(output_path):
                index += 1
                folder = "{}_{}_{}_{}".format(year, month, day, index)
                output_path = directory + folder

            self.output_path = output_path
            os.mkdir(output_path)

        if type(moves) != Moves:
            print("Graph exporter error", type(moves), " is  not of type Moves like intented")
            self.ready_to_export = False

        else:
            self.ready_to_export = True
            self.moves_to_export = moves
            self.plot_fonction = plot_fonction

    def export_to_pdf(self):
        if self.ready_to_export:
            for m in self.moves_to_export:
                self.plot_fonction(m, fontsize=20, v_line_drop_in=True, v_line_drop_end=False, add_vel=False,
                                   add_accel=False, absolute=False, add_phase=True, event_patch=True, save_to_pdf=True,
                                   path_to_save_graph=self.output_path)
