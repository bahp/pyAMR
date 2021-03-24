"""
Index - Frequency
============================

.. warning::
        - Improve visualization.
        - Create further examples with temporal visualization.
        - Create further examples with general heatmap.
        - Create further examples with animation?
"""


# Import libraries
import sys
import glob
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import specific libraries
from pyamr.core.freq import Frequency

# Configure seaborn style (context=talk)
sns.set(style="white")

# Set matplotlib
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 9

# -----------------------
# Load data
# -----------------------
# Path
# Path
path = '../../../pyamr/datasets/microbiology/susceptibility.csv'

# Load all files
data = pd.read_csv(path,
    parse_dates=['dateReceived'],
    low_memory=False)

# -------------------------
# Main
# -------------------------
# Keep only relevant columns
#data = data[['antibioticCode',
#             'organismCode',
#             'dateReceived',
#             'sensitivity']]


# .. note: To reduce computing time and to be able
#          to plot the results we are selecting only
#          one (organism, antimicrobial) pair.

# Selected
orgs = ['ECOL', 'PAER']
abxs = ['ATAZ', 'ATRI', 'AGEN', 'AAUG']

# Filter for two examples
is_org = data['organismCode'].isin(orgs)
is_abx = data['antibioticCode'].isin(abxs)
data = data[is_org & is_abx]

# -------------------------
# Create frequency instance
# -------------------------
# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
                 column_organism='organismCode',
                 column_date='dateReceived',
                 column_outcome='sensitivity')

# ------------------------
# Examples compute overall
# ------------------------
# Compute pairs
pairs = freq.compute(data, by_category='pairs')

# Compute antibiotics
antibiotics = freq.compute(data, by_category='antibiotics')

# Compute organisms
organisms = freq.compute(data, by_category='organisms')

# Show
print("\n")
print("-" * 80)
print("Show OVERALL frequencies:")
print("-" * 80)
print("\nPairs:")
print(pairs)
print("\nAntibiotics:")
print(antibiotics)
print("\nOrganisms:")
print(organisms)

# -------------------------------------------
# Examples compute independent time intervals
# -------------------------------------------
# Examples compute ITI
daily = freq.compute(data, strategy='ITI',
                     by_category='pairs',
                     fs='1D')

monthly = freq.compute(data, strategy='ITI',
                       by_category='pairs',
                       fs='1M')

# Show
print("\n")
print("-" * 80)
print("Show TEMPORAL frequencies:")
print("-" * 80)
print("\nDaily:")
print(daily)
print("\nMonthly:")
print(monthly)

# -------------------------------------------
# Examples compute overlapping time intervals
# -------------------------------------------
"""
.. note: Not working! Fix!

# Examples compute OTI (daily)
oti_1 = freq.compute(data, strategy='OTI',
                     by_category='pairs',
                     wshift='1D',
                     wsize=5)

# Examples compute OTI (monthly)
oti_2 = freq.compute(data, strategy='OTI',
                     by_category='pairs',
                     wshift='1M',
                     wsize=2)
"""

# ----------------
# Plot
# ----------------
# Show comparison for each pair
f, axes = plt.subplots(4, 1, figsize=(15, 8))

# Flatten axes
axes = axes.flatten()

# Plot ITI (daily)
for i, (pair, group) in enumerate(daily.groupby(level=[0, 1])):
    group.index = group.index.droplevel([0, 1])
    group.sum(axis=1).plot(marker='o', ms=3, label=pair,
        linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
        ax=axes[0])

# Plot ITI (monthly)
for i, (pair, group) in enumerate(monthly.groupby(level=[0, 1])):
    group.index = group.index.droplevel([0, 1])
    group.sum(axis=1).plot(marker='o', ms=3, label=pair,
          linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
          ax=axes[1])
"""
.. note: Belongs to previously commented part

# Plot OTI
for i, (pair, group) in enumerate(oti_1.groupby(level=[0, 1])):
    group.index = group.index.droplevel([0, 1])
    group.sum(axis=1).plot(marker='o', ms=3, label=pair,
                           linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
                           ax=axes[2])

# Plot OTI
for i, (pair, group) in enumerate(oti_2.groupby(level=[0, 1])):
    group.index = group.index.droplevel([0, 1])
    group.sum(axis=1).plot(marker='o', ms=3, label=pair,
                           linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
                           ax=axes[3])
"""

# Set legend
for ax in axes:
    ax.legend()
    ax.set_xlabel('')
    ax.grid(True)

# Set titles
axes[0].set_ylabel('Daily')
axes[1].set_ylabel('Monthly')
axes[2].set_ylabel('OTI(1D,5)')
axes[3].set_ylabel('OTI(1M,2)')

# Despine
sns.despine(bottom=True, left=True)

# Set title
plt.suptitle("Frequency (daily, monthly and overlapping intervals)")

# Show
plt.show()