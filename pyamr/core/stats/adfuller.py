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

    def _identifier(self):
        """Description of the model"""
        return "%s(%s)" % (self._name, self.regression)

    # --------------------------------------------------------------------------
    #                             new methods
    # --------------------------------------------------------------------------
    def is_stationary(self, alpha=0.05):
        """This method returns a boolean with the stationarity outocme.

        The method rejects the null hypothesis when the value is less than a
        specified significance level. The null hypothesis is unit root exists
        and the alternative is that series is (trend) stationary.

        Notes
        -----
        H0: There is a unit root' hence non-stationary.
        H1: The series does not have a unit root; hence stationary.

        If p-value > 0.05: Failed to reject H0.
        If p-value <= 0.05: Reject H0. Stationary.

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

    def as_summary(self, alpha=0.05, **kwargs):
        """This method creates the summary to display.
        """
        # Create templates
        summary = '  adfuller test stationarity ({r}) \n'
        summary += "==================================\n"
        summary += "statistic:       {statistic:>17.3f}\n"
        summary += "pvalue:          {pvalue:>17.5f}   \n"
        summary += "nlags:           {nlags:>17.0f}    \n"
        summary += "nobs:            {nobs:>17.0f}     \n"
        summary += "stationary ({alpha}): {stationarity:>15s}\n"
        summary += "=================================="

        #print(self.__dict__)

        # Format
        summary = summary.format(r=self.regression,
            statistic=self.statistic, pvalue=self.pvalue,
            nlags=self.nlags, nobs=self.nobs, alpha=alpha,
            stationarity=self.stationarity(alpha), feo=0)

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
    grid_params = {'x': [y], 'regression': ['c', 'nc', 'ct']}

    # Get wrappers.
    lwrappers = adf.grid_search(grid_params=grid_params, verbose=1)

    # Get summary.
    summary = adf.from_list_dataframe(lwrappers, flabel=True)

    # Plot result.
    print("\n")
    print(summary.T)
