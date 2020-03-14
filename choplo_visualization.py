import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import researchpy as rp
import statsmodels.api as sm
import choplo_statistique as cstats
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
import os


def plot_lvl_strat_jt(df, lvl):
    jt = cstats.cget_mean_lvl_jt(df, lvl)
    strat = cstats.get_mean_lvl_strat(df, lvl)
    
    c7 = jt.loc['c7']
    pel = jt.loc['pelvis']
    cof = jt.loc['cof']
    
    time = np.arange(len(strat))
    
    fig, axes = plt.subplots
    

def transform_data_for_lineplot(df):
    players = []
    time = []
    data_type = []
    level = []
    value = []
    
    lvl0 = cstats.get_mean_lvl_jt(df, 0)
    lvl1 = cstats.get_mean_lvl_jt(df, 1)
    lvl2 = cstats.get_mean_lvl_jt(df, 2)
    
    
    for index in lvl0.transpose():
        i = 0
        for signal in lvl0.loc[index]:
        
            level.append('lvl_0')
            players.append(index[0])
            data_type.append(index[1])
            time.append(i)
            value.append(signal)
            i+=1
    
    for index in lvl1.transpose():
        i = 0
        for signal in lvl1.loc[index]:
        
            level.append('lvl_1')
            players.append(index[0])
            data_type.append(index[1])
            time.append(i)
            value.append(signal)
            i+=1
        
    
    for index in lvl2.transpose():
        i = 0
        for signal in lvl2.loc[index]:
        
            level.append('lvl_2')
            players.append(index[0])
            data_type.append(index[1])
            time.append(i)
            value.append(signal)
            i+=1            

    new_df = pd.DataFrame({'time':time, 'players':players, 'level':level, 'data_type': data_type, 'value':value})
    
    return new_df
    
    

def stat_annotation(data, v, group1, group2, ax, orient='v', x='level', p_h=0.05, lw=2.5, symbol = '*', color = 'k'):
    # statistical annotation
    x1, x2 = group1, group2 
    
    data_group1 = data[data[x]==group1]
    data_group2 = data[data[x]==group2]
    My1, my1 = data_group1[v].max(),  data_group1[v].min() 
    My2, my2 = data_group2[v].max(),  data_group2[v].min() 
    
    c = color
    M,m = data[v].max(), data[v].min()


    
    
#     h = l
#     y_s = max(My1,My2) + max(My1,My2)*0.05
#     y_e = y_s+h #end point of v_line
    x_dist= abs(x2-x1)

    
    
#     y = np.array([y_e, y_e, y_e])
#     x = np.array([x1, x1+x_dist*0.5, x2])
#     pos_symbol = y_e+h
    if orient=='v':
        lim = ax.get_ylim()
        l_y= lim[1]- lim[0]
        y_line = M + (l_y*0.2 * x_dist)
        x_symbol = (x1+x2)*0.5
        y_symbol = y_line+(l_y*0.1)
        y = np.array([y_line, y_line, y_line])
        x = np.array([x1, x1+x_dist*0.5, x2])
        ylim=[lim[0], y_symbol +(l_y*0.2)]
        ax.set_ylim(ylim)
        ax.plot(x, y, lw=lw, c=c)
#         ax.text(x_symbol, y_symbol, symbol, fontdict={'size':20}, ha='center', va='bottom', color=c)
        
    elif orient=='h':
        lim = ax.get_xlim()
        l_x= lim[1]- lim[0]
        x_line = M + (l_x*0.01 * x_dist)
        xlim=[lim[0], lim[1]+(l_x*0.2)]
        x = np.array([x_line, x_line, x_line])
        y = np.array([x1, x1+x_dist*0.5, x2])
        x_symbole = x_line+(l_x*0.01)
        y_symbole = (x1+x2)*0.5
        xlim=[m - l_x * 0.1, M - l_x*0.1]
        ax.set_xlim(xlim)
        ax.plot(x, y, lw=lw, c=c)
        ax.text(x_symbole, y_symbole, symbol, fontdict={'size':20}, ha='left', va='center', color=c)
       
        ax.set_xlabel(v)
    else:
        raise(orient, ' not a valid orientation')
        
    return ax

def box_plot_post_hoc_index(df, v:list, x='level', title=None, sharex=False, xlabel=None, ylabel=None,show=True,save=True, name='picture',dt='amplitude', get_fig=False, fig_size=(9.5, 6.5)):
    import matplotlib
    from matplotlib.ticker import FormatStrFormatter

    font = {'family' : 'normal',
            'weight': 'normal',
        'size'   : 12}

 
    
    #### PLOT
    fig, axes = plt.subplots(nrows = len(v), sharex=sharex, sharey=True)
    i=0
    hue = ['index'] * len(v)
    lim = [None, None] 

    for idx in zip(v,hue):
        if len(v) == 1:
            ax= axes
        else:
            ax = axes[i]


        matplotlib.rc('font', **font)
        data = cstats.get_data_for_anova(df, idx[0], idx[1])
        results = ols("{} ~ C({})".format(idx[0], x), data=data).fit() 
        mc = MultiComparison(data[idx[0]], data[x])
        post_hoc = mc.tukeyhsd()
        reject = post_hoc.reject
        n_group = mc.ngroups
        group1 = mc.pairindices[0]
        group2 = mc.pairindices[1]
        
        
        sns.boxplot(x=idx[0], y=x, data=data, ax=ax, orient='h')
#         if lim[0] is None: 
#             lim[0] = data[idx[0]].min()
#         else:
#             if data[idx[0]].min() < lim[0]:
#                 lim[0] = data[idx[0]].min()
#         if lim[1] is None:
#             lim[1] = data[idx[0]].max()
#         else:
#             if data[idx[0]].max() > lim[1]:
#                 lim[1] = data[idx[0]].max()

        
        for j in range(n_group):
            if reject[j]:
                ax = stat_annotation(data, idx[0], group1[j], group2[j], ax, orient='h')
        ylabel = translate_var_name(idx[0],idx[1])
        ax.set_xlim(lim)
        ax.set_ylabel(ylabel)         
        ax.set_xlabel('')
        i+=1
    
    if len(v) == 1:
        xticks = ax.get_xticks()/50
        ax.set_xticklabels(xticks)
    else:
        for ax in axes:
            xticks = ax.get_xticks()/50
            ax.set_xticklabels(xticks)
    if xlabel is None:
        xlabel = 'Temps (s)'
        
    if title is None:
        title = 'Résultat du post-hoc tukey hsd (p<0.05)'
        
    fig.set_size_inches(fig_size[0], fig_size[1])    
    plt.xlabel(xlabel)
    plt.suptitle(title, y=1.04)
    fig.tight_layout()
    if save:
        cwd = os.getcwd().replace('\\', '/')
        png_name = cwd + '/graphique_post_hoc/{}/instant_{}.png'.format(dt, name)
        plt.savefig(png_name, dpi=500)
        
    if show:
        plt.show()
    if get_fig:
        return fig
    
def box_plot_post_hoc_value(df, v:list, x='level', title=None, xlabel=None, ylabel=None,show=True,save=True, name='picture',dt='amplitude', get_fig=False, fig_size=(9.5, 6.5)):
    import matplotlib
    font = {'family' : 'normal',
            'weight': 'normal',
        'size'   : 12}

 
    
    #### PLOT
    fig, axes = plt.subplots(nrows = len(v), sharex=True)
    i=0
    hue = ['value'] * len(v)
    for idx in zip(v,hue):
        if len(v) == 1:
            ax= axes
        else:
            ax = axes[i]
        matplotlib.rc('font', **font)
        data = cstats.get_data_for_anova(df, idx[0], idx[1])
        results = ols("{} ~ C({})".format(idx[0], x), data=data).fit() 
        mc = MultiComparison(data[idx[0]], data[x])
        post_hoc = mc.tukeyhsd()
        reject = post_hoc.reject
        n_group = mc.ngroups
        group1 = mc.pairindices[0]
        group2 = mc.pairindices[1]
        
        sns.boxplot(x=x, y=idx[0], data=data, ax=ax)
        max_range = 1
        l =  data[idx[0]].max() - data[idx[0]].min()
        final_ylim = [data[idx[0]].min()-(l*0.3), data[idx[0]].max()+(l*0.5)]
        for j in range(n_group):
            if reject[j]:
                ax = stat_annotation(data, idx[0], group1[j], group2[j], ax)
        ylabel = translate_var_name(idx[0],idx[1])
        ax.set_ylabel(ylabel)
        ax.set_xlabel('')
        i+=1
    

        
    if xlabel is None:
        xlabel = 'niveau'
        
    if title is None:
        title = 'Résultat du post-hoc tukey hsd (p<0.05)'
        
    fig.set_size_inches(fig_size[0], fig_size[1])    
    plt.xlabel(xlabel)
    if len(v)>1:
        yax = axes[1].twinx()
    else:
        yax = axes.twinx()
    yax.set_ylabel(hue[0])
    yax.yaxis.set_ticklabels([])
    yax.set_yticks([])
    plt.suptitle(title, y=1.04)
    fig.tight_layout()
    if save:
        cwd = os.getcwd().replace('\\', '/')
        png_name = cwd + '/graphique_post_hoc/{}/valeur_{}.png'.format(dt, name)
        plt.savefig(png_name, dpi=500)
        
    if show:
        plt.show()
    if get_fig:
        return fig
    
    
def translate_var_name(v, hue):
    if v == 'start_cm':
        var_name = 't_r'
    if v == 'rel_pt':
        var_name = 'cm_max'
    if v == 'amp_max_cop':
        var_name = 'tML_max CdP'
    if v == 'amp_max_pel':
        var_name = 'tML_max Sb_k'
    if v == 'amp_max_c7':
        var_name = 'tML_max Ms_k'
    if v == 'vel_max_cop':
        var_name = 'Vmax CdP'
    if v == 'vel_max_pel':
        var_name = 'Vmax Sb_k'
    if v == 'vel_max_c7':
        var_name = 'Vmax Ms_k'
    if v == 'dcm':
        var_name = 'd_cm'
    if v == 'dtml':
        var_name = 'd_tML'
    if v == 'overshoot':
        var_name = 'Dépassement'
    if v == 'rcm':
         var_name = 'r_cm'
    if hue == 'index':
        prefix = 'instant du '
    else:
        prefix = 'valeur du '

    return  var_name

def save_post_hoc(df, dt='amplitude'):
    for c in df.columns:
        v, hue = c[0], c[1] #var_name , index or value
        data = cstats.get_data_for_anova(df, v, hue)
        anova = ols("{} ~ C({})".format(v, 'level'), data=data).fit() 
        p = anova.f_pvalue
        print(v, hue, p)
        if p<0.05:
            var_name = translate_var_name(v, hue)
            box_plot_post_hoc(df, v, ylabel=var_name,save=True,dt=dt, show=False)
        
def plot_jt_angl_strat(jt_df, angle_df, st_df, save=True, name = 'jt_angl_strat'):
    import matplotlib
    from matplotlib.ticker import FormatStrFormatter

    font = {'family' : 'normal',
            'weight': 'normal',
        'size'   : 12}

    matplotlib.rc('font', **font)

    fig, axes = plt.subplots(nrows=3, ncols=3, sharex='col', sharey='row', constrained_layout=True)
    ax1 = axes[0]
    ax2 = axes[1]  
    ax3 = axes[2]

    plot_lvl_strat_jt(jt_df, angle_df, st_df, 0, 'cubehelix', ax1 = axes[0][0], ax2=axes[1][0], ax3=axes[2][0])
    plot_lvl_strat_jt(jt_df, angle_df, st_df, 1, 'cubehelix',ax1 = axes[0][1], ax2=axes[1][1], ax3=axes[2][1])
    plot_lvl_strat_jt(jt_df, angle_df, st_df, 2, 'cubehelix', ax1 = axes[0][2], ax2=axes[1][2], ax3=axes[2][2])
    for axi in axes.flat:
        axi.xaxis.set_major_locator(plt.MaxNLocator(5))
        axi.xaxis.set_ticklabels(['0', ' ', ' ', ' ', '100'])

    for ax in axes.flat:
        ax.label_outer()

    #devide groups
    for ax in ax3:
        ax.hlines([1,2,3,4], *ax.get_xlim())
        
    
    for ax in ax1[1:3]:
        ax.legend_.remove()
    for ax in ax2[1:3]:
        ax.legend_.remove()
        




    ax1[0].set_ylabel('Displacement (m)')
    ax2[0].set_ylabel('Angle (degrés)')
    ax3[0].set_ylabel('Stratégie')
    ax3[1].set_xlabel('Temps normalisé du tML (%)')

    ax1[0].title.set_text("Niveau 1")
    ax1[1].title.set_text("Niveau 2")
    ax1[2].title.set_text("Niveau 3")
    plt.suptitle('Condition {}'.format(name), y=1.05, fontsize=20)

    fig.set_size_inches(18,10)
    if save:
        plt.savefig('{}_jt_angl_strat.png'.format(name), dpi=500)
    plt.show()

def plot_lvl_strat_jt(df_jt, df_angle, df_strat, lvl, cm, ax1=None, ax2=None, ax3=None, fig_size=(18, 6.5)):

    jt = cstats.get_mean_lvl_jt(df_jt, lvl)
    angle=cstats.get_mean_lvl_jt(df_angle, lvl)
    strat = cstats.get_mean_lvl_strat(df_strat, lvl)
    
    c7_mean, c7_std = jt.groupby(level=1).mean().loc['c7'], jt.groupby(level=1).std().loc['c7']
    pel_mean, pel_std = jt.groupby(level=1).mean().loc['pelvis'], jt.groupby(level=1).std().loc['pelvis']
    cof_mean, cof_std = jt.groupby(level=1).mean().loc['cof'], jt.groupby(level=1).std().loc['cof']
    
    teta1_mean, teta1_std = angle.groupby(level=1).mean().loc['teta1'], angle.groupby(level=1).std().loc['teta1']
    teta2_mean, teta2_std = angle.groupby(level=1).mean().loc['teta2'], angle.groupby(level=1).std().loc['teta2']
    teta2_v_mean, teta2_v_std = angle.groupby(level=1).mean().loc['teta2_v'], angle.groupby(level=1).std().loc['teta2_v']

    time = np.arange(404)
    idx = pd.IndexSlice
    
    if ax1 is None or ax2 is None or ax3 is None:
        fig, axe = plt.subplots(ncols=1, nrows=3, sharex=True, constrained_layout=True)
        ax1, ax2, ax3= axe[0], axe[1], axe[2]
    for axi in [ax1,ax2, ax3]:
        axi.xaxis.set_major_locator(plt.MaxNLocator(5))
        axi.set_xticks([0,25,50,75,100])

    
    ax1.plot(time,c7_mean,color = 'r', label = 'MSk')
    ax1.fill_between(time, c7_mean + c7_std, c7_mean - c7_std, facecolor='red', alpha=0.3)
    ax1.plot(time,pel_mean,color = 'b', label = 'BSk')
    ax1.fill_between(time, pel_mean + pel_std, pel_mean - pel_std, facecolor='blue', alpha=0.3)
    ax1.plot(time,cof_mean,color = 'k', label = 'CdP')
    ax1.fill_between(time, cof_mean + cof_std, cof_mean - cof_std, facecolor='black', alpha=0.3)
    
    ax2.plot(time,teta1_mean,color = 'b', label = 'teta 1')
    ax2.fill_between(time, teta1_mean + teta1_std, teta1_mean - teta1_std, facecolor='blue', alpha=0.3)
    ax2.plot(time,teta2_mean,color = 'r', label = 'teta 2')
    ax2.fill_between(time, teta2_mean + teta2_std, teta2_mean - teta2_std, facecolor='red', alpha=0.3)
    ax2.plot(time,teta2_v_mean,color = 'g', label = 'teta 2 vertical')
#     ax2.fill_between(time, teta2_v_mean + teta2_v_std, teta2_v_mean - teta2_v_std, facecolor='green', alpha=0.3)
    ax2.legend(loc='upper left')
    ax1.legend(loc='upper left')
    sns.heatmap(strat.groupby(level=1).mean(),ax=ax3, vmin=0, vmax=1, cmap=cm)


    
