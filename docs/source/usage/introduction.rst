Introduction
============

.. _phe: https://www.gov.uk/government/organisations/uk-health-security-agency/

The growing threat of antimicrobial resistance (AMR) is a leading patient health and
safety issue, with estimates that AMR will be responsible for more than 10 million deaths
by 2050. A major driver of AMR has been the misuse of antimicrobials
in humans. Whilst reasons for the misuse of antimicrobials are complex and multifaceted, a number
of factors have been described and investigated. At the individual level, physicians often prioritise
the management of the patient being treated, paying little regard to the long-term consequences of overusing
antimicrobials. Moreover, the majority of antimicrobials are prescribed by individuals who are
not experts in infection management and may have limited understanding of antimicrobials and the
potential consequences of AMR.

For such reason, numerous health organizations have promoted antimicrobial surveillance to regulate
prescriptions within clinical practice. At national level, Public Health England implemented the
English surveillance program for antimicrobial utilisation and resistance (ESPAUR) which
provides annual reports as a benchmark to determine appropriate local action.
At international level, the European Centre for Disease Prevention and Control through
the European antimicrobial resistance surveillance network (EARS-Net) has created the
largest publicly funded system for antimicrobial surveillance in Europe. Furthermore,
the World Health Organization has recently implemented the global antimicrobial resistance surveillance
system (GLASS) to strengthen the evidence base on AMR and inform decision-making.

With increasing electronic recording of data, there is a growing interest in the potential secondary
use of microbiology records to provide the necessary information to support antimicrobial stewardship
programs. These programs are crucial to guide health care organizations designing evidence-based
policies to combat AMR. In particular, susceptibility reporting has shown to be a determinant
data source to inform empiric antimicrobial therapy selection.

.. image:: ../../_static/imgs/susceptibility-test-record.png
   :width: 200
   :align: right
   :alt: ASAI

Susceptibility test records (see Figure) are composed by laboratory identification
number (LID), patient identification number (PID), date, sample type or culture (e.g.
blood or urine), pathogen, antimicrobial, reported status and outcome (resistant, sensitive
or intermediate). In research, the susceptibility test data is usually first grouped by
specimen or culture type, and further grouped by pairs (pathogen, antimicrobial)
since it is widely accepted by clinicians as detailed in the UK five year strategy in AMR.




The AMR indexes
---------------

======== ============================================== ======= =============
Acronym  Name                                           Range   Status
======== ============================================== ======= =============
``SARI`` Single Antimicrobial Resistance Index          [0, 1]  ``Ok``
``MARI`` Multiple Antimicrobial Resistance Index        [0, 1]  ``Ok``
``DRI``  Drug Resistance Index                                  ``Pending``
``SART`` Single Antimicrobial Resistance Trend          [0, 1]  ``Ok``
``ASAI`` Antimicrobial Spectrum of Activity Index       [-1, 1] ``Ok``
======== ============================================== ======= =============

- **Single Antimicrobial Resistance Index (SARI)**

    The single antimicrobial resistance index describes the proportion of resistant isolates for a
    given set of susceptibility tests. It provides a value within the range [0,1] where values close
    to one indicate high resistance. It is agnostic to pathogen, antibiotic and time. The variables *R*,
    *I* and *S* represent the number of susceptibility tests with Resistant, Intermediate and Susceptible
    outcomes respectively. The definition might vary slightly since the intermediate category is not
    always considered.

    See: :py:mod:`pyamr.core.sari.SARI`

    Example: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_sari.py`

- **Multiple Antimicrobial Resistance Index (MARI)**

    The multiple antimicrobial resistance describes the ratio of antimicrobials tested (*T*) to which a
    pathogen is resistant (*R*). It provides a value within the range [0,1] where values close to
    one indicate high multi-drug resistance. It highly depends on the antimicrobials to which the
    pathogen is tested. Since tested antimicrobials vary among health care centres and time, comparison
    and analysis of its evolution in time is not straight forward. In addition, antibiotics which are
    intrinsically resistant should not be considered.

    See: :py:mod:`pyamr.core.mari.MARI`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_mari.py`


- **Drug Resistance Index (DRI)**

    The drug resistance index measures the proportion of pathogens that are resistant to the
    antimicrobials used to treat them. It provides a value within the range [0,1] where values
    close to one indicate high resistant for frequent antimicrobials. The variable *ρik* is the
    proportion of resistance among organism *i* to antimicrobial *k* and *qik* is the
    frequency of drug *k* used to treat organism *i*.

    .. warning:: Not implemented!

- **Antimicrobial Spectrum of Activity Index (ASAI)**

    The antimicrobial spectrum of activity index refers to the range of microbe species that are
    susceptible to these agents and therefore can be treated. In general, antimicrobial agents are
    classified into broad, intermediate or narrow spectrum. Broad spectrum antimicrobials are active
    against both Gram-positive and Gram-negative bacteria. In contrast, narrow spectrum antimicrobials
    have limited activity and are effective only against particular species of bacteria.

    See: :py:mod:`pyamr.core.asai.ASAI`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_asai.py`

- **Single Antimicrobial Resistance Trend (SART)**

    The single antimicrobial resistance trend measures the ratio of change per time unit
    (e.g. monthly or yearly). To compute this metric, it is necessary to generate a
    resistance time series from the susceptibility test data. This is often achieved by
    computing the SARI consecutive or overlapping partitions of the data. Then, the trend
    can be extracted using for example a linear model where the slope, which is a value
    within the range [-1, 1] indicates the ratio of change.

    See: :py:mod:`pyamr.core.sart.SART`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_sart.py`








Time series analysis
--------------------

Time series analysis is a specific way of analyzing a sequence of data points collected over
an interval of time. In time series analysis, analysts record data points at consistent intervals
over a set period of time. Time series analysis typically requires a large number of data points
to ensure consistency and reliability. An extensive data set ensures you have a representative
sample size and that analysis can cut through noisy data. It also ensures that any trends or patterns
discovered are not outliers and can account for seasonal variance. Additionally, time series data
can be used for forecasting—predicting future data based on historical data.

Examples using time-series analysis in ``pyAMR``.

    - :ref:`sphx_glr__examples_tutorial_guide_plot_step_03.py`
    - :ref:`sphx_glr__examples_tutorial_guide_plot_step_04.py`

..
    - :ref:`examples-with-tsa`


..
    Time-series analysis is a method of analyzing data to extract useful statistical information and
    characteristics. One of the study's main goals is to predict future value. When forecasting with
    time series analysis, which is extremely complex, extrapolation is required. However, the forecasted
    value and the associated uncertainty estimation can make the result extremely valuable.

In time-series analysis, it is necessary to understand various statistical properties/tests
in order to assess which method to use and to better understand the behaviour of the
produced models. A summary of these statistical properties/tests is presented below.


Statistical properties
~~~~~~~~~~~~~~~~~~~~~~

A statistic (singular) or sample statistic is any quantity computed from values in a sample which
is considered for a statistical purpose. Some of the most commonly used descriptive statistics are
central tendency, dispersion, skewness, and tailednes.


====================== ==================================================== ============= ========
Name                   Description                                          Range         Choose
====================== ==================================================== ============= ========
``pearson``            Measures linear correlation between variables        [-1, 1]         ≈0
``kurtosis``           Measure of tailedness of a probability distribution  [1, ∞)          ≈0
``skewness``           Measure of asymmetry of a probability distribution                   ≈0
``R2``                 Measures goodness-of-fit or linear regression models [0, 100]        ↑
``aic``                Measures goodness-of-fit among models                                ↓
``bic``                Measures goodness-of-fit among models                                ↓
``hqic``               Measures goodness-of-fit among models                                ↓
``llf``                Measures goodness-of-fit among models                (-∞, ∞)         ↑
====================== ==================================================== ============= ========

Pearson
*******

.. _R1: https://cdn.scribbr.com/wp-content/uploads/2022/05/Strong-positive-correlation-and-strong-negative-correlation.webp
.. _R2: https://upload.wikimedia.org/wikipedia/commons/3/34/Correlation_coefficient.png

.. image:: https://www.simplilearn.com/ice9/free_resources_article_thumb/Pearson_Correlation_1.jpg
   :width: 320
   :align: right
   :alt: pearson

In statistics, the Pearson correlation coefficient is a measure of linear correlation
between two sets of data. It is the ratio between the covariance of two variables and
the product of their standard deviations; thus, it is essentially a normalized measurement
of the covariance, such that the result always has a value between −1 and 1. The measure
can only reflect a linear correlation of variables, and ignores many other types of
relationships or correlations.


R2
**

.. _R3: https://statisticsbyjim.com/regression/interpret-r-squared-regression/

R-squared is a goodness-of-fit measure for linear regression models. This
statistic indicates the percentage of the variance in the dependent variable
that the independent variables explain collectively. R-squared measures the
strength of the relationship between your model and the dependent variable
on a convenient 0 – 100% scale. R-squared is always between 0 and 100% where
(i) **0%** represents a model that does not explain any of the variation in the
response variable around its mean. The mean of the dependent variable predicts
the dependent variable as well as the regression model and (ii) **100%** represents
a model that explains all the variation in the response variable around its mean.


Skewness
********

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Negative_and_positive_skew_diagrams_%28English%29.svg/446px-Negative_and_positive_skew_diagrams_%28English%29.svg.png
   :width: 320
   :align: right
   :alt: skewness

Skewness is a measure of the asymmetry of the probability distribution of a
real-valued random variable about its mean. The skewness value can be positive,
zero, negative, or undefined.

For a unimodal distribution, negative skew commonly indicates that the tail is
on the left side of the distribution, and positive skew indicates that the tail
is on the right. In cases where one tail is long but the other tail is fat,
skewness does not obey a simple rule. For example, a zero value means that the
tails on both sides of the mean balance out overall; this is the case for a
symmetric distribution, but can also be true for an asymmetric distribution
where one tail is long and thin, and the other is short but fat.


Kurtosis
********

.. image:: https://surferhelp.goldensoftware.com/Resources/image/kurtosis.png
   :width: 320
   :align: right
   :alt: kurtosis

Kurtosis describes the extent to which the tails (or extremes) of a set of data
differ from those of a normal distribution. A bell curve distribution would exhibit
kurtosis of 3, so only numbers above or below 3 can be described as “excess” Kurtosis.

It is common to compare the excess kurtosis (defined below) of a distribution to 0,
which is the excess kurtosis of any univariate normal distribution. Distributions
with negative excess kurtosis are said to be platykurtic, although this does not
imply the distribution is "flat-topped" as is sometimes stated. Rather, it means the
distribution produces fewer and/or less extreme outliers than the normal distribution.
An example of a platykurtic distribution is the uniform distribution, which does not
produce outliers. Distributions with a positive excess kurtosis are said to be leptokurt.


Akaike information criterion
******************************

The Akaike information criterion (AIC) is an estimator of prediction error and thereby
relative quality of statistical models for a given set of data. Given a collection
of models for the data, AIC estimates the quality of each model, relative to each of the
other models. Thus, AIC provides a means for model selection.

Bayesian information criterion
******************************

In statistics, the Bayesian information criterion (BIC) or Schwarz information criterion
(also SIC, SBC, SBIC) is a criterion for model selection among a finite set of models; models
with lower BIC are generally preferred. It is based, in part, on the likelihood function and
it is closely related to the Akaike information criterion (AIC).


Hannan-Quinn information criterion
**********************************

The Hannan-Quinn information criterion (HQC) is a measure of the goodness of fit of a statistical
model, and is often used as a criterion for model selection among a finite set of models. It is not
based on log-likelihood function (LLF), and but related to Akaike's information criterion.


Log-likelihood of a model
*************************

The log-likelihood of a model is a measure of model fit that can be used to compare different
kinds of models (or variations on the same model). Higher values (that is, less negative values)
correspond to better fit. The log-likelihood is available for all models.

When calculating log-likelihood values, it’s important to note that adding more predictor
variables to a model will almost always increase the log-likelihood value even if the
additional predictor variables aren’t statistically significant. This means you should only
compare the log-likelihood values between two regression models if each model has the same
number of predictor variables. To compare models with different numbers of predictor variables,
you can perform a likelihood-ratio test to compare the goodness of fit of two nested regression
models.


Stationarity
************

In mathematics and statistics, a ``stationary process`` (or a strict/strictly stationary process or
strong/strongly stationary process) is a stochastic process whose unconditional joint probability
distribution does not change when shifted in time. Consequently, parameters such as mean and
variance also do not change over time. If you draw a line through the middle of a stationary process
then it should be flat; it may have 'seasonal' cycles, but overall it does not trend up nor down.


.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Unit_root_hypothesis_diagram.svg/2560px-Unit_root_hypothesis_diagram.svg.png
   :width: 300
   :align: right

Since stationarity is an assumption underlying many statistical procedures used in time series
analysis, non-stationary data are often transformed to become stationary. The most common cause
of violation of stationarity is a trend in the mean, which can be due either to the presence of
a unit root or of a deterministic trend. In the former case of a ``unit root``, stochastic shocks
have permanent effects, and the process is not mean-reverting (green). In the latter case of a
deterministic trend, the process is called a ``trend-stationary process``, and stochastic shocks
have only transitory effects after which the variable tends toward a deterministically evolving
(non-constant) mean (blue).

A trend stationary process is not strictly stationary, but can easily be transformed into a
stationary process by removing the underlying trend, which is solely a function of time. Similarly,
processes with one or more unit roots can be made stationary through differencing. An important
type of non-stationary process that does not include a trend-like behavior is a cyclostationary
process, which is a stochastic process that varies cyclically with time.

For many applications strict-sense stationarity is too restrictive. Other forms of stationarity
such as wide-sense stationarity or N-th-order stationarity are then employed. The definitions for
different kinds of stationarity are not consistent among different authors.

.. So, in summary, there are three different types of stationarity in time-series:

  - Trend stationary
  - Seasonal stationary
  - Strictly stationary

One strategy to identify the type of stationarity is to apply both ``ADF`` and ``KPSS`` tests.

============== ============== ===================== ========================
ADF            KPSS           Outcome               Note
============== ============== ===================== ========================
Non-Stationary Non-Stationary Non-Stationary
Stationary     Stationary     Stationary
Non-Stationary Stationary     Trend-Stationary      Check de-trended series
Stationary     Non-Stationary Difference-Stationary Check differenced-series
============== ============== ===================== ========================

References: `R5`_.

.. _R5: https://machinelearningmastery.com/time-series-data-stationary-python/

Statistical tests
~~~~~~~~~~~~~~~~~

A statistical test provides a mechanism for making quantitative decisions about a process or
processes. The intent is to determine whether there is enough evidence to "reject" a conjecture
or hypothesis about the process. The conjecture is called the null hypothesis.

======================= ======================================================= ============= ========
Name                    Description                                             Range         Choose
======================= ======================================================= ============= ========
``jarque-bera``         Goodness-of-fit measure data matches normal distb.                      ↓?
``durbin-watson``       Measure auto-correlation of residuals in regression     [0, 4]          ≈2
``omnibus``                                                                                     ↓?
``kendall``             Tests for monotonic upward or downward trend            [0, 1]          ?
``adfuller``            Tests for ``unit root``
``kpss``                Tests for stationary around a deterministic trend
``normal``
``Kolmogorov-smirnov``  Compares sample F(x) against given G(x) distributions
``Shapiro-wilkinson``   Test data was drawn from a normal distribution
``Anderson-darling``    Test data was drawn from a given G(x) distribution
``D'Agostino-pearsons`` Test whether a sample differs from a normal distb
======================= ======================================================= ============= ========

| If p-value > alpha: Failed to reject H0
| If p-value <= alpha: Reject H0

Kendal
******

.. _R8: https://help.healthycities.org/hc/en-us/articles/233420187-Mann-Kendall-test-for-trend-overview
.. _R9: https://vsp.pnnl.gov/help/vsample/design_trend_mann_kendall.htm

The Mann-Kendall statistical test for trend is used to assess whether a set of
data values is increasing over time or decreasing over time, and whether the
trend in either direction is statistically significant. It has the range [0,1] —
a value of zero indicates no agreement between the samples whereas a value of
unity indicates complete agreement.The Mann-Kendall test does NOT assess the
magnitude of change. Also, the trend may or may not be linear.

  - **H0:** Existence of no trend
  - **H1:** Existence of significant increasing or decreasing trend.

Mann-Kendall trend test is ``non-parametric`` test that is this test is applicable to all
types of distribution. It can be applied on any data set containing a number of data points
greater than four but sometimes with less number of samples the test has more chances of not
finding a trend.



Omnibus
*******

.. warning:: Pending!



Range Unit Root Test
********************

.. _R10: https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.range_unit_root_test.html

.. warning:: Pending!



Augmented Dicker-Fuller
***********************

The Augmented Dickey-Fuller (ADF) test can be used to test for a ``unit root`` in
a univariate process in the presence of serial correlation. It tests the
null hypothesis that a unit root is present in a time series sample. The
alternative hypothesis is different depending on which version of the test
is used, but is usually stationarity or trend-stationarity. The more
negative the statistic, the stronger the rejection of the hypothesis that
there is a unit root at some level of confidence.

  - **H0:** The series has a unit root  => ``Non-stationary``
  - **H1:** The series has no unit root => ``Stationary`` / ``Trend-Stationary``

The absence of unit root is not a proof of non-stationarity. As such, it
is also possible to use the Kwiatkowski–Phillips–Schmidt–Shin (KPSS) test
to identify the existence of an underlying trend which can also be removed
to obtain a stationary process. These are called ``trend-stationary`` processes.
In both, unit-root and trend-stationary processes, the mean can be increasing
or decreasing over time; however, in the presence of a shock, trend-stationary
processes revert to this mean tendency in the long run (deterministic trend)
while unit-root processes have a permanent impact (stochastic trend).



Kwiatkowski–Phillips–Schmidt–Shin
*********************************

The Kwiatkowski–Phillips–Schmidt–Shin (KPSS) test is used to identify
whether a time series is stationary around a deterministic trend (thus
trend stationary) against the alternative of a unit root. In the KPSS test,
the absence of a unit root is not a proof of stationarity but, by design, of
trend stationarity. This is an important distinction since it is possible for
a time series to be non-stationary, have no unit root yet be trend-stationary.

  - **H0:** The series has no unit root => ``Trend Stationary``
  - **H1:** The series has unit root => No Trend Stationary.

Later, Denis Kwiatkowski, Peter C. B. Phillips, Peter Schmidt and Yongcheol Shin (1992)
proposed a test of the null hypothesis that an observable series is trend-stationary
(stationary around a deterministic trend). The series is expressed as the sum of
deterministic trend, random walk, and stationary error, and the test is the Lagrange
multiplier test of the hypothesis that the random walk has zero variance. KPSS-type
tests are intended to complement unit root tests, such as the Dickey–Fuller tests. By
testing both the unit root hypothesis and the stationarity hypothesis, one can distinguish
series that appear to be stationary, series that appear to have a unit root, and series for
which the data (or the tests) are not sufficiently informative to be sure whether they are
stationary or integrated.

.. note:: Contrary to most unit root tests, the presence of a unit root is not the null
          hypothesis (H0) but the alternative (H1).



Normal
******

.. warning:: Pending!



Jarque Bera
************

.. _R6: https://www.statsmodels.org/dev/generated/statsmodels.stats.stattools.jarque_bera.html

In statistics, the Jarque–Bera (JB) test is a goodness-of-fit test of whether sample data
have the ``skewness`` and ``kurtosis`` matching a normal distribution. The test statistic
is always non negative. If it is far from zero, it signals the data do not have a normal
distribution.

  - **H0:** The data is normally distributed (skewness and kurtosis).
  - **H1:** The data follows a different distribution.



D’Agostino-Pearson
******************

.. _r11: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html
.. _r12: https://towardsdatascience.com/choose-the-appropriate-normality-test-d53146ca1f1c

D'Agostino-Pearson test is a goodness-of-fit measure of departure from normality.
This function tests the null hypothesis that a sample comes from a normal
distribution. It is based on D’Agostino and Pearson’s, test that combines skew and
kurtosis to produce an omnibus test of normality.

  - **H0:** The data follows a normal distribution
  - **H1:** The data does not follow a normal distribution.

It uses a similar approach than Jarque-Bera (skewness and kurtosis)
but it is considered to be more powerful. It is in general the
recommended test to assess normality when there are clear differences
in skewness and kurtosis. Overall, it is preferable that normality be assessed both
visually and through normality tests, of which the Shapiro-Wilk test is highly
recommended.

..
  note:: The test is based on transformations of the sample kurtosis and skewness,
          and has power only against the alternatives that the distribution is skewed
          and/or kurtic.



Anderson-darling
****************

The Anderson-Darling test tests the null hypothesis that a sample is drawn from a
population that follows a particular distribution. For the Anderson-Darling test,
the critical values depend on which distribution is being tested against. This
function works for normal, exponential, logistic, or Gumbel (Extreme Value Type I)
distributions.

  - **H0:** The data comes from the chosen distribution.
  - **H1:** The data does not come from the chosen distribution.

Critical values provided are for the following significance levels:

  - normal/exponential: 15%, 10%, 5%, 2.5%, 1%
  - logistic: 25%, 10%, 5%, 2.5%, 1%, 0.5%
  - Gumbel: 25%, 10%, 5%, 2.5%, 1%

If the returned statistic is larger than these critical values then for the
corresponding significance level, the null hypothesis that the data come from
the chosen distribution can be rejected. The returned statistic is referred to
as ‘A2’ in the references.

The value of the statistic (barely) exceeds the critical value associated with
a significance level of 2.5%, so the null hypothesis may be rejected at a
significance level of 2.5%, but not at a significance level of 1%.



Shapiro-wilkinson
*****************

The Shapiro-Wilk test tests the null hypothesis that the data was drawn from a
normal distribution. Like most statistical significance tests, if the sample
size is sufficiently large this test may detect even trivial departures from the
null hypothesis (i.e., although there may be some statistically significant effect,
it may be too small to be of any practical significance); thus, additional investigation
of the effect size is typically advisable, e.g., a Q–Q plot in this case.

  - **H0:** The population is normally distributed.
  - **H1:** The population is not normally distributed.

The popularity of this test is due to its excellent power in a wide variety of
situations of interest. It generally comes out toward the top against a wide
variety of non-normal distributions in power comparisons with other possible choices.

.. note:: The Shapiro–Wilk test is known not to work well in samples with many identical values.



Kolmogorov-smirnov
******************

Performs the (one-sample or two-sample) Kolmogorov-Smirnov test for goodness of fit.
The one-sample test compares the underlying distribution F(x) of a sample against a
given distribution G(x). The two-sample test compares the underlying distributions
of two independent samples. Both tests are valid only for continuous distributions.

  - **H0:** The sample data from F(x) does follow given distribution G(x).
  - **H1:** The sample data from F(x) does not follow given distribution G(x).

In statistics, the Kolmogorov–Smirnov test (K–S test or KS test) is a ``non-parametric``
test of the equality of continuous, one-dimensional probability distributions that
can be used to compare a sample with a reference probability distribution (one-sample K–S test),
or to compare two samples (two-sample K–S test). In essence, the test answers the question
"How likely is it that we would see a collection of samples like this if they were drawn
from that probability distribution?" or, in the second case, "How likely is it that we
would see two sets of samples like this if they were drawn from the same (but unknown)
probability distribution?

.. note:: The two-sample K–S test is one of the most useful and general nonparametric
          methods for comparing two samples, as it is sensitive to differences in both
          location and shape of the empirical cumulative distribution functions of the
          two samples.

The Kolmogorov–Smirnov test can be modified to serve as a goodness of fit test. In the
special case of testing for normality of the distribution, samples are standardized and
compared with a standard normal distribution. This is equivalent to setting the mean and
variance of the reference distribution equal to the sample estimates, and it is known
that using these to define the specific reference distribution changes the null distribution
of the test statistic (see Test with estimated parameters). Various studies have found that,
even in this corrected form, the test is less powerful for testing normality than the
Shapiro–Wilk test or Anderson–Darling test. However, these other tests have their own
disadvantages. For instance the Shapiro–Wilk test is known not to work well in samples
with many identical values.



Durbin Watson
*************

Durbin and Watson (1950, 1951) applied this statistic to the residuals from least
squares regressions, and developed bounds tests for the null hypothesis that the
errors are serially uncorrelated against the alternative that they follow a first
order autoregressive process. Note that the distribution of this test statistic
does not depend on the estimated regression coefficients and the variance of the
errors.

  - **H0:** Residuals (errors of regression) are serially uncorrelated.
  - **H1:** Residuals follow a first order autoregressive process.

The Durbin Watson (DW) statistic is a test for autocorrelation in the residuals
from a statistical model or regression analysis. The Durbin-Watson statistic will
always have a value ranging between 0 and 4. A value of 2.0 indicates there is
no autocorrelation (also denoted as serial correlation) detected in the sample.
Values from 0 to less than 2 point to positive autocorrelation and values from 2
to 4 means negative autocorrelation. A rule of thumb is that DW test statistic values
in the range of 1.5 to 2.5 are relatively normal. Values outside this range could,
however, be a cause for concern.

.. note:: The Durbin–Watson statistic, while displayed by many regression analysis programs,
          is not applicable in certain situations. For instance, when lagged dependent variables
          are included in the explanatory variables.



Registries
----------

Microorganisms
~~~~~~~~~~~~~~

A microorganism, or microbe, is an organism of microscopic size, which may exist in its
single-celled form or as a colony of cells. Microbes are important in human culture and health
in many ways, serving to ferment foods and treat sewage, and to produce fuel, enzymes, and
other bioactive compounds. Microbes are essential tools in biology as model organisms and have
been put to use in biological warfare and bioterrorism. Microbes are a vital component of
fertile soil. In the human body, microorganisms make up the human microbiota, including the
essential gut flora. The pathogens responsible for many infectious diseases are microbes and,
as such, are the target of hygiene measures.

The table below shows some relevant characteristics that can be used to describe various
microorganisms. Therefore, these can also be used to categorise or group microorganisms
that have similar properties

==================== ============================================================= ==========
Definition           Categories                                                    Status
==================== ============================================================= ==========
taxonomy             domain, kingdom, phylum, class, order, family, genus, species ``Ok``
gram_stain           positive, negative                                            ``Ok``
shape/morphology     cocci, bacilli, vibrio, spirochete
growth               aerobic, anaerobic
hemolysis            alpha, beta, gamma, no-hemolysis
coagulase_production positive, negative
group                A, B, C, D, ...
arrangement
endospores
mobility?
salinity
oxygen_requirements
habitat
temp_range
temp_optima
disease
host                 human, animals, swine, cattle, ...
fermenting           lactose, non-lactose
acid_fastness_stain
ziehl_nealson_tain
==================== ============================================================= ==========

.. note:: Most of these categories have not been used within the library.


Taxonomy
********

.. image:: https://textimgs.s3.amazonaws.com/boundless-microbiology/assification-l-pengo-vflip.svg#fixme
   :width: 130
   :align: right
   :alt: pyAMR

Bacterial taxonomy is a rank-based classification, of bacteria. In the scientific classification
established by Carl Linnaeus, each species has to be assigned to a genus (binary nomenclature),
which in turn is a lower level of a hierarchy of ranks (family, suborder, order, subclass, class,
division/phyla, kingdom and domain). In the currently accepted classification of life, there are
three domains (Eukaryotes, Bacteria and Archaea), which, in terms of taxonomy, despite following
the same principles have several different conventions between them and between their subdivisions.
See an example below.

  - life:
  - domain: Bacteria
  - kingdom:
  - phylum: Proteobacteria
  - class: Gamma Proteobacteria
  - order: Enterobacteriales
  - family: Enterobacteriaceae
  - genus: Escherichia
  - species: Escherichia coli
  - subspecies (missing in dataset)


Gram Stain
**********

Gram stain or Gram staining, also called Gram's method, is a method of staining used to
distinguish and classify bacterial species into two large groups according to the chemical
and physical properties of their cell walls: gram-positive bacteria and gram-negative
bacteria. The name comes from the Danish bacteriologist Hans Christian
Gram, who developed the technique.

- **Gram positive** bacteria take up the crystal violet stain used in the test, and then
  appear to be purple-coloured when seen through an optical microscope. This is because the
  thick peptidoglycan layer in the bacterial cell wall retains the stain after it is washed
  away from the rest of the sample, in the decolorization stage of the test.

- **Gram-negative** bacteria cannot retain the violet stain after the decolorization step;
  alcohol used in this stage degrades the outer membrane of gram-negative cells, making the
  cell wall more porous and incapable of retaining the crystal violet stain. Their peptidoglycan
  layer is much thinner and sandwiched between an inner cell membrane and a bacterial outer
  membrane, causing them to take up the counterstain (safranin or fuchsine) and appear red or
  pink.

.. note:: Despite their thicker peptidoglycan layer, gram-positive bacteria are more
    receptive to certain cell wall–targeting antibiotics than gram-negative bacteria,
    due to the absence of the outer membrane.


Shape or morphology
*******************

[REF]: https://www.sciencedirect.com/topics/medicine-and-dentistry/microbial-morphology

Different types of microbes have different, but characteristic, shapes. Under suitable
conditions, the shape and size of microbes are relatively stable. It is important to know
the morphological structure of microbes, as it provides us with a better understanding of
microbial physiology, pathogenic mechanisms, antigenic features, and allows us to identify
them by species. In addition, knowledge of microbial morphology can be helpful in diagnosing
disease and in preventing microbial infections.

Bacteria are complex and highly variable microbes. They come in four basic shapes: **spherical**
(cocci), **rod-shaped** (bacilli), **arc-shaped** (vibrio), and **spiral** (spirochete). See some
examples included in the figure below.


.. image:: https://upload.wikimedia.org/wikipedia/commons/1/1b/Bacterial_morphology_diagram-ro.svg
   :width: 600
   :align: center
   :alt: pyAMR

.. raw:: html

    <!--
    <img src="https://microbenotes.com/wp-content/uploads/2020/05/Bacterial-Shapes-and-Arrangement.jpeg"/>
    <img src="https://ars.els-cdn.com/content/image/3-s2.0-B978012802234400001X-f01-03-9780128022344.jpg"/>
    <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Bacterial_morphology_diagram-ro.svg"/>
    -->


Growth Type
***********

The two main types of bacterial growth are **aerobic** and **anaerobic**. The basic difference
between the two, is that the former thrives in oxygenated environment and latter in an environment
marked by the absence of oxygen, there also exist other differences which cannot be ignored.

- **Aerobic:** These are the species of bacteria which require oxygen for their basic survival,
  growth, and the process of reproduction. It is very easy to isolate these bacteria by culturing
  a mass of bacterial strains in some liquid medium. As they require oxygen for survival, they
  tend to come to the surface in a bid to derive maximum oxygen available. Examples are Bacillus
  or Nocardia.

- **Anaerobic**: these are the species of bacteria which don’t require oxygen for growth. There are
  different types of anaerobic species, including the aerotolerant anaerobes, which can survive in the
  presence of oxygen, and obligate anaerobes, which can’t survive in the presence of oxygen. Examples
  are Escherichia coli or Bacteroides.



Haemolysis
**********

Hemolysis (from Greek αιμόλυση, meaning 'blood breakdown') is the breakdown of red blood cells. The
ability of bacterial colonies to induce hemolysis when grown on blood agar is used to classify certain
microorganisms. This is particularly useful in classifying streptococcal species. A substance that causes
hemolysis is a hemolysin.

- **Alpha-hemolysis:** When alpha-hemolysis (α-hemolysis) is present, the agar under the colony is
  light and greenish. Streptococcus pneumoniae and a group of oral streptococci (Streptococcus viridans
  or viridans streptococci) display alpha hemolysis.

- **Beta-hemolysis:** Sometimes called complete hemolysis, is a complete lysis of red cells in the media
  around and under the colonies: the area appears lightened (yellow) and transparent. Streptolysin, an
  exotoxin, is the enzyme produced by the bacteria which causes the complete lysis of red blood cells. There
  are two types of streptolysin: Streptolysin O (SLO) and streptolysin S (SLS).

- **Gamma-hemolysis:** If an organism does not induce hemolysis, the agar under and around the colony
  is unchanged, and the organism is called non-hemolytic or said to display gamma-hemolysis (γ-hemolysis).
  Enterococcus faecalis (formerly called "Group D Strep"), Staphylococcus saprophyticus, and Staphylococcus
  epidermidis display gamma hemolysis.


Coagulase Production
********************

Coagulase is a protein enzyme produced by several microorganisms that enables the conversion of fibrinogen
to fibrin. In the laboratory, it is used to distinguish between different types of Staphylococcus isolates.
Importantly, S. aureus is generally coagulase-positive, meaning that a positive coagulase test would indicate
the presence of S. aureus or any of the other 11 coagulase-positive Staphylococci. A negative coagulase
test would instead show the presence of coagulase-negative organisms such as S. epidermidis or S. saprophyticus.
However, it is now known that not all S. aureus are coagulase-positive. Whereas coagulase-positive
Staphylococci are usually pathogenic, coagulase-negative Staphylococci are more often associated with
opportunistic infection.

Antimicrobials
~~~~~~~~~~~~~~

An antimicrobial is an agent that kills microorganisms or stops their growth. Antimicrobial
medicines can be grouped according to the microorganisms they act primarily against in for main
categories: (i) **anibiotics** which are used against bacteria, (ii) **antifungals** which are used
against fungi, (iii) **antivirals** which are used against viruses and (iv) **antiparasitics** which
are used against parasites.

.. image:: https://antibioticguardian.com/assets/Antimicrobials_AMR-infographic_UKHSA.png

An antibiotic is a type of antimicrobial substance active against bacteria. It is the most important type
of antibacterial agent for fighting bacterial infections, and antibiotic medications are widely used in the
treatment and prevention of such infections.

[REF]: https://en.wikipedia.org/wiki/Antibiotic

.. image:: https://girlymicrobiologist.files.wordpress.com/2020/10/antibiotic-classes.png





