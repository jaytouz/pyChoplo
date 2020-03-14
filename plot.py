import matplotlib.pyplot as plt
import numpy as np


def plot_cof_and_return_ax(move, ax=None, fig=None, v_line_drop_in=True, v_line_drop_end=True, add_vel=True,
                           add_accel=True, event_patch=True, move_reaction_time=True, player_reaction_time=True,
                           add_phase=False, add_pre_drop_threshold=True):
    """Creates a plot with the cof and events"""

    plt.style.use("seaborn-poster")
    show = False
    pax = None
    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(18.5, 10.5, forward=True)
        fig.suptitle(
            "PlayerID : {p} - MoveID : {m} - {dt} - Side : {s}".format(p=move.player_id, m=move.move_id, dt="cof",
                                                                       s=move.side))

    if ax is None:
        ax = plt.subplot()
        ax.grid(True)
        show = True

    time = move.t_norm
    displ = move.cof.x_arr
    vel = move.cof.vel_x
    accel = move.cof.accel_x
    min_data_pax = min([min(move.cof.x_arr), min(move.pelvis.x_arr), min(move.c7.x_arr)])
    max_data_vline = max([max(move.cof.x_arr), max(move.pelvis.x_arr), max(move.c7.x_arr)])

    # DISPLACEMENT
    ax.plot(time, displ, '-', color='k', label="cof's displacement")
    if v_line_drop_in:
        ax.axvline(0, ymin=min_data_pax, ymax=max_data_vline, color='#006600')
    if v_line_drop_end:
        ax.axvline(move.drop_end, ymin=min_data_pax, ymax=max_data_vline, color='#800000')

    if event_patch:
        if move.cof.cm.have_cm:
            add_patch(ax, move.cof.cm.start_cm.index, displ[move.cof.cm.start_cm.index], "cm", facecolor='g',
                      size=10)  # start_cm
            add_patch(ax, move.cof.cm.rel_pt.index, displ[move.cof.cm.rel_pt.index], "r", facecolor='b',
                      size=10)  # rel_pnt_cm
            add_patch(ax, move.cof.cm.end_cm.index, displ[move.cof.cm.end_cm.index], "e", facecolor='r', size=10)  # end_cm
        add_patch(ax, move.cof.max_vel.index, displ[move.cof.max_vel.index], "vel", facecolor='r', size=10)  # max_vel
        add_patch(ax, move.cof.max_amp.index, displ[move.cof.max_amp.index], "amp", facecolor='r', size=10)  # max_amp

    if add_vel:
        ax.plot(time, vel, '--', color='k', label="cof's velocity")
        if event_patch:
            if move.cof.cm.have_cm:
                add_patch(ax, move.cof.cm.start_cm.index, vel[move.cof.cm.start_cm.index], "cm", facecolor='g',
                          size=10)  # start_cm
                add_patch(ax, move.cof.cm.rel_pt.index, vel[move.cof.cm.rel_pt.index], "r", facecolor='b',
                          size=10)  # rel_pnt_cm
                add_patch(ax, move.cof.cm.end_cm.index, vel[move.cof.cm.end_cm.index], "e", facecolor='r', size=10)  # end_cm
            add_patch(ax, move.cof.max_vel.index, vel[move.cof.max_vel.index], "vel", facecolor='r', size=10)  # max_vel
            add_patch(ax, move.cof.max_amp.index, vel[move.cof.max_amp.index], "amp", facecolor='r', size=10)  # max_amp

    if add_accel:
        ax.plot(time, accel, ':', color='k', label="cof's acceleration")
        if event_patch:
            if move.cof.cm.have_cm:
                add_patch(ax, move.cof.cm.start_cm.index, accel[move.cof.cm.start_cm.index], "cm", facecolor='g',
                          size=10)  # start_cm
                add_patch(ax, move.cof.cm.rel_pt.index, accel[move.cof.cm.rel_pt.index], "r",
                          facecolor='b', size=10)  # rel_pnt_cm
                add_patch(ax, move.cof.cm.end_cm.index, accel[move.cof.cm.end_cm.index], "e", facecolor='r',
                          size=10)  # end_cm
            add_patch(ax, move.cof.max_vel.index, accel[move.cof.max_vel.index], "vel", facecolor='b',
                      size=10)  # max_vel
            add_patch(ax, move.cof.max_amp.index, accel[move.cof.max_amp.index], "amp", facecolor='b',
                      size=10)  # max_amp

    if add_phase:
        pax = ax.scatter(time, (np.ones(len(time)) * min_data_pax) - 0.02, c=move.gamma_angle.gamma, marker='s', s=1000,
                         linewidths=1, cmap=plt.cm.brg)
        if show:
            position = fig.add_axes([0.25, 0.04, 0.5, 0.02])  # posHori, posVert, length, height
            cb = fig.colorbar(pax, ax=ax, cax=position, orientation='horizontal')
            cb.set_ticks([-0.9, 0, 0.9])
            cb.set_ticklabels(["100%  Out-of-Phase", "neutral", "In-Phase  100%"])
            pax.set_clim(-1.0, 1.0)

    if move_reaction_time:
        add_patch(ax, move.cof.reaction_time_from_move.index, displ[move.cof.reaction_time_from_move.index], "m",
                  facecolor='#ff33ff', size=10)  # reaction_time
        if add_pre_drop_threshold:
            y_mean = move.pre_drop_mean_data['cof']
            std = move.pre_drop_std_data['cof']
            y_std_up = y_mean + std
            y_std_down = y_mean - std

            ax.hlines(y_mean, xmin=0, xmax=len(move) - 1, alpha=0.5, color='#660066')
            ax.hlines(y_std_up, linestyles="--", xmin=0, xmax=len(move) - 1, alpha=0.5, color='#ffccff')
            ax.hlines(y_std_down, linestyles="--", xmin=0, xmax=len(move) - 1, alpha=0.5, color='#ffccff')

    if player_reaction_time:
        add_patch(ax, move.cof.reaction_time_from_player.index, displ[move.cof.reaction_time_from_player.index], "m",
                  facecolor='#212F3C', size=10)  # reaction_time
        if add_pre_drop_threshold:
            y_mean = move.player_threshold["mean"]['cof']
            std = move.player_threshold["std"]['cof']
            y_std_up = y_mean + std
            y_std_down = y_mean - std

            ax.hlines(y_mean, xmin=0, xmax=len(move) - 1, alpha=0.5, color='#212F3C')
            ax.hlines(y_std_up, linestyles="--", xmin=0, xmax=len(move) - 1, alpha=0.5, color='#3498DB')
            ax.hlines(y_std_down, linestyles="--", xmin=0, xmax=len(move) - 1, alpha=0.5, color='#3498DB')

    ax.legend(loc="best")

    plot_object = {"ax": ax, "pax": pax}

    if show:
        plt.show()
        return plot_object
    else:
        return plot_object


def plot_c7_and_return_ax(move, ax=None, fig=None, v_line_drop_in=True, v_line_drop_end=True, add_vel=True,
                          add_accel=True, event_patch=True, add_phase=False, add_pre_drop_threshold=False):
    """Creates a plot with the c7 and events"""
    plt.style.use("seaborn-poster")
    show = False
    pax = None

    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(18.5, 10.5, forward=True)
        fig.suptitle(
            "PlayerID : {p} - MoveID : {m} - {dt} - Side : {s}".format(p=move.player_id, m=move.move_id, dt="MJjt",
                                                                       s=move.side))

    if ax is None:
        ax = plt.subplot()
        ax.grid(True)
        show = True

    time = move.t_norm
    displ = move.c7.x_arr
    vel = move.c7.vel_x
    accel = move.c7.accel_x
    min_data_pax = min([min(move.cof.x_arr), min(move.pelvis.x_arr), min(move.c7.x_arr)])
    max_data_vline = max([max(move.cof.x_arr), max(move.pelvis.x_arr), max(move.c7.x_arr)])

    # DISPLACEMENT
    ax.plot(time, displ, '-', color='r', label="MSjt's displacement")

    if v_line_drop_in:
        ax.axvline(0, ymin=min_data_pax, ymax=max_data_vline, color='#006600')
    if v_line_drop_end:
        ax.axvline(move.drop_end, ymin=min_data_pax, ymax=max_data_vline, color='#800000')

    if event_patch:
        if move.cof.cm.have_cm:
            add_patch(ax, move.cof.cm.start_cm.index, displ[move.cof.cm.start_cm.index], "cm", facecolor='g',
                      size=3)  # start_cm
            add_patch(ax, move.cof.cm.rel_pt.index, displ[move.cof.cm.rel_pt.index], "r", facecolor='b',
                      size=3)  # rel_pnt_cm
            add_patch(ax, move.cof.cm.end_cm.index, displ[move.cof.cm.end_cm.index], "e", facecolor='r', size=10)  # end_cm
        add_patch(ax, move.c7.max_vel.index, displ[move.c7.max_vel.index], "vel", facecolor='r', size=10)  # max_vel
        add_patch(ax, move.c7.max_amp.index, displ[move.c7.max_amp.index], "amp", facecolor='r', size=10)  # max_amp

    if add_vel:
        ax.plot(time, vel, '--', color='r', label="MSjt's velocity")
        if event_patch:
            if move.cof.cm.have_cm:
                add_patch(ax, move.cof.cm.start_cm.index, vel[move.cof.cm.start_cm.index], "cm", facecolor='g',
                          size=10)  # start_cm
                add_patch(ax, move.cof.cm.rel_pt.index, vel[move.cof.cm.rel_pt.index], "r", facecolor='b',
                          size=10)  # rel_pnt_cm
                add_patch(ax, move.cof.cm.end_cm.index, vel[move.cof.cm.end_cm.index], "e", facecolor='r', size=10)  # end_cm
            add_patch(ax, move.c7.max_vel.index, vel[move.c7.max_vel.index], "vel", facecolor='r', size=10)  # max_vel
            add_patch(ax, move.c7.max_amp.index, vel[move.c7.max_amp.index], "amp", facecolor='r', size=10)  # max_amp

    if add_accel:
        ax.plot(time, accel, ':', color='r', label="MSjt's acceleration")
        if event_patch:
            if move.cof.cm.have_cm:
                add_patch(ax, move.cof.cm.start_cm.index, accel[move.cof.cm.start_cm.index], "cm", facecolor='g',
                          size=10)  # start_cm
                add_patch(ax, move.cof.cm.rel_pt.index, accel[move.cof.cm.rel_pt.index], "r",
                          facecolor='b', size=10)  # rel_pnt_cm
                add_patch(ax, move.cof.cm.end_cm.index, accel[move.cof.cm.end_cm.index], "e", facecolor='r',
                          size=10)  # end_cm
            add_patch(ax, move.c7.max_vel.index, accel[move.c7.max_vel.index], "vel", facecolor='b', size=10)  # max_vel
            add_patch(ax, move.c7.max_amp.index, accel[move.c7.max_amp.index], "amp", facecolor='b', size=10)  # max_amp

    if add_phase:
        pax = ax.scatter(time, (np.ones(len(time)) * min_data_pax) - 0.02, c=move.gamma_angle.gamma, marker='s', s=1000,
                         linewidths=1, cmap=plt.cm.brg)
        if show:
            position = fig.add_axes([0.25, 0.04, 0.5, 0.02])  # posHori, posVert, length, height
            cb = fig.colorbar(pax, ax=ax, cax=position, orientation='horizontal')
            cb.set_ticks([-0.9, 0, 0.9])
            cb.set_ticklabels(["100%  Out-of-Phase", "neutral", "In-Phase  100%"])
            pax.set_clim(-1.0, 1.0)

    plot_object = {"ax": ax, "pax": pax}

    if show:
        plt.show()
        return plot_object
    else:
        return plot_object


def plot_pelvis_and_return_ax(move, ax=None, fig=None, v_line_drop_in=True, v_line_drop_end=True, add_vel=True,
                           add_accel=True, event_patch=True, add_phase=False, add_pre_drop_threshold=False):
    """Creates a plot with the pelvis and events"""
    plt.style.use("seaborn-poster")
    show = False
    pax = None

    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(18.5, 10.5, forward=True)
        fig.suptitle(
            "PlayerID : {p} - MoveID : {m} - {dt} - Side : {s}".format(p=move.player_id, m=move.move_id, dt="SBjt",
                                                                       s=move.side))

    if ax is None:
        ax = plt.subplot()
        ax.grid(True)
        show = True

    time = move.t_norm
    displ = move.pelvis.x_arr
    vel = move.pelvis.vel_x
    accel = move.pelvis.accel_x
    min_data_pax = min([min(move.cof.x_arr), min(move.pelvis.x_arr), min(move.c7.x_arr)])
    max_data_vline = max([max(move.cof.x_arr), max(move.pelvis.x_arr), max(move.c7.x_arr)])

    # DISPLACEMENT
    ax.plot(time, displ, '-', color='b', label="SBjt's displacement")
    if v_line_drop_in:
        ax.axvline(0, ymin=min_data_pax, ymax=max_data_vline, color='#006600')
    if v_line_drop_end:
        ax.axvline(move.drop_end, ymin=min_data_pax, ymax=max_data_vline, color='#800000')

    if event_patch:
        if move.cof.cm.have_cm:
            add_patch(ax, move.cof.cm.start_cm.index, displ[move.cof.cm.start_cm.index], "cm", facecolor='g',
                      size=3)  # start_cm
            add_patch(ax, move.cof.cm.rel_pt.index, displ[move.cof.cm.rel_pt.index], "r", facecolor='b',
                      size=3)  # rel_pnt_cm
            add_patch(ax, move.cof.cm.end_cm.index, displ[move.cof.cm.end_cm.index], "e", facecolor='r', size=10)  # end_cm
        add_patch(ax, move.pelvis.max_vel.index, displ[move.pelvis.max_vel.index], "vel", facecolor='r', size=10)  # max_vel
        add_patch(ax, move.pelvis.max_amp.index, displ[move.pelvis.max_amp.index], "amp", facecolor='r', size=10)  # max_amp

    if add_vel:
        ax.plot(time, vel, '--', color='b', label="SBjt's velocity")
        if event_patch:
            if move.cof.cm.have_cm:
                add_patch(ax, move.cof.cm.start_cm.index, vel[move.cof.cm.start_cm.index], "cm", facecolor='g',
                          size=10)  # start_cm
                add_patch(ax, move.cof.cm.rel_pt.index, vel[move.cof.cm.rel_pt.index], "r", facecolor='b',
                          size=10)  # rel_pnt_cm
                add_patch(ax, move.cof.cm.end_cm.index, vel[move.cof.cm.end_cm.index], "e", facecolor='r', size=10)  # end_cm
            add_patch(ax, move.pelvis.max_vel.index, vel[move.pelvis.max_vel.index], "vel", facecolor='r', size=10)  # max_vel
            add_patch(ax, move.pelvis.max_amp.index, vel[move.pelvis.max_amp.index], "amp", facecolor='r', size=10)  # max_amp

    if add_accel:
        ax.plot(time, accel, ':', color='b', label="SBjt's acceleration")
        if event_patch:
            if move.cof.cm.have_cm:
                add_patch(ax, move.cof.cm.start_cm.index, accel[move.cof.cm.start_cm.index], "cm", facecolor='g',
                          size=10)  # start_cm
                add_patch(ax, move.cof.cm.rel_pt.index, accel[move.cof.cm.rel_pt.index], "r",
                          facecolor='b', size=10)  # rel_pnt_cm
                add_patch(ax, move.cof.cm.end_cm.index, accel[move.cof.cm.end_cm.index], "e", facecolor='r',
                          size=10)  # end_cm
            add_patch(ax, move.pelvis.max_vel.index, accel[move.pelvis.max_vel.index], "vel", facecolor='b',
                      size=10)  # max_vel
            add_patch(ax, move.pelvis.max_amp.index, accel[move.pelvis.max_amp.index], "amp", facecolor='b',
                      size=10)  # max_amp

    if add_phase:
        pax = ax.scatter(time, (np.ones(len(time)) * min_data_pax) - 0.02, c=move.gamma_angle.gamma, marker='s', s=1000,
                         linewidths=1, cmap=plt.cm.brg)
        if show:
            position = fig.add_axes([0.25, 0.04, 0.5, 0.02])  # posHori, posVert, length, height
            cb = fig.colorbar(pax, ax=ax, cax=position, orientation='horizontal')
            cb.set_ticks([-0.9, 0, 0.9])
            cb.set_ticklabels(["100%  Out-of-Phase", "neutral", "In-Phase  100%"])
            pax.set_clim(-1.0, 1.0)

    ax.legend(loc="best")

    plot_object = {"ax": ax, "pax": pax}

    if show:
        plt.show()
        return plot_object
    else:
        return plot_object


def plot_lower_and_return_ax(move, ax=None, fig=None, v_line_drop_in=True, v_line_drop_end=True, absolute=False,
                             event_patch=True):
    """Creates a plot with the lower angle"""
    plt.style.use("seaborn-poster")
    show = False

    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(18.5, 10.5, forward=True)
        fig.suptitle("PlayerID : {p} - MoveID : {m} - {dt} - Side : {s}".format(p=move.player_id, m=move.move_id,
                                                                                dt="lowerAngle", s=move.side))

    if ax is None:
        ax = plt.subplot()
        ax.grid(True)
        show = True

    time = move.t_norm
    abs_angle = move.angle_lower.abs_arr
    rel_angle = move.angle_lower.rel_arr

    if not absolute:
        ax.plot(time, rel_angle, color='c', label="lower relative angle")
        max_data_vline = max(rel_angle)
        min_data_vline = min(rel_angle)


    else:
        ax.plot(time, abs_angle, color='c', label="lower absolute angle")
        max_data_vline = max(abs_angle)
        min_data_vline = min(abs_angle)

    if v_line_drop_in:
        ax.axvline(0, ymin=min_data_vline, ymax=max_data_vline, color='#006600')
    if v_line_drop_end:
        ax.axvline(move.drop_end, ymin=min_data_vline, ymax=max_data_vline, color='#800000')

    ax.legend(loc="best")

    plot_object = {"ax": ax}

    if show:
        plt.show()
        return plot_object
    else:
        return plot_object


def plot_trunk_and_return_ax(move, ax=None, fig=None, v_line_drop_in=True, v_line_drop_end=True, absolute=False,
                             event_patch=True):
    """Creates a plot with the lower angle"""
    plt.style.use("seaborn-poster")
    show = False
    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(18.5, 10.5, forward=True)
        fig.suptitle("PlayerID : {p} - MoveID : {m} - {dt} - Side : {s}".format(p=move.player_id, m=move.move_id,
                                                                                dt="Trunk Angle", s=move.side))

    if ax is None:
        ax = plt.subplot()
        ax.grid(True)
        show = True

    time = move.t_norm
    abs_angle = move.angle_trunk.abs_arr
    rel_angle = move.angle_trunk.rel_arr

    if not absolute:
        ax.plot(time, rel_angle, color='m', label="Trunk relative angle")
        max_data_vline = max(rel_angle)
        min_data_vline = min(rel_angle)

    else:
        ax.plot(time, abs_angle, color='m', label="Trunk absolute angle")
        max_data_vline = max(abs_angle)
        min_data_vline = min(abs_angle)

    if v_line_drop_in:
        ax.axvline(0, ymin=min_data_vline, ymax=max_data_vline, color='#006600')
    if v_line_drop_end:
        ax.axvline(move.drop_end, ymin=min_data_vline, ymax=max_data_vline, color='#800000')

    ax.legend(loc="best")

    plot_object = {"ax": ax}

    if show:
        plt.show()
        return plot_object
    else:
        return plot_object


def plot_main_joint(move, ax=None, fig=None, v_line_drop_in=True, v_line_drop_end=True, add_vel=True, add_accel=True,
                    event_patch=True, move_reaction_time=True, player_reaction_time=True, add_phase=True):
    plt.style.use("seaborn-poster")
    show = False

    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(18.5, 10.5, forward=True)
        fig.suptitle("PlayerID : {p} - MoveID : {m} - {dt} - Side : {s}".format(p=move.player_id, m=move.move_id,
                                                                                dt="main joints", s=move.side))

    if ax is None:
        ax = plt.subplot()
        ax.grid(True)
        show = True

    cof_ax = plot_cof_and_return_ax(move, ax=ax, fig=fig, v_line_drop_in=v_line_drop_in,
                                    v_line_drop_end=v_line_drop_end, add_vel=add_vel, add_accel=add_accel,
                                    event_patch=event_patch, add_phase=add_phase, move_reaction_time=move_reaction_time,
                                    player_reaction_time=player_reaction_time)
    c7_ax = plot_c7_and_return_ax(move, ax=ax, fig=fig, v_line_drop_in=v_line_drop_in, v_line_drop_end=v_line_drop_end,
                                  add_vel=add_vel, add_accel=add_accel, event_patch=event_patch)
    pelvis_ax = plot_pelvis_and_return_ax(move, ax=ax, fig=fig, v_line_drop_in=v_line_drop_in,
                                    v_line_drop_end=v_line_drop_end, add_vel=add_vel, add_accel=add_accel,
                                    event_patch=event_patch)

    if show:
        plt.show()


def plot_main_angle(move, ax=None, fig=None, v_line_drop_in=True, v_line_drop_end=True, absolute=False, add_phase=True):
    plt.style.use("seaborn-poster")
    show = False
    pax = None

    if fig is None:
        fig = plt.figure()
        fig.set_size_inches(18.5, 10.5, forward=True)
        fig.suptitle("PlayerID : {p} - MoveID : {m} - {dt} - Side : {s}".format(p=move.player_id, m=move.move_id,
                                                                                dt="Main angles", s=move.side))

    if ax is None:
        ax = plt.subplot()
        ax.grid(True)
        show = True

    ax_lower = plot_lower_and_return_ax(move, ax=ax, fig=fig, v_line_drop_in=v_line_drop_in,
                                        v_line_drop_end=v_line_drop_end, absolute=absolute)
    ax_trunk = plot_trunk_and_return_ax(move, ax=ax, fig=fig, v_line_drop_in=v_line_drop_in,
                                        v_line_drop_end=v_line_drop_end, absolute=absolute)
    if absolute:

        min_data = min([min(move.angle_lower.abs_arr), min(move.angle_trunk.abs_arr)]) - 2
    else:
        min_data = min([min(move.angle_lower.rel_arr), min(move.angle_trunk.rel_arr)]) - 2

    if add_phase:
        time = move.t_norm
        pax = ax.scatter(time, (np.ones(len(time)) * min_data), c=move.gamma_angle.gamma, marker='s', s=1000, linewidths=1,
                         cmap=plt.cm.brg)
        if show:
            position = fig.add_axes([0.25, 0.04, 0.5, 0.02])  # posHori, posVert, length, height
            cb = fig.colorbar(pax, ax=ax, cax=position, orientation='horizontal')
            cb.set_ticks([-0.9, 0, 0.9])
            cb.set_ticklabels(["100%  Out-of-Phase", "neutral", "In-Phase  100%"])
            pax.set_clim(-1.0, 1.0)
    if show:
        plt.show()


def add_patch(ax, x, y, text, facecolor='w', textcolor='k', size=10):
    bb_circle = dict(boxstyle="circle", fc=facecolor, ec="0.5", alpha=1, label="yoooooo")
    t = ax.text(x, y, text, color=textcolor, ha="center", va="center", size=size, label=text, bbox=bb_circle)

    bb = t.get_bbox_patch()
    bb.set_boxstyle("circle", pad=0.3)


def graph_move(move, fontsize=20, v_line_drop_in=True, v_line_drop_end=True, add_vel=False, add_accel=False,
               absolute=False, add_phase=True, move_reaction_time=True, player_reaction_time=False, event_patch=False,
               save_to_pdf=False, path_to_save_graph=None):
    """data to graph : cof, pelvis, c7, lower angle, trunk angle
    event to graph : reaction_time, start_cm, release, peak_vel, peak_amp
       ax1 = c7
       ax2 = pelvis
       figure model = 2x1
    """
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.rcParams.update({'font.size': fontsize})

    fig, axes = plt.subplots(nrows=2, ncols=1)
    title = """{rep} - {player_id} - {move_id} - {side}""".format(rep=move.rep, player_id=move.player_id,
                                                                  move_id=move.move_id, side=move.side)
    fig.suptitle(title)
    fig.set_size_inches(18.5, 10.5, forward=True)

    ax1 = axes[0]
    ax2 = axes[1]

    plot_main_joint(move, ax=ax1, fig=fig, v_line_drop_in=v_line_drop_in, v_line_drop_end=v_line_drop_end,
                    add_vel=add_vel, add_accel=add_accel, event_patch=event_patch,
                    move_reaction_time=move_reaction_time, player_reaction_time=player_reaction_time,
                    add_phase=add_phase)
    plot_main_angle(move, ax=ax2, fig=fig, v_line_drop_in=v_line_drop_in, v_line_drop_end=v_line_drop_end,
                    absolute=absolute, add_phase=add_phase)

    print(move.drop_in_index, move.drop_end_cm.index, move.end_cm.index)
    if save_to_pdf:
        if path_to_save_graph is None:
            fig.savefig("{rep}_{player_id}_{move_id}_{side}.pdf".format(rep=move.rep, player_id=move.player_id,
                                                                        move_id=move.move_id, side=move.side), dpi=200,
                        bbox_inches='tight')
        else:
            fig.savefig("{}/{rep}_{player_id}_{move_id}_{side}.pdf".format(path_to_save_graph, rep=move.rep,
                                                                           player_id=move.player_id,
                                                                           move_id=move.move_id, side=move.side),
                        dpi=200, bbox_inches='tight')

    else:
        plt.show()



