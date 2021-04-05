"""
SART - Spectrum (gram type)
---------------------------

.. todo: Simplify and explain
"""

import sys
import glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.core.sari import SARI
from pyamr.core.asai import ASAI
from pyamr.datasets.load import load_data_nhs
from pyamr.datasets.registries import MicroorganismRegistry
from pyamr.utils.plot import scalar_colormap

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
    .specimen_code.value_counts(normalize=True) \
    .sort_values(ascending=False)

# Filter most frequent specimens
data = data[data.specimen_code.isin( \
    specimen_code_count.index.values[:5])]

# -------------------
# Compute SARI
# -------------------
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

# ------------------------------
# Include registry information
# ------------------------------
# Load registry
mreg = MicroorganismRegistry()

# Format sari dataframe
dataframe = sari_overall.copy(deep=True)
dataframe = dataframe.reset_index()

# Create genus and species
dataframe[['genus', 'species']] = \
    dataframe.microorganism_name \
        .str.capitalize() \
        .str.split(expand=True, n=1)

# Combine with registry information
dataframe = mreg.combine(dataframe)

# Fill missing gram stain
dataframe.gram_stain = dataframe.gram_stain.fillna('u')

# -------------------------------
# Compute ASAI
# -------------------------------
# Create asai instance
asai = ASAI(column_genus='genus',
            column_specie='species',
            column_resistance='sari',
            column_frequency='freq')

# Compute
scores = asai.compute(dataframe,
    groupby=['specimen_code',
             'antimicrobial_name',
             'gram_stain'],
    weights='uniform',
    threshold=0.5,
    min_freq=0)

# Stack
scores = scores.unstack()

# .. note: In order to sort the scores we need to compute metrics
#          that combine the different subcategories (e.g. gram-negative
#          and gram-positive). Two possible options are: (i) use the
#          gmean or (ii) the width.
# Measures
scores['width'] = np.abs(scores['ASAI_SCORE'].sum(axis=1))
scores['gmean'] = np.sqrt(scores['ASAI_SCORE'].product(axis=1))

# Show
print("\nASAI (overall):")
print(scores)


# -------------------------------------------
# Plot
# -------------------------------------------
# Reset
scores = scores.reset_index()

# Loop
for specimen, df in scores.groupby(by='specimen_code'):

    # Sort
    df = df.sort_values(by='width', ascending=False)

    # Show
    print("\n\nASAI (%s)" % specimen)
    print(df)

    # Variables to plot.
    x = df.antimicrobial_name
    y_n = df['ASAI_SCORE']['n'].values
    y_p = df['ASAI_SCORE']['p'].values

    # Constants
    colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
    colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)

    # ----------
    # Example
    # ----------
    # This example shows an stacked figure using more than two categories.
    # For instance, it uses gram-positive, gram-negative and gram-unknown.
    # All the indexes go within the range [0,1].
    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(5, 6))

    # Plot
    sns.barplot(x=y_p, y=x, palette=colormap_p, ax=ax, orient='h',
        saturation=0.5, label='Gram-positive')
    sns.barplot(x=-y_n, y=x, palette=colormap_n, ax=ax, orient='h',
        saturation=0.5, label='Gram-negative')

    # Configure
    sns.despine(bottom=True)

    # Format figure
    plt.subplots_adjust(wspace=0.0, hspace=0.0)

    # Set x-axis
    ax.set_xlim([-1, 1])

    # Adjust
    plt.legend(loc=8)
    plt.suptitle(specimen)
    plt.tight_layout()

# Show
plt.show()
