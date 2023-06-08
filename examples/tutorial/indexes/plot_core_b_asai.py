"""
Spectrum of Activity (``ASAI``)
===============================

.. warning:: There is an error in the Figure displayed below. The contribution (cont) value
             for Staphylococcus haemolyticus should be 0 instead of 1/10 because the sari
             index is higher than the threshold (32 > 20) and therefore the antimicrobial
             is not considered effective.

The Antimicrobial Spectrum of Activity Index or ``ASAI`` refers to the range of microbe species that are
susceptible to these agents and therefore can be treated. In general, antimicrobial agents
are classified into broad, intermediate or narrow spectrum. Broad spectrum antimicrobials
are active against both Gram-positive and Gram-negative bacteria. In contrast, narrow
spectrum antimicrobials have limited activity and are effective only against particular
species of bacteria. While these profiles appeared in the mid-1950s, little effort has been
made to define them. Furthermore, such ambiguous labels are overused for different
and even contradictory purposes.

For more information see: :py:mod:`pyamr.core.asai.ASAI`

.. image:: ../../../_static/imgs/index-asai.png
    :width: 600
    :align: center
    :alt: ASAI

"""

# Import libraries
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.core.asai import ASAI
from pyamr.core.asai import asai
from pyamr.datasets.load import fixture
from pyamr.graphics.utils import scalar_colormap

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


# ---------------------
# Create data
# ---------------------
# Load data
dataframe = fixture(name='fixture_04.csv')

# Show
print("Summary:")
print(dataframe)

#%%
# Lets see the dataframe
dataframe

############################################################
#
# Lets use the ASAI object
#

# -------------------------------
# Create antimicrobial spectrum
# -------------------------------
# Create antimicrobial spectrum of activity instance
asai = ASAI(column_genus='GENUS',
            column_specie='SPECIE',
            column_resistance='RESISTANCE',
            column_frequency='FREQUENCY',
            column_threshold='THRESHOLD',
            column_wgenus='W_GENUS',
            column_wspecie='W_SPECIE')

# Compute ASAI with uniform weights
scores1 = asai.compute(dataframe,
    groupby=['ANTIBIOTIC', 'GRAM'],
    weights='uniform',
    threshold=None,
    min_freq=0).unstack()

# compute ASAI with frequency weights
scores2 = asai.compute(dataframe,
    groupby=['ANTIBIOTIC', 'GRAM'],
    weights='frequency',
    threshold=None,
    min_freq=0).unstack()

#%%
# Lets see the ``ASAI`` with ``uniform`` weights
scores1

#%%
# Lets see the ``ASAI`` with ``frequency`` weights
scores2

###############################################################
#
# Lets display the information graphically

def plot_graph_asai(scores):
    """Display ASAI as a horizontal bars
    """
    # Variables to plot.
    x = scores.index.values
    y_n = scores['ASAI_SCORE']['N'].values
    y_p = scores['ASAI_SCORE']['P'].values

    # Constants
    colormap_p = scalar_colormap(y_p, cmap='Blues', vmin=-0.1, vmax=1.1)
    colormap_n = scalar_colormap(y_n, cmap='Reds', vmin=-0.1, vmax=1.1)

    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(8, 0.5))

    # Plot
    sns.barplot(x=y_p, y=x, palette=colormap_p, ax=ax, orient='h',
                saturation=0.5, label='Gram-positive')
    sns.barplot(x=-y_n, y=x, palette=colormap_n, ax=ax, orient='h',
                saturation=0.5, label='Gram-negative')

    # Configure
    sns.despine(bottom=True)

    # Configure
    ax.set_xlim([-1, 1])
    ax.legend(loc='center left')

# -----------------------------
# Plot
# -----------------------------
# Display bar graphs
plot_graph_asai(scores1)
plot_graph_asai(scores2)

# Display
plt.show()