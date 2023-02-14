"""
Frequency counts
==========================================
"""

"""
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
"""