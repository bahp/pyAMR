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

# -------------------------------------------
# Plot
# -------------------------------------------
# Reset
sari_overall = sari_overall.reset_index()

# Loop
for specimen, df in sari_overall.groupby(by='specimen_code'):

    # -------------
    # Create matrix
    # -------------
    # Filter
    matrix = df.copy(deep=True)
    matrix = df.reset_index()
    #matrix = matrix[matrix.freq > 100]

    # Pivot table
    matrix = pd.pivot_table(matrix,
         index='microorganism_name',
         columns='antimicrobial_name',
         values='sari')

    # ------------
    # Plot Heatmap
    # ------------
    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(12, 12))

    # Create colormap
    cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

    # Specify cbar axes
    # cbar_ax = f.add_axes([.925, .3, .05, .3])

    # Plot
    ax = sns.heatmap(data=matrix*100, annot=True, fmt=".0f",
                     annot_kws={'fontsize': 7}, cmap=cmap,
                     linewidth=0.5, vmin=0, vmax=100, ax=ax,
                     #cbar_ax=cbar_ax,
                     xticklabels=1, yticklabels=1)

    # Configure axes
    #ax.set(aspect="equal")

    # Set rotation
    plt.yticks(rotation=0)

    # Add title
    plt.suptitle("Antibiogram (%s)" % specimen, fontsize=15)

    # Tight layout
    plt.tight_layout()

# Show
plt.show()