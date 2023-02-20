"""
Step 01 - Indexes
=================
"""


#######################################################################
#
# Loading data
# ------------
#
# .. image:: ../../../_static/imgs/susceptibility-test-record.png
#    :width: 200
#    :align: right
#    :alt: ASAI
#
# A ``Susceptibility test`` record (see figure 4.1) is composed by laboratory
# identification number (LID), patient identification number (PID), date, sample
# type, specimen or culture (e.g. blood or urine), pathogen, antimicrobial, reported
# status and outcome (resistant, sensitive or intermediate). In this research,
# the susceptibility test data were grouped firstly by specimen type. Moreover,
# for each sample type, the data were grouped by pairs (pathogen, antimicrobial)
# since it is widely accepted by clinicians as detailed in the UK five year
# strategy in AMR.
#
# A small dataset will be used for this example.
#

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

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.dtypes)

# Show unique elements
print("\nUnique values:")
for c in ['microorganism_code',
          'antimicrobial_code',
          'specimen_code',
          'laboratory_number']:
    print('%-18s -> %5s' % (c, data[c].nunique()))


#######################################################################
#
# Computing SARI
# --------------
#
# The Single Antimicrobial Resistance Index - ``SARI`` - describes the proportion
# of resistant isolates for a given set of susceptibility tests. It provides a
# value within the range [0, 1] where values close to one indicate high resistance.
# It is agnostic to pathogen, antibiotic and/or time. The variables ``R``, ``I`` and
# ``S`` represent the number of susceptibility tests with Resistant, Intermediate and
# Susceptible outcomes respectively. The definition might vary slightly since the
# intermediate category is not always considered.
#
# The parameter strategy accepts the following options:
#
#   - ``soft``   as R / R+I+S
#   - ``medium`` as R / R+S
#   - ``hard``  as R+I / R+I+S
#   - ``other``  as R+0.5I / R+0.5I+S
#
# For more information see: :py:mod:`pyamr.core.sari.SARI`
#
# For more examples see:
#
#   - :ref:`sphx_glr__examples_tutorial_indexes_plot_core_sari.py`
#   - :ref:`sphx_glr__examples_indexes_plot_sari_antibiogram.py`
#   - :ref:`sphx_glr__examples_indexes_plot_sari_clustermap.py`
#   - :ref:`sphx_glr__examples_indexes_plot_sari_relmap.py`
#

# -------------------------------------------
# Compute SARI
# -------------------------------------------
# Libraries
from pyamr.core.sari import SARI

# Create sari instance
sari = SARI(groupby=['specimen_code',
                     'microorganism_name',
                     'antimicrobial_name',
                     'sensitivity'])

# Compute SARI overall
sari_overall = sari.compute(data,
    return_frequencies=True)

# Show
print("SARI (overall):")
print(sari_overall)

# Plot Heatmap
# ------------
# Filter
matrix = sari_overall.copy(deep=True)
matrix = matrix.reset_index()
matrix = matrix[matrix.freq > 100]
matrix = matrix[matrix.specimen_code.isin(['BLDCUL'])]

# Pivot table
matrix = pd.pivot_table(matrix,
    index='microorganism_name',
    columns='antimicrobial_name',
    values='sari')

# Create figure
f, ax = plt.subplots(1, 1, figsize=(10, 4))

# Create colormap
cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

# Plot
ax = sns.heatmap(data=matrix*100, annot=True, fmt=".0f",
    annot_kws={'fontsize': 'small'}, cmap=cmap,
    linewidth=0.5, vmin=0, vmax=100, ax=ax,
    xticklabels=1, yticklabels=1)

# Add title
plt.suptitle("Antibiogram", fontsize='xx-large')

# Tight layout
plt.tight_layout()
plt.subplots_adjust(right=1.05)

#######################################################################
#
# Computing ASAI
# --------------
#
# The antimicrobial spectrum of activity refers to the range of microbe species
# that are susceptible to these agents and therefore can be treated. In general,
# antimicrobial agents are classified into broad, intermediate or narrow spectrum.
# Broad spectrum antimicrobials are active against both Gram-positive and
# Gram-negative bacteria. In contrast, narrow spectrum antimicrobials have limited
# activity and are effective only against particular species of bacteria. While these
# profiles appeared in the mid-1950s, little effort has been made to define them.
# Furthermore, such ambiguous labels are overused for different and even contradictory
# purposes.
#
# In order to compute the antimicrobial spectrum of activity index - ``ASAI`` -, it
# is necessary to previously obtain the overall resistance (SARI) for all the
# microbe-antimicrobial pairs. Furthermore, by following the criteria used in the
# narrow-broad approach, these pairs were grouped into Gram-positive and Gram-negative.
# Briefly, the weighted proportion of species to which the antimicrobial
# is effective is computed for each genus. These are later added up and normalized by
# the number of genera tested. An antimicrobial is considered effective to treat a
# particular species when the corresponding resistance index (SARI) is lower than
# a given threshold.
#
# For more information see: :py:mod:`pyamr.core.asai.ASAI`
#
# For more examples see:
#
#   - :ref:`sphx_glr__examples_tutorial_indexes_plot_core_asai.py`
#   - :ref:`sphx_glr__examples_indexes_plot_spectrum_gramtype.py`
#   - :ref:`sphx_glr__examples_indexes_plot_spectrum_multiple.py`
#
#
# In order to compute ``ASAI``, we need to have the following columns present
# in our dataset: ``antimicrobial``, ``microorganism_genus``, ``microorganism_species``
# and ``resistance``.  Moreover, in this example we will compute the ASAI for each
# ``gram_stain`` category independently so we will need the microorganism gram stain
# information too. This information is available in the registries: :py:mod:`pyamr.datasets.registries`
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
dataframe = sari_overall.copy(deep=True)
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

##############################################################################
#
# Now that we have the ``genus``, ``species`` and ``gram_stain`` information,
# lets compute ``ASAI``.
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
    groupby=['specimen_code',
             'antimicrobial_name',
             'gram_stain'],
    weights='uniform',
    threshold=0.5,
    min_freq=0)

# Stack
scores = scores.unstack()

# Filter and drop index.
scores = scores.filter(like='URICUL', axis=0)
scores.index = scores.index.droplevel()

# Show
print("\nASAI (overall):")
print(scores)

#######################################################################
#
# Lets plot it now!

# ----------------
# Helper method
# ----------------
def scalar_colormap(values, cmap, vmin, vmax):
    """This method creates a colormap based on values.

    Parameters
    ----------
    values : array-like
      The values to create the corresponding colors

    cmap : str
      The colormap

    vmin, vmax : float
      The minimum and maximum possible values

    Returns
    -------
    scalar colormap
    """
    # Create scalar mappable
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    # Gete color map
    colormap = sns.color_palette([mapper.to_rgba(i) for i in values])
    # Return
    return colormap

# ---------------------------------------------------------------
# Plot
# ---------------------------------------------------------------
# .. note: In order to sort the scores we need to compute metrics
#          that combine the different subcategories (e.g. gram-negative
#          and gram-positive). Two possible options are: (i) use the
#          gmean or (ii) the width.
# Measures
scores['width'] = np.abs(scores['ASAI_SCORE'].sum(axis=1))

# Variables to plot.
x = scores.index.values
y_n = scores['ASAI_SCORE']['n'].values
y_p = scores['ASAI_SCORE']['p'].values
y_u = scores['ASAI_SCORE']['u'].values

# Constants
colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)
colormap_u = scalar_colormap(y_u, cmap='Greens', vmin=-0.1, vmax=1.1)

# ----------
# Example
# ----------
# This example shows an stacked figure using more than two categories.
# For instance, it uses gram-positive, gram-negative and gram-unknown.
# All the indexes go within the range [0,1].
# Create the figure
f, axes = plt.subplots(1, 3, figsize=(7, 9))

# Plot each category
sns.barplot(x=y_p, y=x, palette=colormap_p, ax=axes[0], orient='h',
            saturation=0.5, label='Gram-positive')
sns.barplot(x=y_n, y=x, palette=colormap_n, ax=axes[1], orient='h',
            saturation=0.5, label='Gram-negative')
sns.barplot(x=y_u, y=x, palette=colormap_u, ax=axes[2], orient='h',
            saturation=0.5, label='Gram-unknown')

# Configure
sns.despine(bottom=True)

# Format figure
plt.subplots_adjust(wspace=0.0, hspace=0.0)

# Remove yticks
axes[1].set_yticks([])
axes[2].set_yticks([])

# Set title
axes[0].set_title('Gram-positive')
axes[1].set_title('Gram-negative')
axes[2].set_title('Gram-unknown')

# Set x-axis
axes[0].set_xlim([0, 1.1])
axes[1].set_xlim([0, 1.1])
axes[2].set_xlim([0, 1.1])

# Adjust
plt.tight_layout()



#######################################################################
#
# Computing SART
# --------------
#
# The single antimicrobial resistance trend - ``SART`` - measures the ratio
# of change per time unit (e.g. monthly or yearly). To compute this metric,
# it is necessary to generate a resistance time series from the susceptibility
# test data. This is often achieved by computing the SARI on consecutive or
# overlapping partitions of the data. Then, the trend can be extracted using
# for example a linear model where the slope, which is represented by a value
# within the range [-1, 1], indicates the ratio of change.
#
# For more information see: :py:mod:`pyamr.core.sart.SART`
#
# For more examples see:
#
#   - :ref:`sphx_glr__examples_tutorial_indexes_plot_core_sart.py`
#   - :ref:`sphx_glr__examples_indexes_plot_trend_basic.py`
#
# .. note:: Be cautious when Computing the ``SART`` index using a small dataset
#           (e.g. a low number of susceptibility tests records) since it is very
#           likely that the statistics produced (e.g. kurtosis or skewness) will
#           be ill defined.
#
# Since it is necessary to have a decent amount of records to be
# able to compute the trends accurately, lets filter and choose
# the tuples were are interested in.


# -------------------------------------------
# Show top combinations
# -------------------------------------------
from pyamr.core.sari import SARI

# Create SARI instance
sar = SARI(groupby=['specimen_code',
                    'microorganism_code',
                    'antimicrobial_code',
                    'sensitivity'])

# Compute SARI overall
sari_overall = sar.compute(data,
     return_frequencies=True)

# Compute top tuples
top = sari_overall \
    .sort_values(by='freq', ascending=False) \
    .head(10)

# Show
print("\nTop by Frequency:")
print(top)

# -------------------------------------------
# Filter data
# -------------------------------------------
# Define spec, orgs, abxs of interest
spec = ['URICUL']
orgs = ['ECOL']
abxs = ['ACELX', 'ACIP', 'AAMPC', 'ATRI', 'AAUG',
        'AMER', 'ANIT', 'AAMI', 'ACTX', 'ATAZ',
        'AGEN', 'AERT', 'ACAZ', 'AMEC', 'ACXT']

# Create auxiliary DataFrame
aux = data.copy(deep=True) \

# Filter
idxs_spec = data.specimen_code.isin(spec)
idxs_orgs = data.microorganism_code.isin(orgs)
idxs_abxs = data.antimicrobial_code.isin(abxs)

# Filter
aux = aux[idxs_spec & idxs_orgs & idxs_abxs]


########################################################
#
# Now, lets compute the resistance trend.

# Libraries
import warnings

# Import specific libraries
from pyamr.core.sart import SART

# Variables
shift, period = '10D', '180D'

# Create instance
sar = SART(column_specimen='specimen_code',
           column_microorganism='microorganism_code',
           column_antimicrobial='antimicrobial_code',
           column_date='date_received',
           column_outcome='sensitivity',
           column_resistance='sari')

with warnings.catch_warnings():
    warnings.simplefilter('ignore')

    # Compute resistance trends
    table, objs = sar.compute(aux, shift=shift,
        period=period, return_objects=True)

######################################################
#
# Lets see the summary DataFrame (note it is transposed!)

# Configure pandas
pd.set_option(
    'display.max_colwidth', 20,
    'display.width', 1000
)

# Show
print("Results:")
print(table.T)

######################################################
#
# Lets see the model summary for the first entry

# Display
# This example shows how to make predictions using the wrapper and how
# to plot the result in data. In addition, it compares the intervals
# provided by get_prediction (confidence intervals) and the intervals
# provided by wls_prediction_std (prediction intervals).

# Variables
name, obj = objs[2] # AAUG

# Series
series = obj.as_series()

# Variables.
start, end = None, 50

# Get x and y
x = series['wls-exog'][:,1]
y = series['wls-endog']

# Compute predictions (exogenous?). It returns a 2D array
# where the rows contain the time (t), the mean, the lower
# and upper confidence (or prediction?) interval.
preds = obj.get_prediction(start=start, end=end)

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(11, 5))

# Plotting confidence intervals
# -----------------------------
# Plot truth values.
ax.plot(x, y, color='#A6CEE3', alpha=0.5, marker='o',
        markeredgecolor='k', markeredgewidth=0.5,
        markersize=5, linewidth=0.75, label='Observed')

# Plot forecasted values.
ax.plot(preds[0, :], preds[1, :], color='#FF0000', alpha=1.00,
        linewidth=2.0, label=obj._identifier(short=True))

# Plot the confidence intervals.
ax.fill_between(preds[0, :], preds[2, :],
                preds[3, :],
                color='r',
                alpha=0.1)

# Legend
plt.legend()
plt.title(name)


print("Name: %s\n" % str(name))
print(obj.as_summary())

#######################################################
#
# Lets display the information as a table graph

# Libraries
from pyamr.graphics.table_graph import _DEFAULT_CONFIGURATION
from pyamr.graphics.table_graph import vlinebgplot

# Configuration for display
info = _DEFAULT_CONFIGURATION

# Lets define one as an example.
info['freq'] = {
    'cmap': 'Blues',
    'title': 'Freq',
    'xticks': [0, 8000],
    'kwargs': {
        's': 80,
        'vmin': 0
    }
}

# .. note: It is important to ensure that the column names
#          match with the keys of the previously loaded
#          info configuration so that it is used.

# Rename columns
rename = {
    'wls-x1_coef': 'sart_m',
    'wls-const_coef': 'offset',
    'wls-rsquared': 'r2',
    'wls-rsquared_adj': 'r2_adj',
    'wls-m_skew': 'skew',
    'wls-m_kurtosis': 'kurtosis',
    'wls-m_jb_prob': 'jb',
    'wls-m_dw': 'dw',
    'wls-const_tprob': 'ptm',
    'wls-x1_tprob': 'ptn',
    'wls-pearson': 'pearson',
    'freq': 'freq',
}


# ----------------
# Combine with SARI

# Format combined DataFrame
comb = table.join(sari_overall)
comb.index = comb.index.map('_'.join)
comb = comb.reset_index()
comb = comb.rename(columns=rename)

# Add new columns
comb['sart_y'] = comb.sart_m * 12   # Yearly trend
comb['sari_pct'] = comb.sari * 100  # SARI percent

# Sort by trend
comb = comb.sort_values(by='sart_y', ascending=False)

# Select only numeric columns
# data = comb.select_dtypes(include=np.number)
data = comb[[
    'index',
    'sart_m',
    #'sart_y',
    'sari_pct',
    'r2',
    #'r2_adj',
    'skew',
    'kurtosis',
    'jb',
    'dw',
    'ptm',
    #'ptn',
    'pearson',
    'freq'
]]

# Show DataFrame
print("\nResults:")
print(data)

# Create pair grid
g = sns.PairGrid(data, x_vars=data.columns[1:],
    y_vars=["index"], height=4, aspect=.45)

# Set common features
g.set(xlabel='', ylabel='')

# Plot strips and format axes (skipping index)
for ax, c in zip(g.axes.flat, data.columns[1:]):

    # Get information
    d = info[c] if c in info else {}

    # .. note: We need to use scatter plot if we want to
    #          assign colors to the markers according to
    #          their value.

    # Using scatter plot
    sns.scatterplot(data=data, x=c, y='index', s=100,
                    ax=ax, linewidth=0.75, edgecolor='gray',
                    c=data[c], cmap=d.get('cmap', None),
                    norm=d.get('norm', None))

    # Plot vertical lines
    for e in d.get('vline', []):
        vlinebgplot(ax, top=data.shape[0], **e)

    # Configure axes
    ax.set(title=d.get('title', c),
           xlim=d.get('xlim', None),
           xticks=d.get('xticks', []),
           xlabel='', ylabel='')
    ax.tick_params(axis='y', which='both', length=0)
    ax.xaxis.grid(False)
    ax.yaxis.grid(visible=True, which='major',
                  color='gray', linestyle='-', linewidth=0.35)

# Despine
sns.despine(left=True, bottom=True)

# Adjust layout
plt.tight_layout()
plt.show()
