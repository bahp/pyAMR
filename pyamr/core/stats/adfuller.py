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


class ADFWrapper(BaseWrapper):
    """The ADF wrapper.

    The Augmented Dickey-Fuller test can be used to test for a unit root in
    a univariate process in the presence of serial correlation. It tests the
    null hypothesis that a unit root is present in a time series sample. The
    alternative hypothesis is different depending on which version of the test
    is used, but is usually stationarity or trend-stationarity. The more
    negative the statistic, the stronger the rejection of the hypothesis that
    there is a unit root at some level of confidence.

    Notes
    -----
    H0: The series has a unit root => Non-stationary
    H1: The series has no unit root => Stationary / Trend-Stationary

    If p-value > 0.05: Failed to reject H0.
    If p-value <= 0.05: Reject H0.

    The absence of unit root is not a proof of non-stationarity. As such, it
    is also possible to use the Kwiatkowski–Phillips–Schmidt–Shin (KPSS) test
    to identify the existence of an underlying trend which can also be removed
    to obtain a stationary process. These are called trend-stationary processes.

    In both, unit-root and trend-stationary processes, the mean can be increasing
    or decreasing over time; however, in the presence of a shock, trend-stationary
    processes revert to this mean tendency in the long run (deterministic trend)
    while unit-root processes have a permanent impact (stochastic trend).

    [1] https://machinelearningmastery.com/time-series-data-stationary-python/
    [2] https://www.statsmodels.org/stable/examples/notebooks/generated/stationarity_detrending_adf_kpss.html

    .. todo: .
    """

    def _identifier(self):
        """Description of the model"""
        return "%s(%s)" % (self._name, self.regression)

    # --------------------------------------------------------------------------
    #                             new methods
    # --------------------------------------------------------------------------
    def is_stationary(self, alpha=0.05):
        """This method returns a boolean with the stationarity outocme.

        Parameters
        ----------
        alpha : float
          The statistical significance

        Returns
        -------

        """
        return True if self._result['pvalue'] <= alpha else False

    def stationarity(self, alpha=0.05):
        """This method returns the stationarity outcome.

        Parameters
        ----------
        alpha : float
          The stastistical significance

        Returns
        -------

        """
        return 'stationary' if self.is_stationary(alpha) else 'non-stationary'

    # --------------------------------------------------------------------------
    #                          overriden methods
    # --------------------------------------------------------------------------
    def evaluate(self, **kwargs):
        """Evaluates the model.
        """
        # Create dictionary
        d = {}

        # Basic statistics
        d['statistic'] = self._raw[0]
        d['pvalue'] = self._raw[1]
        d['nlags'] = self._raw[2]
        d['nobs'] = self._raw[3]
        d['stationary'] = self._raw[1] < 0.05

        # Format critical value array.
        for key, value in self._raw[4].items():
            d['criticalvalue_%s' % key] = value

        # Return
        return d

    def as_summary(self, alpha=0.05, verbose=1, **kwargs):
        """This method creates the summary to display.

        .. note: Use self.__dict__ to pass all the parameters
                 to format? Note however that the parameters
                 used are in self._result.
        """
        # Symbols
        alpha_symbol = '\u03B1'

        # Template start
        summary = '    adfuller test stationarity ({r})    \n'
        summary += "=======================================\n"
        summary += "statistic:           {statistic:>18.3f}\n"
        summary += "pvalue:              {pvalue:>18.5f}   \n"
        summary += "nlags:               {nlags:>18.0f}    \n"
        summary += "nobs:                {nobs:>18.0f}     \n"
        summary += "stationarity ({s}={alpha}): {stationarity:>16s}\n"

        if verbose > 5:
            # Add critical values
            summary += "---------------------------------------\n"
            summary += "critical value (1%):  {cc1:>17.5f} \n"
            summary += "critical value (5%):  {cc5:>17.5f} \n"
            summary += "critical value (10%): {cc10:>17.5f}\n"

        if verbose > 7:
            # Add hypothesis description
            summary += "---------------------------------------\n"
            summary += "H0:                    Exists unit-root\n"
            summary += "H1:                 No Exists unit-root\n"
            summary += "pvalue <= {s}:                  Reject H0\n"

        # Template end
        summary += "======================================="

        # Format
        summary = summary.format(r=self.regression,
            statistic=self.statistic, pvalue=self.pvalue,
            nlags=self.nlags, nobs=self.nobs, alpha=alpha,
            stationarity=self.stationarity(alpha),
            cc1=self._result['criticalvalue_1%'],
            cc5=self._result['criticalvalue_5%'],
            cc10=self._result['criticalvalue_10%'],
            s=alpha_symbol)

        # Return
        return summary


if __name__ == '__main__':

    # Libraries
    import pandas as pd

    # Import specific
    from statsmodels.tsa.stattools import adfuller

    # ----------------------------
    # set basic configuration
    # ----------------------------
    # Set pandas configuration.
    pd.set_option('display.max_colwidth', 14)
    pd.set_option('display.width', 150)
    pd.set_option('display.precision', 4)

    # ----------------------------
    # create data
    # ----------------------------
    # Constants
    length = 100
    offset = 100
    slope = 10

    # Create timeseries.
    x = np.arange(length)
    y = np.random.rand(length) * slope + offset

    # ----------------------------
    # create adfuller object
    # ----------------------------
    # Create object
    adf = ADFWrapper(estimator=adfuller).fit(x=y, regression='ct')

    # Print series.
    print("\n")
    print(adf.as_series())

    # Print summary.
    print("\n")
    print(adf.as_summary())
    print(adf.as_summary(verbose=10))

    # Print identifier.
    print("\n")
    print(adf._identifier())

    # -----------------
    # Save and load
    # -----------------
    # File location
    # fname = '../examples/saved/adfuller-sample.pickle'

    # Save
    # adf.save(fname=fname)

    # Load
    # adf = ADFWrapper().load(fname=fname)

    # -----------
    # Grid search
    # -----------
    # Create wrapper
    adf = ADFWrapper(adfuller)

    # Grid parameters.
    grid_params = {'x': [y], 'regression': ['c', 'n', 'ct']}

    # Get wrappers.
    lwrappers = adf.grid_search(grid_params=grid_params, verbose=1)

    # Get summary.
    summary = adf.from_list_dataframe(lwrappers, flabel=True)

    # Plot result.
    print("\n")
    print(summary.T)
