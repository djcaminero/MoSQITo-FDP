# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np
import math
import scipy as sp
import matplotlib.pyplot as plt
from scipy.signal import welch


def out_mid_validation(fs, signal, signal_filtered, sos_ear):
    """ Function that serves for the validation of the outer and middle ear filtering  section.

    Parameters
    ----------
    fs: float
        'Hz', sampling frequency.

    signal: numpy.array
        Time signal values of the input signal.

    signal_filtered: numpy.array
        Time signal values of the filtered signal.

    sos_ear: List[List[float]]
        "sos coefficients".

    Returns
    -------

    """
    dim = signal.ndim
    time = np.arange(len(signal)) / fs
    x_limit = len(signal) / fs

    print('Outer & Middle Ear Filter Coefficients:\n' + str(sos_ear) + '\n')

    """ GRAPHIC REPRESENTATION """
    # Frequency response 'sos'
    plt.figure(figsize=(10, 5))
    w_om, h_om = sp.signal.sosfreqz(sos_ear, worN=round(fs / 2))
    w_om_hertz = w_om * (fs / (2.0 * math.pi))
    h_om_db = 20.0 * np.log10(np.maximum(np.abs(h_om), 1e-7))
    plt.semilogx(w_om_hertz, h_om_db)
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

    if dim == 2:
        # Left channel
        plt.figure(figsize=(10, 5))
        plt.plot(time, signal_filtered[:, 0], 'r', label='Señal filtrada por el oído (Canal 1)')
        plt.plot(time, signal[:, 0], 'b', label='Señal de entrada (Canal 1)')
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.7)

        plt.xlim(0, len(signal_filtered))
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud [Pa]')
        plt.title('Filtrado del oído externo y medio/interno (Canal 1)')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()

        # Right channel
        plt.figure(figsize=(10, 5))
        plt.plot(time, signal_filtered[:, 1], 'r', label='Señal filtrada por el oído (Canal 2)')
        plt.plot(time, signal[:, 1], 'b', label='Señal de entrada (Canal 2)')
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.7)

        plt.xlim(0, len(signal_filtered))
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitud [Pa]')
        plt.title('Filtrado del oído externo y medio/interno (Canal 2)')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()

    elif dim == 1:
        # Mono channel
        plt.figure(figsize=(10, 5))
        plt.plot(time, signal_filtered, 'r', label='Señal filtrada por el oído')
        plt.plot(time, signal, 'b', label='Señal de entrada')
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.7)

        plt.xlim(0, x_limit)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitud [Pa]')
        plt.title('Filtrado del oído externo y medio/interno')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()


def afb_validation(fs, dim, centre_freq_array, f_bandwidth_array, t_delay_array, d_coefficients_array, sb_array,
                   sh_array, am_mod_coefficient_array, bm_mod_coefficient_array, band_pass_signal_array):
    """ Function that serves for the validation of the Auditory Filtering Bank.

    Parameters
    ----------
    fs: float
        'Hz', sampling frequency.

    dim: int
        Number of dimensions that has the input signal.

    centre_freq_array: List[float]
        Central frequencies for the auditory filtering bank.

    f_bandwidth_array: List[float]
        Bandwidth for the auditory filtering bank.

    t_delay_array: List[float]
        Time constant (delay) for the auditory filtering bank.

    d_coefficients_array: List[float]
        "d" coefficients for the auditory filtering bank.

    sb_array: List[int]
        Block size.

    sh_array: List[int]
        Hop size.

    am_mod_coefficient_array: numpy.array
        Real part of the "am" coefficients for the auditory filtering bank.

    bm_mod_coefficient_array: numpy.array
        Real part of the "bm" coefficients for the auditory filtering bank.

    band_pass_signal_array: numpy.array
        Band-pass filtered signals.

    Returns
    -------

    """
    # Representative band-pass signals that we want to display
    rep_bands = np.array([4, 9, 17, 27, 37, 47])
    time = np.arange(len(band_pass_signal_array[0])) / fs
    x_limit = len(band_pass_signal_array[0]) / fs

    print('\n\n_____________Banco de Filtros Auditivos_____________\n')
    print('Frecuencias de corte:\n' + str(centre_freq_array) + '\n')
    print('Anchos de banda:\n' + str(f_bandwidth_array) + '\n')
    print('Retardos:\n' + str(t_delay_array) + '\n')
    print('Coeficientes d:\n' + str(d_coefficients_array) + '\n')
    print('Sb - Tamaño de bloque:\n' + str(sb_array) + '\n')
    print('Sh - Distancia entre bloques:\n' + str(sh_array) + '\n')
    print('Coeficientes am - filtro paso-banda:\n' + str(am_mod_coefficient_array) + '\n')
    print('Coeficientes bm - filtro paso-banda:\n' + str(bm_mod_coefficient_array) + '\n')

    """ GRAPHIC REPRESENTATION """
    # Frequency response of the filters
    plt.figure(figsize=(17.5, 7.5))
    for afb_band in range(0, 53):
        band_number = afb_band + 1
        w_afb, h_afb = sp.signal.freqz(bm_mod_coefficient_array[afb_band],
                                       am_mod_coefficient_array[afb_band], worN=round(fs/2))
        w_afb_hertz = w_afb * (fs / (2.0 * math.pi))
        h_afb_db = 20.0 * np.log10(np.abs(h_afb))
        plt.semilogx(w_afb_hertz, h_afb_db,
                     label='RF banda: ' + str(band_number)
                           + ' (' + str(round(float(centre_freq_array[afb_band]), 2)) + 'Hz)')

    plt.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0, loc='upper left', ncol=2)
    plt.subplots_adjust(right=0.65)

    plt.xlim(right=20000)
    plt.ylim(bottom=-250)
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Nivel de presión sonora [dB SPL]')
    plt.title('Banco de filtros auditivos')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
               ["20", "50", "100", "200", "500", "1K", "2K", "5K", "10K", "20K"])
    plt.show()

    if dim == 2:
        # Left channel
        plt.figure(figsize=(10, 5))
        [plt.plot(time, band_pass_signal_array[band_num, :, 0],
                  label='Señal paso-banda ' + str(band_num + 1) + ' - '
                        + str(round(float(centre_freq_array[band_num]), 2)) + 'Hz)') for band_num in rep_bands]
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.65)

        plt.xlim(0, x_limit)
        plt.ylim(bottom=0)
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud [Pa]')
        plt.title('Señales paso-banda después del filtrado con el BFA (Canal 1)')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()

        # Right channel
        plt.figure(figsize=(10, 5))
        [plt.plot(time, band_pass_signal_array[band_num, :, 1],
                  label='Señal paso-banda ' + str(band_num + 1) + ' - '
                        + str(round(float(centre_freq_array[band_num]), 2)) + 'Hz)') for band_num in rep_bands]
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.65)

        plt.xlim(0, x_limit)
        plt.ylim(bottom=0)
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud [Pa]')
        plt.title('Señales paso-banda después del filtrado con el BFA (Canal 2)')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()

    elif dim == 1:
        # Mono channel
        plt.figure(figsize=(10, 5))
        [plt.plot(time, band_pass_signal_array[band_num],
                  label='Señal paso-banda ' + str(band_num + 1) + ' - '
                        + str(round(float(centre_freq_array[band_num]), 2)) + 'Hz)') for band_num in rep_bands]
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.65)

        plt.xlim(0, x_limit)
        plt.ylim(bottom=0)
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud [Pa]')
        plt.title('Señales paso-banda después del filtrado con el BFA')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()


def sl_validation(dim, centre_freq_array, n_array):
    """ Function that serves for the validation of the specific loudness.

    Parameters
    ----------
    dim: int
        Number of dimensions that has the input signal.

    centre_freq_array: List[float]
        Central frequencies for the auditory filtering bank.

    n_array: numpy.array
        Specific loudness.

    Returns
    -------

    """
    # Representative blocks that we want to display
    n_blocks = len(n_array)
    rep_blocks = np.array([str(round(n_blocks / 12)), str(round(n_blocks / 8)), str(round(n_blocks / 4)),
                           str(round(n_blocks / 2)), str(int(float((n_blocks * 3) / 4)))])

    rep_blocks = np.array([17])

    """ EXTRACTION OF PARAMETERS & GRAPHIC REPRESENTATION """
    # If n_array has 2 dimensions (stereo), we have to extract the data dimension by dimension
    if dim == 2:
        # Left channel
        print('Valores de la sonoridad específica (Canal 1):\n' + str(n_array[:, :, 0]) + '\n')
        np.savetxt("sonoridad_específica_CANAL1.txt", n_array[:, :, 0], fmt='%f',
                   delimiter='\t')

        plt.figure(figsize=(10, 5))
        [plt.semilogx(centre_freq_array, n_array[int(block_num), :, 0],
                      label='Valores SE, bloque: ' + str(int(block_num + 1))) for block_num in rep_blocks]
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.75)

        plt.xlim(left=50, right=15000)
        plt.ylim(bottom=0)
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Nivel de presión sonora [soniosHMS]')
        plt.title('Sonoridad específica (Canal 1), banda de 1 kHz')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.xticks([50, 100, 200, 500, 1000, 2000, 5000, 10000, 15000],
                   ["50", "100", "200", "500", "1K", "2K", "5K", "10K", "15K"])
        plt.show()

        # Right channel
        print('Valores de la sonoridad específica (Canal 2):\n' + str(n_array[:, :, 1]) + '\n')
        np.savetxt("sonoridad_específica_CANAL2.txt", n_array[:, :, 1], fmt='%f',
                   delimiter='\t')

        plt.figure(figsize=(10, 5))
        [plt.semilogx(centre_freq_array, n_array[int(block_num), :, 1],
                      label='Valores SE, bloque: ' + str(int(block_num + 1))) for block_num in rep_blocks]
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.75)

        plt.xlim(left=50, right=15000)
        plt.ylim(bottom=0)
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Nivel de presión sonora [soniosHMS]')
        plt.title('Sonoridad específica (Canal 2), banda de 1 kHz')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.xticks([50, 100, 200, 500, 1000, 2000, 5000, 10000, 15000],
                   ["50", "100", "200", "500", "1K", "2K", "5K", "10K", "15K"])
        plt.show()

    elif dim == 1:
        # Mono channel
        print('Valores de la sonoridad específica:\n' + str(n_array) + '\n')
        np.savetxt("sonoridad_específica.txt", n_array[:, :, 0], fmt='%f',
                   delimiter='\t')

        plt.figure(figsize=(10, 5))
        [plt.semilogx(centre_freq_array, n_array[int(block_num), :, 0],
                      label='Valores SE, bloque: ' + str(int(block_num))) for block_num in rep_blocks]
        plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.75)

        plt.xlim(left=50, right=15000)
        plt.ylim(bottom=0)
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Nivel de presión sonora [soniosHMS]')
        plt.title('Sonoridad específica, ISO_532-1, 1 kHz 60 dB')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.xticks([50, 100, 200, 500, 1000, 2000, 5000, 10000, 15000],
                   ["50", "100", "200", "500", "1K", "2K", "5K", "10K", "15K"])
        plt.show()


def tl_validation(dim, t_array):
    """ Function that serves for the validation of the total loudness.

    Parameters
    ----------
    dim: int
        Number of dimensions that has the input signal.

    t_array: numpy.array
        Total loudness.

    Returns
    -------

    """
    print('Valores de la sonoridad total:\n' + str(t_array) + '\n')

    """ EXTRACTION OF PARAMETERS & GRAPHIC REPRESENTATION """
    # If n_array has 2 dimensions (stereo), we have to extract the data dimension by dimension
    if dim == 2:
        # Left channel
        print('Valores de la sonoridad total (CANAL 1):\n' + str(t_array[:, 0]) + '\n')
        np.savetxt("sonoridad_total_CANAL1.txt", t_array[:, 0], fmt='%f',
                   delimiter='\t')

        plt.figure(figsize=(10, 5))
        plt.plot(t_array[:, 0])
        plt.legend(['Sonoridad total de la señal'], bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.75)

        plt.xlim(left=0, right=len(t_array))
        plt.ylim(bottom=0)
        plt.xlabel('Número de bloque')
        plt.ylabel('Nivel de presión sonora [soniosHMS]')
        plt.title('Valor de la sonoridad total por número de bloque (CANAL 1)')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()

        # Right channel
        print('Valores de la sonoridad total (CANAL 2):\n' + str(t_array[:, 0]) + '\n')
        np.savetxt("sonoridad_total_CANAL2.txt", t_array[:, 1], fmt='%f',
                   delimiter='\t')

        plt.figure(figsize=(10, 5))
        plt.plot(t_array[:, 0])
        plt.legend(['Sonoridad total de la señal'], bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.75)

        plt.xlim(left=0, right=len(t_array))
        plt.ylim(bottom=0)
        plt.xlabel('Número de bloque')
        plt.ylabel('Nivel de presión sonora [soniosHMS]')
        plt.title('Valor de la sonoridad total por número de bloque (CANAL 2)')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()

    elif dim == 1:
        print('Valores de la sonoridad total:\n' + str(t_array) + '\n')
        np.savetxt("sonoridad_total.txt", t_array, fmt='%f', delimiter='\t')

        plt.figure(figsize=(10, 5))
        plt.plot(t_array[:, 0])
        plt.legend(['Total loudness (signal)'], bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
        plt.subplots_adjust(right=0.75)

        plt.xlim(left=0, right=len(t_array))
        plt.ylim(bottom=0)
        plt.xlabel('Número de bloque')
        plt.ylabel('Nivel de presión sonora [soniosHMS]')
        plt.title('Valor de la sonoridad total por número de bloque, ISO_532-1, 1 kHz 60 dB')
        plt.grid(which='both', linestyle='-', color='grey')
        plt.show()


def annex_f_validation(fs, signal, signal_filtered, sos_ear, centre_freq_array, f_bandwidth_array, t_delay_array,
                       d_coefficients_array, sb_array, sh_array, am_mod_coefficient_array, bm_mod_coefficient_array,
                       band_pass_signal_array, n_array, t_array):
    """ Function that serves for the validation of the principal parameters presented in Annex F of ECMA-74. As well as
    the general validation, here it is also verified the final result for specific and total loudness.

    Parameters
    ----------
    fs: float
        'Hz', sampling frequency.

    signal: numpy.array
        Time signal values of the input signal.

    signal_filtered: numpy.array
        Time signal values of the filtered signal.

    sos_ear: List[List[float]]
        "sos coefficients".

    centre_freq_array: List[float]
        Central frequencies for the auditory filtering bank.

    f_bandwidth_array: List[float]
        Bandwidth for the auditory filtering bank.

    t_delay_array: List[float]
        Time constant (delay) for the auditory filtering bank.

    d_coefficients_array: List[float]
        "d" coefficients for the auditory filtering bank.

    sb_array: List[int]
        Block size.

    sh_array: List[int]
        Hop size.

    am_mod_coefficient_array: numpy.array
        Real part of the "am" coefficients for the auditory filtering bank.

    bm_mod_coefficient_array: numpy.array
        Real part of the "bm" coefficients for the auditory filtering bank.

    band_pass_signal_array: numpy.array
        Band-pass filtered signals.

    n_array: numpy.array
        Specific loudness.

    t_array: numpy.array
        Total loudness.

    Returns
    -------

    """
    signal_dimension = signal.ndim
    print("Mono signal (1) / Stereo signal (2): " + str(signal_dimension) + '\n')

    """ OUTER AND MIDDLE EAR FILTERING """
    out_mid_validation(fs, signal, signal_filtered, sos_ear)

    """ AUDITORY FILTERING BANK """
    afb_validation(fs, signal_dimension, centre_freq_array, f_bandwidth_array, t_delay_array, d_coefficients_array,
                   sb_array, sh_array, am_mod_coefficient_array, bm_mod_coefficient_array, band_pass_signal_array)

    """ SPECIFIC LOUDNESS WITH CONSIDERATION OF THRESHOLD IN QUIET """
    sl_validation(signal_dimension, centre_freq_array, n_array)

    """ TOTAL LOUDNESS """
    tl_validation(signal_dimension, t_array)
