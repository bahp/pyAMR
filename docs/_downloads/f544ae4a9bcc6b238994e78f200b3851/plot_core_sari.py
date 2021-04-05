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