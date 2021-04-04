"""
ASAI - Timeseries
-----------------

.. |1D30| replace:: 1D\ :sub:`30`
.. |1M1| replace:: 1M\ :sub:`1`
.. |1M30| replace:: 1M\ :sub:`30`
.. |7D4| replace:: 1M\ :sub:`12`
.. |1M12| replace:: 1M\ :sub:`12`
.. |1M6| replace:: 1M\ :sub:`6`
.. |1M3| replace:: 1M\ :sub:`3`
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
# Let's see how to compute ASAI time series with examples.
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
from pyamr.core.asai import asai
from pyamr.datasets.load import load_data_nhs


# -------------------------
# Methods
# -------------------------
def create_mapper(dataframe, column_key, column_value):
    """This method constructs a mapper

    Parameters
    ----------
    dataframe: dataframe-like
    The dataframe from which the columns are extracted

    column_key: string-like
    The name of the column with the values for the keys of the mapper

    column_value: string-like
    The name of the column with the values for the values of the mapper

    Returns
    -------
    dictionary
    """
    dataframe = dataframe[[column_key, column_value]]
    dataframe = dataframe.drop_duplicates()
    return dict(zip(dataframe[column_key], dataframe[column_value]))

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
idxs_abxs = data.antimicrobial_code.isin(['AAUG'])

# Filter
data = data[idxs_spec & idxs_abxs]

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
#
# .. todo :: Include in ASAI an option to filter and keep only those genus
#            and species that have values over all the time period? or at
#            least for more than 80 percent of the period?

# -------------------------------------------
# Compute ITI sari (temporal)
# -------------------------------------------
from pyamr.core.sari import SARI

# Create SARI instance
sari = SARI(groupby=['specimen_code',
                    'microorganism_code',
                    'antimicrobial_code',
                    'sensitivity'])

# Create constants
shift, period = '6M', '800D'

# Compute sari timeseries
temp = sari.compute(data, shift=shift,
    period=period, cdate='date_received')

# Reset index
temp = temp.reset_index()

# Show
print("\nSARI (temporal)")
print(temp)


# -------------------------------------------
# Filter for sari (temporal)
# -------------------------------------------
# Appearance of organisms by date (or even freq instead of 1/0).
s = pd.crosstab(temp['microorganism_code'], temp['date_received'])

# Filter
#temp = temp[temp['microorganism_code'].isin(s[s.all(axis=1)].index)]

# Show
print("Remaining microorganisms:")
print(temp.microorganism_code.unique())

# -------------------------
# Format dataframe
# -------------------------
# Create mappers
abx_map = create_mapper(antimicrobials, 'antimicrobial_code', 'category')
org_map = create_mapper(microorganisms, 'microorganism_code', 'genus')
grm_map = create_mapper(microorganisms, 'microorganism_code', 'gram_stain')

#iti = iti[['date_received', 'freq', 'sari', 'antimicrobial_code', 'microorganism_code']]

# Include categories
temp['category'] = temp['antimicrobial_code'].map(abx_map)
temp['genus'] = temp['microorganism_code'].map(org_map)
temp['gram'] = temp['microorganism_code'].map(grm_map)

# Empty grams are a new category (unknown - u)
temp.gram = temp.gram.fillna('u')

# Show
print("\nMicroorganisms without gram stain:")
print(temp[temp.gram=='u'].microorganism_code.unique())

# -------------------------------
# Create antimicrobial spectrum
# -------------------------------
# Libraries
from pyamr.core.asai import ASAI

# Create antimicrobial spectrum of activity instance
asai = ASAI(column_genus='genus',
            column_specie='microorganism_code',
            column_resistance='sari',
            column_frequency='freq')
# Compute
scores = asai.compute(temp,
    groupby=['date_received',
             'antimicrobial_code',
             'gram'],
    weights='uniform',
    threshold=None,
    min_freq=0)

# Unstack
scores = scores

# Show scores
print("\nASAI:")
print(scores.unstack())

# Plot
# ----
# Create figure
fig, axes = plt.subplots(1, 2, figsize=(10, 3), sharey=True)

# Show
sns.lineplot(data=scores, x='date_received', y='ASAI_SCORE',
             hue='gram', palette="tab10", linewidth=0.75, linestyle='--',
             marker='o', markersize=3, markeredgecolor='k',
             markeredgewidth=0.5, markerfacecolor=None,
             alpha=0.5, ax=axes[0])


plt.show()

# -------------------------
# Compute ASAI
# -------------------------
iti = iti.rename(columns={
    'microorganism_code': 'SPECIE',
    'sari': 'RESISTANCE',
    'genus': 'GENUS'
})


fig, axes = plt.subplots(1, 2, figsize=(10, 3), sharey=True)

# Variable for filtering
s = pd.crosstab(iti['SPECIE'], iti['date_received'])

# Create aux (non filtered)
aux = iti.copy(deep=True)
aux = aux.groupby(['date_received',
                   'antimicrobial_code',
                   'gram'])\
         .apply(asai, weights='uniform', threshold=0.5)


plt.show()

# Create aux (filtered)
aux2 = iti.copy(deep=True)
aux2 = aux2[aux2['SPECIE'].isin(s[s.all(axis=1)].index)]
aux2 = aux2.groupby(['date_received',
                   'antimicrobial_code',
                   'gram'])\
         .apply(asai, weights='uniform', threshold=0.8)

a = 1
# Display
print("\nCrosstab:")
print(s)
print("\nSelected:")
print(s[s.all(axis=1)])
print("\nRemaining:")
print(iti)
print(aux.unstack())
print(aux2.unstack())

sns.lineplot(data=aux.reset_index(),
             x='date_received',
             y='ASAI_SCORE',
             palette="tab10",
             linewidth=0.75,
             hue='gram',
             marker='o',
             ax=axes[0])

sns.lineplot(data=aux2.reset_index(),
             x='date_received',
             y='ASAI_SCORE',
             palette="tab10",
             linewidth=0.75,
             hue='gram',
             marker='o',
             ax=axes[1])