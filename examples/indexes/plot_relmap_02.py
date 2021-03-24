"""
SARI - Relplot (by culture)
----------------------------

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

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.columns)

# -------------------------------------------
# For each culture type
# -------------------------------------------
# Count records per order code
specimen_code_count = data.specimen_code.value_counts()

# Filter most frequent order codes
data = data[data.specimen_code.isin( \
    specimen_code_count.index.values[:5])]

# Loop
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

    # Compute SARI
    sari_overall = SARI(strategy='hard').compute(freq_overall)

    # -------------------------------
    # Create matrix
    # -------------------------------
    # Create mappers
    abx_map = create_mapper(data, 'antimicrobial_code', 'antimicrobial_class')
    org_map = create_mapper(data, 'microorganism_code', 'microorganism_genus')

    # Create matrix
    matrix = sari_overall
    matrix['freq'] = freq_overall.sum(axis=1)
    matrix = matrix.reset_index()
    matrix['microorganism_genus'] = matrix.SPECIE.map(org_map)
    matrix['antimicrobial_class'] = matrix.ANTIBIOTIC.map(abx_map)

    # Show
    print("\nData:")
    print(matrix)
    print("\nColumns:")
    print(matrix.columns)
    print("\nFrequencies:")
    print(matrix.freq.describe())

    # Create colormap
    cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

    # Configura
    sizes = (matrix.freq.min(), matrix.freq.max())

    # Plot
    g = sns.relplot(data=matrix, x='SPECIE',
        y='ANTIBIOTIC', hue="sari", size="freq",
        palette='Reds', hue_norm=(0, 1), edgecolor="gray",
        linewidth=0.5, sizes=sizes, #size_norm=sizes,
        dashes=True, legend='brief', height=10
    )

    # Configure plot
    g.set(xlabel="Antimicrobial",
          ylabel="Microorganism",
          title='Antibiogram (with frequency)')
          #aspect="equal")
    g.despine(left=True, bottom=True)
    g.ax.margins(.1)

    # Configure xticks
    for label in g.ax.get_xticklabels():
        label.set_rotation(90)

    # Configure legend
    for artist in g.legend.legendHandles:
        artist.set_edgecolor("k")
        artist.set_linewidth(0.5)

    # Suptitle
    plt.suptitle(specimen_code)

    # Add grid lines.
    #plt.grid(linestyle='-', linewidth=0.5, color='.7')

    # Adjust
    plt.tight_layout()

# Show
plt.show()
