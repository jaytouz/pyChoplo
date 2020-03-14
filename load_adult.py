from pickling import load_pickle, create_pickle
from moves import Moves
import analyse

#
lst_adulte = list(range(1,11))
# amp1 = analyse.AnalyseAdult(lst_adulte, 'amp', 1)
# amp2 = analyse.AnalyseAdult(lst_adulte, 'amp', 2)
# amp3 = analyse.AnalyseAdult(lst_adulte, 'amp', 3)
amp4 = analyse.AnalyseAdult(lst_adulte, 'amp', 4)
# # # #
# vit1 = analyse.AnalyseAdult(lst_adulte, 'vit', 1)
# vit2 = analyse.AnalyseAdult(lst_adulte, 'vit', 2)
# vit3 = analyse.AnalyseAdult(lst_adulte, 'vit', 3)
vit4 = analyse.AnalyseAdult(lst_adulte, 'vit', 4)
# # #
# #
# #
#
# create_pickle("adulte_amp_1", amp1)
# create_pickle("adulte_amp_2", amp2)
# create_pickle("adulte_amp_3", amp3)
create_pickle("adulte_amp_4", amp4)
# # #
# create_pickle("adulte_vit_1", vit1)
# create_pickle("adulte_vit_2", vit2)
# create_pickle("adulte_vit_3", vit3)
create_pickle("adulte_vit_4", vit4)

# a1 = Moves.from_analysis([load_pickle("adulte_amp_1")])
# a2 = Moves.from_analysis([load_pickle("adulte_amp_2")])
# a3 = Moves.from_analysis([load_pickle("adulte_amp_3")])
a4 = Moves.from_analysis([load_pickle("adulte_amp_4")])
#
# v1 = Moves.from_analysis([load_pickle("adulte_vit_1")])
# v2 = Moves.from_analysis([load_pickle("adulte_vit_2")])
# v3 = Moves.from_analysis([load_pickle("adulte_vit_3")])
v4 = Moves.from_analysis([load_pickle("adulte_vit_4")])