#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Module that implement butterworth filter. data is an np.array """
# @auteur : Jérémie Tousignant
# @email : tousijer@gmail.com
# @année : 2018

from scipy.signal import butter, filtfilt


def butter_bandpass(lowcut, highcut, fs, order=1):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=1):
    """implementation of butterworth bandpass

    :param data: array to filter
    :param lowcut: lowcut
    :param highcut: highcut
    :param fs: sample frequency of the data
    :param order: order of the filter, is double because of fillfill

    :type data: np.array
    :type lowcut: float
    :type highcut: float
    :type fs: float
    :type order: int

    :return: data filter with bandpass
    :rtype: np.array
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def butter_lowpass(cutoff, fs, order=1):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=1):
    """implementation of butterworth lowpass

    :param data: array to filter
    :param cutoff: lowcut
    :param fs: sample frequency of the data
    :param order: order of the filter, is double because of fillfill

    :type data: np.array
    :type cutoff: float
    :type fs: float
    :type order: int

    :return: data filter with lowpass
    :rtype: np.array
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def butter_highpass(cutoff, fs, order=1):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=1):
    """implementation of butterworth highpass

    :param data: array to filter
    :param cutoff: highcut
    :param fs: sample frequency of the data
    :param order: order of the filter, is double because of fillfill

    :type data: np.array
    :type cutoff: float
    :type fs: float
    :type order: int

    :return: data filter with highpass
    :rtype: np.array
    """
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def rolling_mean(data, window, center = True):
    import pandas as pd
    import numpy as np
    window = int(window)
    half_win = int(window/2)

    mean_fill_nan = data.mean()
    series_filt= pd.Series(data).rolling(window,center=center).mean().fillna(value=mean_fill_nan)
    arr = np.array(series_filt)
    first_data = arr[half_win]
    last_data = arr[-half_win]
    arr[:half_win] = first_data
    arr[-half_win:] = last_data
    return arr

def test_filter(fct, data, cutoff, fs, order):
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    data_f = fct(data, cutoff, fs, order)
    ax.plot(data, color = 'k', label = 'raw')
    ax.plot(data_f, color = 'r', label='filtered')
    ax.legend(loc = 'best')
    plt.show()

