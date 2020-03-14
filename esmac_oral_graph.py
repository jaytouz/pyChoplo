from pickling import load_pickle
from moves import Moves
import numpy as np
import matplotlib.pyplot as plt


def get_describe(condition):
    m, std = condition.describe()
    return m, std

def get_event_index(mean):
    from counter_movement import CounterMovement
    mean.COF.cm = CounterMovement(mean.COF.x_arr, 10)
    mean.COF.set_event()

    mean.COM.set_event()

    mean.C7.set_event()

def plot_joint(mean, std, drop_end, name="", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False):
    """Creates a plot with the lower angle"""
    import matplotlib as mpl
    mpl.rcParams['hatch.linewidth'] = 0.1
    SMALL_SIZE = 25
    MEDIUM_SIZE = 30
    BIGGER_SIZE = 35

    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)

    plt.style.use("seaborn-poster")
    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5, forward=True)


    ax = plt.subplot()
    ax.grid(True)

    cof = mean.COF.x_arr[75:] # error, 75 data before drop. Probably since pre_drop_data was create
    com = mean.COM.x_arr[75:]
    c7 = mean.C7.x_arr[75:]
    time = np.linspace(0, len(cof)/50, len(cof))


    if show_cof_event:
        ax.fill_between(time[mean.COF.cm.start_index-75:mean.COF.cm.end_index-75], cof[mean.COF.cm.start_index-75:mean.COF.cm.end_index-75], mean.COF.cm.start_val, hatch = '/', facecolors="#a9c5f2", label = "CoF's absement")
        ax.scatter((mean.COF.max_vel.index-75)/50, mean.COF.max_vel.val, s=200, c='k', marker='s', label = "peak velocity")
        ax.scatter((mean.COF.max_amp.index-75)/50, mean.COF.max_amp.val, s=200, c='k', marker='p', label = "peak amplitude")

    if show_com_event:
        ax.scatter((mean.COM.max_vel.index-75)/50, mean.COM.max_vel.val, s=200, c='k', marker='s')
        ax.scatter((mean.COM.max_amp.index-75)/50, mean.COM.max_amp.val, s=200, c='k', marker='p')
    if show_c7_event:
        ax.scatter((mean.C7.max_vel.index-75)/50, mean.C7.max_vel.val, s=200, c='k', marker='s')
        ax.scatter((mean.C7.max_amp.index-75)/50, mean.C7.max_amp.val, s=200, c='k', marker='p')



    ax.plot(time, cof, '-', color='k', label="CoF's displacement")
    if show_std:
        ax.fill_between(time, cof - std.COF.x_arr[75:], cof+std.COF.x_arr[75:], facecolors= 'k',color = 'k', alpha=0.1)

    ax.plot(time, com, '--', color='b', label="SBjt's displacement")
    if show_std:
        ax.fill_between(time, com - std.COM.x_arr[75:], com+std.COM.x_arr[75:], facecolors= 'b',color = 'b', alpha=0.1)

    ax.plot(time, c7, '-.', color='r', label="MSjt's displacement")
    if show_std:
        ax.fill_between(time, c7 - std.C7.x_arr[75:], c7+std.C7.x_arr[75:], facecolors= 'r', color = 'r', alpha=0.1)

    if drop_end is not None:
        ax.vlines(time[drop_end], min(cof) -0.04, max(c7) + 0.04, color='b')

    plt.ylim([-0.03, 0.175])
    plt.xlim([0,9])
    #
    # if v_line_drop_in:
    #     ax.axvline(0, ymin=min_data_vline, ymax=max_data_vline, color='#006600')
    # if v_line_drop_end:
    #     ax.axvline(move.drop_end, ymin=min_data_vline, ymax=max_data_vline, color='#800000')

    ax.legend(loc="best", prop={'size': 20})
    plt.ylabel("Position (m)", fontsize=40)
    plt.xlabel("Time (s)", fontsize=40)
    plt.tight_layout()
    plt.savefig(name + ".pdf", dpi = 400)


def get_drop_end_index(cond):
    d_e = []
    for i in range(0, len(cond)):
        d_e.append(cond[i].drop_end_index)
    drop_end_index = int(np.array(d_e).mean())
    print(drop_end_index)
    return drop_end_index


def add_cof_to_plot(mean_lvl, std_lvl, ax, lvl_c, drop_end, label, event_m_size=400, show_drop_end=True, show_std = True, show_cof_event=False):

    cof = mean_lvl.COF.x_arr[75:]  # error, 75 data before drop. Probably since pre_drop_data was create
    c7 = mean_lvl.C7.x_arr[75:]
    time = np.linspace(0, len(cof) / 50, len(cof))

    if show_cof_event:
        # ax.fill_between(time[mean_lvl.COF.cm.start_index-75:mean_lvl.COF.cm.end_index-75], cof[mean_lvl.COF.cm.start_index-75:mean_lvl.COF.cm.end_index-75], mean_lvl.COF.cm.start_val, hatch = '/', facecolors="#a9c5f2")
        ax.scatter((mean_lvl.COF.max_vel.index-75)/50, mean_lvl.COF.max_vel.val, s=event_m_size, c=lvl_c, marker='s')
        ax.scatter((mean_lvl.COF.max_amp.index-75)/50, mean_lvl.COF.max_amp.val, s=event_m_size, c=lvl_c, marker='p')


    ax.plot(time, cof, '-', color=lvl_c, label=label)
    if show_std:
        ax.fill_between(time, cof - std_lvl.COF.x_arr[75:], cof+std_lvl.COF.x_arr[75:], facecolors= lvl_c,color = lvl_c, alpha=0.1)

    if show_drop_end:
        ax.vlines(time[drop_end], min(cof) -0.04, max(c7) + 0.04, color=lvl_c)


    ax.legend(loc='best')


def add_com_to_plot(mean_lvl, std_lvl, ax, lvl_c, drop_end, label, event_m_size=400, show_drop_end=True, show_std = True, show_com_event=False):

    cof = mean_lvl.COF.x_arr[75:]  # error, 75 data before drop. Probably since pre_drop_data was create
    com = mean_lvl.COM.x_arr[75:]
    c7 = mean_lvl.C7.x_arr[75:]
    time = np.linspace(0, len(cof) / 50, len(cof))

    if show_com_event:
        ax.scatter((mean_lvl.COM.max_vel.index-75)/50, mean_lvl.COM.max_vel.val, s=event_m_size, c=lvl_c, marker='s')
        ax.scatter((mean_lvl.COM.max_amp.index-75)/50, mean_lvl.COM.max_amp.val, s=event_m_size, c=lvl_c, marker='p')

    ax.plot(time, com, '--', color=lvl_c, label=label)
    if show_std:
        ax.fill_between(time, com - std_lvl.COM.x_arr[75:], com+std_lvl.COM.x_arr[75:], facecolors= lvl_c,color = lvl_c, alpha=0.1)

    if show_drop_end:
        ax.vlines(time[drop_end], min(cof) -0.04, max(c7) + 0.04, color=lvl_c)


    ax.legend(loc="best")



def add_c7_to_plot(mean_lvl, std_lvl, ax, lvl_c, drop_end, label, event_m_size=400, show_drop_end=True, show_std = True, show_c7_event=False):

    cof = mean_lvl.COF.x_arr[75:]  # error, 75 data before drop. Probably since pre_drop_data was create
    c7 = mean_lvl.C7.x_arr[75:]
    time = np.linspace(0, len(cof) / 50, len(cof))

    if show_c7_event:
        ax.scatter((mean_lvl.C7.max_vel.index-75)/50, mean_lvl.C7.max_vel.val, s=event_m_size, c=lvl_c, marker='s')
        ax.scatter((mean_lvl.C7.max_amp.index-75)/50, mean_lvl.C7.max_amp.val, s=event_m_size, c=lvl_c, marker='p')

    ax.plot(time, c7, '-.', color=lvl_c, label=label)
    if show_std:
        ax.fill_between(time, c7 - std_lvl.C7.x_arr[75:], c7+std_lvl.C7.x_arr[75:], facecolors= lvl_c, color = lvl_c, alpha=0.1)

    if show_drop_end:
        ax.vlines(time[drop_end], min(cof) -0.04, max(c7) + 0.04, color=lvl_c)


    ax.legend(loc="best")


def plot_level_by_joint(lvl1=None, lvl2=None, lvl3=None, lvl4=None, event_m_size=400, show_std=False, show_drop_end=True, show_cof_event=True, show_com_event=True, show_c7_event=True, save=False, savename=""):
    import matplotlib as mpl
    mpl.rcParams['hatch.linewidth'] = 0.1
    SMALL_SIZE = 20
    MEDIUM_SIZE = 40
    BIGGER_SIZE = 50

    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
    fig.set_size_inches(18.5, 10.5, forward=True)

    ax1 = axes[0]
    ax2 = axes[1]
    ax3 = axes[2]


    if lvl1 is not None:
        drop_end1 = get_drop_end_index(lvl1)
        mean1, std1 = get_describe(lvl1)
        get_event_index(mean1)
        add_c7_to_plot(mean1, std1, ax1, 'g', drop_end1, "level 1", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_c7_event=show_c7_event)
        add_com_to_plot(mean1, std1, ax2, 'g', drop_end1, "level 1", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_com_event=show_com_event)
        add_cof_to_plot(mean1, std1, ax3, 'g', drop_end1, "level 1", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_cof_event=show_cof_event)


    if lvl2 is not None:
        drop_end2 = get_drop_end_index(lvl2)
        mean2, std2 = get_describe(lvl2)
        get_event_index(mean2)
        add_c7_to_plot(mean2, std2, ax1, 'b', drop_end2, "level 2", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_c7_event=show_c7_event)
        add_com_to_plot(mean2, std2, ax2, 'b', drop_end2, "level 2", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_com_event=show_com_event)
        add_cof_to_plot(mean2, std2, ax3, 'b', drop_end2, "level 2", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_cof_event=show_cof_event)

    if lvl3 is not None:
        drop_end3 = get_drop_end_index(lvl3)
        mean3, std3 = get_describe(lvl3)
        get_event_index(mean3)
        add_c7_to_plot(mean3, std3, ax1, 'k', drop_end3, "level 3", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_c7_event=show_c7_event)
        add_com_to_plot(mean3, std3, ax2, 'k', drop_end3, "level 3", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_com_event=show_com_event)
        add_cof_to_plot(mean3, std3, ax3, 'k', drop_end3, "level 3", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_cof_event=show_cof_event)

    if lvl4 is not None:
        drop_end4 = get_drop_end_index(lvl4)
        mean4, std4 = get_describe(lvl4)
        get_event_index(mean4)
        add_c7_to_plot(mean4, std4, ax1, 'r', drop_end4, "level 4", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_c7_event=show_c7_event)
        add_com_to_plot(mean4, std4, ax2, 'r', drop_end4, "level 4", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_com_event=show_com_event)
        add_cof_to_plot(mean4, std4, ax3, 'r', drop_end4, "level 4", event_m_size=event_m_size, show_drop_end=show_drop_end, show_std = show_std, show_cof_event=show_cof_event)


    plt.ylim([-0.03, 0.175])
    plt.xlim([0,6])
    plt.tight_layout()
    fig.subplots_adjust(hspace=0.04)
    i = 1
    for a in fig.axes:
        if i <=2:
            T = [-0.05, 0, 0.05, 0.1, 0.15]
            a.set_yticks(T)
            L = [" ", "0", "0.05", "0.1", "0.15"]
            a.set_yticklabels(L)
        else:
            T = [-0.05, 0, 0.05, 0.1, 0.15]
            a.set_yticks(T)
            L = ["-0.05", "0", "0.05", "0.1", "0.15"]
            a.set_yticklabels(L)
        i+=1
    plt.setp([a.get_xticklabels() for a in fig.axes[1:2]], visible=False)

    # plt.xlabel("TIME (s)")
    # plt.ylabel("Displacement (m)")
    if save:
        plt.savefig(savename + ".png", dpi=400)

def plot_cm(lvl1=None, lvl2=None, lvl3=None, lvl4=None, event_m_size=400, show_std=False, show_cof_event=True, save=False, savename=""):
    import matplotlib as mpl
    mpl.rcParams['hatch.linewidth'] = 0.1
    SMALL_SIZE = 20
    MEDIUM_SIZE = 40
    BIGGER_SIZE = 50

    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)

    fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
    fig.set_size_inches(18.5, 10.5, forward=True)


    if lvl1 is not None:
        drop_end1 = get_drop_end_index(lvl1)
        mean1, std1 = get_describe(lvl1)
        get_event_index(mean1)
        add_cof_to_plot(mean1, std1, ax1, 'g', drop_end1, "level 1", event_m_size=event_m_size, show_drop_end=False, show_std = show_std, show_cof_event=show_cof_event)


    if lvl2 is not None:
        drop_end2 = get_drop_end_index(lvl2)
        mean2, std2 = get_describe(lvl2)
        get_event_index(mean2)
        add_cof_to_plot(mean2, std2, ax1, 'b', drop_end2, "level 2", event_m_size=event_m_size, show_drop_end=False, show_std = show_std, show_cof_event=show_cof_event)

    if lvl3 is not None:
        drop_end3 = get_drop_end_index(lvl3)
        mean3, std3 = get_describe(lvl3)
        get_event_index(mean3)
        add_cof_to_plot(mean3, std3, ax1, 'k', drop_end3, "level 3", event_m_size=event_m_size, show_drop_end=False, show_std = show_std, show_cof_event=show_cof_event)

    if lvl4 is not None:
        drop_end4 = get_drop_end_index(lvl4)
        mean4, std4 = get_describe(lvl4)
        get_event_index(mean4)
        add_cof_to_plot(mean4, std4, ax1, 'r', drop_end4, "level 4", event_m_size=event_m_size, show_drop_end=False, show_std = show_std, show_cof_event=show_cof_event)


    plt.ylim([-0.03, 0.1])
    plt.xlim([0,2])
    plt.tight_layout()

    T = [-0.03, 0, 0.05, 0.1]
    ax1.set_yticks(T)
    L = ["-0.03", "0", "0.05", "0.1"]
    ax1.set_yticklabels(L)

    # plt.xlabel("TIME (s)")
    # plt.ylabel("Displacement (m)")
    if save:
        plt.savefig(savename + ".png", dpi=400)

def plot_move_against_avg(cond, index, show_move=True, show_mean=False, show_std=True, hide_ticks=True):
    drop_end = get_drop_end_index(cond)
    mean, std = get_describe(cond)
    get_event_index(mean)

    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5, forward=True)

    ax = plt.subplot()
    mean_cof = mean.COF.x_arr[75:]  # error, 75 data before drop. Probably since pre_drop_data was create
    arr = np.zeros(len(mean_cof))

    move_cof = cond[index].COF.x_arr[75:]
    move_cof = arr + move_cof[0:len(mean_cof)]

    time = np.linspace(0, len(mean_cof)/50, len(mean_cof))
    if show_mean:
        ax.plot(time, mean_cof, '--', color='k')
    if show_move:
        ax.plot(time, move_cof, color = 'k')
    if show_std:
        ax.fill_between(time, mean_cof - std.COF.x_arr[75:], mean_cof + std.COF.x_arr[75:], facecolors='k', color='k', alpha=0.1)

    if hide_ticks:
        plt.xticks([], [])
        plt.yticks([], [])
    plt.tight_layout()
    plt.xlim(0, max())



def plot_condition(cond, name="", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False):
    drop_end = get_drop_end_index(cond)
    mean, std = get_describe(cond)
    get_event_index(mean)

    plot_joint(mean, std, drop_end, name=name,show_std = show_std, show_cof_event=show_cof_event, show_com_event=show_com_event, show_c7_event=show_c7_event)




#
# amp1_full_data, amp1 = load_pickle("adulte_amp_1"), Moves.from_analysis([load_pickle("adulte_amp_1")])
# amp2_full_data, amp2 = load_pickle("adulte_amp_2"), Moves.from_analysis([load_pickle("adulte_amp_2")])
# amp3_full_data, amp3 = load_pickle("adulte_amp_3"), Moves.from_analysis([load_pickle("adulte_amp_3")])
# amp4_full_data, amp4 = load_pickle("adulte_amp_4"), Moves.from_analysis([load_pickle("adulte_amp_4")])
# # #
# vit1_full_data, vit1 = load_pickle("adulte_vit_1"), Moves.from_analysis([load_pickle("adulte_vit_1")])
# vit2_full_data, vit2 = load_pickle("adulte_vit_2"), Moves.from_analysis([load_pickle("adulte_vit_2")])
# vit3_full_data, vit3 = load_pickle("adulte_vit_3"), Moves.from_analysis([load_pickle("adulte_vit_3")])
# vit4_full_data, vit4 = load_pickle("adulte_vit_4"), Moves.from_analysis([load_pickle("adulte_vit_4")])
#
amp_td_full_data, amp_td = load_pickle("amp_td"), Moves.from_analysis([load_pickle("amp_td")])
vit_td_full_data, vit_td = load_pickle("vit_td"), Moves.from_analysis([load_pickle("vit_td")])
# plot_condition(amp1,name = "amp1_std", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False)
# plot_condition(amp1, name = "amp1_event", show_std = False, show_cof_event=True, show_com_event=True, show_c7_event=True)
#
# plot_condition(amp2,name = "amp2_std", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False)
# plot_condition(amp2, name = "amp2_event", show_std = False, show_cof_event=True, show_com_event=True, show_c7_event=True)
#
# plot_condition(amp3,name = "amp3_std", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False)
# plot_condition(amp3, name = "amp3_event", show_std = False, show_cof_event=True, show_com_event=True, show_c7_event=True)
#
# plot_condition(amp4,name = "amp4_std", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False)
# plot_condition(amp4, name = "amp4_event", show_std = False, show_cof_event=True, show_com_event=True, show_c7_event=True)
#
# plot_condition(vit1,name = "vit1_std", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False)
# plot_condition(vit1, name = "vit1_event", show_std = False, show_cof_event=True, show_com_event=True, show_c7_event=True)
#
# plot_condition(vit2,name = "vit2_std", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False)
# plot_condition(vit2, name = "vit2_event", show_std = False, show_cof_event=True, show_com_event=True, show_c7_event=True)
#
# plot_condition(vit3,name = "vit3_std", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False)
# plot_condition(vit3, name = "vit3_event", show_std = False, show_cof_event=True, show_com_event=True, show_c7_event=True)
#
# plot_condition(vit4,name = "vit4_std", show_std = True, show_cof_event=False, show_com_event=False, show_c7_event=False)
# plot_condition(vit4, name = "vit4_event", show_std = False, show_cof_event=True, show_com_event=True, show_c7_event=True)



# plot_level_by_joint(amp1, amp2, amp3, amp4, save=True, savename="amplitude_no_std")
# plot_level_by_joint(vit1, vit2, vit3, vit4, save=True, savename="speed_no_std")

# plot_cm(amp1, amp2, amp3, amp4, show_cof_event=False, show_std=True, save=True, savename="cm_amp_std")
# plot_cm(amp1, amp2, amp3, amp4, show_cof_event=True, show_std=False, save=True, savename="cm_amp_event")
#
# plot_cm(vit1, vit2, vit3, vit4, show_cof_event=False, show_std=True, save=True, savename="cm_vit_std")
# plot_cm(vit1, vit2, vit3, vit4, show_cof_event=True, show_std=False, save=True, savename="cm_vit_event")

plot_level_by_joint(amp_td, show_std=True, show_cof_event=False, show_com_event=False, show_c7_event=False, save=True, savename="amplitude_std_no_event")
plot_level_by_joint(vit_td, show_std=True, show_cof_event=False, show_com_event=False, show_c7_event=False, show_drop_end=True, save=True, savename="speed_std_no_event")
#


print("DONE")