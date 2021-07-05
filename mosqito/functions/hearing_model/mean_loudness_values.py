# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np

# Project Imports
from mosqito.functions.hearing_model.sine_wave_generator import sine_wave_generator
from mosqito.functions.hearing_model.comp_loudness import comp_loudness


def mean_loudness_values():
    """ Mean loudness values from a sine wave input of 10 dB SPL to 90 dB SPL.

    Parameters
    ----------

    Returns
    -------
    mean_loudness_array: numpy.array
        Mean loudness values for a range of inputs from 10 dB SPL to 90 dB SPL
    """
    # Variables that help to set the limits between ranges. The whole spectrum has 10 dB more at bottom and top than
    # ECMA-418-2 limits.
    phon_limit_array = [
        0.00,
        5.00,
        10.00,
        15.00,
        20.00,
        25.00,
        30.00,
        35.00,
        40.00,
        45.00,
        50.00,
        55.00,
        60.00,
        65.00,
        70.00,
        75.00,
        80.00,
        85.00,
        90.00,
        100.00
    ]

    mean_loudness_array = np.zeros(len(phon_limit_array))

    for i in range(len(phon_limit_array)):
        # Generation of the sine wave
        signal, time = sine_wave_generator(48000, 2, phon_limit_array[i], 1000)
        s_l, t_l = comp_loudness(signal, validation=False)

        # Round mean loudness value to 6 decimals.
        mean_loudness_value = np.round(np.mean(t_l), 6)
        mean_loudness_array[i] = mean_loudness_value

        print('Input ' + str(phon_limit_array[i]) + 'dB, Expected output , Output ' + str() + str(mean_loudness_value) + ' sones')

    return mean_loudness_array
