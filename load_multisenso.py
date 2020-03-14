from pickling import load_pickle, create_pickle
from moves import Moves
import analyse
import pandas as pd
import numpy as np
from excel_multisenso import *
from scipy import stats

#create data

# lst_patient_id = list(range(1,18))
# lst_patient_id.remove(8) #ENLEVER LE 8
# lst_patient_id.remove(4) #ENLEVER LE 4
# lst_patient_id.remove(10) #ENLEVER LE 10
#
#
# rep1 = analyse.AnalyseChildCPMultiSenso(lst_patient_id, repetition=1)
# rep2 = analyse.AnalyseChildCPMultiSenso(lst_patient_id, repetition=2)
# rep3 = analyse.AnalyseChildCPMultiSenso(lst_patient_id, repetition=3)
# rep4 = analyse.AnalyseChildCPMultiSenso(lst_patient_id, repetition=4)
#
# create_pickle("rep1_ms_cp", rep1)
# create_pickle("rep2_ms_acp", rep2)
# create_pickle("rep3_ms_cp", rep3)
# create_pickle("rep4_ms_cp", rep4)



r1 = load_pickle("rep1_ms_cp")
r2 = load_pickle("rep2_ms_cp")
r3 = load_pickle("rep3_ms_cp")
r4 = load_pickle("rep4_ms_cp")

moves = Moves.from_analysis([r1, r2, r3, r4])

df = create_df_multisenso_single_col(moves).replace('NaN', np.nan)


#
create_pickle('multisenso_df', df)


output_path = 'C:/Users/tousi/Documents/Labo_Laurent_Ballaz/Projet_ChopLo/pyChoplo_output/'
folder = 'df_excel/'
path = output_path + folder

df_success= df.loc[df['target_reach']=='success']
df_success_and_cm = df.loc[(df['target_reach']=='success') & (df['have_cm'] == 'with_cm')]

df_success_and_cm = filter_outlier(df_success_and_cm)

df_mean_per_rep = get_mean_per_rep(df_success_and_cm)
df_std_per_rep = get_std_per_rep(df_success_and_cm)
df_player_mean = get_mean_per_player(df_success_and_cm)
df_std_player = get_std_per_player(df_success_and_cm)

df_success_and_cm.to_csv(path + 'df_success_and_cm.csv')
df_mean_per_rep.to_csv(path + 'df_mean_per_rep.csv')
df_std_per_rep.to_csv(path + 'df_std_per_rep.csv')
df_player_mean.to_csv(path + 'df_player_mean.csv')
df_std_player.to_csv(path + 'df_std_player.csv')

