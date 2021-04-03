"""
SARI - Timeseries
-----------------

.. |1D30| replace:: 1D\ :sub:`30`
.. |1M1| replace:: 1M\ :sub:`1`
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
# Constants
# -------------------------------------------
# Create grouper
grouper = pd.Grouper(freq='M', key='date_received')

# Define window
window = 12

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
# month - |1M1| or year - |12M1|).

# -------------------------------------------
# Compute ITI sari (temporal)
# -------------------------------------------
# Variables
shift = '1M'
period = 1 # Always 1 for ITI.

# Create grouper
grouper = pd.Grouper(freq=shift, key='date_received')

# Create DataFrame
iti = data.groupby([grouper,
                    'specimen_code',
                    'microorganism_code',
                    'antimicrobial_code',
                    'sensitivity']) \
          .size().unstack().fillna(0)

# Compute frequency
iti['freq'] = iti.sum(axis=1)

# Compute sari
iti['sari'] = sari(iti, strategy='hard')

# Plot
sns.lineplot(data=iti, x='date_received', y='sari',
    palette="tab10", linewidth=0.75,
    hue='antimicrobial_code')

# Configure
plt.title('Time-series $%s_{%s}$' % (shift, period))
plt.ylim([-0.1, 1.1])
sns.despine(bottom=True)

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
# length of the window and ``shift`` the distance between consecutive windows.
#

# -------------------------------------------
# Compute OTI sari (temporal)
# -------------------------------------------
# Variables
shift = '1M'
period = 6

# Create grouper
grouper = pd.Grouper(freq=shift, key='date_received')

# Create DataFrame
oti = data.groupby([grouper,
                    'specimen_code',
                    'microorganism_code',
                    'antimicrobial_code',
                    'sensitivity']) \
          .size() \
          .rolling(window=period, min_periods=1) \
          .sum().unstack().fillna(0)

# Compute frequency
oti['freq'] = oti.sum(axis=1)

# Compute sari
oti['sari'] = sari(oti, strategy='hard')

# Plot
sns.lineplot(data=oti, x='date_received', y='sari',
    palette="tab10", linewidth=0.75,
    hue='antimicrobial_code')

# Configure
plt.title('Time-series $%s_{%s}$' % (shift, period))
plt.ylim([-0.1, 1.1])
sns.despine(bottom=True)

# Show
print("\nTemporal (OTI):")
print(oti)

######################################################################################
#
# Lets compare them graphically
#

# -------------------------------------------
# Display
# -------------------------------------------
"""
sns.lineplot(data=iti, x='date_received', y='sari',
    palette="tab10", linewidth=0.75,
    hue='antimicrobial_code',
    label='')

sns.lineplot(data=iti, x='date_received', y='sari_rolling',
    linewidth=0.75, color='g',
    label='iti-rolling')

sns.lineplot(data=oti, x='date_received', y='sari',
    linewidth=0.75, color='k',
    label='oti')
"""
plt.show()

######################################################################################
#
# Important considerations
# ~~~~~~~~~~~~~~~~~~~~~~~~
#
# .. todo :: Would it be any useful to use plotly to allow readers to
#          toggle which timeseries to be shown/hidden?
#
# .. warning ::
#
#     The rolling(window=w) just applies the function on w size windows. Note
#     however that it does not take into consideration the dates. Thus it could
#     be applying the mean operation on months Jan, Feb, May if there was not
#     data and therefore no entry in the dataframe for March. This issue can be
#     addressed in two different ways:
#       - setting the date_received as index and using w='3M'.
#       - resampling the dataframe so that all date entries appear. Note that
#         depending on the function applied we might want to fill gaps with
#         different values (e.g. NaN, 0, ...)
#

# --------------------------------
# Comparison
# --------------------------------
# Configuration
shift = '1M'

# Create figure
f, axes = plt.subplots(2, 2, figsize=(10, 10), sharey=True)
axes = axes.flatten()

# Loop
for period in [1, 3, 6, 9, 12]:

    # Create groupers
    grouper_iti = pd.Grouper(freq='%sM' % period, key='date_received')
    grouper_oti = pd.Grouper(freq='%s' % shift, key='date_received')

    # Create DataFrame ITI
    iti = data.groupby([grouper_iti,
                        'specimen_code',
                        'microorganism_code',
                        'antimicrobial_code',
                        'sensitivity']) \
              .size().unstack().fillna(0)

    # Create DataFrame OTI
    oti = data.groupby([grouper_oti,
                        'specimen_code',
                        'microorganism_code',
                        'antimicrobial_code',
                        'sensitivity']) \
              .size() \
              .rolling(window=period, min_periods=1) \
              .sum().unstack().fillna(0)

    # Compute frequency
    iti['freq'] = iti.sum(axis=1)
    oti['freq'] = oti.sum(axis=1)

    # Compute sari
    iti['sari'] = sari(iti, strategy='hard')
    oti['sari'] = sari(oti, strategy='hard')
    
    # Compute rolling mean
    iti['sari_rolling'] = iti.sari.rolling(window=3,
        win_type='gaussian', min_periods=1).mean(std=3)
    oti['sari_rolling'] = oti.sari.rolling(window=3,
        win_type='gaussian', min_periods=1).mean(std=3)

    # Plot
    sns.lineplot(data=iti, x='date_received', y='sari',
                 linewidth=0.75, ax=axes[0], marker='o',
                 label='$%sM_{%s}$' % (period, 1))

    sns.lineplot(data=oti, x='date_received', y='sari',
                 linewidth=0.75, ax=axes[1], marker='o',
                 label='$%s_{%s}$' % (shift, period))

    sns.lineplot(data=iti, x='date_received', y='sari_rolling',
                 linewidth=0.75, ax=axes[2],
                 label='$%sM_{%s}$ - smooth' % (period, 1))

    sns.lineplot(data=oti, x='date_received', y='sari_rolling',
                 linewidth=0.75, ax=axes[3],
                 label='$%s_{%s}$ - smooth' % (shift, period))

# Configure
sns.despine(bottom=True)

# Configure axes
axes[0].set(title='Independent Time Intervals',
            xlabel='date', ylabel='sari')
axes[1].set(title='Overlapping Time Intervals',
            xlabel='date', ylabel='sari')

# Adjust
plt.tight_layout()

# Show
plt.show()


"""
# Compute rolling
iti['sari_rolling'] = iti.sari.rolling(3,
    win_type='gaussian', min_periods=1).mean(std=3)
"""
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