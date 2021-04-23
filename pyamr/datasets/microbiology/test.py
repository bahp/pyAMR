import pandas as pd

# -------------------------------------------------
# Test to_csv date_format
# -------------------------------------------------
# Create DataFrame
a = pd.DataFrame()

# Create dates
a['dates'] = ['23/01/2015 19:37',
              '23/01/2015 20:08']

# Format dates
a.dates = pd.to_datetime(a.dates)

# Save
print("\nDF:")
print(a)
print("Saving...")
#a.to_csv('test-v0.1.csv')
#a.to_csv('test-v0.2.csv', date_format='%Y-%m-%d %H:%M:%S')

# -------------------------------------------------
# Test cleaning / replacing
# -------------------------------------------------
# Create DataFrame
a = pd.DataFrame()

# Create regexpmap
REGEX_MAP = {
    '\([^)]*\)': '',  # Remove everything between ().
    'species': '',  # Rename species for next regexp
    'sp(\.)?(\s|$)+': ' ',  # Remove sp from word.
    'strep(\.|\s|$)': 'streptococcus ',  # Complete
    'staph(\.|\s|$)': 'staphylococcus ',  # Complete
    '\s+': ' '  # Remove duplicated spaces.
}

# Create data
a['spaces'] = [' in   between ', ' sides ', 'end ', ' start', None]
a['species'] = [' sp.', ' sp', 'sp ', ' sp. ', 'species']
a['occus'] = ['haemolytic streptococcus',
              'haemolytic strep',
              'haemolytic strep.',
              'haemolytic strep. aureus',
              'haemolytic strep aureus']

a['occus2'] = ['strep.aureus',
               'staph.aureus',
               'methicillin resistant staph.aureus',
               'feo strepococcus',
               'streptococcus feo']

# Cleaned
cleaned = a.copy(deep=True)
cleaned = cleaned.replace(regex=REGEX_MAP)
cleaned = cleaned.apply(lambda x: x.str.strip() \
    if x.dtype == "object" else x)

# Show
print("-"*80)
print("\nOriginal")
print(a)
print("\nCleaned")
print(cleaned)

# ---------------------------------------------------
# Haemolytic
# --------------------------------------------------
# .. note: https://regex101.com/r/KFXCCM/1

# ----------------------------------------------------
# Test genus at the beginning
# ----------------------------------------------------
# Import regular expressions
import re

# Import function
from pyamr.datasets.clean import word_to_start

# Species examples
series = pd.Series(['is viridians, enteroccocus en',
                    'is viridians, enteroccocus',
                    'viridians enteroccocus',
                    'enterococcus viridians',
                    'non haemolytic feo enteroccocus',
                    'non-haemolytic enteroccocus',
                    'non haemolytic enteroccocus',
                    'vancomycin resistant enteroccocus',
                    None])


# Corrected
corrected = series.apply(word_to_start, w='enteroccocus')

# Show
print("-"*80)
print("\n\n\nRaw")
print(series)
print("\nCorrected")
print(corrected)

# ----------------------------------------------------
# Test hyphen
# ----------------------------------------------------
# Import
from pyamr.datasets.clean import hyphen_before

# Haemolytic examples
series= pd.Series(['non haemolytic something',
                   ' non haemolytic something',
                   ' when beta haemolytic something',
                   ' whn gamma haemolytic',
                   'non    haemolytic'])

# Correct it
corrected = series.apply(hyphen_before, w='haemolytic')

# Show
print("-"*80)
print("\n\n\nRaw:")
print(series)
print("\nCorrected:")
print(corrected)

# ----------------------------------------------------
# Full test
# ----------------------------------------------------
# In this section, we do a full test, specially for
# those examples that have shown to be problematic in
# the final microorganisms.csv outcome.
# Import clean common
from pyamr.datasets.clean import clean_common
from pyamr.datasets.registries import _clean_microorganism

# Create dataframe
df = pd.DataFrame()

# Add microorganism names.
df['microorganism_name'] = [
    'non haemolytic streptococcus aureus',
    'this non haemolytic streptococcus',
    'beta-haemolytic streptococcus group a',
    'beta-haemolytic streptococcus group b',
    'beta-haemolytic streptococcus group c',
    'beta-haemolytic streptococcus group c/g',
    'beta-haemolytic streptococcus group g',
    'this is haemolyticus',
    'perestreptococcus',
    'Coagulase negative staphylococcus',
    'Methicillin Resistant Staph.aureus',
    'mixed streptococcus alpha-haemolytic',
    'non-coliform lactose fermenting',
    'Non-haemolytic streptococcus',
    'Non-lactose Fermenting Coliform',
    'Vancomycin Resistant Enterococcus',
    ' non- lactose fermenting coliform',
    'non-lactose fermenting coliform',
    'mixed lactose fermenting coliform',
    'paenibacillus sp',
    'paenibacillus sp.',
    'paenibacillus sp..',
    'escherichia coli o157',
    '*** mrsa *** isolated',
    'streptococcus milleri group',
    'aspergillus fumigatus'
]

# Any alterations
df.microorganism_name = df.microorganism_name.str.upper()

# Clean
#aux = clean_common(df.copy(deep=True))
aux = _clean_microorganism(df.microorganism_name)

# Show
print("-"*80)
print("\nData:")
print(df)
print("\nCorrected:")
print(aux)