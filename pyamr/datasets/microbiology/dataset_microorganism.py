# Import pandas
import pandas as pd

replace = {
    'sp.': '',
    'sp': '',  # order matters
    'second': '',
    'third': '',
    '2nd': '',
    '3rd': '',
    'mixed coagulase negative staphylococci': 'coagulase negative staphylococcus',
    'methicillin resistant': '',
    'vancomycin resistant': '',
    '\([^)]*\)': '', # Remove everything between ()
    '\s{2,}': ' ',   # Remove duplicated spaces
}

# Read csv
data = pd.read_csv('./susceptibility.csv')

# Transformations
data.organismName = data.organismName.str.lower()

# Do str replacements
for k, v in replace.items():
    data.organismName = \
        data.organismName.str.replace(k, v)

data.organismName = data.organismName.str.strip()

# Filter and format
data = data[['organismName', 'organismCode']]
data = data.set_index('organismCode')
data = data.drop_duplicates()

# Find duplicates
print("\nDuplicates:")
print(data[data.index.duplicated(keep=False)])

# Drop duplicates
data = data.drop_duplicates()

# Show
print("Count:")
print(data.reset_index().nunique())

data.to_csv('db_microorganisms.csv')