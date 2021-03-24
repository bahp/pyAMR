"""
SARI - Antibiogram
------------------

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
# Path
path = '../../pyamr/datasets/microbiology/susceptibility.csv'

# Columns
usecols = ['dateReceived',
           'labNumber',
           'patNumber',
           'orderName',
           'orderCode',
           'organismName',
           'organismCode',
           'antibioticName',
           'antibioticCode',
           'sensitivity']

# Load data
data = pd.read_csv(path, usecols=usecols,
    parse_dates=['dateReceived'])

# Clean
data = data.drop_duplicates()

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.columns)


# -------------------------------------------
# Compute Freq and SARI
# -------------------------------------------
# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
              column_organism='organismCode',
              column_date='dateReceived',
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
f, ax = plt.subplots(1, 1, figsize=(18, 11))

# Create colormap
cmap = sns.color_palette("Reds", desat=0.5, n_colors=10)

# Plot
ax = sns.heatmap(data=matrix, annot=True, fmt=".0f",
    annot_kws={'fontsize': 'small'}, cmap=cmap,
    linewidth=0.5, vmin=0, vmax=100, ax=ax,
    xticklabels=1, yticklabels=1)

# Add title
plt.suptitle("Antibiogram", fontsize='xx-large')

# Tight layout
plt.tight_layout()
plt.subplots_adjust(right=1.05)