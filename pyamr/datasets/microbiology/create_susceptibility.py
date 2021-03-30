# Libraries
import glob
import time
import pandas as pd

# Import pyAMR
from pyamr.datasets.registries import acronym_series
from pyamr.datasets.load import load_registry_microorganisms
from pyamr.datasets.load import load_registry_antimicrobials

# ---------------------------------
# Methods
# ---------------------------------
def create_microorganisms_lookup_table(orgs):
    """Creates the look up table for the organisms.

    This method uses the information in the organisms dataframe
    and the information in the default microorganisms registry
    to create a unique lookup table for the data.

    Parameters
    ----------
    orgs: pd.DataFrame
        The DataFrame with the organism genus and organism species
        for which the look up table should be created. The DataFrame
        must contain the following columns:
            microorganism_name
            genus
            species

    Returns
    -------
    pd.DataFrame
        Lookup table DataFrame with the following columns:
            'domain'
            'phylum'
            'class'
            'order'
            'family'
            'genus'
            'species'
            'acronym'
            'exists_in_registry'
            'gram_stain'
            'microorganism_code'
            'microorganism_name
    """
    # Check
    if not 'genus' in orgs:
        print("Missing <genus> column.")
    if not 'species' in orgs:
        print("Missing <species> column.")
    if not 'microorganism_name' in orgs:
        print("Missing <microorganism_name> column.")

    # Read microorganisms registry
    reg = load_registry_microorganisms()

    # --------------
    # Step 1
    # --------------
    # First, merge those rows within gram_stain and taxonomy
    # that have equal genus and species. Note that we are
    # only merging if both values exist and are equal.
    # Merge
    orgs = pd.merge(orgs, reg,
        how='left',
        left_on=['genus', 'species'],
        right_on=['genus', 'species']
    )

    # Those merged exist in registry.
    orgs['exists_in_registry'] = orgs.acronym.notna()

    # --------------
    # Step 2
    # --------------
    # Second, for those values whose taxonomy-related columns
    # are null, use the taxonomy information based only on the
    # genus. This does not overwrite step 1.
    # Taxonomy columns
    ctaxonomy = ['domain', 'phylum', 'class', 'order', 'family']

    # Create aux
    aux = pd.merge(orgs[['genus']],
        reg.drop(columns=['species', 'acronym'])\
           .drop_duplicates() \
           .groupby('genus') \
           .head(1),
        how='left',
        left_on=['genus'],
        right_on=['genus']
    )

    # Update orgs
    orgs.update(aux)

    # -------------------
    # Create new acronyms
    # -------------------
    # .. note: In order to be similar to the ones used in
    #          HH hospital, we can pass the minimum value
    #          as lg=1, ls=4 and length of 4 if only one
    #          word.
    # Columns with missing acronyms
    idxs = orgs.acronym.isna()

    # Fill with new acronyms
    orgs.loc[idxs, 'acronym'] = \
        acronym_series(orgs.loc[idxs, 'microorganism_name'].fillna(''),
            exclude_acronyms=reg.acronym.unique().tolist(),
            unique_acronyms=True, verbose=0,
            kwgs_acronym={'sep': '_'})

    # Columns
    keep = ['domain',
            'phylum',
            'class',
            'order',
            'family',
            'genus',
            'species',
            'acronym',
            'exists_in_registry',
            'gram_stain',
            'microorganism_code',
            'microorganism_name']

    # Filter
    orgs = orgs[[c for c in keep if c in orgs]]

    # Return
    return orgs


def create_antimicrobials_lookup_table(abxs):
    """Creates the look up table for the antimicorbials.

    This method uses the information in the antibiotics dataframe
    and the information in the default antimicrobials registry
    to create a unique lookup table for the data.

    Parameters
    ----------
    abxs: pd.DataFrame
        The DataFrame with ... The DataFrame must contain the following
        columns:


    Returns
    -------
    pd.DataFrame
        Lookup table DataFrame with the following columns:
    """
    # Check
    if not 'microorganism_name' in abxs:
        print("Missing <antimicrobial_name> column.")

    # Read microorganisms registry
    reg = load_registry_antimicrobials()

    # --------------
    # Step 1
    # --------------
    # First, merge those rows with equal names.
    # Merge
    abxs = pd.merge(abxs, reg,
        how='left',
        left_on=['antimicrobial_name'],
        right_on=['name']
    )

    # Those merged exist in registry.
    abxs['exists_in_registry'] = abxs.acronym.notna()

    # -------------------
    # Create new acronyms
    # -------------------
    # .. note: In order to be similar to the ones used in
    #          HH hospital, we can pass the minimum value
    #          as lg=1, ls=4 and length of 4 if only one
    #          word.
    # Columns with missing acronyms
    idxs = abxs.acronym.isna()

    # Fill with new acronyms
    abxs.loc[idxs, 'acronym'] = \
        acronym_series(abxs.loc[idxs, 'antimicrobial_name'].fillna(''),
            exclude_acronyms=reg.acronym.unique().tolist(),
            unique_acronyms=True, verbose=0,
            kwgs_acronym={
                'sep': '_',
                'exceptions': []})

    # Columns
    keep = ['name',
            'category',
            'acronym',
            'exists_in_registry',
            'antimicrobial_code']

    # Filter
    abxs = abxs[[c for c in keep if c in abxs]]

    # Return
    return abxs




if __name__ == '__main__':

    # Import
    import csv
    import yaml
    import time
    import logging
    import logging.config
    import pandas as pd

    # Specific
    from pathlib import Path

    # PyAMR specific methods
    from pyamr.datasets.clean import clean_clwsql008
    from pyamr.datasets.clean import clean_legacy

    # Configure logging
    with open('./logging.yaml', 'rt') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    # Get logger
    logger = logging.getLogger('dev')

    # ---------------------------------
    # Constant
    # ---------------------------------
    # Time
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # ---------------------------------
    # Methods
    # ---------------------------------
    def strdf(df):
        return "\n\t{0}\n".format(df.to_string().replace('\n', '\n\t'))


    # ---------------------------------
    # Load data
    # ---------------------------------
    # Define path
    path = './nhs/legacy/'
    path = './nhs/clwsql008/'

    tuples = [
        ('./nhs/legacy', clean_legacy),
        ('./nhs/clwsql008', clean_clwsql008)
    ]

    # Combined data
    combined = []

    # For each tuple
    for path, f_clean in tuples:
        # Load data (multiple files)
        data = pd.concat([pd.read_csv(f)
            for f in glob.glob(path + "/*.csv")])
        # Clean data
        data = f_clean(data)
        # Remove those empty
        data = data.dropna(how='any',
            subset=['date_received',
                    'microorganism_name',
                    'antimicrobial_name',
                    'sensitivity'])
        # Combine
        combined.append(data)

    # Merge
    data = pd.concat(combined)

    # Basic formatting
    data = data.drop_duplicates()

    # -------------------
    # Anonymise
    # -------------------
    # Create hos_number to id mapper
    unique = data.patient_id.unique()
    pid_map = dict(zip(unique, range(len(unique))))

    # Include categories
    data.patient_id = data.patient_id.map(pid_map)

    # Show
    #logger.info("\nData:\n{0}".format(strdf(data.head(10))))
    logger.info("\nColumns:\n\t{0}\n".format(data.columns))
    logger.info("\nDTypes:\n{0}".format(strdf(data.dtypes)))
    logger.info("\nNaNs:\n{0}".format(strdf(data.isna().sum(axis=0))))


    # ----------------------------------
    # Create Microorganisms LookUp table
    # ----------------------------------
    # Organism columns
    columns = ['microorganism_code',
               'microorganism_name']

    # Extract organisms information from susceptibility
    orgs = data[columns].copy(deep=True)
    orgs = orgs.drop_duplicates(subset=['microorganism_name'])

    # Create genus and species
    orgs[['genus', 'species']] = \
        orgs.microorganism_name.str.split(expand=True, n=1)

    # Format genus and species
    orgs.genus = orgs.genus.str.title()
    orgs.species = orgs.species.str.lower()

    # Sort
    orgs = orgs.sort_values(by=['genus', 'species'])

    # Create microorganisms database
    orgs = create_microorganisms_lookup_table(orgs)


    # ----------------------------------
    # Create Antimicrobials LookUp table
    # ----------------------------------
    # Organism columns
    columns = ['antimicrobial_code',
               'antimicrobial_name']

    # Extract organisms information from susceptibility
    abxs = data[columns].copy(deep=True)
    abxs = abxs.drop_duplicates(subset=['antimicrobial_name'])

    # Format genus and species
    abxs.antimicrobial_name = abxs.antimicrobial_name.str.capitalize()

    # Sort
    abxs = abxs.sort_values(by=['antimicrobial_name'])

    # Create microorganisms database
    abxs = create_antimicrobials_lookup_table(abxs)

    # ------------------
    # Useful information
    # ------------------
    # Create basic information
    sensitivity = data.sensitivity.value_counts()
    gram_stain = orgs.gram_stain.value_counts()

    # Create duplicates
    aux = orgs[['microorganism_name',
                'microorganism_code',
                'acronym']]

    # Find duplicates
    idxs_dup_code = orgs.duplicated(subset=['microorganism_code'], keep=False)
    idxs_dup_acrm = orgs.duplicated(subset=['acronym'], keep=False)

    # Basic information
    logger.info("\nSensitivity:\n{0}".format(strdf(sensitivity)))
    logger.info("\nGram stain:\n{0}".format(strdf(gram_stain)))
    logger.info("\nDuplicate codes:\n{0}".format(strdf(aux[idxs_dup_code])))
    logger.info("\nDuplicate acronyms:\n{0}".format(strdf(aux[idxs_dup_acrm])))


    # ----------
    # Filter
    # ----------
    # Columns
    keep = ['date_received',
            'date_outcome',
            'patient_id',
            'laboratory_number',
            'specimen_code',
            'specimen_name',
            'specimen_description',
            'microorganism_code',
            'microorganism_name',
            'antimicrobial_code',
            'antimicrobial_name',
            'sensitivity_method',
            'sensitivity',
            'mic',
            'reported']

    # Filter
    data = data[[c for c in keep if c in data]]


    # ----------
    # Save
    # ----------
    # Define path
    path = Path('./%s' % timestr)

    # Create path if it does not exist
    path.mkdir(parents=True, exist_ok=True)

    # Save databases
    abxs.to_csv(path / 'antimicrobials.csv', index=False)
    orgs.to_csv(path / 'microorganisms.csv', index=False)

    # Create grouper
    grouper = pd.Grouper(key='date_received', freq='Y')

    # Save susceptibility grouped
    for n, g in data.groupby(grouper):
        filename = "susceptibility-%s.csv" % n.strftime('%Y')
        g.to_csv(path / filename, index=False,
                quoting=csv.QUOTE_ALL)  # QUOTE_NONNUMERIC

    # Logging
    logger.info('The results have been saved in: %s' % path)