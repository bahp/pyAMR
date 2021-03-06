"""
Step 03 - TSA for trends
========================

.. warning:: To be completed!

"""

##############################################################
#
# The diagram in Figure 4.7 describes the methodology implemented to estimate secular
# trends in AMR from susceptibility data. Since data corruption might occur in clinical
# environments, those susceptibility test records wrongly reported (human or device errors)
# or duplicated were discarded. The remaining records were divided into combinations
# (tuples defined by sample type, pathogen and antimicrobial) for which a resistance time
# series signal was generated using either independent or overlapping time intervals (see
# xxx). The time series were linearly interpolated to fill sporadic missing values. No
# additional filters or preprocessing steps were applied. An analysis of stationarity around
# a trend was carried out to identify interesting combinations and regression
# analysis was used to quantify its tendency
#

# .. image:: ../../../_static/imgs/sart-diagram.png
#   :width: 600
#   :align: center
#   :alt: Diagram
#
# |
#
# The linear model (see Equation 4.3) has been selected to quantify resistance tendency
# for several reasons: (i) the development of resistance in pathogens is an evolutionary
# response to the selective pressure of antimicrobials, hence large variations in short
# periods (e.g. consecutive days or months) are not expected (ii) the slope parameter can
# be directly translated to change over time increasing its practicability and (iii) the
# offset parameter is highly related with the overall resistance. Hence, the response variable
# in regression analysis (resistance index) is described by the explanatory variable (time).
# The slope (m) ranges within the interval [-1,1] where sign and absolute value capture
# direction and rate of change respectively. The unit of the slope is represented by ∆y/∆x.
#
# - **Least Squares Regression**
#
#   The optimization problem in ordinary least squares - ``OLS`` - regression minimizes the least
#   square errors to find the best fitting model. Ordinary least squares - OLS - assumes
#   identical weights (wi) and independently distributed residuals with a normal distribution.
#   It is frequent to observe that some residuals might have higher variance than others,
#   meaning that those observations are effectively less certain. To contemplate such variability,
#   weighted linear squares - ``WLS`` - regression (see Equation 4.4) applies a weighting
#   function to the residuals. The confidence of the computed resistance index (observed
#   variable) relies on the number of susceptibility test records manipulated. Hence, the
#   sigmoid function has been used to define weights proportional to the population size.
#
# - **Auto Regressive Integrated Moving Average** - ``ARIMA``
#
#   An autoregressive integrated moving average (ARIMA) model is a generalization of an
#   autoregressive moving average (ARMA) model which can be also applied in scenarios
#   where data show evidence of non-stationarity. The autoregressive (AR) part expresses
#   the variable of interest (resistance index) as a function of past values of the variable.
#   The moving average (MA) indicates that the regression error is a linear combination of
#   error terms which occurred contemporaneously and at various times in the past. An
#   ARIMA(p,d,q) model is described by: p is the number of autoregressive terms,
#   d is the number of differences needed for stationarity and q is the
#   number of lagged forecast errors.
#
#   Include formula.
#
#   The interpretation of the parameter µ depends on the ARIMA model used for the
#   fitting. In order to estimate the linear trend, it was interesting to consider exclusively
#   MA models so that the expected value of µ was the mean of the one-time differenced
#   series; that is, the slope coefficient of the un-differenced series. The Bayesian information
#   criterion (BIC) was used to select the best ARIMA(0,1,q) model, being the one with the
#   lowest BIC the preferred.
#
#

# Import
import pandas as pd