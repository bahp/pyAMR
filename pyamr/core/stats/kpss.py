##############################################################################
# Author: Bernard Hernandez
# Filename: adfuller.py
#
# Description : This file contains a wrapper for the adfuller module.
###############################################################################
# https://mkaz.blog/code/python-string-format-cookbook/
# Future
from __future__ import division

# Libraries
import sys
import numpy as np
import pandas as pd

# Import base wrapper
from pyamr.core.stats.wbase import BaseWrapper


class KPSSWrapper(BaseWrapper):
    """
    The Kwiatkowski–Phillips–Schmidt–Shin (KPSS) test is used to identify
    whether a time series is stationary around a deterministic trend (thus
    trend stationary) against the alternative of a unit root.

    In the KPSS test, the absence of a unit root is not a proof of stationarity
    but, by design, of trend stationarity. This is an important distinction since
    it is possible for a time series to be non-stationary, have no unit root yet
    be trend-stationary.

    In both, unit-root and trend-stationary processes, the mean can be increasing
    or decreasing over time; however, in the presence of a shock, trend-stationary
    processes revert to this mean tendency in the long run (deterministic trend)
    while unit-root processes have a permanent impact (stochastic trend).

    ====== =========================== =====================================
    H      Hypothesis                  Stationarity
    ====== =========================== =====================================
    **H0** The series has no unit root ``Trend-stationary``
    **H1** The series has a unit root  ``No Trend-Stationary``
    ====== =========================== =====================================

    | If p-value > alpha: Failed to reject H0
    | If p-value <= alpha: Reject H0
    """
    pass