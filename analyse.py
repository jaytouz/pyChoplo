# !/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la segmentation du
 mouvement selon 5 différents GAMEMODE """

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


import path as p
from adult import PlayerAdult
from player import Player
from players import DescribePlayers
from players import Players


class Analyse:

    def __init__(self):
        self.players = Players([])
        self.p1_S = None
        self.p2_S = None
        self.p3_S = None
        self.p4_S = None

        Player.player_num = 0

    def add_mean_players(self):
        # TODO NOT WORKING RIGHT NOW SINCE CHANGE WITH PHASE CLASS
        self.describe_all_moves = DescribePlayers(self.players, describe_att_name="all_moves")

    def add_strategy(self):
        from copy import deepcopy
        from strategy import Strategy

        self.p1_S = Strategy.from_analyse(deepcopy(self), name_phase='p1_S')
        self.p2_S = Strategy.from_analyse(deepcopy(self), name_phase='p2_S')
        self.p3_S = Strategy.from_analyse(deepcopy(self), name_phase='p3_S')
        self.p4_S = Strategy.from_analyse(deepcopy(self), name_phase='p4_S')

    def format_moves_in_list(self, analyse_name=None, analyse_id=None):
        """creates a list with only the Move of every players"""
        from copy import deepcopy
        list_move = []
        for p in self.players:
            for m in p.all_moves:
                m.player_id = p.player_id
                m.analyse_name = analyse_name + analyse_id
                list_move.append(deepcopy(m))
        self.list_move = list_move

    def format_normalize_moves_in_list(self, analyse_name=None, analyse_id=None):
        """creates a list with only the Move of every players"""
        from copy import deepcopy
        list_move = []
        for p in self.players:
            for m in p.norm_all_moves:
                m.player_id = p.player_id
                m.analyse_name = analyse_name + analyse_id
                list_move.append(deepcopy(m))
        self.list_move = list_move

    def __add__(self, other):
        """allows to get back all moves after extracting main info"""
        from copy import deepcopy
        list_move = []
        for p in self.players:
            for m in p.all_moves:
                list_move.append(deepcopy(m))

        for p in other.players:
            for m in p.all_moves:
                list_move.append(deepcopy(m))
        return list_move


class AnalyseAdult(Analyse):

    def __init__(self, lst_patient_id, condition, repetition):
        self.path = p.DirectoryAdult2017(None, condition=condition, repetition=repetition, data_type='kinect')
        Analyse.__init__(self)
        self.add_players(lst_patient_id)
        self.format_moves_in_list(analyse_name=str(condition), analyse_id=str(repetition))
        self.add_strategy()

    def add_players(self, lst_patient_id):
        for i in lst_patient_id:
            self.path.patient = i
            self.path.update_path()
            _patient = PlayerAdult(self.path)
            _patient.load_data()
            _patient.split_data_in_moves(use_droplets=False, limit=30)
            _patient.add_pre_drop_data()
            _patient.add_mean_pre_drop_data()
            _patient.set_threshold_state()
            _patient.add_phase_data()
            _patient.add_describe()
            _patient.add_velocity()
            _patient.add_acceleration()
            _patient.add_droplet_info_in_move()
            _patient.check_for_target_reach(target_dist=abs(_patient.droplets[0].amp))
            _patient.add_max_amp()
            _patient.add_max_vel()
            _patient.add_cof_rel_event()
            _patient.add_cm()
            _patient.correct_max_vel()
            _patient.check_for_valid_movement()
            # _patient.find_reaction_time() from mean static posture
            _patient.add_phase()
            _patient.quantify_strategy()
            self.players.append(_patient)

    @classmethod
    def create_dataframe_from_analyse(cls, list_analyse, lvl=3, player=10, move=30):
        """export main measures to pandas dataframe with multiindex as (lvl, player, move) and columns (measures, (mean, std))
        measure = tr, rel_pt, amp_max_cop, amp_max_pel, amp_max_c7, vel_max_cop, vel_max_pel, vel_max_c7, overshoot, dcm, dtml, rcm"""
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        index_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        index_player = list("player_{}".format(i) for i in range(0, player))
        index_move = list("move_{}".format(i) for i in range(0, move))
        index = pd.MultiIndex.from_product([index_lvl, index_player, index_move])

        measure_lvl = ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
        spatio_temp_lvl = ['index', 'value']
        columns = pd.MultiIndex.from_product([measure_lvl, spatio_temp_lvl])

        n_row = lvl * player * move
        n_col = len(measure_lvl) * len(spatio_temp_lvl)
        data = np.empty((n_row, n_col))
        data[:] = np.nan

        df = pd.DataFrame(data, index=index, columns=columns)

        ######## ADD DATA ########

        for a in list_analyse:
            for p in a.players:
                for m in p.valid_moves:
                    lvl, player_id, move_id = "lvl_{}".format(int(m.rep[-1]) - 2), "player_{}".format(
                        m.player_id), "move_{}".format(m.move_id)
                    # print(lvl, player_id, move_id)
                    # start_cm
                    df.loc[(lvl, player_id, move_id)][("start_cm", 'index')] = m.cof.cm.start_cm.index
                    df.loc[(lvl, player_id, move_id)][("start_cm", 'value')] = m.cof.cm.start_cm.val

                    # rel_pt
                    df.loc[(lvl, player_id, move_id)][("rel_pt", 'index')] = m.cof.cm.rel_pt.index
                    df.loc[(lvl, player_id, move_id)][("rel_pt", 'value')] = m.cof.cm.rel_pt.val

                    # "amp_max_cop", 'amp_max_pel', 'amp_max_c7',
                    df.loc[(lvl, player_id, move_id)][("amp_max_cop", 'index')] = m.cof.max_amp.index
                    df.loc[(lvl, player_id, move_id)][("amp_max_cop", 'value')] = m.cof.max_amp.val

                    df.loc[(lvl, player_id, move_id)][("amp_max_pel", 'index')] = m.pelvis.max_amp.index
                    df.loc[(lvl, player_id, move_id)][("amp_max_pel", 'value')] = m.pelvis.max_amp.val

                    df.loc[(lvl, player_id, move_id)][("amp_max_c7", 'index')] = m.c7.max_amp.index
                    df.loc[(lvl, player_id, move_id)][("amp_max_c7", 'value')] = m.c7.max_amp.val

                    # "vel_max_cop", 'vel_max_pel', 'vel_max_c7'

                    df.loc[(lvl, player_id, move_id)][("vel_max_cop", 'index')] = m.cof.max_vel.index
                    df.loc[(lvl, player_id, move_id)][("vel_max_cop", 'value')] = m.cof.max_vel.max_vel

                    df.loc[(lvl, player_id, move_id)][("vel_max_pel", 'index')] = m.pelvis.max_vel.index
                    df.loc[(lvl, player_id, move_id)][("vel_max_pel", 'value')] = m.pelvis.max_vel.max_vel

                    df.loc[(lvl, player_id, move_id)][("vel_max_c7", 'index')] = m.c7.max_vel.index
                    df.loc[(lvl, player_id, move_id)][("vel_max_c7", 'value')] = m.c7.max_vel.max_vel

                    # "overshoot", "dcm", "dtml", "rcm"

                    overshoot = abs(m.cof.max_amp.val - m.cof.x_arr[m.end_drop_median])
                    overshoot_time = m.cof_rel.max_amp.index - m.end_drop_median
                    df.loc[(lvl, player_id, move_id)][("overshoot", 'value')] = overshoot
                    df.loc[(lvl, player_id, move_id)][("overshoot", 'index')] = overshoot_time

                    dcm = abs(m.cof.cm.start_cm.val - m.cof.cm.rel_pt.val)
                    dcm_time = abs(m.cof.cm.start_cm.index - m.cof.cm.rel_pt.index)
                    df.loc[(lvl, player_id, move_id)][('dcm', 'value')] = dcm
                    df.loc[(lvl, player_id, move_id)][('dcm', 'index')] = dcm_time

                    dtml = abs(m.cof.cm.start_cm.val - m.cof.x_arr[m.cof_rel.pdispl_100.index])
                    dtml_time = abs(m.cof.cm.start_cm.index - m.cof_rel.pdispl_target.index)
                    df.loc[(lvl, player_id, move_id)][('dtml', 'value')] = dtml
                    df.loc[(lvl, player_id, move_id)][('dtml', 'index')] = dtml_time

                    rcm = dcm / dtml
                    rcm_time_ratio = dcm_time / dtml_time
                    df.loc[(lvl, player_id, move_id)][('rcm', 'value')] = rcm
                    df.loc[(lvl, player_id, move_id)][('rcm', 'index')] = rcm_time_ratio

        return df

    @classmethod
    def create_dataframe_from_analyse_sep_side(cls, lst_analyse, lvl=3, player=10, move=30):
        """just like create_dataframe_from_analyse except with level=0 of columns is side (left, right)"""
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        index_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        index_player = list("player_{}".format(i) for i in range(0, player))
        index_move = list("move_{}".format(i) for i in range(0, move))
        index = pd.MultiIndex.from_product([index_lvl, index_player, index_move])

        measure_lvl = ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
        spatio_temp_lvl = ['index', 'value']
        side_lvl = ['right','left']
        columns = pd.MultiIndex.from_product([measure_lvl, spatio_temp_lvl, side_lvl])

        n_row = lvl * player * move
        n_col = len(side_lvl) * len(measure_lvl) * len(spatio_temp_lvl)
        data = np.empty((n_row, n_col))
        data[:] = np.nan

        df = pd.DataFrame(data, index=index, columns=columns)

        ######## ADD DATA ########

        for a in lst_analyse:
            for p in a.players:
                for m in p.valid_moves:
                    lvl, player_id, move_id = "lvl_{}".format(int(m.rep[-1]) - 2), "player_{}".format(
                        m.player_id), "move_{}".format(m.move_id)
                    # print(lvl, player_id, move_id)
                    side = m.side
                    # start_cm
                    df.loc[(lvl, player_id, move_id)][("start_cm", 'index', side)] = m.cof.cm.start_cm.index
                    df.loc[(lvl, player_id, move_id)][("start_cm", 'value', side)] = m.cof.cm.start_cm.val

                    # rel_pt
                    df.loc[(lvl, player_id, move_id)][("rel_pt", 'index', side)] = m.cof.cm.rel_pt.index
                    df.loc[(lvl, player_id, move_id)][("rel_pt", 'value', side)] = m.cof.cm.rel_pt.val

                    # "amp_max_cop", 'amp_max_pel', 'amp_max_c7',
                    df.loc[(lvl, player_id, move_id)][("amp_max_cop", 'index', side)] = m.cof.max_amp.index
                    df.loc[(lvl, player_id, move_id)][("amp_max_cop", 'value', side)] = m.cof.max_amp.val

                    df.loc[(lvl, player_id, move_id)][("amp_max_pel", 'index', side)] = m.pelvis.max_amp.index
                    df.loc[(lvl, player_id, move_id)][("amp_max_pel", 'value', side)] = m.pelvis.max_amp.val

                    df.loc[(lvl, player_id, move_id)][("amp_max_c7", 'index', side)] = m.c7.max_amp.index
                    df.loc[(lvl, player_id, move_id)][("amp_max_c7", 'value', side)] = m.c7.max_amp.val

                    # "vel_max_cop", 'vel_max_pel', 'vel_max_c7'

                    df.loc[(lvl, player_id, move_id)][("vel_max_cop", 'index', side)] = m.cof.max_vel.index
                    df.loc[(lvl, player_id, move_id)][("vel_max_cop", 'value', side)] = m.cof.max_vel.max_vel

                    df.loc[(lvl, player_id, move_id)][("vel_max_pel", 'index', side)] = m.pelvis.max_vel.index
                    df.loc[(lvl, player_id, move_id)][("vel_max_pel", 'value', side)] = m.pelvis.max_vel.max_vel

                    df.loc[(lvl, player_id, move_id)][("vel_max_c7", 'index', side)] = m.c7.max_vel.index
                    df.loc[(lvl, player_id, move_id)][("vel_max_c7", 'value', side)] = m.c7.max_vel.max_vel

                    # "overshoot", "dcm", "dtml", "rcm"

                    overshoot = abs(m.cof.max_amp.val - m.cof.x_arr[m.end_drop_median])
                    overshoot_time = m.cof.max_amp.index - m.end_drop_median
                    dcm = abs(m.cof.cm.start_cm.val - m.cof.cm.rel_pt.val)
                    dcm_time = abs(m.cof.cm.start_cm.index - m.cof.cm.rel_pt.index)

                    dtml = abs(m.cof.cm.start_cm.val - m.cof.x_arr[m.cof_rel.pdispl_100.index])
                    dtml_time = abs(m.cof.cm.start_cm.index - m.cof_rel.pdispl_target.index)
                    rcm = dcm / dtml
                    rcm_time_ratio = dcm_time / dtml_time

                    df.loc[(lvl, player_id, move_id)][("overshoot", 'value', side)] = overshoot
                    df.loc[(lvl, player_id, move_id)][("overshoot", 'index', side)] = overshoot_time

                    df.loc[(lvl, player_id, move_id)][('dcm', 'value', side)] = dcm
                    df.loc[(lvl, player_id, move_id)][('dcm', 'index', side)] = dcm_time

                    df.loc[(lvl, player_id, move_id)][('dtml', 'value', side)] = dtml
                    df.loc[(lvl, player_id, move_id)][('dtml', 'index', side)] = dtml_time

                    df.loc[(lvl, player_id, move_id)][('rcm', 'value', side )] = rcm
                    df.loc[(lvl, player_id, move_id)][('rcm', 'index', side)] = rcm_time_ratio

        return df


    @classmethod
    def create_missing_value_df(cls,lst_analyse, lvl=3, player=10):
        """creates the dataframe showing the invalid move from all player"""
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        col_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        index_player = list("player_{}".format(i) for i in range(0, player))


        n_row = player
        n_col = lvl
        data = np.empty((n_row, n_col))
        data[:] = np.nan

        df = pd.DataFrame(data, index=index_player, columns=col_lvl)


        ######## POPULATE DATAFRAME ########
        for i in range(0, lvl):
            for j in range(0,player):
                a, a_idx = lst_analyse[i], "lvl_{}".format(i)
                p, p_idx = a.players[j], "player_{}".format(j)

                df.loc[p_idx][a_idx] = len(p.invalid_moves)


        return df

    @classmethod
    def get_all_joints_norm(cls, list_analyse, lvl=3, player=10, move=30):
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        col_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        col_player = list("player_{}".format(i) for i in range(0, player))
        col_move = list("move_{}".format(i) for i in range(0, move))
        col_joint = ['cof', 'pelvis', 'c7']
        columns = pd.MultiIndex.from_product([col_lvl, col_player, col_move, col_joint])

        index = list(range(404))

        ncol = len(col_lvl) * len(col_player) * len(col_move) * len(col_joint)
        nrow = len(index)

        data = np.empty((nrow, ncol))
        data[:] = np.nan
        df = pd.DataFrame(data, index=index, columns=columns)

        for i in range(0, len(col_lvl)):
            a = list_analyse[i]
            lvl_col = col_lvl[i]
            for j in range(0, len(a.players)):
                p = a.players[j]
                p_col = col_player[j]
                for k in range(0, len(p.valid_moves)):
                    m = p.valid_moves[k]
                    m_col = "move_{}".format(m.move_id)

                    M = m.get_full_move_norm_joints()

                    df[(lvl_col, p_col, m_col, 'cof')] = M[0]
                    df[(lvl_col, p_col, m_col, 'pelvis')] = M[1]
                    df[(lvl_col, p_col, m_col, 'c7')] = M[2]
                    # print(lvl_col, p_col, m_col)
        return df

    @classmethod
    def get_all_angle_norm(cls, list_analyse, lvl=3, player=10, move=30):
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        col_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        col_player = list("player_{}".format(i) for i in range(0, player))
        col_move = list("move_{}".format(i) for i in range(0, move))
        col_angle = ['teta1', 'teta2', 'teta2_v']
        columns = pd.MultiIndex.from_product([col_lvl, col_player, col_move, col_angle])

        index = list(range(404))

        ncol = len(col_lvl) * len(col_player) * len(col_move) * len(col_angle)
        nrow = len(index)

        data = np.empty((nrow, ncol))
        data[:] = np.nan
        df = pd.DataFrame(data, index=index, columns=columns)

        for i in range(0, len(col_lvl)):
            a = list_analyse[i]
            lvl_col = col_lvl[i]
            for j in range(0, len(a.players)):
                p = a.players[j]
                p_col = col_player[j]
                for k in range(0, len(p.valid_moves)):
                    m = p.valid_moves[k]
                    m_col = "move_{}".format(m.move_id)

                    M = m.get_full_move_norm_angle()

                    df[(lvl_col, p_col, m_col, 'teta1')] = M[0]
                    df[(lvl_col, p_col, m_col, 'teta2')] = M[1]
                    df[(lvl_col, p_col, m_col, 'teta2_v')] = M[2]

                    # print(lvl_col, p_col, m_col)
        return df

    @classmethod
    def get_all_joints(cls, list_analyse, lvl=3, player=10, move=30):
        """return dataframe with all joint data"""
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        col_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        col_player = list("player_{}".format(i) for i in range(0, player))
        col_move = list("move_{}".format(i) for i in range(0, move))
        col_joint = ['cof', 'pelvis', 'c7']
        columns = pd.MultiIndex.from_product([col_lvl, col_player, col_move, col_joint])

        index_len = cls.get_max_move_len(list_analyse)
        index = np.arange(index_len)

        ncol = len(col_lvl) * len(col_player) * len(col_move) * len(col_joint)
        nrow = len(index)

        data = np.empty((nrow, ncol))
        data[:] = np.nan
        df = pd.DataFrame(data, index=index, columns=columns)

        def set_move_data(dt_data, len_index):
            data = np.empty(len_index)
            data[:] = np.nan
            data[:len(m)] = dt_data
            s = pd.Series(index = np.arange(len_index), data=data)
            return s

        for i in range(0, len(col_lvl)):
            a = list_analyse[i]
            lvl_col = col_lvl[i]
            for j in range(0, len(a.players)):
                p = a.players[j]
                p_col = col_player[j]
                for k in range(0, len(p.valid_moves)):
                    m = p.valid_moves[k]
                    m_col = "move_{}".format(m.move_id)
                    print(len(m), len(m.cof.x_arr), len(df[(lvl_col, p_col, m_col, 'cof')].loc[:len(m)]))
                    df[(lvl_col, p_col, m_col, 'cof')].loc[:len(m)] = set_move_data(m.cof.x_arr, index_len)
                    df[(lvl_col, p_col, m_col, 'pelvis')].loc[:len(m)] = set_move_data(m.pelvis.x_arr, index_len)
                    df[(lvl_col, p_col, m_col, 'c7')].loc[:len(m)] = set_move_data(m.c7.x_arr, index_len)
                    # print(lvl_col, p_col, m_col)
        return df

    @classmethod
    def get_all_ankle(cls, list_analyse, lvl=3, player=10, move=30):
        """return dataframe with all joint data"""
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        col_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        col_player = list("player_{}".format(i) for i in range(0, player))
        col_move = list("move_{}".format(i) for i in range(0, move))
        col_ankle = ['ankle_l', 'ankle_r']
        columns = pd.MultiIndex.from_product([col_lvl, col_player, col_move, col_ankle])

        index_len = cls.get_max_move_len(list_analyse)
        index = np.arange(index_len)

        ncol = len(col_lvl) * len(col_player) * len(col_move) * len(col_ankle)
        nrow = len(index)

        data = np.empty((nrow, ncol))
        data[:] = np.nan
        df = pd.DataFrame(data, index=index, columns=columns)

        def set_move_data(dt_data, len_index):
            data = np.empty(len_index)
            data[:] = np.nan
            data[:len(m)] = dt_data
            s = pd.Series(index = np.arange(len_index), data=data)
            return s

        for i in range(0, len(col_lvl)):
            a = list_analyse[i]
            lvl_col = col_lvl[i]
            for j in range(0, len(a.players)):
                p = a.players[j]
                p_col = col_player[j]
                for k in range(0, len(p.valid_moves)):
                    m = p.valid_moves[k]
                    m_col = "move_{}".format(m.move_id)
                    # print(len(m), len(m.cof.x_arr), len(df[(lvl_col, p_col, m_col, 'ankle_l')].loc[:len(m)]))
                    df[(lvl_col, p_col, m_col, 'ankle_l')].loc[:len(m)] = set_move_data(m.ankle_l.x_arr, index_len)
                    df[(lvl_col, p_col, m_col, 'ankle_r')].loc[:len(m)] = set_move_data(m.ankle_r.x_arr, index_len)
                    # print(lvl_col, p_col, m_col)
        return df

    @classmethod
    def get_all_angle(cls, list_analyse, lvl=3, player=10, move=30):
        """return dataframe with all angle data"""
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        col_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        col_player = list("player_{}".format(i) for i in range(0, player))
        col_move = list("move_{}".format(i) for i in range(0, move))
        col_angle = ['teta1', 'teta2']
        columns = pd.MultiIndex.from_product([col_lvl, col_player, col_move, col_angle])

        index_len = cls.get_max_move_len(list_analyse)
        index = np.arange(index_len)

        ncol = len(col_lvl) * len(col_player) * len(col_move) * len(col_angle)
        nrow = len(index)

        data = np.empty((nrow, ncol))
        data[:] = np.nan
        df = pd.DataFrame(data, index=index, columns=columns)

        def set_move_data(dt_data, len_index):
            data = np.empty(len_index)
            data[:] = np.nan
            data[:len(m)] = dt_data
            s = pd.Series(index = np.arange(len_index), data=data)
            return s

        for i in range(0, len(col_lvl)):
            a = list_analyse[i]
            lvl_col = col_lvl[i]
            for j in range(0, len(a.players)):
                p = a.players[j]
                p_col = col_player[j]
                for k in range(0, len(p.valid_moves)):
                    m = p.valid_moves[k]
                    m_col = "move_{}".format(m.move_id)

                    df[(lvl_col, p_col, m_col, 'teta1')].loc[:len(m)] = set_move_data(m.angle_lower.rel_arr, index_len)
                    df[(lvl_col, p_col, m_col, 'teta2')].loc[:len(m)] = set_move_data(m.angle_trunk.rel_arr, index_len)
                    # print(lvl_col, p_col, m_col)
        return df

    @classmethod
    def get_max_move_len(cls, lst_analyse):
        M = 0
        for lvl in lst_analyse:
            for p in lvl.players:
                for m in p.valid_moves:
                    if len(m) > M:
                        M = len(m)
        return M

    @classmethod
    def get_all_strats_norm(cls, list_analyse, lvl=3, player=10, move=30):
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        col_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        col_player = list("player_{}".format(i) for i in range(0, player))
        col_move = list("move_{}".format(i) for i in range(0, move))
        col_strat = ['PS', 'ST', 'SPI', 'DPIp', 'DPIap']
        columns = pd.MultiIndex.from_product([col_lvl, col_player, col_move, col_strat])

        index = list(range(404))

        ncol = len(col_lvl) * len(col_player) * len(col_move) * len(col_strat)
        nrow = len(index)

        data = np.empty((nrow, ncol))
        data[:] = np.nan
        df = pd.DataFrame(data, index=index, columns=columns)

        for i in range(0, len(col_lvl)):
            a = list_analyse[i]
            lvl_col = col_lvl[i]
            for j in range(0, len(a.players)):
                p = a.players[j]
                p_col = col_player[j]
                for k in range(0, len(p.valid_moves)):
                    m = p.valid_moves[k]
                    m_col = "move_{}".format(m.move_id)

                    M = m.get_full_move_strat_matrix()

                    df[(lvl_col, p_col, m_col, 'PS')] = M[0]
                    df[(lvl_col, p_col, m_col, 'ST')] = M[1]
                    df[(lvl_col, p_col, m_col, 'SPI')] = M[2]
                    df[(lvl_col, p_col, m_col, 'DPIp')] = M[3]
                    df[(lvl_col, p_col, m_col, 'DPIap')] = M[4]
                    # print(lvl_col, p_col, m_col)

        return df
    @classmethod
    def get_sum_strat(cls, list_analyse, lvl=3, player=10, move=30):
        import pandas as pd
        import numpy as np

        ######## CREATE EMPTY NAN DATAFRAME ########
        idx_lvl = list("lvl_{}".format(i) for i in range(0, lvl))
        idx_player = list("player_{}".format(i) for i in range(0, player))
        idx_move = list("move_{}".format(i) for i in range(0, move))
        index = pd.MultiIndex.from_product([idx_lvl, idx_player, idx_move])

        col_phase = list('phase_{}'.format(i) for i in range(1, 5))
        col_strat = ['PS', 'ST', 'SPI', 'DPIp', 'DPIap']
        columns = pd.MultiIndex.from_product([col_phase, col_strat])

        nrow = len(idx_lvl) * len(idx_player) * len(idx_move)
        ncol = len(col_phase) * len(col_strat)

        data = np.empty((nrow, ncol))
        data[:] = np.nan
        df = pd.DataFrame(data, index=index, columns=columns)
        for i in range(0, len(idx_lvl)):
            a = list_analyse[i]
            lvl_idx = idx_lvl[i]
            for j in range(0, len(a.players)):
                p = a.players[j]
                p_idx = idx_player[j]
                for k in range(0, len(p.valid_moves)):
                    m = p.valid_moves[k]
                    m_idx = "move_{}".format(m.move_id)
                    for idx in zip(['data1','data2','data3','data4'], col_phase):
                        data_num = idx[0]
                        col_name = idx[1]
                        sum_vec = m.phase.__dict__[data_num].S.S.sum(axis=1, dtype='int')
                        df.loc[(lvl_idx, p_idx, m_idx)][col_name] = sum_vec
                    # df[(lvl_idx, p_idx, m_idx)]['ST'] = sum_vec[1]
                    # df[(lvl_idx, p_idx, m_idx)]['SPI'] = sum_vec[2]
                    # df[(lvl_idx, p_idx, m_idx)]['DPIp'] = sum_vec[3]
                    # df[(lvl_idx, p_idx, m_idx)]['DPIap'] = sum_vec[4]
                    # print(lvl_col, p_col, m_col)

        return df

    def get_all_player_strat_matrix(self):
        import numpy as np
        M = np.concatenate([self.p1_S.matrix, self.p2_S.matrix, self.p3_S.matrix, self.p4_S.matrix], axis=1)
        return M

    def get_all_player_norm_joints_std(self):
        import numpy as np
        MEAN = self.get_all_player_norm_joints_mean()
        STD = np.zeros(MEAN.shape)
        for i in range(0, len(self.players)):
            STD += (MEAN - self.players[i].get_all_player_norm_joints_mean()) ** 2
        STD /= len(self.players)
        M_STD = np.sqrt(STD)
        return M_STD

    def get_all_player_norm_joints_mean(self):
        M = self.players[0].get_full_move_norm_joints_mean()
        for i in range(1, len(self.players)):
            M += self.players[i].get_full_move_norm_joints_mean()
        M /= len(self.players)
        return M


class AnalyseChildTD(Analyse):

    def __init__(self, lst_patient_id, condition, repetition):
        self.path = p.DirectoryChildTd(None, condition=condition, repetition=repetition, data_type='kinect')
        Analyse.__init__(self)
        self.add_players(lst_patient_id)
        self.format_moves_in_list(analyse_name=str(condition), analyse_id=str(repetition))

    def add_players(self, lst_patient_id):
        for i in lst_patient_id:
            print(i, "ID PATIENT")
            self.path.patient = i
            self.path.update_path()
            _patient = PlayerChildTD(self.path)
            _patient.load_data()
            _patient.split_data_in_moves(use_droplets=True)
            _patient.add_pre_drop_data()
            _patient.add_mean_pre_drop_data()
            _patient.set_threshold_state()
            _patient.add_phase_data()
            _patient.add_describe()
            _patient.add_velocity()
            _patient.add_acceleration()
            _patient.add_event()
            self.players.append(_patient)


class AnalyseChildCpVd(Analyse):

    def __init__(self, lst_patient_id, condition, repetition):
        self.path = p.DirectoryChildCpVd(None, condition=condition, repetition=repetition, data_type='kinect')
        Analyse.__init__(self)
        self.add_players(lst_patient_id)
        self.format_moves_in_list(analyse_name=str(condition), analyse_id=str(repetition))

    def add_players(self, lst_patient_id):
        for i in lst_patient_id:
            self.path.patient = i
            self.path.update_path()
            _patient = PlayerChildVd(self.path)
            _patient.load_data()
            _patient.split_data_in_moves(use_droplets=True)
            _patient.add_pre_drop_data()
            _patient.add_mean_pre_drop_data()
            _patient.set_threshold_state()
            _patient.add_phase_data()
            _patient.add_describe()
            _patient.add_velocity()
            _patient.add_acceleration()
            _patient.add_event()
            self.players.append(_patient)


class AnalyseChildCpEval(Analyse):

    def __init__(self, lst_patient_id, evaluation):
        self.path = p.DirectoryChildCpJcEval(None, evaluation=evaluation, data_type='kinect')
        Analyse.__init__(self)
        self.add_players(lst_patient_id)
        self.add_mean_players()
        self.format_moves_in_list(analyse_name="eval_", analyse_id=str(evaluation))

    def add_players(self, lst_patient_id):
        for i in lst_patient_id:
            self.path.patient = i
            self.path.update_path()
            _patient = PlayerCpJcEval(self.path)
            _patient.load_data()
            _patient.split_data_in_moves(use_droplets=True)
            _patient.add_pre_drop_data()
            _patient.add_mean_pre_drop_data()
            _patient.set_threshold_state()
            _patient.add_phase_data()
            _patient.add_describe()
            _patient.add_velocity()
            _patient.add_acceleration()
            _patient.add_event()
            self.players.append(_patient)


class AnalyseChildCPMultiSenso(Analyse):

    def __init__(self, lst_patient_id, repetition):
        self.path = p.DirectoryChildCpJcMultiSenso(None, repetition=repetition, data_type='kinect')
        Analyse.__init__(self)
        self.add_players(lst_patient_id)
        # self.add_mean_players() #TODO NOT WORKING RIGHT NOW SINCE CHANGE WITH PHASE CLASS
        self.format_moves_in_list(analyse_name="rep", analyse_id=str(repetition))

    def add_players(self, lst_patient_id):
        for i in lst_patient_id:
            self.path.patient = i
            self.path.update_path()
            _patient = PlayerCpJcMultiSenso(self.path)
            _patient.load_data()
            _patient.split_data_in_moves(use_droplets=True)
            _patient.add_pre_drop_data()
            _patient.add_mean_pre_drop_data()
            _patient.set_threshold_state()
            _patient.add_phase_data()
            _patient.add_describe()
            _patient.add_velocity()
            _patient.add_acceleration()
            _patient.add_event()
            _patient.check_for_target_reach(target_dist=0.4)
            _patient.add_droplet_info_in_move()
            _patient.add_time_axis(unit='normalize')  # normalize or second

            self.players.append(_patient)
