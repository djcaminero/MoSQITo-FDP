# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

from bisect import bisect


def reassignment_loudness(loudness_original_value, mean_loudness_array):
    """ Function that reassigns values of loudness based on their own value to a new scale under the assumption that the
    original scale does not meet the required criteria (ECMA-418-2).

    Parameters
    ----------
    loudness_original_value: float
        'sones HMS', total loudness value in sones HMS (Hearing Model of Sottek) according to section 5 of ECMA-418-2.

    mean_loudness_array: numpy.array
        Mean loudness values for a range of inputs from 10 dB SPL to 90 dB SPL

    Returns
    -------
    loudness_modified_value: float
        'sones HMS', total loudness value in sones HMS (Hearing Model of Sottek) according to section 5 of ECMA-418-2.
    """
    # Variable to contain the modified value of loudness
    corrected_loudness = 0.00

    sones_limit_array = [
        0.000,
        0.003,
        0.019,
        0.060,
        0.138,
        0.261,
        0.439,
        0.683,
        1.000,
        1.414,
        2.000,
        2.828,
        4.000,
        5.657,
        8.000,
        11.314,
        16.000,
        22.627,
        32.000,
        64.000,
    ]

    # Number of limits
    total_positions = len(mean_loudness_array)

    # Position of the specified loudness value among the limits before correction
    position = bisect(mean_loudness_array, loudness_original_value)

    # Sign ">=" is used instead of "==" in order to avoid possible mismatches
    if position >= total_positions:
        corrected_loudness = mean_loudness_array[total_positions - 1]
    elif position == 0:
        corrected_loudness = 0.00
    else:
        # Limits before correction
        uncorrected_upper_limit = mean_loudness_array[position]
        uncorrected_lower_limit = mean_loudness_array[position - 1]

        # Limits after correction
        corrected_upper_limit = sones_limit_array[position]
        corrected_lower_limit = sones_limit_array[position - 1]

        # Ranges of old/new values
        old_loudness_range = uncorrected_upper_limit - uncorrected_lower_limit
        new_loudness_range = corrected_upper_limit - corrected_lower_limit

        # Calculation of the new loudness value according to the new/old ranges
        corrected_loudness = (
(new_loudness_range * (loudness_original_value - uncorrected_upper_limit)) / old_loudness_range) + corrected_upper_limit

    return corrected_loudness
