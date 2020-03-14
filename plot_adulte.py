import matplotlib.pyplot as plt
import numpy as np


def coordination_graph(moves):
    n_max = len(moves[0])
    for m in moves:
        if len(m)< n_max:
            n_max = len(m)
    drop_end_index = 0
    for m in moves:
        drop_end_index += m.drop_end_index
    drop_end_index /= len(moves)

    norm_t = np.arange(n_max)/drop_end_index*100

    fig, axes = plt.subplots(nrows=3)

    xm0, xm1, xm2= find_axis_min(moves, 'angle_lower', 'rel_arr'), 0, 0
    xM0, xM1, xM2 = find_axis_max(moves, 'angle_lower', 'rel_arr'), norm_t[-1], norm_t[-1]

    ym0,ym1,ym2 = find_axis_min(moves, 'angle_trunk', 'rel_arr'), 0, find_axis_min(moves, 'cof_rel', 'x_arr')
    yM0,yM1,yM2 = find_axis_max(moves, 'angle_trunk', 'rel_arr'), 360, find_axis_max(moves, 'cof_rel', 'x_arr')

    #set axis 0
    axes[0].set_xlim([xm0,xM0])
    axes[0].set_ylim([ym0,yM0])

    #set axis 1
    axes[1].set_xlim([xm1,xM1])
    axes[1].set_ylim([ym1,yM1])

    #set axis 2
    axes[2].set_xlim([xm2,xM2])
    axes[2].set_ylim([ym2,yM2])

    colors = iter(plt.cm.jet(np.linspace(0, 1, len(moves)+1)))
    c = next(colors)
    m=moves[0]
    norm_t = np.arange(len(m)) / drop_end_index * 100
    axes[0].plot(m.angle_lower.rel_arr, m.angle_trunk.rel_arr, color=c, label='Teta1(x) - Teta2(y)')
    axes[1].plot(norm_t, m.gamma_angle.gamma, color=c, label='Gamma')
    axes[2].plot(norm_t, m.cof_rel.x_arr, color=c, label='CoF')
    for m in moves:
        norm_t = np.arange(len(m)) / drop_end_index * 100
        c = next(colors)

        axes[0].plot(m.angle_lower.rel_arr, m.angle_trunk.rel_arr, color=c)
        axes[1].plot(norm_t, m.gamma_angle.gamma, color=c)
        axes[2].plot(norm_t, m.cof_rel.x_arr, color=c)

    axes[0].legend(loc='best')
    axes[1].legend(loc='best')
    axes[2].legend(loc='best')

    plt.show()


def coordination_2_condition(moves1, moves2):
    pass

def find_axis_min(moves,dt, axis):
    axism = moves[0].__dict__[dt].__dict__[axis].min()
    for m in moves:
        temp = m.__dict__[dt].__dict__[axis].min()
        if temp < axism:
            axism = temp
    return axism

def find_axis_max(moves,dt, axis):
    axisM = moves[0].__dict__[dt].__dict__[axis].max()
    for m in moves:
        temp = m.__dict__[dt].__dict__[axis].max()
        if temp > axisM:
            axisM = temp
    return axisM


def plot_circular_plot(data1, data2, data3, p_id):
    import seaborn as sns
    import pandas as pd
    import numpy as np

    sns.set()

    n1, n2, n3 = len(data1.players[p_id].rep), len(data2.players[p_id].rep), len(data3.players[p_id].rep)

    c1, c2, c3 = data1.players[p_id].rep.cof_rel.x_arr, data2.players[p_id].rep.cof_rel.x_arr, data3.players[
        p_id].rep.cof_rel.x_arr
    cof = np.append(c1, c2)
    cof = np.append(cof, c3)

    g1, g2, g3 = data1.players[p_id].rep.gamma_angle.gamma, data2.players[p_id].rep.gamma_angle.gamma, data3.players[
        p_id].rep.gamma_angle.gamma
    gamma = np.append(g1, g2)
    gamma = np.append(gamma, g3)

    n_data1 = ['lvl1'] * n1
    n_data2 = ['lvl2'] * n2
    n_data3 = ['lvl3'] * n3
    hue = n_data1 + n_data2 + n_data3
    print(len(gamma), len(hue), len(cof))
    df = pd.DataFrame({'gamma': gamma, 'level': hue, 'cof': cof})
    g = sns.FacetGrid(df, col="level", hue="level", subplot_kws=dict(projection='polar'), height=4.5, sharex=False,
                      sharey=False, despine=False)

    # Draw a scatterplot onto each axes in the grid
    g.map(sns.scatterplot, "gamma", "cof")
