from pickling import load_pickle, create_pickle
from moves import Moves
import analyse
from analyse import AnalyseAdult
import matplotlib.pyplot as plt
import numpy as np

# # #
lst_adulte = list(range(1,11))
# # # amp1 = analyse.AnalyseAdult(lst_adulte, 'amp', 1)
# amp2 = analyse.AnalyseAdult(lst_adulte, 'amp', 2)
# amp3 = analyse.AnalyseAdult(lst_adulte, 'amp', 3)
# amp4 = analyse.AnalyseAdult(lst_adulte, 'amp', 4)
# # # # # # # # #
# # # # vit1 = analyse.AnalyseAdult(lst_adulte, 'vit', 1)
# vit2 = analyse.AnalyseAdult(lst_adulte, 'vit', 2)
# vit3 = analyse.AnalyseAdult(lst_adulte, 'vit', 3)
# vit4 = analyse.AnalyseAdult(lst_adulte, 'vit', 4)
# # # # # # # #
# # # # # # #
# # # #
# # # # # #
# create_pickle("adulte_amp_2", amp2)
# create_pickle("adulte_amp_3", amp3)
# create_pickle("adulte_amp_4", amp4)
# # # #
# create_pickle("adulte_vit_2", vit2)
# create_pickle("adulte_vit_3", vit3)
# create_pickle("adulte_vit_4", vit4)

amp2 = load_pickle("adulte_amp_2")
amp3 = load_pickle("adulte_amp_3")
amp4 = load_pickle("adulte_amp_4")

vit2 = load_pickle("adulte_vit_2")
vit3 = load_pickle("adulte_vit_3")
vit4 = load_pickle("adulte_vit_4")


# amp_sum_strat_df = AnalyseAdult.get_sum_strat([amp2,amp3,amp4])
# vit_sum_strat_df = AnalyseAdult.get_sum_strat([vit2,vit3,vit4])
# create_pickle('a_sum_strat_df_new_filt', amp_sum_strat_df)
# create_pickle('v_sum_strat_df_new_filt', vit_sum_strat_df)

#
#
# #
# a2 = Moves.from_analysis([load_pickle("adulte_amp_2")])
# a3 = Moves.from_analysis([load_pickle("adulte_amp_3")])
# a4 = Moves.from_analysis([load_pickle("adulte_amp_4")])
# # # #
# v2 = Moves.from_analysis([load_pickle("adulte_vit_2")])
# v3 = Moves.from_analysis([load_pickle("adulte_vit_3")])
# v4 = Moves.from_analysis([load_pickle("adulte_vit_4")])
# # #
#
# amp_df = AnalyseAdult.create_dataframe_from_analyse([amp2,amp3,amp4])
# vit_df = AnalyseAdult.create_dataframe_from_analyse([vit2,vit3,vit4])
# create_pickle('amp', amp_df)
# create_pickle('vit', vit_df)
#
# side_amp_df = AnalyseAdult.create_dataframe_from_analyse_sep_side([amp2,amp3,amp4])
# side_vit_df = AnalyseAdult.create_dataframe_from_analyse_sep_side([vit2,vit3,vit4])
# create_pickle('side_amp', side_amp_df)
# create_pickle('side_vit', side_vit_df)
# # #
# amp_jt_df = AnalyseAdult.get_all_joints_norm([amp2,amp3,amp4])
# amp_angle_df = AnalyseAdult.get_all_angle_norm([amp2,amp3,amp4])
# vit_jt_df = AnalyseAdult.get_all_joints_norm([vit2,vit3,vit4])
# vit_angle_df = AnalyseAdult.get_all_angle_norm([vit2,vit3,vit4])
#
# create_pickle('amp_angle_new_filt', amp_angle_df)
# create_pickle('vit_angle_new_filt', vit_angle_df)
# #
# create_pickle('amp_jt_new_filt', amp_jt_df)
# create_pickle('vit_jt_new_filt', vit_jt_df)
#
# # #
# amp_strat_df = AnalyseAdult.get_all_strats_norm([amp2,amp3,amp4])
# vit_strat_df = AnalyseAdult.get_all_strats_norm([vit2,vit3,vit4])
#
# create_pickle('amp_strat_new_filt', amp_strat_df)
# create_pickle('vit_strat_new_filt', vit_strat_df)
#
# missing_amp_df = AnalyseAdult.create_missing_value_df([amp2,amp3,amp4])
# missing_vit_df = AnalyseAdult.create_missing_value_df([vit2,vit3,vit4])
#
# create_pickle('missing_amp', missing_amp_df)
# create_pickle('missing_vit', missing_vit_df)


# amp_raw_joint_df = AnalyseAdult.get_all_joints([amp2, amp3, amp4])
# amp_raw_angle_df =AnalyseAdult.get_all_angle([amp2, amp3, amp4])
# vit_raw_joint_df = AnalyseAdult.get_all_joints([vit2, vit3, vit4])
# vit_raw_angle_df = AnalyseAdult.get_all_angle([vit2, vit3, vit4])
#
# create_pickle('amp_not_norm_joint_df_new_filt', amp_raw_joint_df)
# create_pickle('amp_not_norm_angle_df_new_filt', amp_raw_angle_df)
# create_pickle('vit_not_norm_joint_df_new_filt', vit_raw_joint_df)
# create_pickle('vit_not_norm_angle_df_new_filt', vit_raw_angle_df)

amp_raw_ankle_df = AnalyseAdult.get_all_ankle([amp2, amp3, amp4])
vit_raw_ankle_df = AnalyseAdult.get_all_ankle([vit2, vit3, vit4])



def plot_state(rep1,rep2, name1, name2, c1, c2):
    import matplotlib.pyplot as plt
    al1,at1 = rep1.angle_lower.rel_arr, rep1.angle_trunk.rel_arr
    al2, at2 = rep2.angle_lower.rel_arr, rep2.angle_trunk.rel_arr

    xm,xM = min(al1.min(), al2.min()), max(al1.max(), al2.max())
    ym,yM = min(at1.min(), at2.min()), max(at1.max(), at2.max())


    fig, axes = plt.subplots(nrows=2)


    axes[0].plot(al1,at1,color = c1, label =name1)
    axes[0].set_xlim([xm,xM])
    axes[0].set_ylim([ym,yM])

    axes[1].plot(al2,at2,color = c2, label = name2)
    axes[1].set_xlim([xm,xM])
    axes[1].set_ylim([ym,yM])
    fig.legend(loc='best')
    plt.show()


def write_log_cm(fileName, moves):
    line = "{patient},{rep},{move_id},{have_cm}"

    with open(fileName +".csv", 'w+') as f:
        f.write("patient,rep,move_id,have_cm\n")
        for m in moves:
            h_cm = 1 if m.COF.cm.have_cm else 0
            f.write(line.format(patient=m.player_id,rep=m.analyse_name, move_id=m.move_id, have_cm =h_cm))
            f.write("\n")
    print(fileName, " created")

def plot_info_rep(p, data,dtype_threshold = 'cof',name=''):
    import matplotlib.pyplot as plt

    ax = plt.subplot()
    ax.set_title(name)
    ax.plot(data.players[p].rep.com.x_arr, color='b', label='com')
    ax.plot(data.players[p].rep.cof.x_arr, color='k', label='cof')
    ax.plot(data.players[p].rep.ankle_r.x_arr, color='g', label='ankle_r')
    ax.plot(data.players[p].rep.ankle_l.x_arr, color='c', label='ankle_l')
    ax.legend(loc='best')

    dt =dtype_threshold
    ax.hlines(data.players[p].all_moves[0].player_threshold["mean"][dt]+data.players[p].all_moves[0].player_threshold["std"][dt]
              , 0, len(data.players[p].rep), color='r')

    ax.hlines(data.players[p].all_moves[0].player_threshold["mean"][dt],0,len(data.players[p].rep),color='y')

    ax.hlines(data.players[p].all_moves[0].player_threshold["mean"][dt]-data.players[p].all_moves[0].player_threshold["std"][dt]
              , 0, len(data.players[p].rep), color='r')
    if name != '':
        plt.savefig(name + ".png")
        plt.close()



def plot_posturographie(i,data_list, dtype_threshold = 'cof'):
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    ax.plot(data_list[i].ankle_r.x_arr, color = 'g')
    ax.plot(data_list[i].ankle_l.x_arr, color='c')

    ax.plot(data_list[i].com.x_arr, color='b')
    ax.plot(data_list[i].cof.x_arr, color='k')

    dt =dtype_threshold
    ax.hlines(data_list[i].player_threshold["mean"][dt]+data_list[i].player_threshold["std"][dt]
              , 0, len(data_list[i].cof), color='c')

    ax.hlines(data_list[i].player_threshold["mean"][dt],0,len(data_list[i].cof),color='k')

    ax.hlines(data_list[i].player_threshold["mean"][dt]-data_list[i].player_threshold["std"][dt]
              , 0, len(data_list[i].cof), color='c')

def plot_move(move):
    fig = plt.figure(figsize=(19, 10.8))
    ax = plt.subplot()
    cof = move.cof.x_arr
    a_l = move.ankle_l.x_arr
    a_r = move.ankle_r.x_arr
    com = move.com.x_arr
    dt = 'cof'

    ax.plot(cof, color ='k', label='cof')
    ax.plot(com, color ='b', label='com')
    ax.plot(a_r, color ='g', label='ankle_r')
    ax.plot(a_l, color ='c', label='ankle_l')

    ax.hlines(move.player_threshold["mean"][dt] + move.player_threshold["std"][dt], 0,
              len(move.cof), color='c')

    ax.hlines(move.player_threshold["mean"][dt], 0, len(move.cof), color='k')

    ax.hlines(move.player_threshold["mean"][dt] - move.player_threshold["std"][dt], 0,
              len(move.cof), color='c')

    ax.legend(loc='best')
    title = "rep{}_p{}_m{}".format(move.rep, move.player_id, move.move_id)
    plt.savefig(title + ".png")
    plt.close()






print("done")