"""
Step 02 - Temporal evolution
============================

In this example, we will explore how to compute a time series from susceptibility
test data and examine different indexes that can be utilized. Through this analysis,
we will gain a deeper understanding of how to utilize these indexes to evaluate the
evolving patterns of bacterial susceptibility and guide effective antimicrobial therapy
strategies.

.. |1D30| replace:: 1D\ :sub:`30`
.. |1M1| replace:: 1M\ :sub:`1`
.. |1M30| replace:: 1M\ :sub:`30`
.. |7D4| replace:: 1M\ :sub:`12`
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

.. image:: ../../../_static/imgs/timeseries-generation.png
   :width: 500
   :align: center
   :alt: Generation of Time-Series

|

The notation to define the time series generation methodology (|SP|) is described with
various examples in Table 4.2. For instance, |7D4| defines a time series with weekly resistance
indexes (7D) calculated using the microbiology records available for the previous four weeks
(4x7D). It is important to note that some notations are equivalent representations of the same
susceptibility data at different granularities, hence their trends are comparable. As an example,
the trend estimated for |1M1| should be approximately thirty times the trend estimated for |1D30|.

.. note:: Using overlapping time intervals to compute an index is better than applying a moving
       average because it captures more detailed patterns in the data and reduces bias from
       fixed window sizes. It provides a more comprehensive analysis and improves accuracy in
       representing the characteristics of the time series.

"""

#######################################################################
#
# Loading data
# ------------
#
# A small dataset will be used for this example.

# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import from pyAMR
from pyamr.datasets.load import make_susceptibility

# -------------------------------------------
# Load data
# -------------------------------------------
# Load data
data = make_susceptibility()
data = data.drop_duplicates()

# Convert date to datetime
data.date_received = pd.to_datetime(data.date_received)

# Filter (speeds up the execution)
idxs_spec = data.specimen_code.isin(['URICUL'])
idxs_abxs = data.antimicrobial_name.isin(['augmentin'])

# Filter
data = data[idxs_spec & idxs_abxs]

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.dtypes)

#######################################################################
# Computing SARI timeseries
# -------------------------
#
# In order to study the temporal evolution of AMR, it is necessary to generate
# a resistance time series from the susceptibility test data. This is often
# achieved by calculating the resistance index; that is ``SARI`` on consecutive
# partitions of the data. Note that each partition contains the susceptibility
# tests that will be used to compute the resistance index.
#
# For more information see: :py:mod:`pyamr.core.sari.SARI`
#
# For more examples see:
#
#   - :ref:`sphx_glr__examples_indexes_plot_sari_d_temporal.py`
#
# First, let's compute the time series

# -----------------------------------------
# Compute  sari (temporal)
# -----------------------------------------
from pyamr.core.sari import SARI

# Create SARI instance
sar = SARI(groupby=['specimen_code',
                    'microorganism_name',
                    'antimicrobial_name',
                    'sensitivity'])

# Create constants
shift, period = '30D', '30D'

# Compute sari timeseries
iti = sar.compute(data, shift=shift,
     period=period, cdate='date_received')

# Reset index
iti = iti.reset_index()

# Show
#print("\nSARI (temporal):")
#print(iti)

iti.head(10)

#%%
#
# Let's plot the evolution of a single combination.
#

# --------------
# Filter
# --------------
# Constants
s, o, a = 'URICUL', 'escherichia coli', 'augmentin'

# Filter
idxs_spec = iti.specimen_code == s
idxs_orgs = iti.microorganism_name == o
idxs_abxs = iti.antimicrobial_name == a
aux = iti[idxs_spec & idxs_orgs & idxs_abxs]

# --------------
# Plot
# --------------
# Create figure
fig, axes = plt.subplots(2, 1, sharex=True,
     gridspec_kw={'height_ratios': [2, 1]})
axes = axes.flatten()

# Plot line
sns.lineplot(x=aux.date_received, y=aux.sari,
    linewidth=0.75, linestyle='--', #palette="tab10",
    marker='o', markersize=3, markeredgecolor='k',
    markeredgewidth=0.5, markerfacecolor=None,
    alpha=0.5, ax=axes[0])

# Compute widths
widths = [d.days for d in np.diff(aux.date_received.tolist())]

# Plot bars
axes[1].bar(x=aux.date_received, height=aux.freq,
    width=.8*widths[0], linewidth=0.75, alpha=0.5)

# Configure
axes[0].set(ylim=[-0.1, 1.1],
    title='[%s, %s, %s] with $%s_{%s}$' % (
        s, o.upper(), a.upper(), shift, period))

# Despine
sns.despine(bottom=True)

# Tight layout
plt.tight_layout()

# Show
#print("\nTemporal (ITI):")
#print(aux)
aux


#######################################################################
# Computing ASAI timeseries
# -------------------------
#
# .. warning:: It is important to take into account that computing
#              this index, specially over a period of time, requires
#              a lot of consistent data. Ideally, all the species
#              for the genus of interest should appear on all the
#              time periods.
#
# Once we have computed ``SARI`` on a temporal fashion, it is possible
# to use such information to compute ``ASAI`` in a temporal fashion too.
# However, as explained in the previous tutorial, in order to compute
# ``ASAI``, we need to at least have columns with the following
# information:
#
#   - ``antimicrobial``
#   - ``microorganism genus``
#   - ``microorganism species``
#   - ``resistance``
#
# Moreover, in this example we will compute the ASAI for each ``gram_stain`` category
# independently so we will need the microorganism gram stain information too. This
# information is available in the registries: :py:mod:`pyamr.datasets.registries`.
#
# Lets include all this information using the ``MicroorganismRegistry``.
#

# ------------------------------
# Include gram stain
# ------------------------------
# Libraries
from pyamr.datasets.registries import MicroorganismRegistry

# Load registry
mreg = MicroorganismRegistry()

# Format sari dataframe
dataframe = iti.copy(deep=True)
dataframe = dataframe.reset_index()

# Create genus and species
dataframe[['genus', 'species']] = \
    dataframe.microorganism_name \
        .str.capitalize() \
        .str.split(expand=True, n=1)

# Combine with registry information
dataframe = mreg.combine(dataframe, on='microorganism_name')

# Fill missing gram stain
dataframe.gram_stain = dataframe.gram_stain.fillna('u')

# Show
dataframe.head(4).T

##############################################################################
#
# Now that we have the ``genus``, ``species`` and ``gram_stain`` information,
# lets see how to compute ``ASAI`` in a temporal fashion with an example. It is
# important to highlight that now the date (``date_received``) is also included
# in the groupby parameter when calling the compute method.
#
# For more information see: :py:mod:`pyamr.core.asai.ASAI`
#
# For more examples see:
#
#   - :ref:`sphx_glr__examples_indexes_plot_asai_c_temporal.py`
#

# -------------------------------------------
# Compute ASAI
# -------------------------------------------
# Import specific libraries
from pyamr.core.asai import ASAI

# Create asai instance
asai = ASAI(column_genus='genus',
            column_specie='species',
            column_resistance='sari',
            column_frequency='freq')

# Compute
scores = asai.compute(dataframe,
    groupby=['date_received',
             'specimen_code',
             'antimicrobial_name',
             'gram_stain'],
    weights='uniform',
    threshold=0.5,
    min_freq=0)

# Stack
scores = scores

# Show
print("\nASAI (overall):")
print(scores.unstack())
scores.unstack()

#############################################################################
#
# Let's plot the evolution for both stains.
#

# Libraries
import calendar

# Month numbers to abbr
def month_abbr(v):
    return [calendar.month_abbr[x] for x in v]

# --------------
# Filter
# --------------
#
s, a = 'URICUL', 'augmentin'
# Filter and drop index.
scores = scores.filter(like=s, axis=0)
scores = scores.filter(like=a, axis=0)
scores.index = scores.index.droplevel(level=[1,2])

# ----------
# Plot
# ----------
# Initialize the matplotlib figure
f, ax = plt.subplots(1, figsize=(10, 5))

# Show
sns.lineplot(data=scores, x='date_received', y='ASAI_SCORE',
             hue='gram_stain', palette="tab10", linewidth=0.75,
             linestyle='--', marker='o', markersize=3,
             markeredgecolor='k', markeredgewidth=0.5,
             markerfacecolor=None, alpha=0.5, ax=ax)#, ax=axes[0])

# Create aux table for visualization
aux = scores[['N_GENUS', 'N_SPECIE']] \
     .unstack().T.round(0) \
     .astype(str).replace({'nan': '-'})

# Rename columns
#aux.columns = month_abbr(range(1, len(aux.columns)+1))

# Draw table
table = ax.table(cellText=aux.to_numpy(),
                 rowLabels=aux.index,
                 colLabels=aux.columns.date,
                 cellLoc='center',
                 loc='bottom')
table.auto_set_font_size(False)
table.set_fontsize(7.5)
table.scale(1, 1.2)

# Sns config
sns.despine(left=True, bottom=True)

# Add a legend and informative axis label
ax.set(xlabel='', ylabel='ASAI', xticks=[],
       title="[%s, %s] with $%s_{%s}$" % (
        s, a.upper(), shift, period))


# Tight layout()
plt.tight_layout()

# Show
plt.show()

# Show
#print("\nASAI (overall):")
#print(scores.unstack())

scores.unstack()

#########################################################################
#
# Further considerations
# ----------------------
#
# .. warning:: Pending!