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
from pyamr.core.freq import Frequency
from pyamr.core.sari import SARI
from pyamr.core.asai import ASAI
from pyamr.datasets.load import load_data_nhs

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
#                             Methods
# --------------------------------------------------------------------
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


# --------------------------------------------------------------------
#                               Main
# --------------------------------------------------------------------
# Load data
data, antibiotics, organisms = load_data_nhs()

# Count records per specimen code
specimen_code_count = data.specimen_code.value_counts()

# Filter most frequent specimens
data = data[data.specimen_code.isin( \
    specimen_code_count.index.values[:5])]

# Loop for each specimen
for specimen_code, df in data.groupby(by='specimen_code'):
    # ----------------------------
    # Compute frequencies and SARI
    # ----------------------------
    # Create instance
    freq = Frequency(column_antibiotic='antimicrobial_code',
                     column_organism='microorganism_code',
                     column_date='date_received',
                     column_outcome='sensitivity')

    # Compute frequencies overall
    freq_overall = freq.compute(df, strategy='overall',
                                by_category='pairs')

    # Compute sari
    sari_overall = SARI(strategy='medium').compute(freq_overall)

    # ------------------------
    # Format dataframe
    # -------------------------
    # Create mappers
    abx_map = create_mapper(antibiotics, 'antimicrobial_code', 'category')
    org_map = create_mapper(organisms, 'microorganism_code', 'genus')
    grm_map = create_mapper(organisms, 'microorganism_code', 'gram_stain')
    name_map = create_mapper(antibiotics, 'antimicrobial_code', 'name')

    # Copy dataframe
    dataframe = sari_overall.copy(deep=True)
    dataframe = dataframe.reset_index()

    # Include categories
    dataframe['category'] = dataframe['ANTIBIOTIC'].map(abx_map)
    dataframe['genus'] = dataframe['SPECIE'].map(org_map)
    dataframe['gram'] = dataframe['SPECIE'].map(grm_map)
    dataframe['ANTIBIOTIC'] = dataframe.ANTIBIOTIC.map(name_map)

    # Empty grams are a new category (unknown - u)
    dataframe.gram = dataframe.gram.fillna('u')

    # ------------------------
    # Compute spectrum index
    # ------------------------
    # Create antimicrobial spectrum of activity instance
    asai = ASAI(weights='uniform', threshold=0.05,
                column_genus='genus',
                column_specie='SPECIE',
                column_antibiotic='ANTIBIOTIC',
                column_resistance='sari')

    # Compute
    scores = asai.compute(dataframe, by_category='gram')

    # Show scores
    print("\n\nData ASAI (%s):" % specimen_code)
    print(scores.head(10))

    # Sort
    scores = scores.fillna(0.0)
    scores['width'] = np.abs(scores['ASAI_SCORE']['n'] + scores['ASAI_SCORE']['p'])
    scores['gmean'] = np.sqrt(scores['ASAI_SCORE']['n'] * scores['ASAI_SCORE']['p'])
    scores = scores.sort_values(by='gmean', ascending=False)

    # Variables to plot.
    x = scores.index.values
    y_n = scores['ASAI_SCORE']['n'].values
    y_p = scores['ASAI_SCORE']['p'].values

    # Constants
    colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
    colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)

    # ----------
    # Example
    # ----------
    # This example shows a diverging figure using exclusively the gram-positive
    # and gram-negative categories. Note that the gram negative categories has
    # values in the range [-1,0] while the gram-positive category has values
    # within the range [0, 1]
    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(5, 12))

    # Plot
    sns.barplot(x=y_p, y=x, palette=colormap_p, ax=ax, orient='h',
     saturation=0.5, label='Gram-positive')
    sns.barplot(x=-y_n, y=x, palette=colormap_n, ax=ax, orient='h',
     saturation=0.5, label='Gram-negative')

    # Configure
    sns.despine(bottom=True)

    # Show legend.
    plt.legend(loc=8)
    plt.suptitle(specimen_code)
    plt.tight_layout()

# Show
plt.show()