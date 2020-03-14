"""INFO 
    https://pythonfordatascience.org/anova-python/#test
    https://pythonfordatascience.org/independent-t-test-python/"""


import pandas as pd
import numpy as np
from scipy import stats
import researchpy as rp
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

def get_mean_lvl_strat(df, lvl):
    l = "lvl_{}".format(lvl)
    idx = pd.IndexSlice
    index_0 = df.transpose().loc[l].index.get_level_values(0).unique() #player_0, player_1...
    index_1 = df.transpose().loc[l].index.get_level_values(2).unique() #PS', 'ST', 'SPI', 'DPIp', 'DPIap
    index = pd.MultiIndex.from_product([index_0, index_1])
    columns = df.transpose().columns
    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan
    df_lvl_strat = pd.DataFrame(data, index=index, columns=columns)
    
    for p in range(0, len(index_0)):
        player = index_0[p]
        p_id = player[-1]
        df_player = get_mean_player_strat(df, lvl, p_id)
        for s in index_1:
            df_lvl_strat.loc[(player,s)] = df_player.loc[s]
    return df_lvl_strat
    
def get_std_lvl_strat(df, lvl):
    l = "lvl_{}".format(lvl)
    idx = pd.IndexSlice
    index_0 = df.transpose().loc[l].index.get_level_values(0).unique() #player_0, player_1...
    index_1 = df.transpose().loc[l].index.get_level_values(2).unique() #PS', 'ST', 'SPI', 'DPIp', 'DPIap
    index = pd.MultiIndex.from_product([index_0, index_1])
    columns = df.transpose().columns
    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan
    df_lvl_strat = pd.DataFrame(data, index=index, columns=columns)
    
    for p in range(0, len(index_0)):
        player = index_0[p]
        df_player = get_std_player_strat(df, lvl, p)
        for s in index_1:
            df_lvl_strat.loc[(player,s)] = df_player.loc[s]
    return df_lvl_strat

def get_mean_lvl_jt(df, lvl):
    print(df.shape)
    l = "lvl_{}".format(lvl)
    idx = pd.IndexSlice
    index_0 = df.transpose().loc[l].index.get_level_values(0).unique() #player_0, player_1...
    index_1 = df.transpose().loc[l].index.get_level_values(2).unique() #cop, pel, c7
    index = pd.MultiIndex.from_product([index_0, index_1])
    columns = df.transpose().columns
    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan
    df_lvl_strat = pd.DataFrame(data, index=index, columns=columns)
    
    for p in range(0, len(index_0)):
        player = index_0[p]
        p_id = player[-1]
        df_player = get_mean_player_joint(df, lvl, p_id)
        for s in index_1:
            df_lvl_strat.loc[(player,s)] = df_player.loc[s]
    return df_lvl_strat

def get_std_lvl_joint(df, lvl):
    l = "lvl_{}".format(lvl)
    idx = pd.IndexSlice
    index_0 = df.transpose().loc[l].index.get_level_values(0).unique() #player_0, player_1...
    index_1 = df.transpose().loc[l].index.get_level_values(2).unique() #PS', 'ST', 'SPI', 'DPIp', 'DPIap
    index = pd.MultiIndex.from_product([index_0, index_1])
    columns = df.transpose().columns
    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan
    df_lvl_strat = pd.DataFrame(data, index=index, columns=columns)
    
    for p in range(0, len(index_0)):
        player = index_0[p]
        df_player = get_std_player_joint(df, lvl, p)
        for s in index_1:
            df_lvl_strat.loc[(player,s)] = df_player.loc[s]
    return df_lvl_strat

def get_mean_player_strat(df, lvl, p):
    idx = pd.IndexSlice
    l, p = "lvl_{}".format(lvl), "player_{}".format(p)
    df_st = df.transpose().loc[idx[l, p]].groupby(level=1).mean()
    return df_st

def get_std_player_strat(df, lvl, p):
    idx = pd.IndexSlice
    l, p = "lvl_{}".format(lvl), "player_{}".format(p)
    df_st = df.transpose().loc[idx[l, p]].groupby(level=1).std()
    return df_st

def get_mean_player_joint(df, lvl, p):
    idx = pd.IndexSlice
    l, p = "lvl_{}".format(lvl), "player_{}".format(p)
    df_jt = df.transpose().loc[idx[l, p]].groupby(level=1).mean()
    return df_jt

def get_std_player_joint(df, lvl, p):
    idx = pd.IndexSlice
    l, p = "lvl_{}".format(lvl), "player_{}".format(p)
    df_jt = df.transpose().loc[idx[l, p]].groupby(level=1).std()
    return df_jt


def get_data_for_anova(df, var, hue):
    l0 = get_data_group_by_player_mean(df, 0, var, hue=hue) #series
    l0_df = pd.DataFrame({var: l0.values, 'level': [0]*len(l0)}, index = l0.index) #to df
    l1 = get_data_group_by_player_mean(df, 1, var, hue=hue)
    l1_df = pd.DataFrame({var: l1.values, 'level': [1]*len(l1)}, index = l1.index) #to df
    l2 = get_data_group_by_player_mean(df, 2, var, hue=hue)
    l2_df = pd.DataFrame({var: l2.values, 'level': [2]*len(l2)}, index = l2.index) #to df
    
    df = pd.concat([l0_df, l1_df, l2_df])
    return df

def anova_one_way(df, var, hue='value', show=True):
    df = get_data_for_anova(df, var, hue)
    results = ols("{} ~ C(level)".format(var), data=df).fit()    
    post_hoc= None
    
    if results.f_pvalue < 0.05:
        mc = MultiComparison(df[var], df['level'])
        post_hoc = mc.tukeyhsd()
    
    if show:
        print(results.summary())
        if post_hoc is not None:
            print(post_hoc)
        
        
    aov_table = anova_table(sm.stats.anova_lm(results, typ=2))
    
    return results, post_hoc, aov_table

def create_df_post_hoc(post_hoc, var):
    index_0 = [var]
    index_1 = ["comparaison 0", "comparaison 1", "comparaison 2"]
    index = pd.MultiIndex.from_product([index_0, index_1])
    columns = post_hoc.summary()[0]

    data = np.array(post_hoc.summary()[1:]) #shape 3,6
    
    df = pd.DataFrame(data, index=index, columns=columns)
    return df

def create_df_with_all_anova(df, hue='value'):
    index_0= ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    index_1= ["inter-groupe", "intra-groupe", "total"]
    index = pd.MultiIndex.from_product([index_0, index_1])
    columns = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
    
    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan
    
    full_df = pd.DataFrame(data, index=index, columns=columns)
    results_dict = {}

    for v in index_0:
        data = get_data_for_anova(df, v, hue)
        results = ols("{} ~ C(level)".format(v), data=data).fit() 
        aov_tbl = anova_table(sm.stats.anova_lm(results, typ=2))        
        results_dict[v] = results
        full_df.loc[(v,'inter-groupe')] =  aov_tbl.values[0]
        full_df.loc[(v,'intra-groupe')] =  aov_tbl.values[1]
        full_df.loc[(v,'total')]['sum_sq']  =  full_df.loc[v].iloc[0]['sum_sq'] + full_df.loc[v].iloc[1]['sum_sq']
        full_df.loc[(v,'total')]['df']= full_df.loc[v].iloc[0]['df'] + full_df.loc[v].iloc[1]['df']

        
    return full_df, results_dict


def create_df_with_all_post_hoc(df, hue='value'):
    index_0= ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    index_1= ["comparaison 0", "comparaison 1", "comparaison 2"]
    index = pd.MultiIndex.from_product([index_0, index_1])
    columns = ['group1', 'group2', 'meandiff', 'lower', 'upper', 'reject']
    
    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan
    
    full_df = pd.DataFrame(data, index=index, columns=columns)
    for v in index_0:
        data = get_data_for_anova(df, v, hue)
        results = ols("{} ~ C(level)".format(v), data=data).fit() 
        mc = MultiComparison(data[v], data['level'])
        post_hoc = mc.tukeyhsd()
        df_ph = create_df_post_hoc(post_hoc, v)
        
        if results.f_pvalue < 0.05:
            full_df.loc[(v)] =  df_ph.values
        else:
            full_df.loc[(v)] = 'anova ns'


        
    return full_df

def test_anova_shapiro(df, hue='value'):
    index = ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    columns = ['statistic', 'p-value']
    
    n_row = len(index)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan
    
    full_df = pd.DataFrame(data, index=index, columns=columns)
    
    for v in index:
        data = get_data_for_anova(df, v, hue)
        results = ols("{} ~ C(level)".format(v), data=data).fit() 
        full_df.loc[v] = stats.shapiro(results.resid)
        
    return full_df

def test_anova_skewness(df, hue='value'):
    index = ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    columns = ['statistic', 'p-value']
    
    n_row = len(index)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan
    
    full_df = pd.DataFrame(data, index=index, columns=columns)
    
    for v in index:
        data = get_data_for_anova(df, v, hue)
        results = ols("{} ~ C(level)".format(v), data=data).fit() 
        full_df.loc[v] = stats.skewtest(results.resid)
        
    return full_df
    
def anova_table(aov):
    """from https://pythonfordatascience.org/anova-python/#test"""
    aov['mean_sq'] = aov[:]['sum_sq']/aov[:]['df']
    
    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
    
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*aov['mean_sq'][-1]))/(sum(aov['sum_sq'])+aov['mean_sq'][-1])
    
    cols = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
    aov = aov[cols]
    return aov



    
def get_data_group_by_player_mean(df, lvl, var, hue='value'):
    lvl = 'lvl_{}'.format(lvl)
    idx = pd.IndexSlice
    df = df.loc[idx[lvl, :], idx[:,hue,:]].groupby(level=1).mean()
    df.columns = df.columns.droplevel(level=1)
    
    df = df[var]
    
    return df

def get_data_group_by_player_std(df, lvl, var, hue='value'):
    lvl = 'lvl_{}'.format(lvl)
    idx = pd.IndexSlice
    df = df.loc[idx[lvl, :], idx[:,hue,:]].groupby(level=1).std()
    df.columns = df.columns.droplevel(level=1)
    
    df = df[var]
    
    return df


def test_for_side_difference_one_var(df_side, lvl, var, hue = 'value', plot_dist = True):
    """performs a ttest on each condition for every variables lvl0 : data = players mean of all valid moves"""
    import seaborn as sns
    import researchpy as rp
    import pandas as pd
    import matplotlib.pyplot as plt

    df = get_data_group_by_player_mean(df_side, lvl, var, hue=hue)
    
    describe, results = rp.ttest(df['right'], df['left'], paired=True)
    
    if plot_dist:
        sns.distplot(df['right'],norm_hist =True, color='b', label = 'right - {}'.format(var))
        sns.distplot(df['left'], norm_hist =True, color='g', label = 'left - {}'.format(var))
        plt.legend(loc = 'best')
        
    return df, describe, results


def test_for_side_difference_all_var_res(df_side, lvl=3, hue = 'value'):
    
    
    columns = ['Difference (right - left)', 'Degrees of freedom', 't',
       'Two side test p value', 'Mean of right > mean of left p value',
       'Mean of right < mean of left p value', "Cohen's d",
       "Hedge's g", "Glass's delta", 'r']

    
    index_0 = list("lvl_{}".format(i) for i in range(0, lvl))
    index_1= ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    
    index = pd.MultiIndex.from_product([index_0, index_1])

    
    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan

    df = pd.DataFrame(data, index=index, columns=columns)
    
    for i in range(0, len(index_0)):
        for v in index_1:
            df_var, desc, res = test_for_side_difference_one_var(df_side, i, v,hue=hue, plot_dist=False)
            df.loc[('lvl_{}'.format(i), v)] = res.results.values

            
    return df
        
    
def test_for_side_difference_all_var_desc(df_side, lvl=3, hue = 'value'):
    
    
    columns = ['N', 'Mean', 'SD', 'SE', '95% Conf.', 'Interval']

    
    index_0 = list("lvl_{}".format(i) for i in range(0, lvl))
    index_1= ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    index_2 = ['left', 'right', 'combined']
    
    index = pd.MultiIndex.from_product([index_0, index_1, index_2])

    n_row = len(index_0) * len(index_1) * len(index_2)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan

    df = pd.DataFrame(data, index=index, columns=columns)
    
    for i in range(0, len(index_0)):
        for v in index_1:
            for j in range(0, len(index_2)):
                i0, i1, i2 = index_0[i], v, index_2[j]
                df_var, desc, res = test_for_side_difference_one_var(df_side, i, v,hue=hue, plot_dist=False)
                df.loc[(i0, i1, i2)] = desc.iloc[j].values[1:] #ignorer la colonne variable
                           
    return df

def test_for_side_levene(df_side, lvl=3, hue = 'value'):
    from scipy import stats
    
    columns = ['statistic', 'p-value']

    
    index_0 = list("lvl_{}".format(i) for i in range(0, lvl))
    index_1= ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    
    index = pd.MultiIndex.from_product([index_0, index_1])

    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan

    df = pd.DataFrame(data, index=index, columns=columns)
    
    for i in range(0, len(index_0)):
        for v in index_1:
            i0, i1 = index_0[i], v
            v_df= get_data_group_by_player_mean(df_side, i, v,hue=hue)
            df.loc[(i0, i1)] = stats.levene(v_df['left'], v_df['right'])
    return df


def test_for_side_shapiro(df_side, lvl=3, hue = 'value'):
    from scipy import stats
    
    columns = ['statistic', 'p-value']

    
    index_0 = list("lvl_{}".format(i) for i in range(0, lvl))
    index_1= ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    
    index = pd.MultiIndex.from_product([index_0, index_1])

    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan

    df = pd.DataFrame(data, index=index, columns=columns)
    
    for i in range(0, len(index_0)):
        for v in index_1:
            i0, i1 = index_0[i], v
            v_df= get_data_group_by_player_mean(df_side, i, v,hue=hue)
            df.loc[(i0, i1)] = stats.shapiro(v_df['left']-v_df['right'])
            
    return df


def test_for_side_skewness(df_side, lvl=3, hue = 'value'):
    from scipy import stats
    
    columns = ['statistic', 'p-value']

    
    index_0 = list("lvl_{}".format(i) for i in range(0, lvl))
    index_1= ["start_cm", "rel_pt", "amp_max_cop", 'amp_max_pel', 'amp_max_c7', "vel_max_cop", 'vel_max_pel',
                       'vel_max_c7', "overshoot", "dcm", "dtml", "rcm"]
    
    index = pd.MultiIndex.from_product([index_0, index_1])

    n_row = len(index_0) * len(index_1)
    n_col = len(columns)
    
    data = np.empty((n_row, n_col))
    data[:] = np.nan

    df = pd.DataFrame(data, index=index, columns=columns)
    
    for i in range(0, len(index_0)):
        for v in index_1:
            i0, i1 = index_0[i], v
            v_df= get_data_group_by_player_mean(df_side, i, v,hue=hue)
            df.loc[(i0, i1)] = stats.skewtest(v_df['left']-v_df['right'])
            
    return df