"""
SARI - Antibiogram
------------------

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
from pyamr.graphics.antibiogram import Antibiogram

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


# -------------------------------
# Load data
# -------------------------------
# Load
dataframe = pd.read_csv('../_data/data-antibiogram.csv')

# Show data
print("Data input:")
print(dataframe.head(10))

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
antibiogram.plot(genera=['staphylococcus',
                         'klebsiella',
                         'streptococcus',
                         'enterococcus'],
                 method='weighted',
                 metric='euclidean',
                 figsize=(15,8))

# Show
plt.show()
