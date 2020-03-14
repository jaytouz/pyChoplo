#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Les classes de choppath permet de gerer le chemin vers les données d'intérêts """


# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018


class DirectoryChoplo(object):
    CWD = "C:/Users/tousi/Documents/Labo_Laurent_Ballaz/Projet_ChopLo/DATA/"

    # CWD = "C:/Users/tousi/Documents/Labo_Laurent_Ballaz/Projet_ChopLo/pyChoplo/pyChoplo/DATA/"
    # CWD = "D:/Labo_Laurent_Ballaz/Projet_ChopLo/pyChoplo/pyChoplo/DATA/"

    def __init__(self, path_to_data=None):
        self.cwd = None
        if path_to_data is None:
            self.path_to_data = self.CWD


class DirectoryAdult2017(DirectoryChoplo):
    def __init__(self, patient, condition, repetition, data_type='kinect'):
        DirectoryChoplo.__init__(self)
        self.patient = patient
        self.condition = condition
        self.repetition = repetition
        self.data_type = data_type
        self.update_path()

    def __str__(self):
        s = "Actual directory is : {}".format(self.path)
        return s

    def update_path(self):
        self.path = "ADULTE/to_analyse/amp_vit_4lvl/P{p}/{c}/rep{r}/{t}/data.txt".format(p=self.patient,
                                                                                         c=self.condition,
                                                                                         r=self.repetition,
                                                                                         t=self.data_type)

    @property
    def path(self):
        return self.cwd

    @path.setter
    def path(self, val):
        if isinstance(val, str):
            self.cwd = self.path_to_data + val
        else:
            raise TypeError("Item must be String")

    @path.deleter
    def path(self):
        self.cwd = self.path_to_data


class DirectoryChildTd(DirectoryChoplo):
    def __init__(self, patient, condition, repetition, data_type='kinect'):
        DirectoryChoplo.__init__(self)
        self.patient = patient
        self.condition = condition
        self.repetition = repetition
        self.data_type = data_type
        self.update_path()

    def __str__(self):
        s = "Actual directory is : {}".format(self.path)
        return s

    def update_path(self):
        self.path = "ENFANT_TD/to_analyse/ENF{p}/{c}/rep{r}/{t}/data.txt".format(p=self.patient, c=self.condition,
                                                                                 r=self.repetition, t=self.data_type)

    @property
    def path(self):
        return self.cwd

    @path.setter
    def path(self, val):
        if isinstance(val, str):
            self.cwd = self.path_to_data + val
        else:
            raise TypeError("Item must be String")

    @path.deleter
    def path(self):
        self.cwd = self.path_to_data


class DirectoryChildCpVd(DirectoryChoplo):
    def __init__(self, patient, condition, repetition, data_type='Kinect'):
        DirectoryChoplo.__init__(self)
        self.patient = patient
        self.condition = condition
        self.repetition = repetition
        self.data_type = data_type
        self.update_path()

    def __str__(self):
        s = "Actual directory is : {}".format(self.path)
        return s

    def update_path(self):
        self.path = "ENFANT_DMC/VD_HIV_2017/to_analyse/VD{p}/{c}_1/Rep{r}/{t}/data.txt".format(p=self.patient,
                                                                                               c=self.condition,
                                                                                               r=self.repetition,
                                                                                               t=self.data_type)

    @property
    def path(self):
        return self.cwd

    @path.setter
    def path(self, val):
        if isinstance(val, str):
            self.cwd = self.path_to_data + val
        else:
            raise TypeError("Item must be String")

    @path.deleter
    def path(self):
        self.cwd = self.path_to_data


class DirectoryChildCpJcEval(DirectoryChoplo):

    def __init__(self, patient, evaluation, data_type='Kinect'):
        DirectoryChoplo.__init__(self)
        self.patient = patient
        self.eval_num = evaluation
        self.data_type = data_type
        self.update_path()

    def __str__(self):
        s = "Actual directory is : {}".format(self.path)
        return s

    def update_path(self):
        self.path = """ENFANT_DMC/JC_HIV_2018/evaluation/to_analyse/DMC_{p}/eval_{e}/Amplitude_CP_JC/Rep1/{t}/data.txt""".format(
            p=self.patient, e=self.eval_num, t=self.data_type)

    @property
    def path(self):
        return self.cwd

    @path.setter
    def path(self, val):
        if isinstance(val, str):
            self.cwd = self.path_to_data + val
        else:
            raise TypeError("Item must be String")

    @path.deleter
    def path(self):
        self.cwd = self.path_to_data


class DirectoryChildCpJcMultiSenso(DirectoryChoplo):

    def __init__(self, patient, repetition, data_type='Kinect'):
        DirectoryChoplo.__init__(self)
        self.patient = patient
        self.repetition = repetition
        self.data_type = data_type
        self.update_path()

    def __str__(self):
        s = "Actual directory is : {}".format(self.path)
        return s

    def update_path(self):
        self.path = "ENFANT_DMC/JC_HIV_2018/multisenso_hiv_2018/to_analyse/DMC_{p}/v_va/REP_{r}/{t}/data.txt".format(
            p=self.patient, r=self.repetition, t=self.data_type)

    @property
    def path(self):
        return self.cwd

    @path.setter
    def path(self, val):
        if isinstance(val, str):
            self.cwd = self.path_to_data + val
        else:
            raise TypeError("Item must be String")

    @path.deleter
    def path(self):
        self.cwd = self.path_to_data
