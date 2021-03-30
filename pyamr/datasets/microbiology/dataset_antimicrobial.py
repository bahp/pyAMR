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

replace_antimicrobial = {}

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
data = pd.read_csv('./susceptibility.csv',
    usecols=['antibioticCode',
             'antibioticName'])

# Rename
data = data.rename(columns={
    'antibioticCode': 'antibiotic_code',
    'antibioticName': 'antibiotic_name'})

# Drop duplicates
data = data.drop_duplicates( \
    subset=['antibiotic_code',
            'antibiotic_name'])

# --------------------
# Format antibiotic name
# --------------------
# .. note: We could also add a display name to indicate
#          how the values should be displayed. Specially
#          for those that have been re-arranged to match
#          the genus then specia pattern.
#
# .. note: First we format the organism name. We convert
#          al values to lower case, then we remove some
#          information (see dictionary remove) and then
#          we strip any remaining spaces.
# Format (lower)
data.antibiotic_name = data.antibiotic_name.str.lower()

# Do str replacements
for k, v in remove.items():
    data.antibiotic_name = \
        data.antibiotic_name.str.replace(k, v)

# Format (strip)
data.antibiotic_name = \
    data.antibiotic_name.str.strip()

# Create auxiliary series
data.antibiotic_name = \
    data.antibiotic_name.replace(replace_antimicrobial)

# Drop duplicates
data = data.drop_duplicates()

# --------------------------------------------
# Report duplicated
# --------------------------------------------
# Find duplicates
dup = data.set_index('antibiotic_code') \
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
data['antibiotic_class'] = None

# Loop setting classes
for e in set(category.values()):
    # Get codes
    codes = [k for k,v in category.items() if v==e]
    # Get idxs
    idxs = data.antibiotic_code.isin(codes)
    # Fill gram type
    data.loc[idxs, 'antibiotic_class'] = e

# Drop duplicates
data = data.drop_duplicates()
data = data.sort_index()
data = data.reset_index(drop=True)

# Show
print("\nCounts:")
print(data.nunique())

# --------------------------------------------
# Save
# --------------------------------------------
# Save
data.to_csv('db_antimicrobials.csv', index=False)