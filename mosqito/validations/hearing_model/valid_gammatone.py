# -*- coding: utf-8 -*-

from scipy.signal import gammatone as scipy_gamma, freqz
from numpy import log10, abs as np_abs
import matplotlib.pyplot as plt

from mosqito.functions.hearing_model.gammatone import gammatone as mosqito_gamma


def valid_gammatone():
    """ Compares the frequency response of one of the gammatone filters from the AFB in ECMA-418-2 with the
    gammatone filter obtained with "scipy".

    Parameters
    ----------

    Returns
    -------

    """
    # Band number 17 equals to a central frequency of approximately 1027.025 Hz
    freq = 1027.025
    fs = 48000

    plt.figure(figsize=(10, 5))

    # MoSQITo VERSION
    b, a = mosqito_gamma(freq)
    w, h = freqz(b, a, worN=round(fs / 2), fs=fs)
    h_db = 20.0 * log10(np_abs(h))
    plt.semilogx(w, h_db, label="mosqito")

    # SCIPY VERSION
    b, a = scipy_gamma(freq, "iir", fs=fs)
    w, h = freqz(b, a, worN=round(fs / 2), fs=fs)
    h_db = 20.0 * log10(np_abs(h))
    plt.semilogx(w, h_db, label="scipy")

    # Legend created following the guidelines from:
    #   https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
    plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=2)
    plt.subplots_adjust(right=0.75)

    plt.xlim(right=20000)
    plt.ylim(bottom=-250)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Level [dB]')
    plt.title("Gammatone Filter - Frequency Response Comparison, MoSQITo Vs. SCIPY")
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
               ["20", "50", "100", "200", "500", "1K", "2K", "5K", "10K", "20K"])
    plt.show()


if __name__ == '__main__':
    # Execution of gammatone validation
    valid_gammatone()
