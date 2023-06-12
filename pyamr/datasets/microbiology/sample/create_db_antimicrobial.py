# Import pandas
import pandas as pd
import numpy as np

# -------------------------------------------------
# Constants
# -------------------------------------------------
remove = {
    '\([^)]*\)': '', # Remove everything between ()
    '\s{2,}': ' ',   # Remove duplicated spaces
}

replace = {
    'antimicrobial_code': {
        'AAUGU': 'AAUG'
    },
    'antimicrobial_name': {

    }
}

category = {
    'AAMPC': None,
    'AAMI':	'aminoglycosides',
    'AAMO':	'aminopenicillins',
    'AAMPH': None,
    'AAND': None,
    'AAUG': None,
    'AAZI':	'macrolides',
    'AAZT':	'monobactams',
    'ABAC':	'polypeptides',
    'ACPO': None,
    'ACAS': None,
    'ACIX':	'cephalosporins',
    'ACTX':	'cephalosporins',
    'ACXT':	'cephalosporins',
    'ACAZ':	'cephalosporins',
    'ACONE': 'cephalosporins',
    'ACXM': 'cephalosporins',
    'ACELX': 'cephalosporins',
    'ACHL': None,
    'ACIP':	'fluoroquinolones',
    'ACLA':	'macrolides',
    'ACLI':	'macrolides',
    'ACOL':	'polypeptides',
    'ACOT':	'sulfonamides',
    'ADAP': None,
    'AERT':	'meropenems',
    'AESBL': None,
    'AERY':	'macrolides',
    'AMET':	'penicillins',
    'AFLUZ': None,
    'AFLUC'	: None,
    'AFOS'	: None,
    'AFUS'	: None,
    'AGEN':	'aminoglycosides',
    'AGEN':	'aminoglycosides',
    'AIMP':	'meropenems',
    'AITR'	: None,
    'ALEV'	:'fluoroquinolones',
    'ALIN':	'oxazolidinones',
    'AMLS': None,
    'AMEC':	'penicillins',
    'AMER':	'meropenems',
    'AMTZ':	'nitroimidazoles',
    'AMF':  None,
    'AMOX':	'fluoroquinolones',
    'AMUP': None,
    'ANAL':	'fluoroquinolones',
    'ANEO':	'aminoglycosides',
    'ANIT': None,
    'ANOV':	'aminocoumarin',
    'AOFL':	'fluoroquinolones',
    'AOPT': None,
    'AOXA':	'penicillins',
    'APEF': None,
    'APEN':	'penicillins',
    'APCZ': None,
    'ARIF': None,
    'ASEP': None,
    'ASYN': None,
    'ATAZ': None,
    'ATEI':	'glycopeptide',
    'ATEM':	'penicillins',
    'ATET':	'tetracyclines',
    'ATIG':	'tetracyclines',
    'ATOB':	'aminoglycosides',
    'ATRI': None,
    'AVAN':	'glycopeptide',
    'AVOR': None}


# -----------------------------------------
# Read csv
# -----------------------------------------
# Read csv
data = pd.read_csv('./outputs/susceptibility.csv',
    usecols=['antimicrobial_code',
             'antimicrobial_name'])

# Drop duplicates
data = data.drop_duplicates( \
    subset=['antimicrobial_code',
            'antimicrobial_name'])

# Replace
data = data.replace(replace)

# --------------------
# Format antibiotic name
# --------------------
# Format (lower)
data.antimicrobial_name = data.antimicrobial_name.str.lower()

# Do str replacements
for k, v in remove.items():
    data.antimicrobial_name = \
        data.antimicrobial_name.str.replace(k, v)

# Format (strip)
data.antimicrobial_name = \
    data.antimicrobial_name.str.strip()

# Create auxiliary series
#data.antimicrobial_name = \
#    data.antimicrobial_name.replace(replace_antimicrobial)

# Drop duplicates
data = data.drop_duplicates()

# --------------------------------------------
# Report duplicated
# --------------------------------------------
# Find duplicates
dup = data.set_index('antimicrobial_code') \
    .index.duplicated(keep=False)

# Show
print("\nDuplicates:")
print(data[dup])
print("\nCounts:")
print(data.nunique())

if dup.any():
    print("\nERROR: There are duplicate values in the dataframe. \n"
          "The 'db_antimicrobials.csv' file has therefore not \n"
          "been saved. Please correct the issues and run again.")
    import sys
    sys.exit()

# --------------------------------------------
# Create the categories
# --------------------------------------------
# Initialise gram type
data['antimicrobial_class'] = None

# Loop setting classes
for e in set(category.values()):
    # Get codes
    codes = [k for k,v in category.items() if v==e]
    # Get idxs
    idxs = data.antimicrobial_code.isin(codes)
    # Fill gram type
    data.loc[idxs, 'antimicrobial_class'] = e

# Drop duplicates
data = data.drop_duplicates()
data = data.sort_values('antimicrobial_name')
data = data.reset_index(drop=True)

# Show
print("\nCounts:")
print(data.nunique())

# --------------------------------------------
# Save
# --------------------------------------------
# Save
data.to_csv('./outputs/db_antimicrobials.csv', index=False)