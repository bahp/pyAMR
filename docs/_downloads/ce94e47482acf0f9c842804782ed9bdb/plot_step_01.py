"""
Step 01 - Loading data
============================

.. note: Done quickly, needs review.

.. todo:
    1. Load data
    2. Plot summary
    3. Compute SARI
    4.

"""
# Libraries
import pandas as pd


# -------------------------------------------
# Load data
# -------------------------------------------
# Path
path = '../../../pyamr/datasets/other/susceptibility.csv'

# Load data
data = pd.read_csv(path,
    parse_dates=['dateReceived'])

# Clean
data = data.drop_duplicates()

# Show
print("\nData:")
print(data)
print("\nColumns")
print(data.columns)

# -------------------------------------------
# Show a brief description
# -------------------------------------------


#######################################################################
# Compute the frequency...


# -------------------------------------------
# Compute Freq
# -------------------------------------------
# Libraries
from pyamr.core.freq import Frequency

# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
                 column_organism='organismCode',
                 column_date='dateReceived',
                 column_outcome='sensitivity')

# Compute frequencies monthly
monthly = freq.compute(data, strategy='ITI',
                             by_category='pairs',
                             fs='1M')
# Add freq
monthly['freq'] = monthly.sum(axis=1)

# Show
print("\nFreqs:")
print(monthly)

# Plot
# .. todo: Use bar plot or any other library to plot
#          the frequency in time. Ideally with bars
#          where x-axis is the time and y-axi is the
#          freq. Avoid too many x-labels, keep just
#          years?

#######################################################################
# It can be computed with different strategies...
#
#  - hard ..
#  - soft ..
#  - define your own...


# -------------------------------------------
# Compute SARI
# -------------------------------------------
# Libraries
from pyamr.core.sari import SARI

# Compute SARI
sari = SARI(strategy='hard').compute(monthly)

# Show
print("\nFreqs:")
print(sari)

# Plot
# .. todo: Use bar plot or any other library to plot
#          the frequency in time. Ideally with bars
#          where x-axis is the time and y-axi is the
#          freq. Avoid too many x-labels, keep just
#          years?



"""
summary = data.agg(
    norganisms=('organismCode', 'nunique'),
    nantibiotics=('antibioticCode', 'nunique'),
    ncultures=('orderCode', 'nunique'),
    ntests=('labNumber', 'nunique')
)

print(summary)

print(data.nunique())


print(len(data.groupby(['organismCode', 'antibioticCode'])))
print(data.shape[0])

summary = pd.DataFrame


#from analysis.microbiology.statistics.frequency import Frequency

# -----------------------------------------------------------------------------
#                                 CONSTANTS
# -----------------------------------------------------------------------------
# Paths
fname_tests = "freq_tests_pairs_year"
fname_isola = "freq_isolates_pairs_year"
fpath_tests = "../../results/microbiology/frequencies/%s.csv" % fname_tests
fpath_isola = "../../results/microbiology/frequencies/%s.csv" % fname_isola

# Object
freq = Frequency()

# Read data
dff_tests = freq.load(fpath_tests)
dff_isola = freq.load(fpath_isola)
dff_reset = dff_tests.reset_index()

# Basic dataframe.
# IMPORTANT. Note that isolates refer to a single infectious organism which
# is tested against many different anttibiotics. Hence the only way the sum
# refers to isolate is by grouping the laboratory tests by infectious
# organisms.
dfy = pd.DataFrame()
dfy['Tests'] = dff_tests['freq_ris'].groupby(level=[0]).sum()
dfy['Isolates'] = dff_isola['freq'].groupby(level=[0]).sum()
dfy['Tests/Isolates'] = dfy['Tests'].div(dfy['Isolates'])
dfy['Antibiotics'] = dff_reset.groupby('dateReceived').antibioticCode.nunique()
dfy['Organisms'] = dff_reset.groupby('dateReceived').organismCode.nunique()

# Fill last row.
dfy.loc['Total',:] = np.nan
dfy.loc['Total','Tests'] = dfy['Tests'].sum(axis=0)
dfy.loc['Total','Isolates'] = dfy['Isolates'].sum(axis=0)
dfy.loc['Total','Tests/Isolates'] = dfy['Tests/Isolates'].mean()
dfy.loc['Total','Antibiotics'] = dff_reset.antibioticCode.nunique()
dfy.loc['Total','Organisms'] = dff_reset.organismCode.nunique()

# Print dataframe.
print("\n\n")
print("Pandas:")
print("-------")
print(dfy)

# Print dataframe latex format.
print("\n\n")
print("Latex:")
print("-------")
print(dfy.to_latex())

#print dff_isola.head(10)
import sys
sys.exit()
"""