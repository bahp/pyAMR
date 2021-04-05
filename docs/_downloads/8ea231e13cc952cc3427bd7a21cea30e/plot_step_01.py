"""
Step 01 - Introduction
============================
"""


#######################################################################
#
# Loading data
# ------------
#
#
# .. image:: ../../_static/imgs/susceptibility-test-record.png
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
# strategy in AMR
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

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.dtypes)

# -------------------------------------------
# Show a brief description
# -------------------------------------------
# .. todo: Compute basic information such as the number of unique organisms,
#          antimicrobials, pairs, species, isolates, tests, the range of
#          dates, ....

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
# The parameter strategy accepts three different options:
#
#  (i) ``soft``   as R / R+I+S
#  (ii) ``medium`` as R / R+S
#  (iii) ``hard``  as R+I / R+I+S
#  (iv) ``other``  as R+0.5I / R+0.5I+S
#
# For more information see :ref:`sphx_glr__examples_tutorial_indexes_plot_core_sari.py`.

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
# that are susceptible to these agents and therefore can be treated. In general,
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
# In order to compute ``ASAI``, we need to at least have columns with the following
# information: ``antimicrobial``, ``microorganism genus``, ``microorganism species``
# and ``resistance``. Moreover, in this example we will compute the ASAI for each
# ``gram_stain`` category independently.
#
#
# Lets include all this information using the ``MicroorganismRegistry``.
#
# For more information see :ref:`sphx_glr__examples_tutorial_indexes_plot_core_asai.py`.

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
dataframe = mreg.combine(dataframe)

# Fill missing gram stain
dataframe.gram_stain = dataframe.gram_stain.fillna('u')

##############################################################################
#
# Now that we have the ``gram_stain`` information, lets compute ``ASAI``.
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

# Show
plt.show()


#######################################################################
#
# Computing SART
# --------------
#
# .. warning:: To include.


#######################################################################
#
# Dirty code to use and or delete
# -------------------------------

"""

Summary

summary = data.agg(
    norganisms=('organismCode', 'nunique'),
    nantibiotics=('antibioticCode', 'nunique'),
    ncultures=('orderCode', 'nunique'),
    ntests=('labNumber', 'nunique')
)

print(summary)

print(data.nunique())


print(len(data.groupby(['organismCode', 'antibioticCode'])))
print(data.shape[0])

summary = pd.DataFrame


#from analysis.microbiology.statistics.frequency import Frequency

# -----------------------------------------------------------------------------
#                                 CONSTANTS
# -----------------------------------------------------------------------------
# Paths
fname_tests = "freq_tests_pairs_year"
fname_isola = "freq_isolates_pairs_year"
fpath_tests = "../../results/microbiology/frequencies/%s.csv" % fname_tests
fpath_isola = "../../results/microbiology/frequencies/%s.csv" % fname_isola

# Object
freq = Frequency()

# Read data
dff_tests = freq.load(fpath_tests)
dff_isola = freq.load(fpath_isola)
dff_reset = dff_tests.reset_index()

# Basic dataframe.
# IMPORTANT. Note that isolates refer to a single infectious organism which
# is tested against many different anttibiotics. Hence the only way the sum
# refers to isolate is by grouping the laboratory tests by infectious
# organisms.
dfy = pd.DataFrame()
dfy['Tests'] = dff_tests['freq_ris'].groupby(level=[0]).sum()
dfy['Isolates'] = dff_isola['freq'].groupby(level=[0]).sum()
dfy['Tests/Isolates'] = dfy['Tests'].div(dfy['Isolates'])
dfy['Antibiotics'] = dff_reset.groupby('dateReceived').antibioticCode.nunique()
dfy['Organisms'] = dff_reset.groupby('dateReceived').organismCode.nunique()

# Fill last row.
dfy.loc['Total',:] = np.nan
dfy.loc['Total','Tests'] = dfy['Tests'].sum(axis=0)
dfy.loc['Total','Isolates'] = dfy['Isolates'].sum(axis=0)
dfy.loc['Total','Tests/Isolates'] = dfy['Tests/Isolates'].mean()
dfy.loc['Total','Antibiotics'] = dff_reset.antibioticCode.nunique()
dfy.loc['Total','Organisms'] = dff_reset.organismCode.nunique()

# Print dataframe.
print("\n\n")
print("Pandas:")
print("-------")
print(dfy)

# Print dataframe latex format.
print("\n\n")
print("Latex:")
print("-------")
print(dfy.to_latex())

#print dff_isola.head(10)
import sys
sys.exit()


"""