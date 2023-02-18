"""
Graphics Antibiogram example
============================
"""

# Libraries
from __future__ import division

# Libraries
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

#
from pyamr.graphics.antibiogram import Antibiogram


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

# -------------------------------------------------------------------------
#                            helper methods
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
#                                main
# -------------------------------------------------------------------------
# Data path.
path = '../../pyamr/fixtures/fixture_antibiogram.csv'

# -------------------------------
# Load data
# -------------------------------
# Load
dataframe = pd.read_csv(path)

# -------------------------------
# Create object
# -------------------------------
# Antibiogram plotter
antibiogram = Antibiogram(column_organism='organismCode',
                          column_antibiotic='antibioticCode',
                          column_genus='specieName',
                          column_category='antibioticClass',
                          column_index='sari')

# Fit antibiogram
antibiogram = antibiogram.fit(dataframe)

# ---------
# Example 1
# ----------
antibiogram.plot(organisms=['ECOL', 'SAUR'], figsize=(15, 3))

# ---------
# Example 2
# ---------
antibiogram.plot(genera=['staphylococcus',
                         'klebsiella',
                         'streptococcus',
                         'enterococcus',
                         'enterobacter'],
                 categories=None,
                 method='weighted',
                 metric='euclidean',
                 figsize=(16, 9))

# Show
plt.show()