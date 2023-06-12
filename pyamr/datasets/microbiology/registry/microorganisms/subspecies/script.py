# Libraries
import pandas as pd

# Configuration
show_unique = [
    'group',
    'coagulase_production',
    'haemolysis'
]

# Load
data = pd.read_csv('db_groups.csv')

# Show
print(data)

print("\nUnique values:")
for c in show_unique:
    print("\n ==> %s" % c)
    print(pd.Series(data[c].unique()))