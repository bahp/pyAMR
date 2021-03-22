# Import pandas
import pandas as pd
import numpy as np

# -------------------------------------------------
# Constants
# -------------------------------------------------
remove = {
    'sp.': '',
    'sp': '',  # order matters
    'second': '',
    'third': '',
    '2nd': '',
    '3rd': '',
    'methicillin resistant': '',
    'vancomycin resistant': '',
    '\([^)]*\)': '', # Remove everything between ()
    '\s{2,}': ' ',   # Remove duplicated spaces
}

replace_organism = {
    'viridans streptococcus':                  'streptococcus viridans',
    'lactose fermenting coliform':             'coliform lactose fermenting',
    'coagulase negative staphylococcus':       'staphylococcus coagulase negative',
    'beta-haemolytic streptococcus group a':   'streptococcus beta-haemolytic group A',
    'beta-haemolytic streptococcus group b':   'streptococcus beta-haemolytic group B',
    'beta-haemolytic streptococcus group c/g': 'streptococcus beta-haemolytic group C/G',
    'mixed coagulase negative staphylococci':  'staphylococcus coagulase negative'
}

gram_type = {
    'SAUR': 'p',
    'AHS': 'p',
    'BCER': 'p',
    'BACIL': 'p',
    'BHSA': 'p',
    'BHSB': 'p',
    'BHSC': 'p',
    'BHSCG': 'p',

    'BCEP': 'n',
    'BPSE': 'n',
    'CCOL': 'n',
    'CFET': 'n',
    'CJEJ': 'n',
    'CAMPY': 'n',

    'CPER': 'p',
    'CLOST': 'p',
    'CNS': 'p',
    'CHAE': 'p',
    'CJEI': 'p',
    'CORYN': 'p',
    'CSTR': 'p',

'ENTAE'	:'n',
'EASB'	:'n',
'ECLO'	:'n',
'ENTB'	:'n',
'ECASS' :'p',
'EFAS'  :'p',
'EFAM'	:'p',
'EGAL'	:'p',
'ENTC'	:'p',
'ECOL'	:'n',
'FNEC'	:'n',
'KOXY'	:'n',
'KPNE'	:'n',
'KLEBS'	:'n',
'LMON'	:'p',
'SAUR'	:'p',
'NFLA'	:'n',
'NGON'  :'n',
'NMEN'  :'n',
'NEISS'	:'n',
'NHS'	:'p',
'PANA'	:'p',
'PACN'	:'p',
'PROPI'	:'p',
'PMIR'	:'n',
'PROTE'	:'n',
'PVUL'	:'n',
'PSEUD'	:'n',
'PAER'	:'n',
'PLUT'	:'n',
'PORI'	:'n',
'PPUT'	:'n',
'PSTU'	:'n',
'SALMO':'n',
'SLIQ':	'n',
'SMAR':	'n',
'SERRA':'n',
'SFLE':	'n',
'SSON':	'n',
'SHIGE':'n',
'SEPI':	'p',
'SHAEM':'p',
'SLUG':	'p',
'SSAP':	'p',
'STAPH':'p',
'SAGA':	'p',
'SANG':	'p',
'SCON':	'p',
'SDYSEQ':'p',
'SEQU':	'p',
'SGOR':	'p',
'SINT':	'p',
'SMIL':	'p',
'SMIT':	'p',
'SORA':	'p',
'SPARAS':'p',
'SPNE':	'p',
'SPYO':	'p',
'SSAL':	'p',
'SSAN':	'p',
'STREP': 'p',
'ENTC': 'p',
'YENT':	'n'
}

# -----------------------------------------
# Read csv
# -----------------------------------------
# Read csv
data = pd.read_csv('./susceptibility.csv',
    usecols=['organismCode',
             'organismName'])

# Rename
data = data.rename(columns={
    'organismCode': 'organism_code',
    'organismName': 'organism_name'})

# Drop duplicates
data = data.drop_duplicates( \
    subset=['organism_code',
            'organism_name'])

# --------------------
# Format organism name
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
data.organism_name = data.organism_name.str.lower()

# Do str replacements
for k, v in remove.items():
    data.organism_name = \
        data.organism_name.str.replace(k, v)

# Format (strip)
data.organism_name = \
    data.organism_name.str.strip()

# Create auxiliary series
data.organism_name = \
    data.organism_name.replace(replace_organism)

# Drop duplicates
data = data.drop_duplicates()

# --------------------------------------------
# Report duplicated
# --------------------------------------------
# Find duplicates
dup = data.set_index('organism_code') \
    .index.duplicated(keep=False)

# Show
print("\nDuplicates:")
print(data[dup])
print("\nCounts:")
print(data.nunique())

if dup.any():
    print("\nERROR: There are duplicate values in the dataframe. \n"
          "The 'db_microorganisms.csv' file has therefore not \n"
          "been saved. Please correct the issues and run again.")
    import sys
    sys.exit()

# --------------------------------------------
# Create genus, species and gram type
# --------------------------------------------
# .. note: First we format the organism name so that we
#          ensure the first word is the genus and the
#          rest is information relative to the species.
#          Then we split the strs to get both.
# Create genus and species
data[['genus_name', 'specie_name']] = \
    data.organism_name.str.split(expand=True, n=1)

# Initialise gram type
data['gram_type'] = None

# Loop setting classes
for e in set(gram_type.values()):
    # Get codes
    codes = [k for k,v in gram_type.items() if v==e]
    # Get idxs
    idxs = data.organism_code.isin(codes)
    # Fill gram type
    data.loc[idxs, 'gram_type'] = e

# Drop duplicates
data = data.drop_duplicates()
data = data.sort_index()
data = data.reset_index(drop=True)

# --------------------------------------------
# Save
# --------------------------------------------
# Save
data.to_csv('db_microorganisms.csv', index=False)