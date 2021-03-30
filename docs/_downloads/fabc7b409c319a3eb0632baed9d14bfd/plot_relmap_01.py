"""
SARI - Relplot (overall)
-------------------------

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

# ------------------------
# Methods
# ------------------------
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
data = data.head(10000)

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


# -------------------------------------------
# Plot antibiogram clustered
# -------------------------------------------

# -------------------------------
# Create matrix
# -------------------------------
# Create mappers
abx_map = create_mapper(data, 'antimicrobial_code', 'antimicrobial_class')
org_map = create_mapper(data, 'microorganism_code', 'microorganism_genus')

# Create matrix
matrix = sari_overall.copy(deep=True)
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


# -------------------------------
# Plot
# -------------------------------
# Create colormap
cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

# Configura
sizes = (matrix.freq.min(), matrix.freq.max())

# Plot
g = sns.relplot(data=matrix, x='SPECIE',
    y='ANTIBIOTIC', hue="sari", size="freq",
    palette='Reds', hue_norm=(0, 1), edgecolor=".7", # 'k'
    linewidth=1.0, height=10, sizes=sizes, # size_norm=(0, 100000),
    dashes=True, legend='brief',
)

# Configure plot
g.set(xlabel="Microorganisms",
      ylabel="Antimicrobials",
      aspect="equal")
g.despine(left=True, bottom=True)
g.ax.margins(.02)

# Configure xticks
for label in g.ax.get_xticklabels():
    label.set_rotation(90)

# Configure legend
for artist in g.legend.legendHandles:
    artist.set_edgecolor(".7")
    artist.set_linewidth(1.0)

# Set suptitle
plt.suptitle('Antibiogram (with frequency)', fontsize=12)

# Add grid lines.
#plt.grid(linestyle='-', linewidth=0.5, color='.7')

# Tight layout
plt.tight_layout()

# ----------------------------------
# Plotting a useless piece of art!
# ----------------------------------
# Plot piece of art
g = sns.relplot(data=matrix, x='SPECIE',
    y='ANTIBIOTIC', hue="sari", size="freq",
    palette="Reds", hue_norm=(0, 1),
    linewidth=0.5, kind='line',
    height=10, sizes=sizes)

# Configure plot
g.set(xlabel="", ylabel="",
      title='Artist: Bernard Hernandez \n '
            'Collection: Through the (AM) resistance glass \n '
            'Exhibition: The fight for our lives \n'
            'Location: Tate-Modern',
      aspect="equal")
g.despine(left=True, bottom=True)
g.ax.margins(.02)

# Configure xticks
for label in g.ax.get_xticklabels():
    label.set_rotation(90)

# Configure legend
for artist in g.legend.legendHandles:
    artist.set_linewidth(0.5)

# Show
plt.show()
