# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:54:27 2018

@author: tousi
"""

# %load ./../functions/detect_peaks.py
"""Detect peaks in data based on their amplitude and other features."""

import numpy as np

__author__ = "Marcos Duarte, https://github.com/demotu/BMC"
__version__ = "1.0.4"
__license__ = "MIT"


def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising', kpsh=False, valley=False, show=False, ax=None):
    """Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`

    The function can handle NaN's

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    Examples
    --------
    >>> from detect_peaks import detect_peaks
    >>> x = np.random.randn(100)
    >>> x[60:81] = np.nan
    >>> # detect all peaks and plot data
    >>> ind = detect_peaks(x, show=True)
    >>> print(ind)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # set minimum peak height = 0 and minimum peak distance = 20
    >>> detect_peaks(x, mph=0, mpd=20, show=True)

    >>> x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    >>> # set minimum peak distance = 2
    >>> detect_peaks(x, mpd=2, show=True)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # detection of valleys instead of peaks
    >>> detect_peaks(x, mph=0, mpd=20, valley=True, show=True)

    >>> x = [0, 1, 1, 0, 1, 1, 0]
    >>> # detect both edges
    >>> detect_peaks(x, edge='both', show=True)

    >>> x = [-2, 1, -2, 2, 1, 1, 3, 0]
    >>> # set threshold = 2
    >>> detect_peaks(x, threshold = 2, show=True)
    """

    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan - 1, indnan + 1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size - 1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind] - x[ind - 1], x[ind] - x[ind + 1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind):
    """Plot results of the detect_peaks function, see its help."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 4))

        ax.plot(x, 'b', lw=1)
        if ind.size:
            label = 'valley' if valley else 'peak'
            label = label + 's' if ind.size > 1 else label
            ax.plot(ind, x[ind], '+', mfc=None, mec='r', mew=2, ms=8, label='%d %s' % (ind.size, label))
            ax.legend(loc='best', framealpha=.5, numpoints=1)
        ax.set_xlim(-.02 * x.size, x.size * 1.02 - 1)
        ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax.set_ylim(ymin - 0.1 * yrange, ymax + 0.1 * yrange)
        ax.set_xlabel('Data #', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        mode = 'Valley detection' if valley else 'Peak detection'
        ax.set_title("%s (mph=%s, mpd=%d, threshold=%s, edge='%s')" % (mode, str(mph), mpd, str(threshold), edge))
        # plt.grid()
        plt.show()


def find_start_cm(arr, peaks_index, min_index_threshold=None, max_index_threshold=None, search_start=None):
    if max_index_threshold is None:
        max_index_threshold = len(arr)
    if min_index_threshold is None:
        min_index_threshold = 0
    start_cm_peak = None

    if search_start is not None:
        for i in range(len(peaks_index) - 1, -1, -1):
            start_cm_peak = peaks_index[i]
            if start_cm_peak < search_start:
                if arr[start_cm_peak] > 0:
                    # stop with first peak sup to zero
                    break
    return start_cm_peak


def find_max_peak(arr, peaks_index, min_index_threshold=None, max_index_threshold=None, search_start=None,
                  look_left=True):
    """takes a signal and peaks, returns index of peak with max value in signal

    :parameter
    -------
    arr : np.array, plot to look on
    peaks_index : indices of peaks in arr
    index_threshold : event to look from on the left side or right side.
    look_left : if True, look for index inferior to index_threshold. else, look for index superior to.


    """
    if max_index_threshold is None:
        max_index_threshold = len(arr)
    if min_index_threshold is None:
        min_index_threshold = 0
    max_peak_index = None

    if search_start is not None:
        if look_left:
            # looking for max peak index on the right side of threshold

            for i in range(len(peaks_index) - 1, -1, -1):
                p_index = peaks_index[i]
                if p_index < search_start:
                    # checking for max only if left side of threshold
                    if max_peak_index is None:
                        # if first peak, don't compare, just assign first peak
                        max_peak_index = p_index
                    else:
                        if arr[p_index] > arr[max_peak_index]:
                            if p_index > min_index_threshold:
                                max_peak_index = p_index
                                if arr[p_index] > 0:
                                    # makes the looping stop if the first peak > 0 was found. SPECIFIK TO CHOPLO
                                    return max_peak_index
            if max_peak_index is None:
                max_peak_index = 0


        elif not look_left:
            # looking for max peak index on the right side of threshold

            for i in range(0, len(peaks_index), 1):
                p_index = peaks_index[i]
                if p_index > search_start:
                    # checking for max only if right side of threshold
                    if max_peak_index is None:
                        # if first peak, don't compare, just assign first peak
                        max_peak_index = p_index
                    else:
                        if arr[p_index] > arr[max_peak_index]:
                            if p_index < max_index_threshold:
                                max_peak_index = p_index

            if max_peak_index is None:
                max_peak_index = len(arr)

    else:
        # if no threshold, just look in the entire arr for max peak
        for p in peaks_index:
            if max_peak_index is None:
                # if first peak, don't compare, just assign first peak
                max_peak_index = p
            else:
                if arr[p] > arr[max_peak_index]:
                    if p > min_index_threshold and p < max_index_threshold:
                        max_peak_index = p
        if max_peak_index is None:
            max_peak_index = len(arr)

    return max_peak_index


def find_min_valley(arr, valley_index, min_index_threshold=None, max_index_threshold=None, search_start_index=None,
                    look_left=True):
    """takes a signal and valleys, returns index of valleys with min value in signal

    :parameter
    -------
    arr : np.array, plot to look on
    valley_index : indices of valleys in arr
    index_threshold : event to look from on the left side or right side.
    look_left : if True, look for index inferior to index_threshold. else, look for index superior to.


    """
    min_valley_index = None

    if search_start_index is not None:
        if look_left:
            # looking for min valley index on the right side of threshold

            for i in range(len(valley_index) - 1, -1, -1):
                v_index = valley_index[i]
                if v_index < search_start_index:
                    # checking for max only if left side of threshold
                    if min_valley_index is None:
                        # if first valley, don't compare, just assign first valley
                        min_valley_index = v_index
                    else:
                        if arr[v_index] < arr[min_valley_index]:
                            if v_index >= min_index_threshold:
                                min_valley_index = v_index

        elif not look_left:
            # looking for min valley index on the right side of threshold

            for i in range(0, len(valley_index, 1)):
                v_index = valley_index[i]
                if v_index > search_start_index:
                    # checking for min only if right side of threshold
                    if min_valley_index is None:
                        # if first valley, don't compare, just assign first valley
                        min_valley_index = v_index
                    else:
                        if arr[v_index] < arr[min_valley_index]:
                            if v_index < max_index_threshold:
                                min_valley_index = v_index

    else:
        # if no threshold, just look in the entire arr for max peak
        for p in valley_index:
            if min_valley_index is None:
                # if first peak, don't compare, just assign first peak
                min_valley_index = p
            else:
                if arr[p] < arr[min_valley_index]:
                    if p > min_index_threshold and p < max_index_threshold:
                        min_valley_index = p

    return min_valley_index


def find_release_point(arr, valley_index, peaks_index, min_index_threshold=None, max_index_threshold=None,
                       search_start_index=None):
    # min_v = idx of minimum valley
    min_v = find_min_valley(arr, valley_index, min_index_threshold=min_index_threshold,
                            max_index_threshold=max_index_threshold, search_start_index=search_start_index,
                            look_left=True)
    c_v = None  # current_valley_index
    n_v = None  # next_valley_index
    c1,c2 = None, None

    rel_pt_idx = None

    for i in range(len(valley_index) - 1, -1, -1):
        c_v = valley_index[i]
        n_v = valley_index[i - 1]

        if min_v is not None:
            if c_v > min_index_threshold and c_v < max_index_threshold:
                if arr[c_v] < 0:
                    c1 = c_v == min_v  # is the current valley the min valley (if yes, stop search)
                    n_p = find_next_peak(peaks_index, c_v)
                    if n_p is not None:
                        c2 = arr[n_p] > 0  # is next peak > 0 if yes, stop search even if not min index
                    else:
                        c2 = False
                    if c1 or c2:
                        rel_pt_idx = c_v
                        break
                    # else:
                    #     if c2:
                    #         rel_pt_idx = c_v
                    #         break

    if rel_pt_idx is None:
        m = min(arr[min_index_threshold:max_index_threshold])
        rel_pt_idx = np.where(arr == m)[0][0]

    return rel_pt_idx, c1,c2


def find_next_peak(peaks_idx, current_idx, look_left=True):
    """find the closest idx lower or higher to target

    :parameter
    -------
    peaks_idx : list of idx of peaks
    current_idx : index to start search
    look_left : if true, looks from left to right, else looks in ascendent order.
    lower_to : if true, will search for closest idx < target

    :return
    idx : index
    """
    idx = None
    if len(peaks_idx) > 0:
        if look_left:
            i = len(peaks_idx) - 1
            idx = peaks_idx[i]
            while idx > current_idx and i >= 0:
                idx = peaks_idx[i]
                i -= 1

        if not look_left:
            i = 0
            idx = peaks_idx[i]
            while idx < current_idx and i <= len(peaks_idx) - 1:
                idx = peaks_idx[i]
                i += 1

    return idx
