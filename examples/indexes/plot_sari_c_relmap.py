"""
``SARI`` - By specimen w/ ``sns.relmap``
----------------------------------------

.. todo:: Explain...

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
# Methods
# -------------------------------------------
def create_mapper(dataframe, column_key, column_value):
    """This method constructs a mapper

    Parameters
    ----------
    dataframe: dataframe-like
      The dataframe from which the columns are extracted

    column_key: string-like
      The name of the column with the values for the keys of the mapper

    column_value: string-like
      The name of the column with the values for the values of the mapper

    Returns
    -------
    dictionary
    """
    dataframe = dataframe[[column_key, column_value]]
    dataframe = dataframe.drop_duplicates()
    return dict(zip(dataframe[column_key], dataframe[column_value]))


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

    # ------------
    # Plot Heatmap
    # ------------
    # Create colormap
    cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

    # Configura
    sizes = (df.freq.min(), df.freq.max())

    # Plot
    g = sns.relplot(data=df.reset_index(), x='microorganism_code',
                    y='antimicrobial_code', hue="sari", size="freq",
                    palette='Reds', hue_norm=(0, 1), edgecolor="gray",
                    linewidth=0.5, sizes=sizes,  # size_norm=sizes,
                    dashes=True, legend='brief', height=10)

    # Configure plot
    g.set(xlabel="Antimicrobial",
          ylabel="Microorganism",
          title='Antibiogram (with frequency)',
          #aspect='equal'
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