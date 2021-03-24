# Libraries
import glob
import time
import pandas as pd

# Import pyAMR
from pyamr.datasets.clean import clean_clwsql008
from pyamr.datasets.clean import microorganism_gram_type
from pyamr.datasets.clean import antimicrobial_class
from pyamr.datasets.load import make_susceptibility




# ---------------------------------
# Load data
# ---------------------------------
# Define path
path = './raw'

# Load all files
data = pd.concat([ \
    pd.read_csv(f, parse_dates={
        'date_received': ['ReceiveDate', 'ReceiveTime'],
        'date_outcome': ['FinalDate']})
    for f in glob.glob(path + "/*.csv")])

# Clean
data = clean_clwsql008(data)

# Create genus and species
data[['microorganism_genus', 'microorganism_specie']] = \
    data.microorganism_name.str.split(expand=True, n=1)

# Add gram type
data['microorganism_gram_type'] = \
    data.microorganism_code.map(microorganism_gram_type)

# Add antimicrobial class
data['antimicrobial_class'] = \
    data.antimicrobial_code.map(antimicrobial_class)

# ---------
# Anonymise
# ---------
# Create hos_number to id mapper
pid_map =  dict(zip(data.patient_id.unique(), range(data.patient_id.nunique())))

# Include categories
data.patient_id = data.patient_id.map(pid_map)

# Show
print("\nData:")
print(data)
print("\nColumns:")
print(data.columns)

# Find duplicates
nunique_abxs = data[['antimicrobial_code', 'antimicrobial_name']].nunique()
nunique_orgs = data[['microorganism_code', 'microorganism_name']].nunique()

# Show
print("\nUnique (abxs):")
print(nunique_abxs)
print("\nUnique (orgs):")
print(nunique_orgs)

# -----------------------------
# Save
# -----------------------------
# Time
timestr = time.strftime("%Y%m%d-%H%M%S")

# Save
data.to_csv('susceptibility-{0}.csv'.format(timestr), index=False)