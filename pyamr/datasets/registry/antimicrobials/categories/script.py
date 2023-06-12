import glob
import pandas as pd

# Information
antimicrobial_class = {
    'Amikacin':	'Aminoglycosides',
    'Amoxycillin': 'Aminopenicillins',
    'Aztreonam': 'Monobactams',
    'Ceftazidime': 'Cephalosporins',
    'Ciprofloxacin': 'Fluoroquinolones',
    'Colistin sulphate': 'Polypeptides',
    'Cotrimoxazole': 'Sulfonamides',
    'Cefotaxime': 'Cephalosporins',
    'Cefuroxime': 'Cephalosporins',
    'Cefoxitin': 'Cephalosporins',
    'Gentamicin': 'Aminoglycosides',
    'Imipenem':	'Meropenems',
    'Meropenem':'Meropenems',
    'Teicoplanin': 'Glycopeptide',
    'Vancomycin': 'Glycopeptide',
    'Linezolid': 'Oxazolidinones',
    'Tetracycline':	'Tetracyclines',
    'Tobramycin': 'Aminoglycosides',
    'Clindamycin': 'Macrolides',
    'Erythromycin':	'Macrolides',
    'Flucloxacillin': 'Penicillins',
    'Penicillin': 'Penicillins',
    'Cephalexin': 'Cephalosporins',
    'Novobiocin': 'Aminocoumarin',
    'Metronidazole': 'Nitroimidazoles',
    'Mecillinam': 'Penicillins',
    'Neomycin':	'Aminoglycosides',
    'Ertapenem': 'Meropenems',
    'Temocillin': 'Penicillins',
    'Naladixic acid': 'Fluoroquinolones',
    'Clarithromycin': 'Macrolides',
    'Ceftriaxone': 'Cephalosporins',
    'Oxacillin': 'Penicillins',
    'Cefixime':	'Cephalosporins',
    'Azithromycin':	'Macrolides',
    'Levofloxacin':	'Fluoroquinolones',
    'Moxifloxacin':	'Fluoroquinolones',
    'Tigecycline': 'Tetracyclines',
    'Ofloxacin': 'Fluoroquinolones',
    'Bacitracin': 'Polypeptides'
}

# -------------------------------
# Main
# -------------------------------
"""
# Path
path = '../../../nhs/susceptibility-v0.0.1/'

# Load data
data = pd.concat([pd.read_csv(file)
    for file in glob.glob(path + "/susceptibility-*.csv")])
"""

data = pd.read_csv('db_categories.csv')

# Rename columns
data = data.rename(columns={
    'antimicrobial_name': 'name'
})

# Filter
data = data[['name']]

# Format
data.name = data.name.str.strip()
data.name = data.name.str.capitalize()
data.name = data.name.str.replace('-', ' ')

# Drop duplicates
data = data.drop_duplicates(subset=['name'])

# Map
data['category'] = data.name.map(antimicrobial_class)

# Category formatting
data.category = data.category.str.capitalize()

# Final check
data = data.drop_duplicates()
data = data.dropna(how='all')
data = data.sort_values(by='name')

# Show
print("\nShow")
print(data)
print("\nUnique")
print(data.category.unique())

# Save
data.to_csv('db_categories.csv', index=False)