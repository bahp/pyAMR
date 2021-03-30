"""
SARI - Antibiogram
------------------

.. todo:: Explain and Simplify

.. todo: Frequency might not be working?
         Frequency can be computed as sum of columns.

"""

# Libraries
import sys
import glob
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import own libraries
from pyamr.core.freq import Frequency
from pyamr.core.sari import SARI
from pyamr.datasets.load import load_data_mimic

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

# --------------------------------------------------------------------
#                               Main
# --------------------------------------------------------------------
# Load data
data, antibiotics, organisms = load_data_mimic()

# Count records per specimen code
specimen_code_count = data \
    .groupby('laboratory_number').head(1) \
    .specimen_code.value_counts(normalize=True) \
    .sort_values(ascending=False)

# Filter most frequent specimens
data = data[data.specimen_code.isin( \
    specimen_code_count.index.values[:5])]

# Loop for each specimen
for specimen_code, df in data.groupby(by='specimen_code'):

    # -------------------------------------------
    # Compute Freq and SARI
    # -------------------------------------------
    # Create instance
    freq = Frequency(column_antibiotic='antimicrobial_code',
                     column_organism='microorganism_code',
                     column_date='date_received',
                     column_outcome='sensitivity')

    # Compute frequencies (overall)
    freq_overall = freq.compute(df, by_category='pairs')

    # Filter
    freq_overall = freq_overall[freq_overall.sum(axis=1) > 100]

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
    f, ax = plt.subplots(1, 1, figsize=(12, 12))

    # Create colormap
    cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

    # Specify cbar axes
    #cbar_ax = f.add_axes([.925, .3, .05, .3])

    # Plot
    ax = sns.heatmap(data=matrix, annot=True, fmt=".0f",
                     annot_kws={'fontsize': 7}, cmap=cmap,
                     linewidth=0.5, vmin=0, vmax=100, ax=ax,
                     xticklabels=1, yticklabels=1)
                     # cbar_ax=cbar_ax)

    # Configure axes
    ax.set(aspect="equal")

    # Set rotation
    plt.yticks(rotation=0)

    # Add title
    plt.suptitle("Antibiogram (%s)" % specimen_code,
        fontsize=15)

    # Tight layout
    plt.tight_layout()
    #plt.subplots_adjust(right=0.91)

# Show
plt.show()