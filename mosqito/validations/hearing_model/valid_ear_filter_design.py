# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa and modifications by "martin_g" of Eomys
"""

from scipy import signal
from numpy import log10, abs as np_abs, maximum as np_maximum
import matplotlib.pyplot as plt

from mosqito.functions.hearing_model.ear_filter_design import ear_filter_design


def valid_ear_filter_design():
    """ Outputs the frequency response of the outer and middle/inner ear to be compared with figure 3 from ECMA-418-2

    Parameters
    ----------

    Returns
    -------

    """
    # Generates outer and middle/inner ear filter coefficient
    sos_ear = ear_filter_design()
    # Computes the frequency response of the filter
    w, h = signal.sosfreqz(sos_ear, worN=1500, fs=48000)
    db = 20.0 * log10(np_maximum(np_abs(h), 1e-7))

    plt.figure(figsize=(10, 5))
    plt.semilogx(w, db)

    # Legend created following the guidelines from:
    #   https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
    plt.legend(['Curva del filtro auditivo'], bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
    plt.subplots_adjust(right=0.75)

    plt.xlim(20, 20000)
    plt.ylim(-25, 10)
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Nivel de presión sonora [dB SPL]')
    plt.title('Respuesta en frecuencia del oído externo y medio/interno')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
               ["20", "50", "100", "200", "500", "1K", "2K", "5K", "10K", "20K"])
    plt.show()


if __name__ == '__main__':
    # Execution of outer and middle/inner ear filter validation
    valid_ear_filter_design()
