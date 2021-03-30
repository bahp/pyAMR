###############################################################################
# Author: Bernard Hernandez
# Filename:
# Date: 
# Description:
#
###############################################################################
# Float division.
from __future__ import division

# General libraries.
import math
import itertools
import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error


def _mean_absolute_error(y_true, y_pred):
    """It computes the mean absolute error.
    
    .. note: This function is fully implemented in scikits.

    Parameters
    ----------
    y_true : array-like
      Real values

    y_pred: array-like
      Predicted values

    Returns
    -------
    float
    """
    # Format arrays.
    y_true = y_true.ravel()
    y_pred = y_pred.ravel()
    # Return
    return np.abs(y_true - y_pred).sum() / y_true.shape[0]


def _mean_absolute_percentage_error(y_true, y_pred):
    """It computes the mean absolute error.

    .. note: This function crashes when the y_true value is zero.

    Parameters
    ----------
    y_true : array-like
      Real values

    y_pred: array-like
      Predicted values

    Returns
    -------
    float
    """
    # Format arrays.
    y_true = y_true.ravel()
    y_pred = y_pred.ravel()
    # Return
    return (100. / y_pred.shape[0]) * np.abs((y_true - y_pred) / y_true).sum()


def _mean_directional_accuracy(y_true, y_pred):
    """It computes the mean directional accuracy.

    Parameters
    ----------
    y_true : array-like
      Real values

    y_pred: array-like
      Predicted values

    Returns
    -------
    float
    """
    # Format arrays.
    y_true = y_true.ravel()
    y_pred = y_pred.ravel()
    # Compute
    s1 = np.sign(np.ediff1d(y_true))
    s2 = np.sign(np.ediff1d(y_pred))
    # Return
    return (s1 == s2).sum() / y_true.shape[0]


def _mean_absolute_scaled_error(y_train, y_test, y_pred):
    """It computes the mean absolute scaled error.

    Parameters
    ----------
    y_train : array-like
      Training values

    y_test: array-like
      Testing values

    Returns
    -------
    float
    """
    # Format arrays.
    y_train = y_train.ravel()
    y_test = y_test.ravel()
    y_pred = y_pred.ravel()
    # Compute
    n = y_train.shape[0]
    d = np.abs(np.diff(y_train)).sum() / (n - 1)
    forecast_error = np.abs(y_test - y_pred)
    # Return
    return forecast_error.mean() / d


if __name__ == '__main__':

    # Libraries
    import numpy as np

    # Numpy configuration
    np.set_printoptions(precision=2)

    # ---------------------------
    # create data
    # ---------------------------
    # Create time series
    y_true = np.array([10, 11, 12, 11, 12, 11, 13, 12, 13, 14, 15, 16, 18, 17])
    y_pred = np.array([11, 11, 11, 11, 12, 12, 12, 13, 13, 13, 18, 18, 18, 18])

    # Scores
    s1 = mean_absolute_error(y_true, y_pred)
    s2 = _mean_absolute_error(y_true, y_pred)
    s3 = mean_squared_error(y_true, y_pred)
    s4 = mean_squared_log_error(y_true, y_pred)
    s5 = _mean_absolute_percentage_error(y_true, y_pred)
    s6 = _mean_directional_accuracy(y_true, y_pred)
    s7 = _mean_absolute_scaled_error(y_true[:10], y_true[10:], y_pred[10:])
    s10 = median_absolute_error(y_true, y_pred)

    # Compute scores
    print("\nScores:")
    print("-------")
    print('Mean Absolute Error            : %.3f' % s1)
    print('Mean Absolute Error (_)        : %.3f' % s2)
    print('Mean Squared Error             : %.3f' % s3)
    print('Mean Squared Log Error         : %.3f' % s4)
    print('Mean Absolute Percentage (_)   : %.3f' % s5)
    print('Mean Directional Accuracy (_)  : %.3f' % s6)
    print('Mean Absolute Scaled error (_) : %.3f' % s7)
    print('Median Absolute Error          : %.3f' % s10)