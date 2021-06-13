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
from mosqito.functions.hearing_model.mean_loudness_values import mean_loudness_values
from mosqito.functions.hearing_model.reassignment_loudness import reassignment_loudness
from mosqito.functions.hearing_model.sone2phone import sone2phone

import sys

sys.path.append('../../..')


def test_hm_sw(fs, duration, db_spl, sin_freq):
    """ Function that serves as a test and creates a sine wave in order to be processed by the hearing model
    "comp_loudness.py".

    Parameters
    ----------
    fs: int
        'Hz', sampling frequency.

    duration: float
        'Hz', sampling frequency.

    db_spl: float
        Sound pressure level (dB SPL).

    sin_freq: float
        'Hz', sampling frequency.

    Returns
    -------

    """
    # "Peak" value in Pascals (amplitude)
    p_ref = 2e-5

    sig, time = sine_wave_generator(fs, duration, db_spl, sin_freq)
    n = len(sig)
    pressure_rms = p_ref * (10.00 ** (db_spl / 20.00))
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
    plt.title('Frequency Response of Input')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.show()

    # The amplitude of the signal is  taken by calculating SPL = 20 * log10( 2 * amplitude / (2 * (10 ** (-5))),
    # you obtain the SPL level of the input signal. "2 * amplitude" = PeakToPeak value
    s_l, t_l = comp_loudness(sig, validation=True)

    mean_uncorrected = float(np.mean(t_l))
    print('\nMean value, total loudness (Uncorrected): ' + str(mean_uncorrected))
    print('Mean value in phons, total loudness (Uncorrected): ' + str(sone2phone(mean_uncorrected)))

    mean_corrected = reassignment_loudness(mean_uncorrected, mean_loudness_values())
    print('\nMean value, total loudness (Corrected): ' + str(mean_corrected))
    print('Mean value in phons, total loudness (Corrected): ' + str(sone2phone(mean_corrected)))


def test_hm_ls():
    """ Function that serves as a test and loads a signal in order to be processed by the hearing model
    "comp_loudness.py".

    Parameters
    ----------

    Returns
    -------

    """
    # Gets the PATH of the file that its going to be loaded
    wav_file = {"data_file": r"D:\PycharmProjects\tonality_ecma\mosqito\validations\loudness_zwicker\data\ISO_532-1"
                             r"\Test signal 3 (1 kHz 60 dB).wav"}

    # Loads the specified signal
    sig, fs = load(False, wav_file["data_file"], calib=2 * 2 ** 0.5)

    s_l, t_l = comp_loudness(sig, validation=True)

    mean_uncorrected = float(np.mean(t_l))
    print('\nMean value, total loudness (Uncorrected): ' + str(mean_uncorrected))
    print('Mean value in phons, total loudness (Uncorrected): ' + str(sone2phone(mean_uncorrected)))

    mean_corrected = reassignment_loudness(mean_uncorrected, mean_loudness_values())
    print('\nMean value, total loudness (Corrected): ' + str(mean_corrected))
    print('Mean value in phons, total loudness (Corrected): ' + str(sone2phone(mean_corrected)))


if __name__ == '__main__':

    # Ask for input
    case = int(input('OPTIONS - Loudness calculation:\n\t- Sine wave (1) \n\t- Signal from file (2)'))

    if case == 1:
        # For loudness calculation the only valid option for the sine wave is 48 kHz
        fs = 48000

        duration = float(input('\nDuration of the signal [s]:'))
        db_spl = float(input('\nSound pressure level of the signal [dB SPL]:'))
        sin_freq = float(input('\nFrequency of the signal [Hz]:'))
        test_hm_sw(fs, duration, db_spl, sin_freq)

    elif case == 2:
        test_hm_ls()

    else:
        raise Exception('Invalid option. The only possible options are 1 and 2.')
