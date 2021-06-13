# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import cmath
import numpy as np
import math
import scipy as sp
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.special import comb

# Project Imports
from mosqito.functions.shared.load import load
from mosqito.functions.hearing_model.sine_wave_generator import sine_wave_generator
from mosqito.functions.hearing_model.comp_loudness import comp_loudness
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
    plt.semilogx(freq, spectrum_db)
    plt.xlim((1, fs / 2))
    plt.ylim((0, 120))
    plt.grid('on')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('SPL [dB]')
    plt.title('Pure Tone Frequency Response (1 kHz, 40 dB SPL)')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.show()

    s_l, t_l = comp_loudness(sig, validation=True)

    mean_uncorrected = float(np.mean(t_l))
    print('\nMean value, total loudness (Uncorrected): ' + str(mean_uncorrected))
    print('Mean value in phons, total loudness (Uncorrected): ' + str(sone2phone(mean_uncorrected)))

    mean_corrected = reassignment_loudness(mean_uncorrected, mean_loudness_values())
    print('\nMean value, total loudness (Corrected): ' + str(mean_corrected))
    print('Mean value in phons, total loudness (Corrected): ' + str(sone2phone(mean_corrected)))

