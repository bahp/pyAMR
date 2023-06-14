"""
``SARI`` - Compute timeseries
-------------------------------

.. |1D30| replace:: 1D\ :sub:`30`
.. |1M1| replace:: 1M\ :sub:`1`
.. |3M1| replace:: 3M\ :sub:`1`
.. |1M30| replace:: 1M\ :sub:`30`
.. |7D4| replace:: 7D\ :sub:`4`
.. |1M12| replace:: 1M\ :sub:`12`
.. |1M6| replace:: 1M\ :sub:`6`
.. |1M3| replace:: 1M\ :sub:`3`
.. |12M1| replace:: 12M\ :sub:`1`
.. |SP| replace:: SHIFT\ :sub:`period`

In order to study the temporal evolution of AMR, it is necessary to generate a resistance
time series from the susceptibility test data. This is often achieved by computing the
resistance index on consecutive partitions of the data. Note that each partition contains
the susceptibility tests required to compute a resistance index. The traditional strategy
of dealing with partitions considers independent time intervals (see yearly, monthly or
weekly time series in Table 4.2). Unfortunately, this strategy forces to trade-off between
granularity (level of detail) and accuracy. On one side, weekly time series are highly
granular  but inaccurate. On the other hand, yearly time series are accurate but rough.
Note that the granularity is represented by the number of observations in a time series
while the accuracy is closely related with the number of susceptibility tests used to compute
the resistance index. Conversely, the overlapping time intervals strategy drops such dependence
by defining a window of fixed size which is moved across time. The length of the window is
denoted as period and the time step as shift. For instance, three time series obtained using
the overlapping time intervals strategy with a monthly shift (1M) and window lengths of 12,
6 and 3 have been presented for the sake of clarity (see |1M12|, |1M6| and |1M3| in Table 4.2).

.. image:: ../../_static/imgs/timeseries-generation.png
   :width: 500
   :align: center
   :alt: Generation of Time-Series

The notation to define the time series generation methodology (|SP|) is described with
various examples in Table 4.2. For instance, |7D4| defines a time series with weekly resistance
indexes (7D) calculated using the microbiology records available for the previous four weeks
(4x7D). It is important to note that some notations are equivalent representations of the same
susceptibility data at different granularities, hence their trends are comparable. As an example,
the trend estimated for |1M1| should be approximately thirty times the trend estimated for |1D30|.

"""

######################################################################################
#
# Let's see how to compute SARI time series with examples.
#
# We first load the data and select one single pair for clarity.
#

# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import own libraries
from pyamr.core.sari import sari
from pyamr.datasets.load import load_data_nhs

# -------------------------
# Configuration
# -------------------------
# Configure seaborn style (context=talk)
sns.set(style="white")

# Set matplotlib
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 9

# Pandas configuration
pd.set_option('display.max_colwidth', 40)
pd.set_option('display.width', 300)
pd.set_option('display.precision', 4)

# Numpy configuration
np.set_printoptions(precision=2)

# -------------------------------------------
# Load data
# -------------------------------------------
# Load data
data, antimicrobials, microorganisms = load_data_nhs()

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.columns)
print("\nDtypes:")
print(data.dtypes)

# Filter
idxs_spec = data.specimen_code.isin(['URICUL'])
idxs_orgs = data.microorganism_code.isin(['ECOL'])
idxs_abxs = data.antimicrobial_code.isin(['AAUG'])

# Filter
data = data[idxs_spec & idxs_orgs & idxs_abxs]

# Filter dates (2016-2018 missing)
data = data[data.date_received.between('2008-01-01', '2016-12-31')]

######################################################################################
#
# Independent Time Intervals (ITI)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# This is the traditional method used in antimicrobial surveillance systems where
# the time spans considered are independent; that is, they do not overlap (e.g.
# monthly time series - |1M1| or yearly timeseries - |12M1|).

# -------------------------------------------
# Compute ITI sari (temporal)
# -------------------------------------------
from pyamr.core.sari import SARI

# Create SARI instance
sar = SARI(groupby=['specimen_code',
                     'microorganism_code',
                     'antimicrobial_code',
                     'sensitivity'])

# Create constants
shift, period = '30D', '30D'

# Compute sari timeseries
iti = sar.compute(data, shift=shift,
    period=period, cdate='date_received')

# Reset index
iti = iti.reset_index()


# --------------
# Plot
# --------------
# Create figure
fig, axes = plt.subplots(2, 1, sharex=True,
        gridspec_kw={'height_ratios': [2, 1]})
axes = axes.flatten()

# Plot line
sns.lineplot(x=iti.date_received, y=iti.sari,
    palette="tab10", linewidth=0.75, linestyle='--',
    marker='o', markersize=3, markeredgecolor='k',
    markeredgewidth=0.5, markerfacecolor=None,
    alpha=0.5, ax=axes[0])

# Compute widths
widths = [d.days for d in np.diff(iti.date_received.tolist())]

# Plot bars
axes[1].bar(x=iti.date_received, height=iti.freq,
    width=.8*widths[0], linewidth=0.75, alpha=0.5)

# Configure
axes[0].set(ylim=[-0.1, 1.1],
    title='Time-series $%s_{%s}$' % (shift, period))

# Despine
sns.despine(bottom=True)

# Tight layout
plt.tight_layout()

# Show
print("\nTemporal (ITI):")
print(iti)

######################################################################################
#
# Overlapping Time Intervals (OTI)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# This method is defined as a fixed region which is moved across time to compute consecutive
# resistance indexes. It is described by two parameters |SP| where ``period`` denotes the
# length of the window and ``shift`` the distance between consecutive windows. This approach
# it is more versatile and allows to include larger number of susceptibility tests when
# computing ``sari``. Therefore, this is useful in scenarios in which pairs do
# not have a large number of records in the dataset.
#
# Note how the ``sari`` values are now larger than in the previous example!!
#

# -------------------------------------------
# Compute OTI sari (temporal)
# -------------------------------------------
# Variables
shift, period = '30D', '180D'

# Compute sari timeseries
oti = sar.compute(data, shift=shift,
    period=period, cdate='date_received')

# Reset index
oti = oti.reset_index()

# --------------
# Plot
# --------------
# Create figure
fig, axes = plt.subplots(2, 1, sharex=True,
        gridspec_kw={'height_ratios': [2, 1]})
axes = axes.flatten()

# Plot line
sns.lineplot(x=oti.date_received, y=oti.sari,
    palette="tab10", linewidth=0.75, linestyle='--',
    marker='o', markersize=3, markeredgecolor='k',
    markeredgewidth=0.5, markerfacecolor=None,
    alpha=0.5, ax=axes[0])

# Compute widths
widths = [d.days for d in np.diff(oti.date_received.tolist())]

# Plot bars
axes[1].bar(x=oti.date_received, height=oti.freq,
    width=.8*widths[0], linewidth=0.75, alpha=0.5)

# Configure
axes[0].set(ylim=[-0.1, 1.1],
    title='Time-series $%s_{%s}$' % (shift, period))

# Despine
sns.despine(bottom=True)

# Tight layout
plt.tight_layout()

# Show
print("\nTemporal (OTI):")
print(oti)

######################################################################################
#
# Important considerations
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# .. warning ::
#
#     The rolling(window=w) just applies the function on w size windows. Note
#     however that it does not take into consideration the dates. Thus it could
#     be applying the mean operation on months Jan, Feb, May if there was not
#     data and therefore no entry in the dataframe for March. This issue can be
#     addressed in two different ways:
#
#       - setting the date_received as index and using w='3M'.
#       - resampling the dataframe so that all date entries appear. Note that
#         depending on the function applied we might want to fill gaps with
#         different values (e.g. NaN, 0, ...)
#
#     ``Implemented``
#
# As mentioned before, by using the |SP| approach you can define both
# strategies to generate time-series (ITI and OTI). The ITI strategy
# is limited in the number of samples that can be used to compute the
# index and therefore you have to trade between granularity and
# accuracy whereas the latter is more flexible.
#
# For instance, in examples with low number of records ``sari``  might
# go up from barely 0.1 (in ITI) to 0.4 (in OTI) when more records are
# used. The most noticeable increase from |1M1| to |1M3|, that is when
# instead of records for a month we considered records for three months
# and reached certain stability on |1M6| approximately (ish?).
#
# .. note ::
#   - Ideally shift and period same unit (eg. D).
#   - Period should be always larger than shift.


# --------------------------------
# Comparison
# --------------------------------
# Configuration
shift = '30D'

# Create figure
f, axes = plt.subplots(2, 2, figsize=(10, 6), sharey=True)
axes = axes.flatten()

# Loop
for period in ['30D', '90D', '180D', '365D']:

    # Compute sari time-series
    iti = sar.compute(data, shift=period,
        period=period, cdate='date_received')
    oti = sar.compute(data, shift=shift,
        period=period, cdate='date_received')

    # Compute rolling mean
    iti['sari_rolling'] = iti.sari.rolling(window=3,
        win_type='gaussian', min_periods=1).mean(std=3)
    oti['sari_rolling'] = oti.sari.rolling(window=3,
        win_type='gaussian', min_periods=1).mean(std=3)

    # Plot
    sns.lineplot(data=iti, x='date_received', y='sari',
                 linewidth=0.75, linestyle='--', ax=axes[0], marker='o',
                 markersize=3, markeredgecolor='k', markeredgewidth=0.5,
                 markerfacecolor=None, alpha=0.5,
                 label='$%sM_{%s}$' % (period, 1))

    sns.lineplot(data=oti, x='date_received', y='sari',
                 linewidth=0.75, linestyle='--', ax=axes[1], marker='o',
                 markersize=3, markeredgecolor='k', markeredgewidth=0.5,
                 markerfacecolor=None, alpha=0.5,
                 label='$%s_{%s}$' % (shift, period))

    sns.lineplot(data=iti, x='date_received', y='sari_rolling',
                 linewidth=0.75, ax=axes[2],
                 label='$%s_{%s}$ - smooth' % (period, 1))

    sns.lineplot(data=oti, x='date_received', y='sari_rolling',
                 linewidth=0.75, ax=axes[3],
                 label='$%s_{%s}$ - smooth' % (shift, period))

# Configure
sns.despine(bottom=True)

# Configure axes
axes[0].set(title='Independent Time Intervals')
axes[1].set(title='Overlapping Time Intervals')

# Adjust
plt.tight_layout()

# Show
plt.show()


####################################################################
#
# Plotting multiple pairs using FaceGrid.
#

"""
# ----------------------
# Facet Grid
# ----------------------
# Show
print(aux)

# Create palette
pal = sns.cubehelix_palette(50, rot=-.25, light=.7)

# Create
g = sns.FacetGrid(data=aux, col="antimicrobial_code",
    hue="antimicrobial_code", aspect=1.2, height=2,
    sharex=True, sharey=True, palette=pal,
    col_wrap=8)

# Plot line
g.map(sns.lineplot, "date_received", 'sari',
      alpha=1, linewidth=1.5)
"""
"""
g.map(plt.fill_between,
      aux.date_received.values,
      aux.sari.values)
"""
"""
#g.map(label, "x")
#g.set_titles("")
#g.set(yticks=[])
g.set(xlabel='date')
g.despine(bottom=True, left=True)

# Show
plt.show()
"""