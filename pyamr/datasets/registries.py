# Libraries
import pandas as pd

# Import specific
from itertools import product

# Load
from pyamr.datasets.load import load_registry_microorganisms
from pyamr.datasets.load import load_registry_antimicrobials

# -----------------------------------------
# Helper methods
# -----------------------------------------
def length_exceptions(x):
    """This method..."""
    if len(x) == 1:
        return [len(x[0])]
    if len(x) >= 4:
        return [1] * len(x)
    return None

def _loops_strategy_lengths(series):
    """
    :param x:
    :return:
    """
    import numpy as np
    # Create DataFrame with words
    words = series.str.split(expand=True, n=1)
    # Create DataFrame with word lengths
    lengths = words.astype('str').applymap(lambda x: len(x))
    # Create loops
    return list(product(*[range(4, n) for n in lengths.max()]))

# -----------------------------------------
# Constants
# -----------------------------------------
ACRONYM_EXCEPTIONS = [
    length_exceptions
]


def _acronym(x, lengths=None, sep='', exceptions=ACRONYM_EXCEPTIONS):
    """Create an acronym from a string single.

    .. note: Add variable to chose whether we want to keep
             the whole word if the split length is 1.

    Parameters
    ----------
    x: String
        The strings to create the acronym/code.

    sep: String (default ' ')
        The separator to include between the acronym components. For
        instance, the sep values ' ' and '_' for the string
        'artificial intelligence' would lead to 'AI' and 'A_I'
        respectively.

    lengths: tuple
        The number of letters to use from each word after
        the initial string has been split.

    exceptions: dictionary
        The condition to evaluate as key and the lengths to use as values.
        Only the first condition that returns Tue will be valuated. The
        signature of the methods are as follows:

        key function:
        :param x: list - array obtained from split
        :return: boolean - whether

        value function:
        :param x: list - array obtained from split
        :return: list - array with lenghts

    Returns
    --------
    string
        The acronym
    """
    # Splits
    split = x.split()

    # Define default lengths
    if lengths is None:
        lengths = [1] * len(split)

    # Exceptions
    #for k,v in exceptions.items():
    #    if k(split):
    #        lengths = v(split)
    for expt in exceptions:
        aux = expt(split)
        if aux is not None:
            lengths = aux

    # Compute acronym
    return sep.join([c[:l].upper() \
        for c, l in zip(split, lengths)])



def acronym_series_unique(series, split_n=1,
                          exclude_acronyms=[],
                          loops_strategy=None,
                          verbose=10,
                          kwgs_acronym={}):
    """Computes unique acronyms.

    Parameters
    ----------

    Returns
    --------
    """

    # Set default none acronym
    acronym = \
        pd.Series(index=series.index, data=pd.NA, name='acronym')

    # Define loops strategy
    if loops_strategy is None:
        loops_strategy = _loops_strategy_lengths

    # Find loops
    loops = loops_strategy(series)

    # Loop
    for i, l in enumerate(loops):

        # Find duplicates or empty values
        idxs = acronym.duplicated(keep='first') | acronym.isna()

        # Break clause
        if idxs.sum() == 0:
            break

        # Show information
        if verbose > 5:
            print("%s/%s. lengths=%s" % (i, len(loops), l))
        if verbose > 7:
            df = pd.concat([series[idxs], acronym[idxs]], axis=1)
            print("%s\n" % df.sort_values(by='acronym'))

        # Create acronyms
        aux = series[idxs].apply(_acronym, lengths=l, **kwgs_acronym) # Create new
        aux[aux.isin(exclude_acronyms)] = pd.NA                       # Exclude
        acronym[idxs] = aux[idxs]                                     # Update

    # Show warning
    if verbose > 0:
        print("There are %s repeated acronyms!\n" % idxs.sum())

    # Return
    return acronym


def acronym_series(series, unique_acronyms=False, **kwargs):
    """This method...

    Parameters
    ----------
    series: pd.Series
        The series with the names to convert in acronyms.
    unique_acronyms:

    exclude_acronyms:

    split_n: int

    verbose: int
        Level of verbosity

    loops_strategy: function
        The function to indicate what length combinations should
        be used on each iteration. By default it will use the
        default method _loops_strategy_lengths which split the
        series in two and returns all possible lengths from (4, 4)
        till (max_len, max_len). The signature of the function to
        pass as loops_strategy is as follows:

        :param x: series
        :return: list (array of lengths)

    kwgs_split: dict
        The parameters to pass to the split function

    kwgs_acronym: dict
        The parameters to pass to the acronym function.

    Returns
    -------
    pd.Series
        The acronym series

    """
    # Basic check
    if series.duplicated().any() and unique_acronyms:

        # show warning
        repeated = series.value_counts()
        print("\nThe series has the following identical values and \n"
              "therefore they cannot or shouldn't be expressed with \n"
              "different acronyms. The unique_acronyms parameter has \n"
              "been set to 'False'.\n\n{0}" \
                .format(repeated[repeated > 1]))
        # Set unique acronyms to false
        unique_acronyms = False

    # Return acronyms
    if not unique_acronyms:
        return series.apply(_acronym)

    # Return
    return acronym_series_unique(series, **kwargs)


#
class MicroorganismRegistry:
    """This class..."""

    taxonomy = ['domain',
                'class',
                'order',
                'family',
                'genus',
                'species',
                'subspecies']

    reg = None

    def __init__(self, path=None):
        """Load dataframe registry.

        Parameters
        ----------
        path: string
            The path to the csv file.
        """
        # Load registry information
        self.reg = load_registry_microorganisms()

    def combine(self, dataframe):
        """Combines an external dataframe with the registry.

        .. note: The dataframe must contain genus, species..

        Parameters
        ----------

        Returns
        --------
        """
        # Check
        if not 'genus' in dataframe:
            raise ValueError("Missing <genus> column.")
        if not 'species' in dataframe:
            raise ValueError("Missing <species> column.")

        # Copy dataframe
        dataframe = dataframe.copy(deep=True)

        # Format
        dataframe.genus = dataframe.genus.str.capitalize()
        dataframe.species = dataframe.species.str.lower()

        # --------------
        # Step 1
        # --------------
        # First, merge those rows within gram_stain and taxonomy
        # that have equal genus and species. Note that we are
        # only merging if both values exist and are equal.
        # Merge
        dataframe = pd.merge(dataframe, self.reg,
            how='left',
            left_on=['genus', 'species'],
            right_on=['genus', 'species']
        )

        # Those merged exist in registry.
        dataframe['exists_in_registry'] = dataframe.acronym.notna()

        # --------------
        # Step 2
        # --------------
        # Second, for those values whose taxonomy-related columns
        # are null, use the taxonomy information based only on the
        # genus. This does not overwrite step 1.
        # Create aux
        aux = pd.merge(dataframe[['genus']],
            self.reg.drop(columns=['species', 'acronym']) \
                .drop_duplicates() \
                .groupby('genus') \
                .head(1),
            how='left',
            left_on=['genus'],
            right_on=['genus']
        )

        # Update dataframe
        dataframe.update(aux)

        # Return
        return dataframe

    def binomial_name(self):
        pass

    def uuid(self):
        pass

class AntimicrobialRegistry:
    """This class..."""

    reg = None

    def __init__(self, path=None):
        """Load dataframe registry.

        Parameters
        ----------
        path: string
            The path to the csv file.
        """
        # Load registry information
        self.reg = load_registry_antimicrobials()

    def combine(self, dataframe):
        """Combines an external dataframe with the registry.

        .. note: The dataframe must contain genus, species..

        Parameters
        ----------

        Returns
        --------
        """
        # Check
        if not 'antimicrobial_name' in dataframe:
            raise ValueError("Missing <antimicrobial_name> column.")

        # Copy dataframe
        dataframe = dataframe.copy(deep=True)

        # Format
        dataframe.antimicrobial_name = \
            dataframe.antimicrobial_name.str.capitalize()

        # --------------
        # Step 1
        # --------------
        # First, merge those rows within gram_stain and taxonomy
        # that have equal genus and species. Note that we are
        # only merging if both values exist and are equal.
        # Merge
        dataframe = pd.merge(dataframe, self.reg,
            how='left',
            left_on=['antimicrobial_name'],
            right_on=['name']
        )

        # Return
        return dataframe





if __name__ == '__main__':

    # Libraries
    import pandas as pd

    def len1(x):
        """
        :param x: array obtained from split
        :return: boolean
        """
        return len(x) == 1

    def wordl(x):
        """
        :param x: array obtained from split
        :return: array with lenghts
        """""
        return [len(x[0])]

    # Create data.
    organisms = ['Pseudomonas Aeruginosa',
                 'Pseudomonas Aeruginose', # minor variant
                 'Pseudomonas Aeruginosi', # minor variant
                 'Pseudomonas',            # genus 1
                 'Enterococcus',           # genus 2
                 'Enterococcus vagus',
                 'Staphylococcus Beta-Haemolytic Group A',
                 'This is another example',  # Long
                 'Pseu Aeru',                # Extreme
                 'Enterococcus vagus',       # repeated
                 'Pseudomonas',              # repeated
    ]

    # Create series
    series = pd.Series(organisms)

    # Create new acronyms
    acronyms_1 = series.apply(_acronym, sep='')
    acronyms_2 = series.apply(_acronym, sep='_')

    # Create acronyms
    acronyms_3 = acronym_series(series,
        exclude_acronyms=[],
        unique_acronyms=True,
        verbose=0)

    # -----------------------------
    # Creating unique acronyms
    # -----------------------------
    # Create loops from default loop_strategy
    loops = _loops_strategy_lengths(series)


    # Create acronyms
    acronyms_4 =  acronym_series(series[:-3],
        exclude_acronyms=['PSEU_AERU'],
        unique_acronyms=True,
        verbose=10,
        kwgs_acronym={
            'sep': '_'
        })

    # Create result
    result = pd.DataFrame()
    result['series'] = series
    result['acronyms_1'] = acronyms_1
    result['acronyms_2'] = acronyms_2
    result['acronyms_3'] = acronyms_3
    result['acronyms_4'] = acronyms_4

    # Show
    print("Results:")
    print(result)
    print("Loop Strategy:")
    print(pd.DataFrame(loops))