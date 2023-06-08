"""
SARI - Antibiogram (by specimen)
--------------------------------

.. todo:: Explain...

"""

# Libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
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
# Compute SARI
# -------------------------------------------
# Libraries
from pyamr.core.sari import SARI

# Create sari instance
sari = SARI(groupby=['specimen_code',
                     'microorganism_code',
                     'antimicrobial_code',
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

# Count records per specimen
specimen_count = sari_overall \
    .groupby('specimen_code').freq.sum() \
    .sort_values(ascending=False)

# Show
print("Cultures:")
print(specimen_count)

# Filter
sari_overall = sari_overall[sari_overall \
    .specimen_code.isin( \
        specimen_count.index.values[:5])]

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
         index='microorganism_code',
         columns='antimicrobial_code',
         values='sari')

    # ------------
    # Plot Heatmap
    # ------------
    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(10, 10))

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
    ax.set(aspect="equal")

    # Set rotation
    plt.yticks(rotation=0)

    # Add title
    plt.suptitle("Antibiogram (%s)" % specimen, fontsize=15)

    # Tight layout
    plt.tight_layout()

# Show
plt.show()