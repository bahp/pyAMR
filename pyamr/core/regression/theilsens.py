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
import statsmodels.api as sm

# Import pyamr
from pyamr.core.regression.wregression import BaseRegressionWrapper


class TheilSensWrapper(BaseRegressionWrapper):
    # Attributes.
    _name = 'THEILSENS'  # Label to add to the attributes when saving.

    # --------------------------------------------------------------------------
    #                           HELPER METHODS
    # --------------------------------------------------------------------------
    def _init_result(self, alpha=0.05):
        """This method set all the variables into this class.
        """
        # Create series
        d = {}
        # Set results.
        d['slope'] = self._raw[0]
        d['intercept'] = self._raw[1]
        d['ci_lower'] = self._raw[2]
        d['ci_upper'] = self._raw[3]
        # Return
        return d

    def as_summary(self, alpha=0.05):
        """This method displays the summary.
        """
        # Create summary base
        summary = '         TheilSens Slope   \n'
        summary += "==================================\n"
        summary += "slope:     %23s\n" % str(round(self.slope, 4))
        summary += "intercept: %23s\n" % str(round(self.intercept, 4))
        summary += "ci_lower:  %23s\n" % str(round(self.ci_lower, 4))
        summary += "ci_upper:  %23s\n" % str(round(self.ci_upper, 4))
        summary += "=================================="
        # Return
        return summary

    # --------------------------------------------------------------------------
    #                                 FIT
    # --------------------------------------------------------------------------
    def fit(self, **kwargs):
        """This method....

        Parameters
        ----------
        x :
        y :
        alpha :

        Returns
        -------
        object : A KendallWrapper objects.
        """
        # Library.
        from scipy.stats.mstats import theilslopes
        # Save parameters.
        self._config.update(kwargs)
        self._conkwargs = self.fargs(self._config, theilslopes)
        # Compute theilsens slopes
        self._raw = theilslopes(**self._conkwargs)
        # Set series.
        self._result = self._init_result()
        # Compute residuals.
        x, y = kwargs['x'], kwargs['y']
        self._resid = y - (x * self.slope + self.intercept)
        # return
        return self

    def get_prediction(self, exog=None, start=None, end=None, **kwargs):
        """This method...

        Parameters
        ----------
        exog      :
        start     :
        end       :
        kwargs    :

        Returns
        -------
        """
        # Create exogenous variable.
        if start is not None or end is not None:
            exog = self._exog(start, end)

        # Compute prediction
        forecast = exog * self.slope + self.intercept
        # Get plotting values.
        mean = forecast.reshape(1, -1)
        cilo = self.conf_int_insample(mean, alpha=0.05)[:, 0].reshape(1, -1)
        ciup = self.conf_int_insample(mean, alpha=0.05)[:, 1].reshape(1, -1)
        # Add time.
        time = exog.reshape(1, -1)
        # Get plotting values.
        return np.concatenate((time, mean, cilo, ciup), axis=0)


if __name__ == '__main__': # pragma: no cover
    # Libraries.
    import matplotlib.pyplot as plt

    # Set pandas configuration.
    pd.set_option('display.max_colwidth', 14)
    pd.set_option('display.width', 150)
    pd.set_option('display.precision', 4)

    # Constants
    length = 100
    offset = 100
    slope = 10

    # Create timeseries.
    x = np.arange(length)
    y = np.random.rand(length) * slope + offset + x

    # Create object
    theilsens = TheilSensWrapper().fit(x=x, y=y)

    # Print series.
    print("\n")
    print(theilsens.as_series())
    # Print summary.
    print("\n")
    print(theilsens.as_summary())

    import sys
    sys.exit()

    # -----------------
    # Save & Load
    # -----------------
    # File location
    fname = '../../examples/saved/theilsens-sample.pickle'

    # Save
    theilsens.save(fname=fname)

    # Load
    theilsens = TheilSensWrapper().load(fname=fname)

    # -----------------
    #  Predictions
    # -----------------
    # Variables.
    start, end, = 10, 70

    # Compute predictions.
    preds = theilsens.get_prediction(start=start, end=end)

    # Plot truth values.
    plt.plot(x, y, color='#A6CEE3', alpha=0.5, marker='o',
             markeredgecolor='k', markeredgewidth=0.5,
             markersize=5, linewidth=0.75, label='Observed')

    # Plot forecasted values.
    plt.plot(preds[0, :], preds[1, :], color='#FF0000', alpha=1.00,
             linewidth=2.0, label=theilsens._identifier())

    # Plot the confidence intervals.
    plt.fill_between(preds[0, :], preds[2, :],
                     preds[3, :],
                     color='r',
                     alpha=0.1)

    # Legend
    plt.legend()

    # Grid search
    # -----------
    # Grid parameters.
    grid_params = {'x': [x], 'y': [y], 'alpha': [0.05, 0.1]}

    # Get summary.
    summary = TheilSensWrapper().grid_search_dataframe(grid_params=grid_params)

    # Plot result (drop x which is an array to improve visualization).
    print(summary)

    # Show
    plt.show()
