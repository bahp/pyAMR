"""
Spectrum of Activity (ASAI)
==========================================

.. todo::
    - Improve visualization method (generic).
    - Create further examples with temporal visualization.
    - Create further examples with general heatmap.
    - Create further examples with animation?

.. warning:: The contribution (cont) value for Staphylococcus haemolyticus
             should be 0 instead of 1/10 because the sari index is higher
             than the threshold (32 > 20) and therefore the antimicrobial
             is not considered effective.

The antimicrobial spectrum of activity refers to the range of microbe species that are
susceptible to these agents and therefore can be treated. In general, antimicrobial agents
are classified into broad, intermediate or narrow spectrum. Broad spectrum antimicrobials
are active against both Gram-positive and Gram-negative bacteria. In contrast, narrow
spectrum antimicrobials have limited activity and are effective only against particular
species of bacteria. While these profiles appeared in the mid-1950s, little effort has been
made to define them. Furthermore, such ambiguous labels are overused for different
and even contradictory purposes.

For more information see: :py:mod:`pyamr.core.asai.ASAI`

.. image:: ../../../_static/imgs/index-asai.png
    :width: 600
    :align: center
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
from pyamr.graphics.utils import scalar_colormap

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
# Create data
# ---------------------
# Create data
data = [
    ['Staphylococcus', 'coagulase negative', 'ANTIBIOTIC_1', 'P', 0.88, 1, 0.20, 1/10, 1/3],
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
    ['Streptococcus', 'pneumoniae', 'ANTIBIOTIC_1', 'P', 0.89, 2, 0.20, 2/3, 1/3]
]


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


############################################################
#
# Lets use the ASAI object
#

# -------------------------------
# Create antimicrobial spectrum
# -------------------------------
# Create antimicrobial spectrum of activity instance
asai = ASAI(column_genus='GENUS',
            column_specie='SPECIE',
            column_resistance='RESISTANCE',
            column_frequency='FREQUENCY',
            column_threshold='THRESHOLD',
            column_wgenus='W_GENUS',
            column_wspecie='W_SPECIE')
# Compute
scores = asai.compute(dataframe,
    groupby=['ANTIBIOTIC', 'GRAM'],
    weights='uniform',
    threshold=None,
    min_freq=0)

# Unstack
scores = scores.unstack()

# Show
#print("\nASAI (instance):")
#print(scores)

scores

###############################################################
#
# Lets display the information graphically

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
plt.show()