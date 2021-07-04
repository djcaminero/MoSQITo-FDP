# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import numpy as np
import matplotlib.pyplot as plt

# Project Imports
from mosqito.functions.shared.load import load
from mosqito.functions.hearing_model.sine_wave_generator import sine_wave_generator
from mosqito.functions.hearing_model.comp_loudness import comp_loudness
from mosqito.functions.hearing_model.loudness_graphics import loudness_graphics
from mosqito.functions.hearing_model.mean_loudness_values import mean_loudness_values
from mosqito.functions.hearing_model.reassignment_loudness import reassignment_loudness
from mosqito.functions.hearing_model.sone2phone import sone2phone

import sys

sys.path.append('../../..')

if __name__ == '__main__':
    fs = 48000
    p_ref = 2e-5
    duration = 1
    db_SPL = 40
    sin_freq = 1000

    sig, time = sine_wave_generator(fs, duration, db_SPL, sin_freq)

    """
    # SIGNAL FR VALIDATION SECTION
    plt.figure(figsize=(10, 5))
    plt.plot(time, sig, label='Tono puro de ' + str(db_SPL) + ' dB SPL a ' + str(sin_freq) + ' Hz')
    plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
    plt.subplots_adjust(right=0.65)

    plt.xlim(left=0.025, right=0.03)
    plt.ylim(bottom=-0.003, top=0.003)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud [Pa]')
    plt.title('Señal de entrada')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.show()

    n = len(sig)
    pressure_rms = p_ref * (10.00 ** (db_SPL / 20.00))
    sensitivity = np.sqrt(2) * pressure_rms

    # Calculations for the level from time domain signal
    #
    rms_time = np.sqrt(np.mean(np.power(sig, 2)))
    db_time = 20 * np.log10(abs(np.fft.fft(sig * np.blackman(n))))
    window = np.blackman(n)
    signal = sig * window

    spectrum = np.fft.fftshift(np.fft.fft(signal))
    freq = np.fft.fftshift(np.fft.fftfreq(n, 1 / fs))

    spectrum = spectrum[n // 2:]
    freq = freq[n // 2:]

    spectrum *= 2

    if n % 2 == 0:
        spectrum[-1] /= 2

    spectrum_mag = np.abs(spectrum) / np.sum(window)

    # To obtain RMS values, divide by sqrt(2)
    spectrum_rms = spectrum_mag / np.sqrt(2)
    # Do not scale the DC component
    spectrum_rms[0] *= np.sqrt(2) / 2

    # Convert to decibel scale
    spectrum_db = 20 * np.log10(spectrum_rms / p_ref)

    plt.figure(figsize=(10, 5))
    plt.semilogx(freq, spectrum_db, label='Tono puro de ' + str(db_SPL) + ' dB SPL a ' + str(sin_freq) + ' Hz')
    plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
    plt.subplots_adjust(right=0.65)

    plt.xlim((1, fs / 2))
    plt.ylim((0, 120))
    plt.grid('on')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Nivel de presión sonora [dB SPL]')
    plt.title('Respuesta en frecuencia - Tono puro')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
               ["20", "50", "100", "200", "500", "1K", "2K", "5K", "10K", "20K"])
    plt.show()"""

    ####################################################################################################################
    """
    # LOAD SIGNAL CODE SECTION
    # Gets the PATH of the file that its going to be loaded
    wav_file = {"data_file": r"D:\PycharmProjects\tonality_ecma\mosqito\validations\loudness_zwicker\data\ISO_532-1"
                             r"\Test signal 3 (1 kHz 60 dB).wav"}

    # Loads the specified signal
    sig, fs = load(False, wav_file["data_file"], calib=2 * 2 ** 0.5)
    time = np.arange(len(signal)) / fs

    plt.figure(figsize=(10, 5))
    plt.plot(time, sig, label='Test signal 3 (1 kHz 60 dB).wav')
    plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
    plt.subplots_adjust(right=0.65)

    plt.xlim(left=0.025, right=0.03)
    # plt.xlim(left=0, right=0.5)
    # plt.ylim(bottom=0)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud [Pa]')
    plt.title('Señal de entrada, ISO_532-1, 1 kHz 60 dB')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.show()"""
    ####################################################################################################################

    s_l, t_l = loudness_graphics(sig, validation=True)

    mean_uncorrected = float(np.mean(t_l))
    print('\nMean value, total loudness (Uncorrected): ' + str(mean_uncorrected))
    print('Mean value in phons, total loudness (Uncorrected): ' + str(sone2phone(mean_uncorrected)))

    mean_corrected = reassignment_loudness(mean_uncorrected, mean_loudness_values())
    print('\nMean value, total loudness (Corrected): ' + str(mean_corrected))
    print('Mean value in phons, total loudness (Corrected): ' + str(sone2phone(mean_corrected)))
