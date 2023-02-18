# Libraries
import collections
import pandas as pd

# Import specific
from itertools import product

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


def invert(d):
    return {v:k for k,v in d.items()}


def create_registry(data, keyword=None, keep=None):
    """Creates registry from data.

    Parameters
    ----------
    data: pd.DataFrame
        The data

    keyword: string
        The keyword for the columns. All columns starting
        with such keyword will be kept and used for the
        registry.

    keep: list
        The list of columns to keep for the registry
    """
    # Columns to keep
    if keep is None:
        keep = [c for c in data.columns
            if c.startswith(keyword) and
                (c.endswith('name') or
                 c.endswith('code') or
                 c.endswith('description'))]

    # Copy data
    reg = data[keep].copy(deep=True)
    reg = reg.drop_duplicates()
    reg = reg.reset_index(drop=True)

    # Add id
    #if keyword is not None:
    #    reg['%s_id' % keyword] = reg.index.values

    # Return
    return reg


# -----------------------------------------------------
# Microorganism
# -----------------------------------------------------
# The regexp map
REGEX_MAP_MICROORGANISM = {
    '\([^)]*\)': '',      # Remove everything between ()
    '(\s)*\-(\s)*': '-',  # Remove spaces before after hyphen
    'species': '',        # Rename species for next regexp
    'o157': '',           # Remove scherichia coli o157
    'sp(\.)*(\s|$)+': ' ',  # Remove sp from word.
    'strep(\.|\s|$)': 'streptococcus ',   # Complete
    'staph(\.|\s|$)': 'staphylococcus ',  # Complete
    'staphylococci': 'staphylococcus',    # Correction (add mixed? group?)
    'streptococci': 'streptococcus',      # Correction (add mixed? group?)
    '\s+': ' ',           # Remove duplicated spaces.
}

# The hyphens
HYPHENS = ['haemolytic']

# The words to move to the beginning
MOVE_TO_START = ['enterococcus',
                 'staphylococcus',
                 'streptococcus',
                 'coliform']

# The words to move to the end
MOVE_TO_END = ['methicillin resistant',
               'vancomycin resistant',
               'mixed']


def _clean_microorganism(series,
                         hyphens=HYPHENS,
                         move_to_start=MOVE_TO_START,
                         move_to_end=MOVE_TO_END):
    """Cleans the microorganism names.

    .. todo: Put everything below as our own defined function
             but allow users to pass their own functions.

    Parameters
    ----------
    series: pd.Series
        The series with the name of the organisms. Ideally it
        should represent the binomial nomenclature including
        genus and specie respectively.

    hyphens:

    move_to_start:

    move_to_end:

    Returns
    -------
    """

    # Libraries
    from pyamr.datasets.clean import hyphen_before
    from pyamr.datasets.clean import word_to_start

    # Copy
    s = series.copy(deep=True)

    # Lower
    s = s.str.lower()

    # Apply regex mapping
    s = s.replace(regex=REGEX_MAP_MICROORGANISM)

    # Correct hyphens
    for hp in hyphens:
        s = s.transform(hyphen_before, w=hp)

    # Correct order of genus
    for sp in move_to_start:
        s = s.transform(word_to_start, w=sp, pos='start')

    # Correct order of tags
    for sp in move_to_end:
        s = s.transform(word_to_start, w=sp, pos='end')

    # Apply regexp mapping
    s = s.replace(regex=REGEX_MAP_MICROORGANISM)

    # Final strip
    s = s.str.strip()

    # Return
    return s


def clean_specimen(series):
    """
    \sr\s = right -> end
    \sl\s = left -> end


    :param series:
    :return:
    """

# ---------------------------------------------------
# Registry Base
# ---------------------------------------------------
class Registry:
    """This is basically a lookup table."""

    # The order of the columns within the registry
    ORDER = ['id', 'name', 'code', 'description', 'original']
    # The subset to use to drop duplicates
    SUBSET = ['name', 'original']
    # The function to clean the names
    FCLEAN = {}
    # The dictionary to rename columns
    RENAME_COLUMNS = {}
    # Registry dataframe
    REG = None


    def __init__(self, keyword='',
                       order=ORDER,
                       subset=SUBSET,
                       fclean=FCLEAN):
        """Constructor

        .. note: Raise type errors
        .. note: Allow to load from file
        """
        # Set parameters
        self.keyword = keyword
        self.ORDER = order
        self.SUBSET = subset
        self.FCLEAN = fclean

        # Add columns to order. Note that if they are
        # important to drop duplicates, they probably
        # should be kept.
        #if subset is not None:
        #    self.ORDER += sorted(set(subset).difference(set(order)))


    def getr(self, prepend=False):
        """Returns the registry DataFrame"""
        # Get registry
        aux = self.REG.copy(deep=True)

        # Prepend
        if prepend and self.keyword!='':
            aux.columns = ['%s_%s' % (self.keyword, c)
                for c in aux.columns]

        # Fill na with '' so null=False.
        # aux = aux.fillna(aux.dtypes.replace({'O': ''}))

        # Return
        return aux


    def fit(self, data):
        """This method...

        .. note: It assumes name exists...

        Parameters
        ----------
        data: pd.DataFrame
            The DataFrame expects to have the code, the
            name and the description. Specially the name.
            Think what happens if other missing.

        Returns
        -------
        """
        # Create registry
        aux = create_registry(data, keyword=self.keyword)

        # Keep only last label
        aux.columns = [c.split("_", 1)[-1] for c in aux.columns]

        # Raise error
        if not set(['name', 'code']).intersection(aux.columns):
           raise ValueError("Missing either name or code")

        # Add missing columns
        if 'code' not in aux:
            aux['code'] = aux.name
        if 'name' not in aux:
            aux['name'] = aux.code

        # Backup original
        original = aux.name

        # Put everything to lowercase
        aux = aux.applymap(lambda x: x.lower()
            if isinstance(x, str) else x)

        # Restore original
        aux['original'] = original

        """
        # Add code and fill empty name
        aux.name.fillna(aux.code, inplace=True)

        # Replace
        aux.code = aux.code.replace(self.CODE_REPLACE)

        # Map
        aux = aux.replace({
            'name': self.CODE_MAP,
            'code': invert(self.CODE_MAP)
        })
        """

        print("=====> %s" % self.FCLEAN)

        # Apply cleaning
        for k,v in self.FCLEAN.items():
            if not k in aux.columns:
                continue
            if not callable(v):
                continue
            aux[k] = v(aux[k])
            print("cleaned %s with %s" % (k, v))

        # Final formatting
        aux = aux.drop_duplicates(subset=self.SUBSET)
        aux.name = aux.name.astype(str)
        aux = aux.sort_values(by='name')
        aux = aux.reset_index()
        aux['id'] = aux.index + 1

        # Keep
        keep = [c for c in self.ORDER if c in aux.columns]

        # Order information
        aux = aux[keep]

        # Set registry
        self.REG = aux

        # Return
        return self

    def replace(self, series, key='original', value='name'):
        """This method..."""
        tup = zip(self.REG[key], self.REG[value])
        return series.map(dict(tup))

    def transform(self, data, replace={}, include_id=True):
        """Transform data

        Parameters
        ----------
        data: pd.DataFrame
            The data to transform.
        replace:

        include_id

        Returns
        -------
        pd.DataFrame
            The data transformed
        """
        # Include the id.
        if include_id:
            data['%s_id' % self.keyword] = \
                self.replace(data['%s_name' % self.keyword],
                    key='name', value='id')

        # Perform replace
        #for column, (key, value) in replace.items():
        #    data[column] = self.replace(data[column],
        #        key='original', value='name')

        # Return
        return data


    def fit_transform(self, data, **kwargs):
        """Fits and transforms"""
        self.fit(data)
        return self.transform(data, **kwargs)

    def combine(self, data):
        pass

    def clean(self, series):
        pass


# ---------------------------------------------------
# Registry Microorganism
# ---------------------------------------------------
class MicroorganismRegistry(Registry):
    """Registry for microorganisms"""

    taxonomy = ['domain',
                'class',
                'order',
                'family',
                'genus',
                'species',
                'subspecies']

    reg = None

    def __init__(self, **kwargs):
        """"""
        # Super
        super().__init__(**kwargs)

        # For some reason setting the dictionary as an
        # attribute does not work, the variable FCLEAN
        # remains {} (from parent).
        # Set cleaning dictionary
        self.FCLEAN = {
            'name': _clean_microorganism
        }


    def combine(self, dataframe, on='name'):
        """Combines an external dataframe with the registry.

        .. note: The dataframe must contain genus, species..

        Parameters
        ----------

        Returns
        --------
        """
        # Load
        from pyamr.datasets.load import load_registry_microorganisms

        # Copy DataFrame
        aux = dataframe.copy(deep=True)

        # Create genus and species
        aux[['genus', 'species']] = \
            aux[on] \
                .str.capitalize() \
                .str.split(expand=True, n=1)

        # Format
        aux.genus = aux.genus.str.capitalize()
        aux.species = aux.species.str.lower()

        # Load registry information
        if self.reg is None:
            self.reg = load_registry_microorganisms()

        # --------------
        # Step 1
        # --------------
        # First, merge those rows within gram_stain and taxonomy
        # that have equal genus and species. Note that we are
        # only merging if both values exist and are equal.
        # Merge
        aux = pd.merge(aux, self.reg,
            how='left',
            left_on=['genus', 'species'],
            right_on=['genus', 'species']
        )

        # Those merged exist in registry.
        aux['exists_in_registry'] = aux.acronym.notna()

        # --------------
        # Step 2
        # --------------
        # Second, for those values whose taxonomy-related columns
        # are null, use the taxonomy information based only on the
        # genus. This does not overwrite step 1.
        # Create aux
        aux_step2 = pd.merge(aux[['genus']],
            self.reg.drop(columns=['species', 'acronym']) \
                .drop_duplicates() \
                .groupby('genus') \
                .head(1),
            how='left',
            left_on=['genus'],
            right_on=['genus']
        )

        # Update dataframe
        aux.update(aux_step2)

        # Return
        return aux

    def binomial_name(self):
        pass

    def uuid(self):
        pass


# ---------------------------------------------------
# Registry Antimicrobial
# ---------------------------------------------------
class AntimicrobialRegistry(Registry):
    """Registry for antimicrobials"""

    reg = None

    def combine(self, dataframe, on='name'):
        """Combines an external dataframe with the registry.

        .. note: I am assuming the columns that exist in dataframe...

        Parameters
        ----------

        Returns
        --------
        """
        # Load
        from pyamr.datasets.load import load_registry_antimicrobials

        # Copy DataFrame
        aux = dataframe.copy(deep=True)

        # Format
        aux[on] = aux[on].str.capitalize()

        # Load registry information
        if self.reg is None:
            self.reg = load_registry_antimicrobials()

        # --------------
        # Step 1
        # --------------
        # First, merge those rows within gram_stain and taxonomy
        # that have equal genus and species. Note that we are
        # only merging if both values exist and are equal.
        # Merge
        aux = pd.merge(aux, self.reg,
            how='left',
            left_on=[on],
            right_on=['name']
        )

        # Return
        return aux








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