"""
SART - by gram type
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
  '9MRSN':'MRSCUL',
  'URINE CULTURE':'URICUL',
  'WOUND CULTURE':'WOUCUL',
  'BLOOD CULTURE':'BLDCUL',
  'SPUTUM CULTURE':'SPTCUL',
  'CSF CULTURE':'CSFCUL',
  'EYE CULTURE':'EYECUL',
  'GENITALCUL':'GENCUL',
  'NEONATAL SCREEN':'NEOCUL',
}

# Interesting columns
usecols = ['dateReceived',
           'labNumber',
           'patNumber',
           'orderCode',
           'organismCode',
           'antibioticCode',
           'sensitivity']

# Path
path = '../../resources/data/nhs/susceptibility/complete/'

# -------------------------
# Main
# -------------------------
# Load all files
data = pd.concat([  \
    pd.read_csv(f, parse_dates=['dateReceived'],
        usecols=usecols, nrows=1000)
            for f in glob.glob(path + "/*.csv")])

# Replace
data.organismCode = \
    data.organismCode.replace(replace_codes)

# Drop duplicates
data = data.drop_duplicates()

# .. note: This is not counting the number of samples of each
#          culture taken, but also includes one row for each
#          antimicrobial tested. To count the number of samples
#          not the keep just one value per <patient, order_code>
# Frequency
freq = data.organismCode.value_counts()

# Porportion
prop = data.organismCode.value_counts(normalize=True)

#data.groupby
#aux = data.organismCode.apply(freq='value_counts')

aux2 = data[['organismCode', 'antibioticCode']] \
    .agg('value_counts').T


print("\nShow:")
print(freq)
print(prop)
print(aux2.sort_index())


# Show
#print("\nData:")
#print(data)


# --------------------
# compute frequencies
# --------------------
# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
                 column_organism='organismCode',
                 column_date='dateReceived',
                 column_outcome='sensitivity')

# Compute frequencies overall
freq_overall = freq.compute(data, strategy='overall', 
                                  by_category='pairs')

freq = freq.compute(data, strategy='overall', by_category='organisms')

print(freq_overall.sum(axis=1).sort_index())

print(freq)