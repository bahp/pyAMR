"""
Metrics - errors
================

Example with the 'errors' or scores implemented.
"""

# General libraries.
import numpy as np

# Sklearn
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error

# pyAMR
from pyamr.metrics.scores import _mean_absolute_error
from pyamr.metrics.scores import _mean_absolute_percentage_error
from pyamr.metrics.scores import _mean_directional_accuracy
from pyamr.metrics.scores import _mean_absolute_scaled_error

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
