# Read
import pandas as pd

# Load data
data = pd.read_csv('susceptibility.csv')

# Get unique patient numbers
unique = data.patNumber.unique()
nunique = len(unique)

# Create replace map
replace = dict(zip(unique, range(nunique)))

# Replace data
data.patNumber = data.patNumber.replace(replace)

# Save
data.to_csv('susceptibility.csv')