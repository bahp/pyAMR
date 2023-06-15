##############################################################################
# Author: Bernard Hernandez
# Filename: 03-main-create-sari-idxs.py
# Description : This file contains differnent statistics used in time-series.
#               What it mainly does is to format the output of tests provided
#               by external libraries and return them in a dataframe.
#
# TODO: Move it to a module.
#
###############################################################################
# Forces decimals on divisions.
from __future__ import division

# Libraries
import sys
import numpy as np
import pandas as pd

# Import base wrapper
from pyamr.core.stats.wbase import BaseWrapper
from pyamr.core.stats.wbase import fargs


class StationarityWrapper(BaseWrapper):
    """
    In time series analysis, "stationarity" refers to a key assumption about the behavior
    of a time series over time. A stationary time series is one in which statistical properties,
    such as mean, variance, and autocorrelation, remain constant over time. Stationarity is an
    important concept because many time series analysis techniques rely on this assumption for
    their validity. There are different types of stationarity that can be observed in time series
    data.

    The augmented Dickey–Fuller test or ``ADF`` can be used to determine the presence of a unit root.
    When the other roots of the characteristic function lie inside the unit circle the first
    difference of the process is stationary. Due to this property, these are also called
    difference-stationary processes. Since the absence of unit root is not a proof of non-stationarity,
    the Kwiatkowski–Phillips–Schmidt–Shin or ``KPSS`` test can be used to identify the existence of an
    underlying trend which can also be removed to obtain a stationary process. These are called
    trend-stationary processes. In both, unit-root and trend-stationary processes, the mean can be
    increasing or decreasing over time; however, in the presence of a shock, trend-stationary
    processes (blue) revert to this mean tendency in the long run (deterministic trend) while unit-root
    processes (green) have a permanent impact (stochastic trend). The significance level of the tests
    is usually set to 0.05.

    ================== ================== ========================= ============================
     ADF                KPSS               Outcome                   Note
    ================== ================== ========================= ============================
    ``Non-Stationary`` ``Non-Stationary`` ``Non-Stationary``
    ``Stationary``     ``Stationary``     ``Stationary``
    ``Non-Stationary`` ``Stationary``     ``Trend-Stationary``      Check the de-trended series
    ``Stationary``     ``Non-Stationary`` ``Difference-Stationary`` Check the differenced series
    ================== ================== ========================= ============================

    """

    # --------------------------------------------------------------------------
    #                          overriden methods
    # --------------------------------------------------------------------------
    def evaluate(self, alpha=0.05, **kwargs):
        """This method initialises the series.
        """
        # Create dictionary.
        d = {}

        # Basic statistics (adfuller).
        d['adf_ct_statistic'] = self._raw['adfuller-ct'][0]
        d['adf_ct_pvalue'] = self._raw['adfuller-ct'][1]
        d['adf_ct_nlags'] = self._raw['adfuller-ct'][2]
        d['adf_ct_nobs'] = self._raw['adfuller-ct'][3]
        for key, value in self._raw['adfuller-ct'][4].items():
            d['adf_ct_criticalvalue_%s' % key] = value

        # Basic statistics (adfuller).
        d['adf_c_statistic'] = self._raw['adfuller-c'][0]
        d['adf_c_pvalue'] = self._raw['adfuller-c'][1]
        d['adf_c_nlags'] = self._raw['adfuller-c'][2]
        d['adf_c_nobs'] = self._raw['adfuller-c'][3]
        for key, value in self._raw['adfuller-c'][4].items():
            d['adf_c_criticalvalue_%s' % key] = value

        # Basic statistics (kpss).
        d['kpss_ct_statistic'] = self._raw['kpss-ct'][0]
        d['kpss_ct_pvalue'] = self._raw['kpss-ct'][1]
        d['kpss_ct_nlags'] = self._raw['kpss-ct'][2]
        for key, value in self._raw['kpss-ct'][3].items():
            d['kpss_ct_criticalvalue_%s' % key] = value

        # Basic statistics (kpss).
        d['kpss_c_statistic'] = self._raw['kpss-c'][0]
        d['kpss_c_pvalue'] = self._raw['kpss-c'][1]
        d['kpss_c_nlags'] = self._raw['kpss-c'][2]
        for key, value in self._raw['kpss-c'][3].items():
            d['kpss_c_criticalvalue_%s' % key] = value

        # Extra parameters.
        d['root_ct_stationary'] = d['adf_ct_pvalue'] <= alpha
        d['root_c_stationary'] = d['adf_c_pvalue'] <= alpha
        d['trend_ct_stationary'] = d['kpss_ct_pvalue'] > alpha
        d['trend_c_stationary'] = d['kpss_c_pvalue'] > alpha

        # Unit root (Range unit root test)
        d['rur_statistic'] = self._raw['rur'][0]
        d['rur_pvalue'] = self._raw['rur'][1]
        for key, value in self._raw['rur'][2].items():
            d['rur_criticalvalue_%s' % key] = value

        # Return
        return d

    def as_summary(self, alpha=0.05):
        """This method creates the summary to display.
        """
        # Create summary.
        summary = '      stationarity (alpha=0.05)   \n'
        summary += '==================================\n'
        summary += '          root           trend    \n'
        summary += '----------------------------------\n'
        summary += 'c   {0!s:>5s} ({1:.3f})   {2!s:>5s} ({3:.3f})\n'
        summary += 'ct  {4!s:>5s} ({5:.3f})   {6!s:>5s} ({7:.3f})\n'
        summary += '=================================='

        # Format
        summary = summary.format(self.root_c_stationary,
                                 self.adf_c_pvalue,
                                 self.trend_c_stationary,
                                 self.kpss_c_pvalue,
                                 self.root_ct_stationary,
                                 self.adf_ct_pvalue,
                                 self.trend_ct_stationary,
                                 self.kpss_ct_pvalue)

        # Return
        return summary

    def fit(self, x, adf_kwargs={}, kpss_kwargs={}, **kwargs):
        """This method studies the stationarity of a given time-series.

        The parameters which can be passed to the adfuller and kpss methods
        are listed below:

        - adfuller_kwargs = {x, maxlag, regression, autolag, store, regresults}
        - kpss_kwargs = {x, regression, lags, store}

        @see statsmodels.tsa.stattools.adfuller
        @see statsmodels.tsa.stattoosl.kpss

        Parameters
        ----------
        x : array-like
          The time series

        adf_kwargs : dict-like
          The parameters to pass to the adfuller function

        kpss_kwargs : dict-like
          The parameters to apss to the kpss function


        Returns
        -------
        object : An StationarityWrapper objects.
        """
        # Library.
        from statsmodels.tsa.stattools import adfuller
        from statsmodels.tsa.stattools import kpss
        from statsmodels.tsa.stattools import range_unit_root_test

        # Empty the class
        self._empty()

        # In this fit a number of scenarios are going to be tested. The
        # term that varies within scenarios is regression, as such, if
        # it is passed it will be deleted.
        adf_kwargs.pop('regression', None)
        kpss_kwargs.pop('regression', None)

        # Update the configuration
        self._config.update({'adf_%s' % k: v for k, v in adf_kwargs.items()})
        self._config.update({'kpss_%s' % k: v for k, v in kpss_kwargs.items()})

        # Initialize raw data.
        self._raw = {'x': x}

        # Compute adfuller and kpss
        self._raw['adfuller-ct'] = adfuller(x=x, regression='ct', **adf_kwargs)
        self._raw['adfuller-c'] = adfuller(x=x, regression='c', **adf_kwargs)
        self._raw['kpss-ct'] = kpss(x=x, regression='ct', **kpss_kwargs)
        self._raw['kpss-c'] = kpss(x=x, regression='c', **kpss_kwargs)
        self._raw['rur'] = range_unit_root_test(x=x)

        print(self._raw['rur'])

        # Evaluate the model
        if self.evaluate:
            self._result = self.evaluate()

        # Save results.
        return self


if __name__ == '__main__':

    # Libraries
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    # ----------------------------
    # set basic configuration
    # ----------------------------
    # Set pandas configuration.
    pd.set_option('display.max_colwidth', 14)
    pd.set_option('display.width', 150)
    pd.set_option('display.precision', 4)

    # Set default parameters.
    mpl.rc('lines', linewidth=0.35)
    mpl.rc('xtick', labelsize=6)
    mpl.rc('ytick', labelsize=6)
    mpl.rc('legend', fontsize=6)
    mpl.rc('grid')
    mpl.rc('figure')
    mpl.rc('axes')
    mpl.rc('font', size=7)

    # Font type.
    font = {
        'family': 'monospace',
        'weight': 'normal',
        'size': 6,
    }

    # ----------------------------
    # create data
    # ----------------------------
    # Constants
    length = 100
    offset = 100
    slope = 4

    # Create variables.
    x = np.arange(length)
    n = np.random.rand(length)

    # Create timeseries.
    y_n = n
    y_c = np.ones(length) * offset
    y_t = x * slope + n
    y_ct = x * slope + offset + n * 20
    y_r = np.concatenate((y_ct[:50], y_ct[50:] - offset))

    # ----------------------------
    # create stationarity objects
    # ----------------------------
    # .. note:: Including the constant series with offset produces
    #           the following error: ValueError: cannot convert float
    #           NaN to integer.

    stationarity_n = StationarityWrapper().fit(x=y_n)
    #stationarity_c = StationarityWrapper().fit(x=y_c)
    stationarity_t = StationarityWrapper().fit(x=y_t)
    stationarity_r = StationarityWrapper().fit(x=y_r)
    stationarity_ct = StationarityWrapper().fit(x=y_ct,
         adf_kwargs={'maxlag': 12, 'autolag': 'BIC'})

    # Print series.
    print("\n")
    print(stationarity_ct.as_series())

    # Print summary.
    print("\n")
    print(stationarity_ct.as_summary())

    # Print identifier.
    print("\n")
    print(stationarity_ct._identifier())

    # ----------------
    # plot
    # ----------------
    # Create figure
    fig, axes = plt.subplots(3, 2, figsize=(10, 4))
    axes = axes.flatten()

    # Plot truth values.
    axes[0].plot(y_n, color='#A6CEE3', alpha=0.5, marker='o',
                 markeredgecolor='k', markeredgewidth=0.5,
                 markersize=2, linewidth=0.75,
                 label=stationarity_n.as_summary())

    #axes[1].plot(y_c, color='#A6CEE3', alpha=0.5, marker='o',
    #             markeredgecolor='k', markeredgewidth=0.5,
    #             markersize=2, linewidth=0.75,
    #             label=stationarity_c.as_summary())

    # Plot truth values.
    axes[2].plot(y_t, color='#A6CEE3', alpha=0.5, marker='o',
                 markeredgecolor='k', markeredgewidth=0.5,
                 markersize=2, linewidth=0.75,
                 label=stationarity_t.as_summary())

    # Plot truth values.
    axes[3].plot(y_ct, color='#A6CEE3', alpha=0.5, marker='o',
                 markeredgecolor='k', markeredgewidth=0.5,
                 markersize=2, linewidth=0.75,
                 label=stationarity_ct.as_summary())

    # Plot truth values.
    axes[4].plot(y_r, color='#A6CEE3', alpha=0.5, marker='o',
                 markeredgecolor='k', markeredgewidth=0.5,
                 markersize=2, linewidth=0.75,
                 label=stationarity_r.as_summary())

    # Add grid
    for ax in axes:
        ax.grid(color='gray', linestyle='--', linewidth=0.2, alpha=0.5)

    # Add legend
    for ax in axes:
        ax.legend(prop=font, loc=2)

    # Study of Stationarity
    plt.suptitle("Study of Stationarity")

    # -----------------
    # Save and load
    # -----------------
    # File location
    # fname = '../examples/saved/stationarity-sample.pickle'

    # Save
    # stationarity_ct.save(fname=fname)

    # Load
    # stationarity_ct = StationarityWrapper().load(fname=fname)

    # Show
    #plt.show()
