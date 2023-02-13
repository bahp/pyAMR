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
    '9MRSN': 'MRSCUL',
    'URINE CULTURE': 'URICUL',
    'WOUND CULTURE': 'WOUCUL',
    'BLOOD CULTURE': 'BLDCUL',
    'SPUTUM CULTURE': 'SPTCUL',
    'CSF CULTURE': 'CSFCUL',
    'EYE CULTURE': 'EYECUL',
    'GENITALCUL': 'GENCUL',
    'NEONATAL SCREEN': 'NEOCUL',
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
    ['2022-01-03', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],
    ['2022-01-04', 'BLDCUL', 'ECOL', 'AAUG', 'resistant'],

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
    ['2021-02-16', 'URICUL', 'SAUR', 'ACIP', 'intermediate'],
    ['2021-02-16', 'URICUL', 'SAUR', 'ACIP', 'intermediate'],
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
    return_frequencies=True)

# Compute SARI temporal (ITI)
sari_iti = sari.compute(data,
    period='1D', shift='1D', cdate='DATE')

# Compute SARI temporal (OTI)
sari_oti = sari.compute(data,
    period='2D', shift='1D', cdate='DATE')

# Compute SARI temporal (ITI monthly)
sari_monthly = sari.compute(data,
    period='1M', cdate='DATE')

# Compute SARI temporal (ITI year)
sari_yyyy = sari.compute(data,
    period='year', cdate='DATE')

# Show
print("\nSARI (overall):")
print(sari_overall)
print("\nSARI (iti):")
print(sari_iti)
print("\nSARI (oti):")
print(sari_oti)
print("\nSARI (ITI year):")
print(sari_yyyy)
print("\nSARI (ITI monthly):")
print(sari_monthly)

# ------------------------------
# Time series
# ------------------------------
# Library
from pyamr.core.sari import sari

# Create sari
sari_yyyy['sari_h'] = sari(sari_yyyy, strategy='hard')
sari_yyyy['sari_m'] = sari(sari_yyyy, strategy='medium')
sari_yyyy['sari_s'] = sari(sari_yyyy, strategy='soft')

# Create time-series
sari_yyyy_ts = sari_yyyy.unstack(-1) \
    .groupby(level=0, axis=1) \
    .apply(lambda x:
        x.droplevel(level=0, axis=1) \
            .round(decimals=2) \
            .apply(lambda x: x.to_dict(), axis=1))
sari_yyyy_ts = sari_yyyy_ts.add_suffix('_ts')

# Complete DataFrame
complete = sari_overall.join(sari_yyyy_ts)

print("\nComplete (year)")
print(complete)
