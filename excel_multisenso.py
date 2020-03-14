# !/usr/bin/python
# -*- coding: utf-8 -*-
""" Ce module a pour but de rassembler les informations nécessaires pour la segmentation du
 mouvement selon 5 différents GAMEMODE """

# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

import numpy as np
import pandas as pd




def create_triple_index(f_layer1, f_layer2, f_layer3, nb_rep, nb_player, nb_move):
    f_layer1 = 'rep_{}'
    f_layer2 = 'player_{}'
    f_layer3 = 'move_{}'

    idx1 = []
    for i in range(1, nb_rep + 1):
        idx1.append(f_layer1.format(i))

    idx2 = []
    for i in range(0, nb_player):
        idx2.append(f_layer2.format(i))

    idx3 = []
    for i in range(0, nb_move):
        idx3.append(f_layer3.format(i))

    mult_ind = pd.MultiIndex.from_product([idx1, idx2, idx3])

    return mult_ind


def create_double_col(col1, col2):
    it = [col1, col2]
    mult_col = pd.MultiIndex.from_product(it)
    return mult_col


def create_df_multisenso_multi_col(multisenso):
    f_layer1 = 'rep_{}'
    f_layer2 = 'player_{}'
    f_layer3 = 'move_{}'

    col1 = ['side', 'target_reach', 'have_cm', 'start_cm', 'rel_pt', 'end_cm', 'abs_1', 'abs_2', 'abs_tot', 'max_vel',
            'max_vel_time', 'tm_target_p', 'tm_target_time', 'dis_target_p', 'dis_5p_time', 'dis_10p_time',
            'dis_25p_time', 'dis_50p_time', 'dis_75p_time', 'tm_5p_time', 'tm_10p_time', 'tm_25p_time', 'tm_50p_time',
            'tm_75p_time', 'max_amp', 'max_amp_time', 'tm', 'rel_pt_amp', 'start_cm_amp', 'd_shift',
            'rel_pt_to_max_amp', 'overshoot', 'overshoot_time', 'd_nmp', 'r_nmp_shift']

    col2 = ['uni', 'multi']
    cols = create_double_col(col1,col2)

    index = create_triple_index(f_layer1, f_layer2, f_layer3, 4, 14, 12)
    df = pd.DataFrame(index=index, columns=cols)
    i = 0
    for m in multisenso:
        l1 = f_layer1.format(m.rep)
        l2 = f_layer2.format(m.player_id)
        l3 = f_layer3.format(m.move_id)
        idx = (l1, l2, l3)
        c_lvl_2 = col2[1] if m.with_sound else col2[0]

        # criteria to remove data from move
        c0 = m.cof.max_amp.val < 0
        if c0:
            for ci in col1:
                df.loc[idx, (ci, c_lvl_2)] = np.nan
            continue
        # max_amp after drop dead
        index_max_amp = m.cof_rel.max_amp.index
        drop_dead = 250  # dead at 250 (half sec delay in case they start moving late)
        c1 = index_max_amp > drop_dead + 25

        if m.cof.cm.have_cm:
            s = m.cof.cm.start_cm.index
            r = m.cof.cm.rel_pt.index
            e = m.cof.cm.end_cm.index
            c2 = s > r or s > e

        if c1:
            for ci in col1:
                df.loc[idx, (ci, c_lvl_2)] = np.nan
            continue

        for c in col1:
            if c == 'side':
                df.loc[idx, (c, c_lvl_2)] = m.side
            elif c == 'target_reach':
                df.loc[idx, (c, c_lvl_2)] = 'success' if m.target_reach else 'failed'
            elif c == 'have_cm':
                df.loc[idx, (c, c_lvl_2)] = 'with_cm' if m.cof.cm.have_cm else 'without_cm'
            elif c == 'max_vel':
                df.loc[idx, (c, c_lvl_2)] = m.cof.max_vel.max_vel
            elif c == 'max_vel_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof.max_vel.index / 50
            elif c == 'dis_p5_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.pdispl_5.index / 50
            elif c == 'dis_p10_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.pdispl_10.index / 50
            elif c == 'dis_p25_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.pdispl_25.index / 50
            elif c == 'dis_p50_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.pdispl_50.index / 50
            elif c == 'dis_p75_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.pdispl_75.index / 50
            elif c == 'dis_target_p':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.pdispl_target.pourc
            elif c == 'tm_5p_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.tm5.index / 50
            elif c == 'tm_10p_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.tm10.index / 50
            elif c == 'tm_25p_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.tm25.index / 50
            elif c == 'tm_50p_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.tm50.index / 50
            elif c == 'tm_75p_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.tm75.index / 50
            elif c == 'max_amp':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.max_amp.val
            elif c == 'max_amp_time':
                df.loc[idx, (c, c_lvl_2)] = m.cof_rel.max_amp.index / 50

            if m.cof.cm.have_cm and not c2:
                # all data that depends on counter movement
                if c == 'start_cm':
                    df.loc[idx, (c, c_lvl_2)] = m.cof.cm.start_cm.index / 50

                elif c == 'rel_pt':
                    # set rel_pt
                    df.loc[idx, (c, c_lvl_2)] = m.cof.cm.rel_pt.index / 50

                elif c == 'end_cm':
                    # set end_cm
                    df.loc[idx, (c, c_lvl_2)] = m.cof.cm.end_cm.index / 50

                elif c == 'abs_1':
                    # set absement neg
                    df.loc[idx, (c, c_lvl_2)] = m.cof.cm.first_absement

                elif c == 'abs_2':
                    # set absement pos
                    df.loc[idx, (c, c_lvl_2)] = m.cof.cm.second_absement

                elif c == 'abs_tot':
                    # set absement total
                    df.loc[idx, (c, c_lvl_2)] = m.cof.cm.total_absement

                elif c == 'rel_pt_amp':
                    df.loc[idx, (c, c_lvl_2)] = m.cof_rel.cm.rel_pt.val

                elif c == 'start_cm_amp':
                    df.loc[idx, (c, c_lvl_2)] = m.cof_rel.cm.start_cm.index / 50

                elif c == 'd_nmp':
                    df.loc[idx, (c, c_lvl_2)] = abs(m.cof_rel.cm.rel_pt.val - m.cof_rel.cm.start_cm.val)

                elif c == 'rel_pt_to_max_amp':
                    df.loc[idx, (c, c_lvl_2)] = m.cof_rel.max_amp.val - m.cof_rel.cm.rel_pt.val

                elif c == 'd_shift':
                    df.loc[idx, (c, c_lvl_2)] = m.cof_rel.max_amp.val - m.cof_rel.cm.start_cm.val

                elif c == 'r_nmp_shift':
                    df.loc[idx, (c, c_lvl_2)] = (abs(m.cof_rel.cm.rel_pt.val - m.cof_rel.cm.start_cm.val)) / (
                            m.cof_rel.max_amp.val - m.cof_rel.cm.start_cm.val)
                elif c == 'tm':
                    df.loc[idx, (c, c_lvl_2)] = (m.cof.max_amp.index - m.cof.cm.start_cm.index) / 50
            else:
                # IF NO COUNTER MOVEMENT
                if c == 'start_cm':
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'rel_pt':
                    # set rel_pt
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'end_cm':
                    # set end_cm
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'abs_1':
                    # set absement neg
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'abs_2':
                    # set absement pos
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'abs_tot':
                    # set absement total
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'rel_pt_amp':
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'start_cm_amp':
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'd_nmp':
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'rel_pt_to_max_amp':
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'd_shift':
                    df.loc[idx, (c, c_lvl_2)] = np.nan

                elif c == 'r_nmp_shift':
                    df.loc[idx, (c, c_lvl_2)] = np.nan
                elif c == 'tm':
                    df.loc[idx, (c, c_lvl_2)] = np.nan

            if m.target_reach:
                # ALL DATA THAT DEPENDS ON TARGET REACH
                if c == 'tm_target_p':
                    df.loc[idx, (c, c_lvl_2)] = m.tm_target.pourc
                elif c == 'tm_target_time':
                    df.loc[idx, (c, c_lvl_2)] = m.tm_target.index / 50
                elif c == 'overshoot':
                    df.loc[idx, (c, c_lvl_2)] = m.cof_rel.max_amp.val - m.tm_target.val
                elif c == 'overshoot_time':
                    df.loc[idx, (c, c_lvl_2)] = (m.cof_rel.max_amp.index - m.tm_target.index) / 50
            else:
                # IF TARGET NOT REACH
                if c == 'tm_target_p':
                    df.loc[idx, (c, c_lvl_2)] = np.nan
                elif c == 'tm_target_time':
                    df.loc[idx, (c, c_lvl_2)] = np.nan
                elif c == 'overshoot':
                    df.loc[idx, (c, c_lvl_2)] = np.nan
                elif c == 'overshoot_time':
                    df.loc[idx, (c, c_lvl_2)] = np.nan
    return df


def create_df_multisenso_single_col(multisenso):
    f_layer1 = 'rep_{}'
    f_layer2 = 'player_{}'
    f_layer3 = 'move_{}'

    col1 = ['side', 'target_reach', 'have_cm', 'start_cm', 'rel_pt', 'end_cm', 'abs_1', 'abs_2', 'abs_tot', 'max_vel',
            'max_vel_time', 'tm_target_p', 'tm_target_time', 'dis_target_p', 'dis_5p_time', 'dis_10p_time',
            'dis_25p_time', 'dis_50p_time', 'dis_75p_time', 'tm_5p_time', 'tm_10p_time', 'tm_25p_time', 'tm_50p_time',
            'tm_75p_time', 'max_amp', 'max_amp_time', 'sound', 'tm', 'rel_pt_amp', 'start_cm_amp', 'd_shift',
            'rel_pt_to_max_amp', 'overshoot', 'overshoot_time', 'd_nmp', 'r_nmp_shift']

    index = create_triple_index(f_layer1, f_layer2, f_layer3, 4, 14, 12)
    df = pd.DataFrame(index=index, columns=col1)
    i = 0
    for m in multisenso:
        l1 = f_layer1.format(m.rep)
        l2 = f_layer2.format(m.player_id)
        l3 = f_layer3.format(m.move_id)
        idx = (l1, l2, l3)

        # criteria to remove data from move
        c0 = m.cof.max_amp.val < 0
        if c0:
            for c in col1:
                df.loc[idx, c] = np.nan
            continue
        # max_amp after drop dead
        index_max_amp = m.cof_rel.max_amp.index
        drop_dead = 250  # dead at 250 (half sec delay in case they start moving late)
        c1 = index_max_amp > drop_dead + 25

        if m.cof.cm.have_cm:
            s = m.cof.cm.start_cm.index
            r = m.cof.cm.rel_pt.index
            e = m.cof.cm.end_cm.index
            c2 = s > r or s > e

        if c1:
            for c in col1:
                df.loc[idx, c] = np.nan
            continue

        for c in col1:
            if c == 'side':
                df.loc[idx, c] = m.side
            elif c == 'target_reach':
                df.loc[idx, c] = 'success' if m.target_reach else 'failed'
            elif c == 'have_cm':
                df.loc[idx, c] = 'with_cm' if m.cof.cm.have_cm else 'without_cm'
            elif c == 'sound':
                df.loc[idx, c] = 'multi' if m.with_sound else 'uni'
            elif c == 'max_vel':
                df.loc[idx, c] = m.cof.max_vel.max_vel
            elif c == 'max_vel_time':
                df.loc[idx, c] = m.cof.max_vel.index / 50
            elif c == 'dis_5p_time':
                df.loc[idx, c] = m.cof_rel.pdispl_5.index / 50
            elif c == 'dis_10p_time':
                df.loc[idx, c] = m.cof_rel.pdispl_10.index / 50
            elif c == 'dis_25p_time':
                df.loc[idx, c] = m.cof_rel.pdispl_25.index / 50
            elif c == 'dis_50p_time':
                df.loc[idx, c] = m.cof_rel.pdispl_50.index / 50
            elif c == 'dis_75p_time':
                df.loc[idx, c] = m.cof_rel.pdispl_75.index / 50
            elif c == 'tm_5p_time':
                df.loc[idx, c] = m.cof_rel.tm5.index / 50
            elif c == 'tm_10p_time':
                df.loc[idx, c] = m.cof_rel.tm10.index / 50
            elif c == 'tm_25p_time':
                df.loc[idx, c] = m.cof_rel.tm25.index / 50
            elif c == 'tm_50p_time':
                df.loc[idx, c] = m.cof_rel.tm50.index / 50
            elif c == 'tm_75p_time':
                df.loc[idx, c] = m.cof_rel.tm75.index / 50
            elif c == 'dis_target_p':
                df.loc[idx, c] = m.cof_rel.pdispl_target.pourc
            elif c == 'max_amp':
                df.loc[idx, c] = m.cof_rel.max_amp.val
            elif c == 'max_amp_time':
                df.loc[idx, c] = m.cof_rel.max_amp.index / 50

            if m.cof.cm.have_cm and not c2:
                # all data that depends on counter movement
                if c == 'start_cm':
                    df.loc[idx, c] = m.cof.cm.start_cm.index / 50

                elif c == 'rel_pt':
                    # set rel_pt
                    df.loc[idx, c] = m.cof.cm.rel_pt.index / 50

                elif c == 'end_cm':
                    # set end_cm
                    df.loc[idx, c] = m.cof.cm.end_cm.index / 50

                elif c == 'abs_1':
                    # set absement neg
                    df.loc[idx, c] = m.cof.cm.first_absement

                elif c == 'abs_2':
                    # set absement pos
                    df.loc[idx, c] = m.cof.cm.second_absement

                elif c == 'abs_tot':
                    # set absement total
                    df.loc[idx, c] = m.cof.cm.total_absement

                elif c == 'rel_pt_amp':
                    df.loc[idx, c] = m.cof_rel.cm.rel_pt.val

                elif c == 'start_cm_amp':
                    df.loc[idx, c] = m.cof_rel.cm.start_cm.index / 50

                elif c == 'd_nmp':
                    df.loc[idx, c] = abs(m.cof_rel.cm.rel_pt.val - m.cof_rel.cm.start_cm.val)

                elif c == 'rel_pt_to_max_amp':
                    df.loc[idx, c] = m.cof_rel.max_amp.val - m.cof_rel.cm.rel_pt.val

                elif c == 'd_shift':
                    df.loc[idx, c] = m.cof_rel.max_amp.val - m.cof_rel.cm.start_cm.val

                elif c == 'r_nmp_shift':
                    df.loc[idx, c] = (abs(m.cof_rel.cm.rel_pt.val - m.cof_rel.cm.start_cm.val)) / (
                            m.cof_rel.max_amp.val - m.cof_rel.cm.start_cm.val)
                elif c == 'tm':
                    df.loc[idx, c] = (m.cof.max_amp.index - m.cof.cm.start_cm.index) / 50
            else:
                # IF NO COUNTER MOVEMENT
                if c == 'start_cm':
                    df.loc[idx, c] = np.nan

                elif c == 'rel_pt':
                    # set rel_pt
                    df.loc[idx, c] = np.nan

                elif c == 'end_cm':
                    # set end_cm
                    df.loc[idx, c] = np.nan

                elif c == 'abs_1':
                    # set absement neg
                    df.loc[idx, c] = np.nan

                elif c == 'abs_2':
                    # set absement pos
                    df.loc[idx, c] = np.nan

                elif c == 'abs_tot':
                    # set absement total
                    df.loc[idx, c] = np.nan

                elif c == 'rel_pt_amp':
                    df.loc[idx, c] = np.nan

                elif c == 'start_cm_amp':
                    df.loc[idx, c] = np.nan

                elif c == 'd_nmp':
                    df.loc[idx, c] = np.nan

                elif c == 'rel_pt_to_max_amp':
                    df.loc[idx, c] = np.nan

                elif c == 'd_shift':
                    df.loc[idx, c] = np.nan

                elif c == 'r_nmp_shift':
                    df.loc[idx, c] = np.nan
                elif c == 'tm':
                    df.loc[idx, c] = np.nan

            if m.target_reach:
                # ALL DATA THAT DEPENDS ON TARGET REACH
                if c == 'tm_target_p':
                    df.loc[idx, c] = m.tm_target.pourc
                elif c == 'tm_target_time':
                    df.loc[idx, c] = m.tm_target.index / 50
                elif c == 'overshoot':
                    df.loc[idx, c] = m.cof_rel.max_amp.val - m.tm_target.val
                elif c == 'overshoot_time':
                    df.loc[idx, c] = (m.cof_rel.max_amp.index - m.tm_target.index) / 50
            else:
                # IF TARGET NOT REACH
                if c == 'tm_target_p':
                    df.loc[idx, c] = np.nan
                elif c == 'tm_target_time':
                    df.loc[idx, c] = np.nan
                elif c == 'overshoot':
                    df.loc[idx, c] = np.nan
                elif c == 'overshoot_time':
                    df.loc[idx, c] = np.nan

    return df


def filter_outlier(df):
    """not design for multiIndex columns"""
    from scipy import stats

    for c in df.columns.values:
        try:
            s = df[c].loc[((df[c] > (df[c].mean() - (3*df[c].std()))) & (df[c] < (df[c].mean() + (3*df[c].std()))))]
            df[c] = s
        except TypeError:
            print('TypeError', c)
    return df


def count_in_condition(df):
    """not design for multiIndex columns"""

    multi_and_s = len(df.loc[(df['sound'] == 'multi') & (df['target_reach'] == 'success')])
    multi_and_f = len(df.loc[(df['sound'] == 'multi') & (df['target_reach'] == 'failed')])
    uni_and_s = len(df.loc[(df['sound'] == 'uni') & (df['target_reach'] == 'success')])
    uni_and_f = len(df.loc[(df['sound'] == 'multi') & (df['target_reach'] == 'failed')])

    multi_cm = len(df.loc[(df['sound'] == 'multi') & (df['have_cm'] == 'with_cm')])
    multi_no_cm = len(df.loc[(df['sound'] == 'multi') & (df['have_cm'] == 'without_cm')])
    uni_cm = len(df.loc[(df['sound'] == 'uni') & (df['have_cm'] == 'with_cm')])
    uni_no_cm = len(df.loc[(df['sound'] == 'uni') & (df['have_cm'] == 'without_cm')])

    print("TOTAL MOVES", len(df))

    print("TOTAL", multi_and_s + multi_and_f)
    print("SUCCESS AND MULTI ", multi_and_s)
    print("FAILED AND MULTI ", multi_and_f)
    print()

    print("TOTAL", uni_and_s + uni_and_f)
    print("SUCCESS AND UNI ", uni_and_s)
    print("FAILED AND UNI ", uni_and_f)
    print()
    print("TOTAL", multi_cm + multi_no_cm)
    print("COUNTER MOVEMENT AND MULTI ", multi_cm)
    print("NO COUNTER MOVEMENT AND MULTI ", multi_no_cm)
    print()
    print("TOTAL", uni_cm + uni_no_cm)
    print("COUNTER MOVEMENT AND UNI ", uni_cm)
    print("NO COUNTER MOVEMENT AND UNI ", uni_no_cm)


def get_mean_per_rep(df, hue='sound'):
    """Only works with single columns df"""
    reps = ['rep_1', 'rep_2', 'rep_3', 'rep_4', 'rep_1_3', 'rep_2_4', 'all']
    idx_reps = ['rep_1', 'rep_2', 'rep_3', 'rep_4', ('rep_1', 'rep_3'), ('rep_2', 'rep_4'), slice(None)]

    if hue == 'sound':
        lvl1 = ['uni', 'multi']
        multi_cols = pd.MultiIndex.from_product([lvl1, reps])

        uni_data = df.loc[df['sound'] == 'uni']
        uni_mean = pd.DataFrame(index=df.columns, columns=reps)

        for i in range(0, len(reps)):
            temp = uni_data.loc[(idx_reps[i], slice(None), slice(None)), :].mean()
            uni_mean[reps[i]] = temp

        multi_data = df.loc[df['sound'] == 'multi']
        multi_mean = pd.DataFrame(index=df.columns, columns=reps)

        for i in range(0, len(reps)):
            temp = multi_data.loc[(idx_reps[i], slice(None), slice(None)), :].mean()
            multi_mean[reps[i]] = temp

        df_mean = pd.DataFrame(index=df.columns, columns=multi_cols)

        df_mean['uni'] = uni_mean
        df_mean['multi'] = multi_mean

    else:
        df_mean = pd.DataFrame(index=df.columns, columns=reps)
        for i in range(0, len(reps)):
            temp = df.loc[(idx_reps[i], slice(None), slice(None)), :].mean()
            df_mean[reps[i]] = temp

    return df_mean


def get_std_per_rep(df, hue='sound'):
    """Only works with single columns df"""
    reps = ['rep_1', 'rep_2', 'rep_3', 'rep_4', 'rep_1_3', 'rep_2_4', 'all']
    idx_reps = ['rep_1', 'rep_2', 'rep_3', 'rep_4', ('rep_1', 'rep_3'), ('rep_2', 'rep_4'), slice(None)]

    if hue == 'sound':
        lvl1 = ['uni', 'multi']
        multi_cols = pd.MultiIndex.from_product([lvl1, reps])

        uni_data = df.loc[df['sound'] == 'uni']
        uni_std = pd.DataFrame(index=df.columns, columns=reps)

        for i in range(0, len(reps)):
            temp = uni_data.loc[(idx_reps[i], slice(None), slice(None)), :].std()
            uni_std[reps[i]] = temp

        multi_data = df.loc[df['sound'] == 'multi']
        multi_std = pd.DataFrame(index=df.columns, columns=reps)

        for i in range(0, len(reps)):
            temp = multi_data.loc[(idx_reps[i], slice(None), slice(None)), :].std()
            multi_std[reps[i]] = temp

        df_std = pd.DataFrame(index=df.columns, columns=multi_cols)

        df_std['uni'] = uni_std
        df_std['multi'] = multi_std

    else:
        df_std = pd.DataFrame(index=df.columns, columns=reps)
        for i in range(0, len(reps)):
            temp = df.loc[(idx_reps[i], slice(None), slice(None)), :].std()
            df_std[reps[i]] = temp

    return df_std


def get_mean_per_player(df, hue='sound'):
    """Only works with single columns df"""

    reps = ['rep_1', 'rep_2', 'rep_3', 'rep_4', 'rep_1_3', 'rep_2_4', 'all']
    idx_reps = ['rep_1', 'rep_2', 'rep_3', 'rep_4', ('rep_1', 'rep_3'), ('rep_2', 'rep_4'), slice(None)]

    players = list('player_{}'.format(i) for i in range(0, len(df.index.levels[1])))
    players.insert(0, 'all')

    idx_players = players.copy()
    idx_players[0] = slice(None)

    two_cols = pd.MultiIndex.from_product([reps, players])

    if hue == 'sound':
        lvl1 = ['uni', 'multi']
        multi_cols = pd.MultiIndex.from_product([lvl1, reps, players])

        uni_data = df.loc[df['sound'] == 'uni']
        uni_mean = pd.DataFrame(index=df.columns, columns=two_cols)

        for i in range(0, len(reps)):
            for j in range(0, len(players)):
                temp = uni_data.loc[(idx_reps[i], idx_players[j], slice(None)), :].mean()
                uni_mean[reps[i], players[j]] = temp

        multi_data = df.loc[df['sound'] == 'multi']
        multi_mean = pd.DataFrame(index=df.columns, columns=two_cols)

        for i in range(0, len(reps)):
            for j in range(0, len(players)):
                temp = multi_data.loc[(idx_reps[i], idx_players[j], slice(None)), :].mean()
                multi_mean[reps[i], players[j]] = temp

        df_mean = pd.DataFrame(index=df.columns, columns=multi_cols)

        df_mean['uni'] = uni_mean
        df_mean['multi'] = multi_mean

    else:
        df_mean = pd.DataFrame(index=df.columns, columns=two_cols)
        for i in range(0, len(idx_reps)):
            for j in range(0, len(idx_players)):
                temp = df.loc[(idx_reps[i], idx_players[j], slice(None)), :].mean()
                df.loc[reps[i], players[j], slice(None)] = temp

    return df_mean


def get_std_per_player(df, hue='sound'):
    """Only works with single columns df"""

    reps = ['rep_1', 'rep_2', 'rep_3', 'rep_4', 'rep_1_3', 'rep_2_4', 'all']
    idx_reps = ['rep_1', 'rep_2', 'rep_3', 'rep_4', ('rep_1', 'rep_3'), ('rep_2', 'rep_4'), slice(None)]

    players = list('player_{}'.format(i) for i in range(0, len(df.index.levels[1])))
    players.insert(0, 'all')

    idx_players = players.copy()
    idx_players[0] = slice(None)

    two_cols = pd.MultiIndex.from_product([reps, players])

    if hue == 'sound':
        lvl1 = ['uni', 'multi']
        multi_cols = pd.MultiIndex.from_product([lvl1, reps, players])

        uni_data = df.loc[df['sound'] == 'uni']
        uni_std = pd.DataFrame(index=df.columns, columns=two_cols)

        for i in range(0, len(reps)):
            for j in range(0, len(players)):
                temp = uni_data.loc[(idx_reps[i], idx_players[j], slice(None)), :].std()
                uni_std[reps[i], players[j]] = temp

        multi_data = df.loc[df['sound'] == 'multi']
        multi_std = pd.DataFrame(index=df.columns, columns=two_cols)

        for i in range(0, len(reps)):
            for j in range(0, len(players)):
                temp = multi_data.loc[(idx_reps[i], idx_players[j], slice(None)), :].std()
                multi_std[reps[i], players[j]] = temp

        df_std = pd.DataFrame(index=df.columns, columns=multi_cols)

        df_std['uni'] = uni_std
        df_std['multi'] = multi_std

    else:
        df_std = pd.DataFrame(index=df.columns, columns=two_cols)
        for i in range(0, len(idx_reps)):
            for j in range(0, len(idx_players)):
                temp = df.loc[(idx_reps[i], idx_players[j], slice(None)), :].std()
                df.loc[reps[i], players[j], slice(None)] = temp

    return df_std

