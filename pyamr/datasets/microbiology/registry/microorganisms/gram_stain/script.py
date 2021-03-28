# Library
import pandas as pd

# --------------------------------
# Methods
# --------------------------------
def create_db_gram_stain(path_positive,
                         path_negative):
    """This method...

    Parameters
    ----------

    Returns
    -------
    """
    # Load data
    gram_n = pd.read_csv(path_negative, header=None)
    gram_p = pd.read_csv(path_positive, header=None)

    # Remove dictionary entries (A, B, C, ...)
    gram_n = gram_n[gram_n[0].str.len() > 1]
    gram_p = gram_p[gram_p[0].str.len() > 1]

    # Create genus and species
    gram_n[['genus', 'species']] = \
        gram_n[0].str.split(expand=True, n=1)
    gram_p[['genus', 'species']] = \
        gram_p[0].str.split(expand=True, n=1)

    # Add gram stain
    gram_n['gram_stain'] = 'n'
    gram_p['gram_stain'] = 'p'

    # Combine
    gram_stain = pd.concat([gram_n, gram_p])

    # Drop first column
    gram_stain = gram_stain.drop(columns=[0])

    # Basic check (include lower?)
    gram_stain = gram_stain.applymap(lambda x:
        x.strip() if x is not None else x)

    # Format
    gram_stain.genus = gram_stain.genus.str.title()
    gram_stain.species = gram_stain.species.str.lower()

    # Remove duplicates
    gram_stain = gram_stain.drop_duplicates()

    # Sort
    gram_stain = gram_stain.sort_values(by=['genus', 'species'])

    # Return
    return gram_stain







if __name__ == '__main__':

    # Import libraries
    import pandas as pd

    # Define paths
    path_negative = './gram_negative.txt'
    path_positive = './gram_positive.txt'
    path_output = './db_gram_stain.csv'

    # Create database
    db = create_db_gram_stain(
        path_positive=path_positive,
        path_negative=path_negative
    )

    # Show database
    print("\nGram stain database:")
    print(db)

    # Show conflicts
    idxs = db.duplicated(subset=['genus', 'species'], keep=False)
    print("\nGram conflicts:")
    print(db[idxs])

    # Save
    print("\nSaving database: %s" % path_output)
    db.to_csv(path_output, index=False)