# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:54:27 2018

@author: tousi
"""

import numpy as np


def thresholding_algo(y, lag=100, threshold=3.5, influence=0):
    """I have constructed an algorithm that works very well
    for these types of datasets. It is based on the principle
    of dispersion: if a new datapoint is a given x number of
    standard deviations away from some moving mean, the algorithm
    signals (also called z-score). The algorithm is very robust
    because it constructs a separate moving mean and deviation,
    such that signals do not corrupt the threshold. Future signals
    are therefore identified with approximately the same accuracy,
    regardless of the amount of previous signals. The algorithm
    takes 3 inputs: lag = the lag of the moving window,
    threshold = the z-score at which the algorithm signals and
    influence = the influence (between 0 and 1) of new signals
    on the mean and standard deviation. For example, a lag of 5
    will use the last 5 observations to smooth the data.
    A threshold of 3.5 will signal if a datapoint is 3.5 standard
    deviations away from the moving mean. And an influence of 0.5
    gives signals half of the influence that normal datapoints
    have. Likewise, an influence of 0 ignores signals completely
    for recalculating the new threshold: an influence of 0 is
    therefore the most robust option; 1 is the least. """

    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0] * len(y)
    stdFilter = [0] * len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i - 1]) > threshold * stdFilter[i - 1]:
            if y[i] > avgFilter[i - 1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i - 1]
        avgFilter[i] = np.mean(filteredY[(i - lag):i])
        stdFilter[i] = np.std(filteredY[(i - lag):i])

    else:
        signals[i] = 0
        filteredY[i] = y[i]
        avgFilter[i] = np.mean(filteredY[(i - lag):i])
        stdFilter[i] = np.std(filteredY[(i - lag):i])

    return dict(signals=np.asarray(signals), avgFilter=np.asarray(avgFilter), stdFilter=np.asarray(stdFilter))
