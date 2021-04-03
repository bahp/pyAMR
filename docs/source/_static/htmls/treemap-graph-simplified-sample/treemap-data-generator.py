###############################################################################
# Author: Bernard Hernandez
# Filename:
# Date: 
# Description:
#
###############################################################################

# Generic libraries.
import sys
import pprint
import pandas as pd


# -----------------------------------------------------------------------------
#                             HELPER METHODS
# -----------------------------------------------------------------------------
def treemap_structure(data):
  """
  """
  # Empty childrens for each organism.
  children = []
  for organism,dataframe in data.groupby("organismCode"):
    children.append(organism_structure(organism, dataframe))
  # Return structure.
  return {"name": "combinations", 
          "children": children}

def organism_structure(name, data):
  """
  """
  # Create children.
  children = []
  for index, row in data.iterrows():
    children.append(row_structure(row))
  # Return organism
  return {"name": name, 
          "children": children}

def row_structure(row):
  """
  """
  return {"name": row["antibioticCode"][1:], 
          "size": row["freq_ris"]}


# -----------------------------------------------------------------------------
#                                  MAIN
# -----------------------------------------------------------------------------
# Read frequencies.
goto = "../../../results/microbiology/frequencies/bldcul/"
path = "%s/freq_tests_pairs_total.csv" % goto
data = pd.read_csv(path)

# Filter interesting data.
data = data[['organismCode', 'antibioticCode', 'freq_ris']]

# Create new structure with data to paste in HTML file.
structure = treemap_structure(data)

# Print.
pprint.PrettyPrinter(indent=4).pprint(structure)

 
