"""
Drug Resistance Index (``DRI``)
==================================

The Drug Resistance Index or ``DRI`` measures changes through time in the proportion
of disease-causing pathogens that are resistant to the antibiotics commonly used to
treat them. The annual percentage change in the ``DRI`` is a measure of the rate of
depletion of antibiotic effectiveness.

Since antibiotic use may change over time in response to changing levels of
antibiotic resistance, we compare trends in the index with the counterfactual
case, where antibiotic use remains fixed to a baseline year. A static-use ``DRI``
allows assessment of the extent to which drug use has adapted in response to
resistance and the burden that this resistance would have caused if antibiotic
use patterns had not changed. Changing antibiotic use patterns over time may
mitigate the burden of antibiotic resistance. To incorporate changing trends
in antibiotic use, we also construct an adaptive version of the ``DRI``.

For more information see: :py:mod:`pyamr.core.dri.DRI`
"""
# Libraries
import pandas as pd

# ----------------------------------
# Create data
# ----------------------------------
# Define susceptibility test records
susceptibility_records = [
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

# Define prescription test records
prescription_records = [
    ['2021-01-01', 'PATIENT_1', 'AAUG', 150],
    ['2021-01-02', 'PATIENT_1', 'AAUG', 221],
    ['2021-01-03', 'PATIENT_1', 'AAUG', 152],

    ['2021-01-01', 'PATIENT_2', 'AAUG', 254],
    ['2021-01-02', 'PATIENT_2', 'AAUG', 325],
    ['2021-01-03', 'PATIENT_2', 'AAUG', 356],

    ['2021-01-01', 'PATIENT_3', 'ACIP', 457],
    ['2021-01-02', 'PATIENT_3', 'ACIP', 428],
    ['2021-01-03', 'PATIENT_3', 'ACIP', 459],

    ['2021-01-01', 'PATIENT_4', 'ACIP', 50],
    ['2021-01-02', 'PATIENT_4', 'ACIP', 50],
    ['2021-01-03', 'PATIENT_4', 'ACIP', 50],

]

# Create DataFrames
susceptibility = pd.DataFrame(susceptibility_records,
                              columns=['DATE',
                                       'SPECIMEN',
                                       'MICROORGANISM',
                                       'ANTIMICROBIAL',
                                       'SENSITIVITY'])

prescriptions = pd.DataFrame(prescription_records,
                             columns=['DATE',
                                      'PATIENT',
                                      'DRUG',
                                      'DOSE'])

# Format dates
susceptibility.DATE = pd.to_datetime(susceptibility.DATE)
prescriptions.DATE = pd.to_datetime(prescriptions.DATE)

#%%
# Lets see the susceptibility test records
susceptibility.head(5)

#%%
# Lets see the prescription records
prescriptions.head(5)


#%%
# Lets create the summary table and compute the ``DRI``

# ------------------------
# Compute summary table
# ------------------------
# Libraries
from pyamr.core.sari import SARI

# Create sari instance
sari = SARI(groupby=['DATE',
                     'SPECIMEN',
                     'MICROORGANISM',
                     'ANTIMICROBIAL',
                     'SENSITIVITY'])

# Compute susceptibility summary table
smmry1 = sari.compute(susceptibility,
                      return_frequencies=False)

# Compute prescriptions summary table.
smmry2 = prescriptions \
    .groupby(by=['DATE', 'DRUG']) \
    .DOSE.sum().rename('use')

# Combine both summary tables
smmry = smmry1.reset_index().merge(
    smmry2.reset_index(), how='inner',
    left_on=['DATE', 'ANTIMICROBIAL'],
    right_on=['DATE', 'DRUG']
)

# -------------------------
# Compute DRI
# -------------------------
# Librarie
from pyamr.core.dri import DRI

# Instance
obj = DRI(
    column_resistance='sari',
    column_usage='use'
)

# Compute DRI overall
dri1 = obj.compute(smmry)

# Compute DRI
dri2 = obj.compute(smmry,
    groupby=['SPECIMEN'])

# Compute DRI
dri3 = obj.compute(smmry,
    groupby=['MICROORGANISM'])

# Compute DRI
dri4 = obj.compute(smmry,
    groupby=['MICROORGANISM', 'ANTIMICROBIAL'])

# Compute DRI
dri5 = obj.compute(smmry,
    groupby=['DATE'],
    return_usage=True)

# Compute DRI
dri6 = obj.compute(smmry,
    groupby=['DATE', 'MICROORGANISM'],
    return_usage=True)

# Compute DRI
dri7 = obj.compute(smmry,
    groupby=['DATE', 'MICROORGANISM', 'ANTIMICROBIAL'],
    return_usage=True,
    return_complete=True)

# Compute DRI (return all elements of summary table).
dri8 = obj.compute(smmry,
    groupby=['MICROORGANISM'],
    return_complete=True)

# Show
print("\nDRI (1):")
print(dri1)
print("\nDRI (2):")
print(dri2)
print("\nDRI (3):")
print(dri3)
print("\nDRI (4):")
print(dri4)
print("\nDRI (5):")
print(dri5)
print("\nDRI (6):")
print(dri6)
print("\nDRI (7):")
print(dri7)
print("\nDRI (8):")
print(dri8)

#%%
# Lets see the summary table
smmry

#%%
# Lets see the sample ``4``.
dri4.to_frame().round(decimals=3)

#%%
# Lets see the sample ``7`` with ``return_components=True``.
dri7.rename(columns={
    'MICROORGANISM': 'ORG',
    'ANTIMICROBIAL': 'ABX'
}).round(decimals=3)

#%%
# Lets see the sample ``8`` with ``return_complete=True``.
dri8.rename(columns={
    'MICROORGANISM': 'ORG',
    'ANTIMICROBIAL': 'ABX'
}).round(decimals=3)

#########################################################################
# Lets compute the ``fixed`` index for comparison

# --------------------------------------------
# Compute DRI fixed
# --------------------------------------------
# Compute prescriptions on t0.
use_t0 = prescriptions \
    .groupby(by=['DATE', 'DRUG']) \
    .DOSE.sum().rename('use') \
    .to_frame().reset_index() \
    .groupby('DRUG').use.first()

# Add to summary table
smmry = smmry.assign(use_t0=smmry.DRUG.map(use_t0))

# Define groupby
groupby = [
    'DATE',
    'MICROORGANISM'
]

# Compute DRI
dri9a = obj.compute(smmry,
                    groupby=groupby,
                    return_usage=True)

# Compute DRI using new USE
dri9b = obj.compute(smmry,
                    groupby=groupby,
                    return_usage=True,
                    column_usage='use_t0')

# aux = pd.concat([dri9a, dri9b], axis=1)
aux = dri9a.merge(dri9b,
                  left_index=True, right_index=True,
                  suffixes=['', '_fixed'])

# Concatenate (series)
# aux = pd.concat([
#    dri9a.rename('dri'),
#    dri9b.rename('dri_fixed')], axis=1)

# Show
print("\n\n")
print("\nSummary (variable):")
print(smmry)
print("\nDRI (9):")
print(aux)


#%%
# Lets see the new summary (added old use column <old> for comparison)
smmry

#%%
# Lets see the results for both fixed and dynamic.
aux

#%%
# Lets visualise it

# --------------------------
# Plot
# --------------------------
# Libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Filter
stacked = aux[['dri', 'dri_fixed']].stack().reset_index()

# Display using relplot
sns.relplot(data=stacked,
    x='DATE', y=0, row='MICROORGANISM', hue='level_2',
    # hue='event', style='event', col='region', palette='palette',
    #height=4, aspect=2.0,
    kind='line', linewidth=1.00, markersize=6, marker='o'
)

# Show
plt.show()


################################################################################
# .. note:: The summary table for the prescriptions data computed above
#           aggregated the values in the column ``dose`` which indicates the
#           specific dose delivered to the patient. In many scenarios, this
#           information might not be available or dosage units might vary (e.g.
#           mg or ml). A possible workaround is to count the number of
#           entries in the prescriptions data by using ``DOSE.count()`` but
#           this workaround should be use with caution.
