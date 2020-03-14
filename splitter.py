#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires
 pour la segmentation du mouvement selon 5 différents GAMEMODE """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from copy import copy

from move import Move


class Splitter(object):
    """cette classe gère la séparation des données. Permet de feeder une
    séquence de choplo et export les moves en list."""

    def __init__(self, repetition):
        from moves import Moves

        self.repetition = repetition
        Move.move_num = 0

        self.current_move = None
        self.moves = Moves([])
        self.index = None

    def create_moves(self):
        self.index = 1
        while self.index < len(self.repetition):
            drop_last = self.repetition.splitter_info.drop_in[self.index - 1]
            vasque_last = self.repetition.splitter_info.vasque_start[self.index - 1]  # could be useful someday
            drop_current = self.repetition.splitter_info.drop_in[self.index]
            vasque_current = self.repetition.splitter_info.vasque_start[self.index]  # could be useful someday

            self.on_event(drop_current, vasque_current, drop_last, vasque_last)
            self.index += 1
        self.save_move()  # essential to save the last move

    def on_event(self, drop_current, vasque_current, drop_last, vasque_last):
        """Permet d'eviter de rentrer dans les conditions a chaque index, si none.. rien ne se passe """
        if drop_last == 0 and drop_current == 1:
            self.drop_in()
        elif drop_last == 1 and drop_current == 0:
            self.drop_end()

        if vasque_last==0 and vasque_current==1:
            self.vasque_in()
        elif vasque_last==1 and vasque_current==0:
            self.vasque_out()

    def drop_in(self):
        if self.current_move is not None:
            self.save_move()

        self.initialise_move()
    def drop_end(self):
        # print("Drop end")
        # print(self.current_move.start_index - self.index, abs(self.current_move.start_index - self.index))
        self.current_move.drop_end = abs(self.current_move.drop_in_index - self.index)
    def vasque_in(self):
        if self.current_move is not None:
            if self.current_move.vasque_in is not None:
                self.current_move.vasque_in = abs(self.current_move.drop_in_index - self.index)

    def vasque_out(self):
        if self.current_move is not None:
            if self.current_move.vasque_in is not None:
                self.current_move.vasque_out = abs(self.current_move.drop_in_index - self.index)


    def initialise_move(self):
        self.current_move = Move()
        self.current_move.drop_in_index = self.index

    def save_move(self):
        self.current_move.end_idx = self.index - 1
        self.current_move.set_data_from_splitter(copy(self.repetition))
        # print(self.current_move.drop_end)
        self.moves.append(copy(self.current_move))

    def get_moves(self, limit):
        return self.moves.list_of_moves[:limit]

