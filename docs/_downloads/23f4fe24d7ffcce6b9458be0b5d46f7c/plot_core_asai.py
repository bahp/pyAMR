"""
Index - ASAI
============================

.. todo::
    - Create data as in the example shown in the figure.
    - Improve visualization.
    - Create further examples with temporal visualization.
    - Create further examples with general heatmap.
    - Create further examples with animation?

The antimicrobial spectrum of activity refers to the range of microbe species that are susceptible to
these agents and therefore can be treated. In general, antimicrobial agents are classified into broad,
intermediate or narrow spectrum. Broad spectrum antimicrobials are active against both Gram-positive
and Gram-negative bacteria. In contrast, narrow spectrum antimicrobials have limited activity and are
effective only against particular species of bacteria. While these profiles appeared in the mid-1950s,
little effort has been made to define them. Furthermore, such ambiguous labels are overused for different
and even contradictory purposes.

.. image:: ../../_static/imgs/index-asai.png
   :align: right
   :alt: ASAI
"""


# Import libraries
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.core.asai import ASAI
from pyamr.core.asai import asai

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


# ---------------------
# helper method
# ---------------------
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


# ---------------------
# Create data
# ---------------------
# Create data
data = [['Staphylococcus', 'coagulase negative', 'ANTIBIOTIC_1', 'P', 0.88, 1, 0.20, 1/10, 1/3],
        ['Staphylococcus', 'epidermidis', 'ANTIBIOTIC_1', 'P', 0.11, 1, 0.20, 1/10, 1/3],
        ['Staphylococcus', 'haemolyticus', 'ANTIBIOTIC_1', 'P', 0.32, 1, 0.20, 1/10, 1/3],
        ['Staphylococcus', 'lugdumensis', 'ANTIBIOTIC_1', 'P', 0.45, 1, 0.20, 1/10, 1/3],
        ['Staphylococcus', 'saporphyticus', 'ANTIBIOTIC_1', 'P', 0.18, 1, 0.20, 1/10, 1/3],
        ['Staphylococcus', 'aureus', 'ANTIBIOTIC_1', 'P', 0.13, 5, 0.20, 5/10, 1/3],

        ['Enterococcus', 'durans', 'ANTIBIOTIC_1', 'N', 0.64, 1, 0.20, 1/4, 1/3],
        ['Enterococcus', 'faecium', 'ANTIBIOTIC_1', 'N', 0.48, 1, 0.20, 1/4, 1/3],
        ['Enterococcus', 'gallinarium', 'ANTIBIOTIC_1', 'N', 0.10, 1, 0.20, 1/4, 1/3],
        ['Enterococcus', 'faecalis', 'ANTIBIOTIC_1', 'N', 0.09, 1, 0.20, 1/4, 1/3],

        ['Streptococcus', 'viridians', 'ANTIBIOTIC_1', 'P', 0.08, 1, 0.20, 1/3, 1/3],
        ['Streptococcus', 'pneumoniae', 'ANTIBIOTIC_1', 'P', 0.89, 2, 0.20, 2/3, 1/3]]


# Create dataframe
dataframe = pd.DataFrame(data, columns=['GENUS',
                                        'SPECIE',
                                        'ANTIBIOTIC',
                                        'GRAM',
                                        'RESISTANCE',
                                        'FREQUENCY',
                                        'THRESHOLD',
                                        'W_SPECIE',
                                        'W_GENUS'])

# Show data
print("\nData:")
print(dataframe)

# ----------------------------------------------------
# ASAI (must raise error)
# ----------------------------------------------------
print("\n\nHandling errors:")

try:
    asai = dataframe.drop(columns=['RESISTANCE']) \
        .groupby(['ANTIBIOTIC']) \
        .apply(asai)
except Exception as e:
    print(e)

try:
    asai = dataframe.drop(columns=['GENUS']) \
        .groupby(['ANTIBIOTIC']) \
        .apply(asai)
except Exception as e:
    print(e)

try:
    asai = dataframe.drop(columns=['SPECIE']) \
        .groupby(['ANTIBIOTIC']) \
        .apply(asai)
except Exception as e:
    print(e)

try:
    asai = dataframe.drop(columns=['W_GENUS']) \
        .groupby(['ANTIBIOTIC']) \
        .apply(asai)
except Exception as e:
    print(e)

try:
    asai = dataframe.drop(columns=['RESISTANCE', 'SPECIE']) \
        .groupby(['ANTIBIOTIC']) \
        .apply(asai)
except Exception as e:
    print(e)


try:
    asai = dataframe \
        .groupby(['ANTIBIOTIC', 'GRAM']) \
        .apply(asai)
except Exception as e:
    print(e)

# ----------------------------------------------------
# ASAI (must show warning)
# ----------------------------------------------------
print("\n\nShow warnings:")

asai_5 = dataframe.drop(columns=['THRESHOLD']) \
    .groupby(['ANTIBIOTIC']) \
    .apply(asai)

asai_6 = dataframe \
    .groupby(['ANTIBIOTIC']) \
    .apply(asai, threshold=0.5)


# ----------------------------------------------------
# ASAI
# ----------------------------------------------------
print("\n\nNo errors or warnings:")

# -------
# DEFAULT
# -------
asai_7 = dataframe \
    .groupby(['ANTIBIOTIC']) \
    .apply(asai, verbose=0)

# Show
print("\n\nASAI (weights):")
print(asai_7)

# -------
# UNIFORM
# -------
asai_8 = dataframe \
    .groupby(['ANTIBIOTIC', 'GRAM']) \
    .apply(asai, weights='uniform')

print("\n\nASAI (uniform):")
print(asai_8)

# ---------
# FREQUENCY
# ---------
asai_9 = dataframe \
    .groupby(['ANTIBIOTIC', 'GRAM']) \
    .apply(asai, weights='frequency')

# Show
print("\n\nASAI (frequency):")
print(asai_9)


# -------------------------------
# Create antimicrobial spectrum
# -------------------------------
# Create antimicrobial spectrum of activity instance
asai = ASAI(weights='uniform', threshold=0.21,
            column_genus='GENUS',
            column_specie='SPECIE',
            column_antibiotic='ANTIBIOTIC',
            column_resistance='RESISTANCE',
            column_frequency='FREQUENCY',
            column_threshold='THRESHOLD',
            column_wgenus='W_GENUS',
            column_wspecie='W_SPECIE')

# Compute
scores = asai.compute(dataframe, by_category='GRAM')

# Show
print("\nASAI:")
print(scores)

# -----------------------------
# Plot
# -----------------------------
# Variables to plot.
x = scores.index.values
y_n = scores['ASAI_SCORE']['N'].values
y_p = scores['ASAI_SCORE']['P'].values

# Constants
colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)

# Create figure
f, ax = plt.subplots(1, 1, figsize=(8, 0.5))

# Plot
sns.barplot(x=y_p, y=x, palette=colormap_p, ax=ax, orient='h',
            saturation=0.5, label='Gram-positive')
sns.barplot(x=-y_n, y=x, palette=colormap_n, ax=ax, orient='h',
            saturation=0.5, label='Gram-negative')

# Configure
sns.despine(bottom=True)

# Configure
ax.set_xlim([-1, 1])

# Legend
plt.legend()

# Display
#plt.show()