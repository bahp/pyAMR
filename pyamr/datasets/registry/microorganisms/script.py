# Libraries
import pandas as pd

# Libraries specific
from itertools import product


from pyamr.datasets.registries import acronym_series

# ------------------------
# Helper methods
# ------------------------
def create_mapper(dataframe, column_key, column_value):
    """This method constructs a mapper

    Parameters
    ----------
    dataframe: dataframe-like
      The dataframe from which the columns are extracted

    column_key: string-like
      The name of the column with the values for the keys of the mapper

    column_value: string-like
      The name of the column with the values for the values of the mapper

    Returns
    -------
    dictionary
    """
    dataframe = dataframe[[column_key, column_value]]
    dataframe = dataframe.drop_duplicates()
    return dict(zip(dataframe[column_key], dataframe[column_value]))



def _acronym(x, lengths=None):
    """This method creates the acronyms.

    .. note: Add variable to chose whether we want
             to keep the whole word if the split
             length is 1.

    Parameters
    ----------
    x:
    lengths:

    Returns
    --------
    """
    # Splits
    split = x.split()

    # Define lengths
    if len(split) == 1:
        lengths = [len(x)]

    # Compute acronym
    return '_'.join([c[:l].upper() for c, l in zip(split, lengths)])


def acronym_series2(series, verbose=10, split_n=1):
    """This method creates the acronyms.

    It ensures that there are no duplicate acronyms.

    .. warning: It could be improved.
    .. warning: Use just a random uuid.

    Parameters
    ----------
    series: pd.Series
        The series with the names to convert in acronyms.
    verbose: int
        Level of verbosity

    Returns
    -------
    pd.Series
        The acronym series
    """

    # Set default none acronym
    acronym = \
        pd.Series(index=series.index, data='', name='acronym')

    # Create DataFrame with words
    words = series.str.split(expand=True, n=split_n)

    # Find the maximum length for each column
    maxln = words.astype('str').applymap(lambda x: len(x)).max()

    # Create loops
    loops = product(*[range(4, n) for n in maxln])

    # Set dup
    dup, keep = True, False

    # Loop
    for i, l in enumerate(loops):

        # Find duplicates and change keep
        idxs = acronym.duplicated(keep=keep)
        keep = 'first'

        # Break clause
        if idxs.sum() == 0:
            break

        # Show acronym info
        if verbose > 5:
            print("%s. values=%s | max=%s" % \
                  (i, l, tuple(maxln.values)))

        # Show duplicates
        if verbose > 7:
            df = pd.concat([series[idxs], acronym[idxs]], axis=1)
            print(df.sort_values(by='acronym'))
            print("\n")

        # Create new acronyms
        acronym[idxs] = series[idxs].apply(_acronym, lengths=l)

    # Show warning
    if verbose > 0:
        print("There are %s repeated acronyms!" % idxs.sum())

    # Return
    return acronym


def create_db_organisms(verbose=10):
    """This method creates the organisms db.

    Explain
    1. Load grams...
    2. load taxonomies...
    3. Merge as follows...
    4. Add unique acronyms...
    5. Select columns...
    6. Formats...

    Returns
    -------
    """

    # Load gram stain database
    gram_stain = pd.read_csv('./gram_stain/db_gram_stain.csv')

    # Load taxonomy
    taxonomy = pd.read_csv('./taxonomy/db_taxonomy.csv')

    # --------------
    # Step 1
    # --------------
    # First, merge those rows within gram_stain and taxonomy
    # that have equal genus and species. Note that we are
    # only merging if both values exist and are equal.
    # Merge
    db = pd.merge(gram_stain.dropna(how='any'), taxonomy,
        how='outer',
        left_on=['genus', 'species'],
        right_on=['genus', 'species']
    )

    # --------------
    # Step 2
    # --------------
    # Second, includes the gram stain for those rows within the gram
    # stain database in which there is no species and therefore it
    # assumes that it should be assigned to the whole genus.
    # Get only genus
    genus_stain = gram_stain[gram_stain.species.isna()]

    # Create mapper
    genus_stain_map = create_mapper(genus_stain, 'genus', 'gram_stain')

    # Fill only empty values
    db.gram_stain = db.gram_stain \
        .mask(db.gram_stain.isna()) \
        .fillna(db.genus.map(genus_stain_map))

    # --------------
    # Step 3
    # --------------
    # There are a number of genus in which we do not have all
    # the taxonomy information. Since the taxonomy information
    # over genus (e.g. family, order, class) does not change,
    # then fill accordingly.
    # Create mapping
    mapping = taxonomy.dropna(how='any').groupby('genus').head(1)
    mapping = mapping.drop(columns=['species'])

    # Fill (it keeps both sides, i would like only one side!)
    db = db.set_index('genus').combine_first( \
        mapping.set_index('genus')).reset_index()


    # --------------
    # Acronyms
    # --------------
    # Sort
    db = db.sort_values(by=['genus', 'species'])

    # Create binomial name
    binomial_name = db[['genus', 'species']] \
        .fillna('').apply(' '.join, axis=1).str.strip()

    # Fill with new acronyms
    db['acronym'] = acronym_series(binomial_name,
        exclude_acronyms=[], unique_acronyms=True,
        verbose=0, kwgs_acronym={'sep': '_'})

    # Reorder columns
    db = db[['domain',
             'phylum',
             'class',
             'order',
             'family',
             'genus',
             'species',
             'acronym',
             'gram_stain']]

    # Formatting
    # ... use str.lower()
    # ... use str.title()
    # ... anything else?

    # Drop duplicates
    db = db.drop_duplicates()
    db = db.dropna(how='all')

    # Return
    return db







if __name__ == '__main__':

    # Libraries
    import pandas as pd


    # Define paths
    path_output = 'registry.csv'

    # Create database
    db = create_db_organisms(verbose=1)

    # Show database
    print("\nMicroorganisms db:")
    print(db)

    # Show duplicates
    idxs = db.duplicated(subset=['genus', 'species'])
    print("\nDuplicated (genus, species): %s" % idxs.sum())
    if idxs.sum() > 0:
        print(db[idxs])

    # Show empty taxonomy
    idxs = db[['domain', 'phylum', 'class', 'order', 'family']].isna().any(axis=1)

    print("\nEmpty taxonomy: %s" % idxs.sum())
    print(db[idxs])

    # Save
    print("\nSaving database: %s" % path_output)
    db.to_csv(path_output, index=False)