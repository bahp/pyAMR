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
programs [20]. These programs are crucial to guide health care organizations designing evidence-based
policies to combat AMR [21, 22]. In particular, susceptibility reporting has shown to be a determinant
data source to inform empiric antimicrobial therapy selection

.. image:: ../../_static/imgs/susceptibility-test-record.png
   :width: 200
   :align: right
   :alt: ASAI

Susceptibility test records (see Figure 4.1) are composed by laboratory identification
number (LID), patient identification number (PID), date, sample type or culture (e.g.
blood or urine), pathogen, antimicrobial, reported status and outcome (resistant, sensitive
or intermediate). In research, the susceptibility test data is usually first grouped by
specimen or culture type, and further grouped by pairs (pathogen, antimicrobial)
since it is widely accepted by clinicians as detailed in the UK five year strategy in AMR [21].

The AMR indexes
---------------

======== ============================================== =============
Acronym  Name                                           Status
======== ============================================== =============
``SARI`` Single Antimicrobial Resistance Index          ``Ok``
``MARI`` Multiple Antimicrobial Resistance Index        ``Pending``
``DRI``  Drug Resistance Index                          ``Pending``
``SART`` Single Antimicrobial Resistance Trend          ``Pending``
``ASAI`` Antimicrobial Spectrum of Activity Index       ``Ok``
======== ============================================== =============

- **Single Antibiotic Resistance Index (SARI)**

    This index describes the proportion of resistant isolates for a given set of susceptibility
    tests. It provides a value within the range [0,1] where values close to one indicate high
    resistance. It is agnostic to pathogen, antibiotic and time. The variables *R*, *I* and *S* represent
    the number of susceptibility tests with Resistant, Intermediate and Susceptible outcomes
    respectively. The definition might vary slightly since the intermediate category is not always
    considered.

    See: :py:mod:`pyamr.core.sari.SARI`

    Example: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_sari.py`

- **Multiple Antibiotic Resistance Index (MARI)**

    This index describes the ratio of antimicrobials tested (*T*) to which a pathogen is resistant (*R*).
    It provides a value within the range [0,1] where values close to one indicate high multi-drug
    resistance. It highly depends on the antimicrobials to which the pathogen is tested. Since
    tested antimicrobials vary among health care centres and time, comparison and analysis of its
    evolution in time is not straight forward. In addition, antibiotics which are intrinsically resistant
    should not be considered.

    See: :py:mod:`pyamr.core.mari.MARI`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_mari.py`


- **Drug Resistance Index (DRI)**

    This index measures the proportion of pathogens that are resistant to the antimicrobials used
    to treat them. It provides a value within the range [0,1] where values close to one indicate
    high resistant for frequent antimicrobials. The variable *ρik* is the proportion of resistance
    among organism *i* to antimicrobial *k* and *qik* is the frequency of drug *k* used to treat
    organism *i*.

    .. warning:: Not implemented!

- **Antimicrobial Spectrum of Activity Index (ASAI)**

    The antimicrobial spectrum of activity refers to the range of microbe species that are susceptible to
    these agents and therefore can be treated. In general, antimicrobial agents are classified into broad,
    intermediate or narrow spectrum. Broad spectrum antimicrobials are active against both Gram-positive
    and Gram-negative bacteria. In contrast, narrow spectrum antimicrobials have limited activity and are
    effective only against particular species of bacteria.

    See: :py:mod:`pyamr.core.asai.ASAI`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_asai.py`

- **Single Antibiotic Resistance Trend (SART)**

    The single antimicrobial resistance trend measures the ratio of change per time unit
    (e.g. monthly or yearly). To compute this metric, it is necessary to generate a
    resistance time series from the susceptibility test data. This is often achieved by
    computing the SARI consecutive or overlapping partitions of the data. Then, the trend
    can be extracted using for example a linear model where the slope, which is a value
    within the range [-1, 1] indicates the ratio of change.

    See: :py:mod:`pyamr.core.sart.SART`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_sart.py`



The Registries
--------------



Time series analysis
--------------------

Summary

R2  0-100 higher the better

================= ==================================================== ============= ========
Name              Full name                                            Range
================= ==================================================== ============= ========
``R2``            Goodness-of-fit measure for linear regression models [0, 100]
``pearson``       Measures linear correlation between variables        [-1, 1]
``kurtosis``      Measure of tailedness of a probability distribution
``skewness``      Measure of asymmetry of a probability distribution
``jarque-bera``   Goodness-of-fit measure data matches normal dist
``durbin-watson`` Measure correlation of residuals in regression
``omnibus``       Blurb
================= ==================================================== ============= ========

.. warning:: Describe how linear regression and weighted linear regression
             work. Highlight that most of the features are computed on the
             residuals.

Pearson
~~~~~~~


.. https://cdn.scribbr.com/wp-content/uploads/2022/05/Strong-positive-correlation-and-strong-negative-correlation.webp
.. https://upload.wikimedia.org/wikipedia/commons/3/34/Correlation_coefficient.png

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
~~

[R]: https://statisticsbyjim.com/regression/interpret-r-squared-regression/

R-squared is a goodness-of-fit measure for linear regression models. This
statistic indicates the percentage of the variance in the dependent variable
that the independent variables explain collectively. R-squared measures the
strength of the relationship between your model and the dependent variable
on a convenient 0 – 100% scale.

R-squared is always between 0 and 100% where (i) **0%** represents a model that
does not explain any of the variation in the response variable around its mean.
The mean of the dependent variable predicts the dependent variable as well as the
regression model and (ii) **100%** represents a model that explains all the variation
in the response variable around its mean.


Skewness
~~~~~~~~

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
~~~~~~~~

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

Jarque Bera
~~~~~~~~~~~

In statistics, the Jarque–Bera test is a goodness-of-fit test of whether sample data
have the skewness and kurtosis matching a normal distribution.

Durbin Watson
~~~~~~~~~~~~~

The Durbin Watson (DW) statistic is a test for autocorrelation in the residuals
from a statistical model or regression analysis. The Durbin-Watson statistic will
always have a value ranging between 0 and 4. A value of 2.0 indicates there is
no autocorrelation detected in the sample.

Normal Test
~~~~~~~~~~~

Kolmogorov-smirnov Test
~~~~~~~~~~~~~~~~~~~~~~~

Shapiro-wilkinson Test
~~~~~~~~~~~~~~~~~~~~~~

Anderson-darling Test
~~~~~~~~~~~~~~~~~~~~~

Omnibus
~~~~~~~
Omnibus tests are a kind of statistical test. They test whether the explained variance
in a set of data is significantly greater than the unexplained ...
