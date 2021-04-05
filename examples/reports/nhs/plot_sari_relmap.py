"""
SARI - Antibiogram (relmap)
---------------------------

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
from pyamr.datasets.load import load_data_nhs

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
data, antibiotics, organisms = load_data_nhs()

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


# Loop for each specimen
for specimen, df in sari_overall.groupby(by='specimen_code'):
    # ------------
    # Plot Heatmap
    # ------------
    # Create colormap
    cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

    # Configura
    sizes = (df.freq.min(), df.freq.max())

    # Plot
    g = sns.relplot(data=df.reset_index(), x='microorganism_name',
                    y='antimicrobial_name', hue="sari", size="freq",
                    palette='Reds', hue_norm=(0, 1), edgecolor="gray",
                    linewidth=0.5, sizes=sizes,  # size_norm=sizes,
                    dashes=True, legend='brief', height=10)

    # Configure plot
    g.set(xlabel="Antimicrobial",
          ylabel="Microorganism",
          title='Antibiogram (with frequency)',
          # aspect='equal'
          )
    g.despine(left=True, bottom=True)
    g.ax.margins(.1)

    # Configure xticks
    for label in g.ax.get_xticklabels():
        label.set_rotation(90)

    # Configure legend
    for artist in g.legend.legendHandles:
        artist.set_edgecolor("k")
        artist.set_linewidth(0.5)

    # Superior title
    plt.suptitle(specimen)

    # Add grid lines.
    # plt.grid(linestyle='-', linewidth=0.5, color='.7')

    # Adjust
    plt.tight_layout()

    # Show
plt.show()