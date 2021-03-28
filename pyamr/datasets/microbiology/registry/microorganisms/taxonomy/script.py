# Library
import re
import pandas as pd

# --------------------------------
# Methods
# --------------------------------
def create_db_taxonomy(path):
    """This method...

    Parameters
    ----------

    Returns
    -------
    """

    # Load data
    taxonomy = pd.read_csv(path, header=None, delimiter = ";")

    # Drop first column
    taxonomy = taxonomy.drop(columns=[0])

    # Rename columns
    taxonomy.columns = ['phylum',
                        'class',
                        'order',
                        'family',
                        'genus',
                        'species']

    # Drop duplicates
    taxonomy = taxonomy.drop_duplicates()

    # Remove name prefixes (e.g. p__, c__, ...)
    taxonomy = taxonomy.applymap(lambda x: x[3:])

    # Remove parts with (.. _A, _E, _UI)
    taxonomy = taxonomy.replace(to_replace='_(\w+)$', value='', regex=True)
    taxonomy = taxonomy.replace(to_replace='_(\w+) ', value=' ', regex=True)

    # Remove parts with (.. sp001201230)
    taxonomy = taxonomy.replace(to_replace='sp(.+)$', value='', regex=True)

    # Find all remaining cells containing numbers
    numbers = taxonomy.applymap(lambda x: bool(re.search(r'(\d)+', x)))

    # Keep only those without numbers
    taxonomy = taxonomy[~numbers.any(axis=1)]

    # Drop rows if any column missing
    taxonomy = taxonomy.dropna(how='any')

    # Remove genus name from species. Note that unfortunately some species
    # have both genus and specie name but without an space in between. Thus
    # we cannot just split and keep the second member! The code below might
    # leave empty spaces which are removed with trim (maybe not anymore
    # since we include an space in the second regexp).
    taxonomy.species = taxonomy.apply(lambda row:
            row.species.replace(str(row.genus), ''), axis=1)
    taxonomy = taxonomy.applymap(lambda x: x.strip())

    # Insert domain
    taxonomy.insert(0, 'domain', 'Bacteria')

    # Format
    taxonomy.domain = taxonomy.domain.str.title()
    taxonomy.phylum = taxonomy.phylum.str.title()
    taxonomy.order = taxonomy.order.str.title()
    taxonomy.family = taxonomy.family.str.title()
    taxonomy.genus = taxonomy.genus.str.title()
    taxonomy.species = taxonomy.species.str.lower()

    # Drop duplicates
    taxonomy = taxonomy.drop_duplicates()

    # Return
    return taxonomy


if __name__ == '__main__':

    # Import libraries
    import pandas as pd

    # Define paths
    path_bacteria = './bac120_taxonomy.tsv'
    path_output = './db_taxonomy.csv'

    # Create database
    db = create_db_taxonomy(
        path = path_bacteria
    )

    # Show database
    print("\nTaxonomy database:")
    print(db)

    print("\nDuplicated (genus, species):")
    print(db[db.duplicated(subset=['genus', 'species'])] \
          .sort_values(by='genus'))

    # Based on duplicates we do correction.
    db = db.groupby(by=['genus', 'species']).head(1)

    # Duplicate correction
    print("\nDuplicated correction:")
    print(db[db.duplicated(subset=['genus', 'species'])] \
          .sort_values(by='genus'))

    # Save
    print("\nSaving database: %s" % path_output)
    db.to_csv(path_output, index=False)