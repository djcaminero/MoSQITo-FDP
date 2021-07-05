# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""

import numpy as np


def phon2sone(phons):
    """ Conversion between sones and phons, based on the work done by Hugo Fastl and Eberhard Zwicker in the article
    "Psychoacoustics: Facts and Models".

    Parameters
    -------
    phons: float
        Logarithmic unit of loudness (phon = Ln). The dB SPL values of the signal at 1 kHz have the same value in
        phons. For example, 50 db SPL @ 1 kHz corresponds to 50 phones. The rest of the frequencies does not have
        the same co-relation between each other.

    Returns
    -------
    sones: float
        One of the units in which loudness is measured. 1 sone equals to 40 phones. The conversion from sones to phones
        is not linear.

    """
    if phons >= 40:
        sones = np.power(2, ((phons - 40) / 10))

    else:
        sones = ((phons / 40) ** 2.86) - 0.005

    return sones
