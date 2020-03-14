from joint import Joint

class CenterOfForce(Joint):

    def __init__(self, x, y, name, data_type='CenterOfForce', fs=50):
        Joint.__init__(self, x,y,name,data_type,fs)

    # def add_event(self, p_th_m, p_th_std, pre_d_mean, pre_d_std):
    #     self.cof.set_event()
    #     self.cof.set_reaction_time_from_player_mean(p_th_m, p_th_std)
    #     self.cof.set_reaction_time_from_move_mean(pre_d_mean, pre_d_std)
    #     self.cof.set_counter_movement()

    # def set_event(self):
    #     pass
