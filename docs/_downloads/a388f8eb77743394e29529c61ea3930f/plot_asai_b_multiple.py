"""
``ASAI`` - By gram stain (multiple)
-----------------------------------

"""

# Import libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.core.asai import ASAI
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
# Include gram stain
# ------------------------------
# Libraries
from pyamr.datasets.registries import MicroorganismRegistry

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
dataframe = mreg.combine(dataframe, on='microorganism_name')

# Fill missing gram stain
dataframe.gram_stain = dataframe.gram_stain.fillna('u')


# -------------------------------------------
# Compute ASAI
# -------------------------------------------
# Import specific libraries
from pyamr.core.asai import ASAI

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


# ------------------------
# Methods
# ------------------------
def scalar_colormap(values, cmap, vmin, vmax):
    """This method creates a colormap based on values.

    Parameters
    ----------
    values : array-like
    The values to create the corresponding colors

    cmap : str
    The colormap

    vmin, vmax : float
    The minimum and maximum possible values

    Returns
    -------
    scalar colormap
    """
    # Create scalar mappable
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    # Gete color map
    colormap = sns.color_palette([mapper.to_rgba(i) for i in values])
    # Return
    return colormap


# -------------------------------------------
# Plot
# -------------------------------------------
# Reset
scores = scores.reset_index()

# Count records per specimen
specimen_count = sari_overall \
 .groupby('specimen_code').freq.sum() \
 .sort_values(ascending=False)

# Show
print("\nCultures:")
print(specimen_count)

# Filter
scores = scores[scores.specimen_code\
    .isin(specimen_count.index.values[:5])]

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
    y_u = df['ASAI_SCORE']['u'].values

    # Constants
    colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
    colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)
    colormap_u = scalar_colormap(y_u, cmap='Greens', vmin=-0.1, vmax=1.1)

    # ----------
    # Example
    # ----------
    # This example shows an stacked figure using more than two categories.
    # For instance, it uses gram-positive, gram-negative and gram-unknown.
    # All theindexes go within the range [0,1].
    # Create the figure
    f, axes = plt.subplots(1, 3, figsize=(7, 8))

    # Plot each category
    sns.barplot(x=y_p, y=x, palette=colormap_p, ax=axes[0], orient='h',
      saturation=0.5, label='Gram-positive')
    sns.barplot(x=y_n, y=x, palette=colormap_n, ax=axes[1], orient='h',
      saturation=0.5, label='Gram-negative')
    sns.barplot(x=y_u, y=x, palette=colormap_u, ax=axes[2], orient='h',
      saturation=0.5, label='Gram-unknown')

    # Configure
    sns.despine(bottom=True)

    # Format figure
    plt.subplots_adjust(wspace=0.0, hspace=0.0)

    # Remove yticks
    axes[1].set_yticks([])
    axes[2].set_yticks([])

    # Set title
    axes[0].set_title('Gram-positive')
    axes[1].set_title('Gram-negative')
    axes[2].set_title('Gram-unknown')

    # Set x-axis
    axes[0].set_xlim([0,1.1])
    axes[1].set_xlim([0,1.1])
    axes[2].set_xlim([0,1.1])

    # Remove ylabels
    axes[1].set_ylabel('')
    axes[2].set_ylabel('')

    # Adjust
    plt.tight_layout()

# Show
plt.show()