"""
Describe
-------------------

.. todo: Simplify and explain
"""

# Import libraries
import sys
import glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import pyamr
from pyamr.core.freq import Frequency
from pyamr.datasets.load import load_data_nhs
from pyamr.utils.plot import create_mapper

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

# -------------------------
# Constants
# -------------------------
# Replace codes
replace_codes = {
  #'9MRSN': 'MRSCUL',
  #'URINE CULTURE': 'URICUL',
  #'WOUND CULTURE': 'WOUCUL',
  #'BLOOD CULTURE': 'BLDCUL',
  #'SPUTUM CULTURE': 'SPTCUL',
  ##'CSF CULTURE': 'CSFCUL',
  #'EYE CULTURE': 'EYECUL',
  #'GENITALCUL': 'GENCUL',
  #'NEONATAL SCREEN': 'NEOCUL',
}

# ----------------------------------------------------------
#                       Main
# ----------------------------------------------------------
# Load data
data, antibiotics, organisms = load_data_nhs(nrows=1000)

print(data.columns)

# Replace
data.specimen_code = \
    data.specimen_code.replace(replace_codes)

# Drop duplicates
data = data.drop_duplicates()

# The total number of cultures
ncultures = data.laboratory_number.nunique()


# The percentage of each specimen
pspecimens = data \
    .groupby('laboratory_number').head(1) \
    .specimen_code.value_counts(normalize=True) \
    .to_frame().reset_index()

mapper = create_mapper(data, 'specimen_code', 'specimen_name')

pspecimens['specimen_name'] = pspecimens['index'].map(mapper)

print(pspecimens)


# The percentages of each organism
pmicroorganisms = data \
    .microorganism_code \
    .value_counts(normalize=True)

# The percentages of each antimicrobial
pantimicrobials = data \
    .antimicrobial_code \
    .value_counts(normalize=True)

# The percentages of (orgnaism, antimicrobial) pairs
ppairs = data[['microorganism_code', 'antimicrobial_code']]
ppairs = ppairs.value_counts(normalize=True)

# Show
print("\nTotal cultures: %s" % ncultures)
print("\nSpecimens (proportions)")
print(pspecimens.to_string())
print("\nMicroorganisms (proportions)")
print(pmicroorganisms)
print("\nAntimicrobials (proportions)")
print(pantimicrobials)
print("\nPairs (proportions")
print(ppairs)

# --------------------
# Compute Frequencies
# --------------------
# Create instance
freq = Frequency(column_antibiotic='antimicrobial_code',
                 column_organism='microorganism_code',
                 column_date='date_received',
                 column_outcome='sensitivity')

# Compute frequencies overall
freq_pairs = freq.compute(data, strategy='overall',
                                by_category='pairs')

freq_orgs = freq.compute(data, strategy='overall',
                               by_category='organisms')

freq_abxs = freq.compute(data, strategy='overall',
                               by_category='organisms')

print("\n\nFreqs:")
print(freq_pairs)
print("Count")
print(freq_pairs.sum(axis=1).sort_values(ascending=False))



pspecimens.specimen_code.plot(kind='pie', ylabel='')
plt.suptitle('SPECIMEN')

plt.show()