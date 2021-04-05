"""
Index - SARI
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
from pyamr.core.sari import SARI

# Set matplotlib
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 9


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

# ---------------------
# Create data
# ---------------------
# Create data
data = [
    ['2021-01-01', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-01-03', 'BLDCUL', 'ECOL', 'AAUG', 'sensitive'],
    ['2021-01-03', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2021-01-04', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],

    ['2021-01-01', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-02', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-03', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],
    ['2021-01-03', 'BLDCUL', 'ECOL', 'ACIP', 'resistant'],
    ['2021-01-04', 'BLDCUL', 'ECOL', 'ACIP', 'sensitive'],

    ['2021-01-01', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-01', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-02', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-02', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-08', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-09', 'BLDCUL', 'SAUR', 'ACIP', 'resistant'],

    ['2021-01-12', 'URICUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-12', 'URICUL', 'SAUR', 'ACIP', 'intermediate'],
    ['2021-01-13', 'URICUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-13', 'URICUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-14', 'URICUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-14', 'URICUL', 'SAUR', 'ACIP', 'resistant'],
    ['2021-01-15', 'URICUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-15', 'URICUL', 'SAUR', 'ACIP', 'sensitive'],
    ['2021-01-16', 'URICUL', 'SAUR', 'ACIP', 'intermediate'],
    ['2021-01-16', 'URICUL', 'SAUR', 'ACIP', 'intermediate'],
]


data = pd.DataFrame(data,
    columns=['DATE',
             'SPECIMEN',
             'MICROORGANISM',
             'ANTIMICROBIAL',
             'SENSITIVITY'])


# Create SARI instance
sari = SARI(groupby=['SPECIMEN',
                     'MICROORGANISM',
                     'ANTIMICROBIAL',
                     'SENSITIVITY'])

# Compute SARI overall
sari_overall = sari.compute(data,
    return_frequencies=False)

# Compute SARI temporal (ITI)
sari_iti = sari.compute(data, shift='1D',
    period='1D', cdate='DATE')

# Compute SARI temporal (OTI)
sari_oti = sari.compute(data, shift='1D',
    period='2D', cdate='DATE')

# Show
print("\nSARI (overall):")
print(sari_overall)
print("\nSARI (iti):")
print(sari_iti)
print("\nSARI (oti):")
print(sari_oti)










"""

Old code


# -------------------------
# Create frequency instance
# -------------------------
# Create instance
freq = Frequency(column_antibiotic='antibioticCode',
                 column_organism='organismCode',
                 column_date='dateReceived',
                 column_outcome='sensitivity')

# Compute frequencies daily
daily = freq.compute(data, strategy='ITI',
                     by_category='pairs',
                     fs='1D')

# Compute frequencies monthly
monthly = freq.compute(data, strategy='ITI',
                       by_category='pairs',
                       fs='1M')

# Compute frequencies overlapping
#oti_1 = freq.compute(data, strategy='OTI',
#                     by_category='pairs',
#                     wshift='1D',
#                     wsize=90)

# -------------------------
# Create sari instance
# -------------------------
# Create instance
sari_daily = SARI(strategy='hard').compute(daily)
sari_monthly = SARI(strategy='hard').compute(monthly)
#sari_oti_1 = SARI(strategy='hard').compute(oti_1)

# -------
# Plot
# -------
# Show comparison for each pair
f, axes = plt.subplots(4, 1, figsize=(15, 8))

# Flatten axes
axes = axes.flatten()

# Plot ITI (monthly)
for i, (pair, group) in enumerate(sari_daily.groupby(level=[0, 1])):
    group.index = group.index.droplevel([0, 1])
    group['sari'].plot(marker='o', ms=3, label=pair,
                       linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
                       ax=axes[0])

# Plot ITI (monthly)
for i, (pair, group) in enumerate(sari_monthly.groupby(level=[0, 1])):
    group.index = group.index.droplevel([0, 1])
    group['sari'].plot(marker='o', ms=3, label=pair,
                       linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
                       ax=axes[1])

# Plot OTI (daily with size 30)
#for i, (pair, group) in enumerate(sari_oti_1.groupby(level=[0, 1])):
#    group.index = group.index.droplevel([0, 1])
#    group['sari'].plot(marker='o', ms=3, label=pair,
#                       linewidth=0.5, markeredgecolor='k', markeredgewidth=0.3,
#                       ax=axes[2])

# Set legend
for ax in axes:
    ax.legend()
    ax.set_xlabel('')
    ax.grid(True)

# Set titles
axes[0].set_ylabel('Daily')
axes[1].set_ylabel('Monthly')
axes[2].set_ylabel('OTI(1D,90)')

# Despine
sns.despine(bottom=True, left=True)

# Set title
plt.suptitle("SARI (Single Antibiotic Resistance Index)")

# Show
plt.show()
"""