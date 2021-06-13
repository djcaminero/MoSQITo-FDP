# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import numpy as np
import matplotlib.pyplot as plt

# Project Imports
from mosqito.functions.hearing_model.sone2phone import sone2phone
from mosqito.functions.hearing_model.phone2spl import phone2spl
from mosqito.functions.hearing_model.comp_loudness import comp_loudness
from mosqito.functions.hearing_model.mean_loudness_values import mean_loudness_values
from mosqito.functions.hearing_model.reassignment_loudness import reassignment_loudness
from mosqito.functions.hearing_model.equal_loudness_contours import (
    equal_loudness_contours,
)
from mosqito.functions.hearing_model.sine_wave_generator import sine_wave_generator

import sys

sys.path.append("../../..")


def loudness_contour_equivalence(mean_loudness_value, phon_ref_value):
    """ Function that serves for the validation of the hearing model presented in Annex F of ECMA-74.

    Parameters
    ----------

    Returns
    -------

    """
    # Conversion to phons of the loudness result that is in sones.
    phon_loudness_value = sone2phone(mean_loudness_value)

    phon_diff = abs(phon_ref_value - phon_loudness_value)

    phon_contour_value = (
        phon_ref_value - phon_diff
        if (phon_ref_value <= phon_loudness_value)
        else phon_ref_value + phon_diff
    )

    return phon_contour_value


def hearing_model_validation():
    """Function that serves for the validation of the hearing model presented in Annex F of ECMA-74.

    Parameters
    ----------

    Returns
    -------

    """
    # Duration of the signal
    duration = 2.00
    # Sampling frequency
    fs = 48000
    # Pressure of reference
    p_ref = 2e-5

    # OPTION A - Array of frequencies of the AFB (MORE DEFINITION IN CONTOURS THAN OPTION B)
    freq_array = np.array(
        [
            41.00914871505695,
            82.2868409326493,
            124.10337868030052,
            166.73259255100055,
            210.45363485007306,
            255.55280759063885,
            302.32543730808527,
            351.0778089705394,
            402.12917164932713,
            455.8138290833099,
            512.4833288269103,
            572.5087643172005,
            636.2832049348641,
            704.2242699719933,
            776.7768633620453,
            854.4160870800056,
            937.6503522908124,
            1027.024708619026,
            1123.1244133410646,
            1226.5787638724394,
            1338.0652186465666,
            1458.3138333702414,
            1588.1120417060679,
            1728.3098116875572,
            1879.8252116330764,
            2043.6504220063591,
            2220.858232591531,
            2412.6090675286264,
            2620.15858421219,
            2844.8658958134583,
            3088.2024712702996,
            3351.7617710254617,
            3637.2696816115767,
            3946.5958174125717,
            4281.765763609721,
            4644.974340483777,
            5038.599975932929,
            5465.22028032323,
            5927.628925661629,
            6428.853939622738,
            6972.177534225708,
            7561.157599006812,
            8199.650999433281,
            8891.838833125257,
            9642.253809273152,
            10455.809930541354,
            11337.834671826557,
            12294.103866589578,
            13330.879529209504,
        ]
    )

    # OPTION B - Array of frequencies for loudness contours (LESS DEFINITION IN CONTOURS THAN OPTION A)
    freq_array_l = np.array(
        [
            20.0,
            25.0,
            31.5,
            40.0,
            50.0,
            63.0,
            80.0,
            100.0,
            125.0,
            160.0,
            200.0,
            250.0,
            315.0,
            400.0,
            500.0,
            630.0,
            800.0,
            1000.0,
            1250.0,
            1600.0,
            2000.0,
            2500.0,
            3150.0,
            4000.0,
            5000.0,
            6300.0,
            8000.0,
            10000.0,
            12500.0,
        ]
    )

    n_frequencies = len(freq_array)

    phons = [20, 40, 60, 80]
    n_phons = len(phons)

    uncorrected_phon_array = np.zeros((n_phons, n_frequencies), dtype=float)
    corrected_phon_array = np.zeros((n_phons, n_frequencies), dtype=float)

    # Mean limits from the uncorrected version of loudness
    mean_loudness_array = mean_loudness_values()

    for i_phone_contours in range(n_phons):
        # The next sentence returns an array with the dB SPL values for an specific phon value
        # spl_contours_array = equal_loudness_contours(phons[i_phone_contours])[0]
        phon_ref_value = phons[i_phone_contours]

        for i_freq in range(n_frequencies):
            signal, samples = sine_wave_generator(
                fs, duration, phon_ref_value, freq_array[i_freq]
            )

            """
            Next sentence returns the "t_array" from the function comp_loudness to then calculate the mean value 
            of the array. That makes possible to retain the resulting loudness.
            """
            t_array = comp_loudness(signal, validation=False)[1]
            mean_loudness_value = float(np.mean(t_array[:, 0]))

            # Function that corrects the loudness
            corrected_loudness = reassignment_loudness(mean_loudness_value, mean_loudness_array)

            # Conversion to phons of the loudness result that is in sones and adapted to the equal loudness contours
            uncorrected_phon_value = loudness_contour_equivalence(mean_loudness_value, phon_ref_value)
            uncorrected_phon_array[i_phone_contours][i_freq] = uncorrected_phon_value

            # Loudness value after correction
            corrected_phon_value = loudness_contour_equivalence(corrected_loudness, phon_ref_value)
            corrected_phon_array[i_phone_contours][i_freq] = corrected_phon_value

    # Function that gets the values of the "Equal Loudness Contours"
    spl_array_0_phons, frequencies = equal_loudness_contours(0)
    spl_array_20_phons = equal_loudness_contours(20)[0]
    spl_array_40_phons = equal_loudness_contours(40)[0]
    spl_array_60_phons = equal_loudness_contours(60)[0]
    spl_array_80_phons = equal_loudness_contours(80)[0]

    """ GRAPHIC REPRESENTATIONS """
    """ EQUAL LOUDNESS CONTOURS Vs. UNCORRECTED VALUES"""
    plt.figure(figsize=(10, 5))
    # The lower threshold of hearing is not represented due to the limit that puts the standard by applicating
    # the threshold in quiet
    # plt.semilogx(frequencies, spl_array_0_phons, 'g:', label='0 phons - equal loudness contour')
    plt.semilogx(frequencies, spl_array_20_phons, 'b:', label='20 phons - equal loudness contour')
    plt.semilogx(frequencies, spl_array_40_phons, 'g:', label='40 phons - equal loudness contour')
    plt.semilogx(frequencies, spl_array_60_phons, 'r:', label='60 phons - equal loudness contour')
    plt.semilogx(frequencies, spl_array_80_phons, 'c:', label='80 phons - equal loudness contour')

    plt.semilogx(freq_array, uncorrected_phon_array[0, :], 'b', label='20 phons - uncorrected loudness')
    plt.semilogx(freq_array, uncorrected_phon_array[1, :], 'g', label='40 phons - uncorrected loudness')
    plt.semilogx(freq_array, uncorrected_phon_array[2, :], 'r', label='60 phons - uncorrected loudness')
    plt.semilogx(freq_array, uncorrected_phon_array[3, :], 'c', label='80 phons - uncorrected loudness')

    # Legend created following the guidelines from:
    #   https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
    plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
    plt.subplots_adjust(right=0.65)

    plt.xlim(left=100, right=10100)
    plt.ylim(bottom=0, top=120)
    plt.ylabel('Sound pressure level [dB SPL]')
    plt.xlabel('Frequency [Hz]')
    plt.title('Loudness contours - Equal Loudness Contours Vs. Uncorrected Values')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks(
        [100, 200, 500, 1000, 2000, 5000, 10000],
        ["100", "200", "500", "1K", "2K", "5K", "10K"],
    )
    plt.show()

    """ EQUAL LOUDNESS CONTOURS Vs. CORRECTED VALUES"""
    plt.figure(figsize=(10, 5))
    # The lower threshold of hearing is not represented due to the limit that puts the standard by applicating
    # the threshold in quiet
    # plt.semilogx(frequencies, spl_array_0_phons, 'g:', label='0 phons - equal loudness contour')
    plt.semilogx(frequencies, spl_array_20_phons, 'b:', label='20 phons - equal loudness contour')
    plt.semilogx(frequencies, spl_array_40_phons, 'g:', label='40 phons - equal loudness contour')
    plt.semilogx(frequencies, spl_array_60_phons, 'r:', label='60 phons - equal loudness contour')
    plt.semilogx(frequencies, spl_array_80_phons, 'c:', label='80 phons - equal loudness contour')

    plt.semilogx(freq_array, corrected_phon_array[0, :], 'b', label='20 phons - corrected loudness')
    plt.semilogx(freq_array, corrected_phon_array[1, :], 'g', label='40 phons - corrected loudness')
    plt.semilogx(freq_array, corrected_phon_array[2, :], 'r', label='60 phons - corrected loudness')
    plt.semilogx(freq_array, corrected_phon_array[3, :], 'c', label='80 phons - corrected loudness')

    # Legend created following the guidelines from:
    #   https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
    plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
    plt.subplots_adjust(right=0.65)

    plt.xlim(left=100, right=10100)
    plt.ylim(bottom=0, top=120)
    plt.ylabel('Sound pressure level [dB SPL]')
    plt.xlabel('Frequency [Hz]')
    plt.title('Loudness contours - Equal Loudness Contours Vs. Corrected Values')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks(
        [100, 200, 500, 1000, 2000, 5000, 10000],
        ["100", "200", "500", "1K", "2K", "5K", "10K"],
    )
    plt.show()

    """ CORRECTED VALUES Vs. UNCORRECTED VALUES"""
    plt.figure(figsize=(10, 5))
    plt.semilogx(freq_array, uncorrected_phon_array[0, :], 'b:', label='20 phons - uncorrected loudness')
    plt.semilogx(freq_array, uncorrected_phon_array[1, :], 'g:', label='40 phons - uncorrected loudness')
    plt.semilogx(freq_array, uncorrected_phon_array[2, :], 'r:', label='60 phons - uncorrected loudness')
    plt.semilogx(freq_array, uncorrected_phon_array[3, :], 'c:', label='80 phons - uncorrected loudness')

    plt.semilogx(freq_array, corrected_phon_array[0, :], 'b', label='20 phons - corrected loudness')
    plt.semilogx(freq_array, corrected_phon_array[1, :], 'g', label='40 phons - corrected loudness')
    plt.semilogx(freq_array, corrected_phon_array[2, :], 'r', label='60 phons - corrected loudness')
    plt.semilogx(freq_array, corrected_phon_array[3, :], 'c', label='80 phons - corrected loudness')

    # Legend created following the guidelines from:
    #   https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
    plt.legend(bbox_to_anchor=(1.04, 0.5), borderaxespad=0, loc='center left', ncol=1)
    plt.subplots_adjust(right=0.65)

    plt.xlim(left=100, right=10100)
    plt.ylim(bottom=0, top=120)
    plt.ylabel('Sound pressure level [dB SPL]')
    plt.xlabel('Frequency [Hz]')
    plt.title('Loudness contours - Uncorrected Values Vs. Corrected Values')
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks(
        [100, 200, 500, 1000, 2000, 5000, 10000],
        ["100", "200", "500", "1K", "2K", "5K", "10K"],
    )
    plt.show()


if __name__ == "__main__":
    # Execution of the hearing model validation
    hearing_model_validation()
