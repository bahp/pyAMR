# Libraries
import pandas as pd


if __name__ == '__main__':

    # Libraries
    import pandas as pd

    from pyamr.datasets.registries import acronym_series

    # Define paths
    path_output = 'registry.csv'

    # Load
    db = pd.read_csv('./categories/db_categories.csv')

    # Sort
    db = db.sort_values(by='name')

    # Fill with new acronyms
    db['acronym'] = acronym_series(db.name.fillna(''),
        exclude_acronyms=[],
        unique_acronyms=True, verbose=0,
        kwgs_acronym={
            'sep': '_',
            'exceptions': []})

    # Final check
    db = db.drop_duplicates()
    db = db.dropna(how='all')

    # Save
    print("\nSaving database: %s" % path_output)
    db.to_csv(path_output, index=False)