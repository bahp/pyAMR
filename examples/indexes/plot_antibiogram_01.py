"""
SARI - Antibiogram (overall)
----------------------------

.. warning:: Explain..?

"""


# Libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import own libraries
from pyamr.core.sari import SARI
from pyamr.core.freq import Frequency
from pyamr.datasets.load import make_susceptibility

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
data = make_susceptibility()

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.columns)


# -------------------------------------------
# Compute Freq and SARI
# -------------------------------------------
# Create instance
freq = Frequency(column_antibiotic='antimicrobial_code',
                 column_organism='microorganism_code',
                 column_date='date_received',
                 column_outcome='sensitivity')

# Compute frequencies (overall)
freq_overall = freq.compute(data, by_category='pairs')

# Compute SARI
sari_overall = SARI(strategy='hard').compute(freq_overall)


# ------------
# Plot Heatmap
# ------------
# Create matrix
matrix = sari_overall[['sari']]
matrix = matrix.unstack() * 100
matrix.columns = matrix.columns.droplevel()

# Create figure
f, ax = plt.subplots(1, 1, figsize=(18, 10))

# Create colormap
cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

# Plot
ax = sns.heatmap(data=matrix.T, annot=True, fmt=".0f",
    annot_kws={'fontsize': 5}, cmap=cmap,
    linewidth=0.5, vmin=0, vmax=100, ax=ax,
    xticklabels=1, yticklabels=1)

# Configure axes
#ax.set(aspect='equal')

# Add title
plt.suptitle("Antibiogram", fontsize='xx-large')

# Tight layout
plt.tight_layout()
#plt.subplots_adjust(right=0.0)

# Show
plt.show()