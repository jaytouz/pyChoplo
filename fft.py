import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np


def plotSpectrum(data, lgd1, Fs):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)

    """

    n = len(data)  # length of the signal
    k = np.arange(n)
    T = n / Fs
    frq = k / T  # two sides frequency range
    frq = frq[range(int(n / 2))]  # one side frequency range
    Y = fft(data) / n  # fft computing and normalization
    Y = Y[range(int(n / 2))]

    plt.plot(frq, abs(Y), 'r', label="{} frequency spectrum".format(lgd1))  # plotting the spectrum
    plt.grid(True)
    plt.xticks(np.arange(min(frq), max(frq) + 1, 2.0))
    plt.xlabel('Freq (Hz)')
    plt.ylabel('|Y(freq)|')
    plt.legend(loc='best')


# VISUALISER LE SPECTRE DE FRÉQUENCE ET LES DONNÉES

def plotData_Spect(data, lgd1, Fs):
    Ts = 1.0 / Fs;  # sampling interval
    n = len(data)
    t = np.arange(0, n / Fs, Ts)  # time vector

    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5, forward=True)

    plt.ion()
    plt.subplot(2, 1, 1)
    plotSpectrum(data, lgd1, Fs)
    plt.pause(0.0001)
    plt.subplot(2, 1, 2)
    plt.grid(True)
    plt.plot(t, data, 'b', label="{}".format(lgd1))
    plt.legend(loc='best')
    plt.xlabel('Time (s)')
    plt.ylabel('metric (m, m/s ou m/s^2)')
    plt.xticks(np.arange(min(t), max(t) + 1, 1.0))
    plt.pause(0.0001)

    plt.subplots_adjust(hspace=0.35)
    plt.suptitle("{} + {} Spectrum".format(lgd1, lgd1))

    plt.show()
