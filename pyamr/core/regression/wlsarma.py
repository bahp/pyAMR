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
import copy
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

import scipy.stats as stats

# Import pyamr
from pyamr.core.regression.wregression import BaseRegressionWrapper
from pyamr.core.regression.wls import WLSWrapper
from pyamr.core.regression.arima import ARIMAWrapper
from pyamr.core.regression.sarimax import SARIMAXWrapper


class WLSARMAWrapper(BaseRegressionWrapper):
    # Attributes.
    _name = 'WLSARMA'  # Label to add to the attributes when saving.

    def _identifier(self, **kwargs):
        """This methods describes de model."""
        # Returns description
        return "%s + %s" % (self._wls._identifier(), self._arma._identifier())

    # --------------------------------------------------------------------------
    #                            SET VARIABLES
    # --------------------------------------------------------------------------
    def _params_from_summary(self):
        """Gets parameters from the summary result of the raw object.
        """
        # Return
        return {}

    def _init_result(self, alpha=0.05):
        """This method set all the variables into this class.

        Notes:
          - if instead of having the attribute series it is desired to set
          each element of the series as an attribute, just used the following
          statement: setattr(self, name, value).

          - Note the difference between the resid and wresid since they will
          also have different statistical properties. Furthermore, there is
          a vector with normalized residuals resid_pearson.

        @see: statsmodels.WLS
        @see: statsmodels.tsa.ARIMA
        @see: statsmodels.RegressionResultsWrapper

        Parameters
        ----------

        Returns
        -------
        """
        # Libraries.
        from statsmodels.iolib.summary import _getnames

        # Create series.
        d = {}

        # Add generic metrics.
        # Create params information.
        # Add coefficients statistics.

        # Further statistics.
        d.update(self._params_from_summary())
        d.update(self._resid_stats())

        # Return
        return d

    # --------------------------------------------------------------------------
    #                           HELPER METHODS
    # --------------------------------------------------------------------------
    def as_summary(self, **kwargs):
        """This method displays the summary.
        """
        # Variables.
        om, dw = 0.0, self.m_dw,
        pom, jb = 0.0, self.m_jb_value
        skew, pjb = self.m_skew, self.m_jb_prob
        kurt, cond = self.m_kurtosis, 0.0
        norm, pnorm = self.m_nm_value, self.m_nm_prob

        # Create summary.
        smry = "WLSARMA Regression Results".center(78)
        smry += "\n" + "=" * 78 + "\n"
        smry += "Omnibus:       %#21.3f  Durbin-Watson:    %#22.3f\n" % (om, dw)
        smry += "Prob(Omnibus): %#21.3f  Jarque-Bera (JB): %#22.3f\n" % (pom, jb)
        smry += "Skew:          %#21.3f  Prob(JB):         %#22.3f\n" % (skew, pjb)
        smry += "Kurtosis:      %#21.3f  Cond. No.:        %#22.3f\n" % (kurt, cond)
        smry += "Normal (N):    %#21.3f  Prob(N):          %#22.3f\n" % (norm, pnorm)
        smry += "=" * 78

        # Return
        return smry

    # --------------------------------------------------------------------------
    #                                 FIT
    # --------------------------------------------------------------------------
    def fit(self, endog, exog=None, weights=None, wls_kwargs={},
            arima_kwargs=None,
            sarimax_kwargs=None,
            **kwargs):
        """This method...

        Parameters
        ----------
        endog        :
        exog         :
        wls_kwargs   :
        arima_kwargs :
        sarimax_kwargs :
        kwargs :

        Returns
        -------
        """
        # Create weighted linear regression
        self._wls = WLSWrapper(sm.WLS).fit(endog=endog, exog=exog,
                                     weights=weights,
                                     **wls_kwargs)

        # Create best fitting for ARIMA.
        if arima_kwargs is not None:
            self._arma = \
                ARIMAWrapper(ARIMA).fit(endog=self._wls._resid, **arima_kwargs)

        # Create best fitting for SARIMAX.
        if arima_kwargs is None and sarimax_kwargs is not None:
            self._arma = \
                SARIMAXWrapper(SARIMAX).fit(endog=self._wls._resid, **sarimax_kwargs)

        # Set fitted values (what if arima d=1).
        self._fittedvalues = self.get_prediction()[1, :]

        # Set residuals
        self._resid = endog - self._fittedvalues

        # Set series.
        self._result = self._init_result(alpha=0.05)

        # Return
        return self

    def get_prediction(self, start=None, end=None, ptype='combined', **kwargs):
        """This method computes the prediction.

        Note: Correct for ARIMA. The arima is trained with n samples (e.g. 24)
        and then we ask for start=50 and end=74 hance for some reason arima
        becomes crazy and return a larger array. Therefore, we predict for
        indices None (begining) till the maxium number to predict which is
        fshape-start.

        Parameters
        ----------
        start : start of prediction (as in wls)
        end   : end of preediction (as in wls)
        type  : string (combined, wls, arma)

        Returns
        -------
        """
        # Create end for arma.
        end_arma = None if start is None or end is None else end - start

        # Return partial predictions.
        if ptype == 'wls':
            return self._wls.get_prediction(start=start, end=end)
        if ptype == 'arma':
            return self._arma.get_prediction(start=None, end=end_arma, **kwargs)

        # Compute both predictions
        pred_wls = self._wls.get_prediction(start=start, end=end)
        pred_arma = self._arma.get_prediction(start=None, end=end_arma, **kwargs)

        # Create combined predictions (careful with this).
        pred = np.empty(pred_wls.shape)
        pred[1, :] = pred_wls[1, :]
        pred[1, pred_arma[0, :].astype(int)] += pred_arma[1, :]

        # Return
        return pred


if __name__ == '__main__':
    # Import class.
    print("E")