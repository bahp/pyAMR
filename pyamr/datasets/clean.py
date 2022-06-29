# Libraries
import re
import collections
import numpy as np
import pandas as pd

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
SENSITIVITY_CODE_REPLACE = {
    'ss': 's',
}


ANTIMICROBIAL_CODE_REPLACE = {
    'AAUGU': 'AAUG'
}

MICROORGANISM_CODE_REPLACE = {
    'ACINE2': 'ACINE',
    'CNS2': 'CNS',
    'CNS3': 'CNS',
    'ECOL2': 'ECOL',
    'KPN2': 'KPNE',
    'PAER2': 'PAER',
    'SAUR2': 'SAUR',
    'LFC2': 'LFC',
    'COLIF2': 'COLIF',
    'COLI2': 'COLIF',
    'ENTAE2': 'EAER',
    'ENTAE': 'EAER',
    'VRE': 'ENTC',
    'MRSA': 'SAUR',
    'MCNS': 'CNS',
    'A_ECOLI': 'ECOL',
    'A_ENTEROBA': 'ENTB',
    'A_SVIRIDANS': 'VIRST',
    'A_CLUSITANI': 'CLUS',
    'A_CDUBLINIE': 'CDUB',
    'A_CPSEUDODI': 'CPSEU'
}

ANTIMICROBIAL_NAME_MAP = {
    '\([^)]*\)': '',  # Remove everything between ()
    '\s{2,}': ' ',  # Remove duplicated spaces
    'gentamicin 200': 'gentamicin'
}

MICROORGANISM_NAME_MAP = {
    # Replace basic
    'strep\.': 'streptococcus ',
    'staph\.': 'staphylococcus ',
    'species': 'sp.',
    'sp.($| )': '',
    'sp(.)?($| )': ' ',
    'second': '',
    'third': '',
    '2nd': '',
    '3rd': '',
    # Specific
    '\*\*\* mrsa \*\*\* isolated': 'staphylococcus aureus',

}

def invert(d):
    return {v:k for k,v in d.items()}

#def invert(d):
#    return reversed(list(d.items()))

# .. note: Keep everything lowercase because all the
#          columns are str.lower() before doing any
#          formatting/replacement in clean_common.
#
# .. note: Using an ordered dict. Thus, when inverting
#          the dictionaries, for repeated entries
#          (e.g. sensitive SS and S) the latter will
#          be used.
SPECIMEN_CODE_MAP = {
    'URNCUL': 'URICUL'
}

SPECIMEN_NAME_MAP = {
    'Urine Micro': 'Urine Culture'
}

# '9MRSN': 'MRSCUL',
# 'URINE CULTURE': 'URICUL',
# 'WOUND CULTURE': 'WOUCUL',
# 'BLOOD CULTURE': 'BLDCUL',
# 'SPUTUM CULTURE': 'SPTCUL',
##'CSF CULTURE': 'CSFCUL',
# 'EYE CULTURE': 'EYECUL',
# 'GENITALCUL': 'GENCUL',
# 'NEONATAL SCREEN': 'NEOCUL',

METHOD_CODE_MAP = {
    'DD': 'Disk Difussion',
    'PHO': 'Public Health Laboratory',
    'MIC': 'Minimum Inhibitory Concentration',
    'MASTU': 'Microscopy-Based Antimicrobial Susceptibility Testing',
}

SENSITIVITY_CODE_MAP = collections.OrderedDict({
    'ss': 'sensitive',
    's': 'sensitive',
    'r': 'resistant',
    'i': 'intermediate',
    'nd': 'not done',
    'hr': 'highly resistant',
    '<<do not report>>': 'hide',
    'hide': '<<do not report>>',
    'validation fix entry': 'fix',
    'fix': 'validation fix entry',
})

# Note that they will be executed in order and thus
# order matters. The changes on the first expression
# will affect the cells that will be used in the next
# iteration
REGEX_MAP = {
    '\([^)]*\)': '',        # Remove everything between ()
    '(\s)?\-(\s)?': '-',    # Remove spaces before after hyphen
    'species': '',          # Rename species for next regexp
    'o157': '',             # Remove scherichia coli o157
    'sp(\.)?(\s|$)+': ' ',  # Remove sp from word.
    'sp..': ' ',            # Remove sp.. <--- HOW TO DO IT WITH PREVIOUS!
    'strep(\.|\s|$)': 'streptococcus ',  # Complete
    'staph(\.|\s|$)': 'staphylococcus ', # Complete
    'staphylococci': 'staphylococcus',   # Correction (add mixed? group?)
    'streptococci': 'streptococcus',     # Correction (add mixed? group?)
    '\s+': ' ',             # Remove duplicated spaces.
}

REGEX_MAP_BASIC = {
    '\s+': ' ',  # Remove duplicated spaces.
}


# -----------------------------------------------------------
# Helper methods
# -----------------------------------------------------------

def hyphen_before(x, w):
    """Ensures hyphen between words is correct.

    Parameters
    ----------
    x: string
        The string to format
    w: string
        The word preceded by hyphen.

    Returns
    -------
    string
        The formatted string
    """
    # Ensure it is a string
    if not isinstance(x, str):
        return x
    # Create expression
    regexp = re.compile(r'(\S*)(\s+)(%s)(\W)+'%w)
    # Return
    return re.sub(regexp, r'\1-\3 ', x)


def word_to_start(x, w, pos='start', verbose=0):
    """Moves the word within the string.

    Parameters
    ----------
    x: string
        The string to format
    w: word
        The word to relocate within the string.
    pos: string, default start
        The position to insert the word. The possible options
        are start (at the beginning) or end (at the end) of the
        string.
    verbose: int
        Level of verbosity

    Returns
    -------
    string
        Formatted string
    """
    # Ensure it is a string
    if not isinstance(x, str):
        return x
    # Create regular expression
    regexp = re.compile(\
        r'(.*|^)(\W|^)%s(\W|$)(.*|$)' % w,
        flags=re.IGNORECASE)
    # Return value if it does not fit.
    if not bool(re.match(regexp, x)):
        return x
    # Return
    if pos == 'start':
        return '%s ' % w + x.replace(w, '')
    if pos == 'end':
        return x.replace(w, '') + ' %s' % w

def string_replace(series, remove={}):
    """This method corrects the strings.

    Parameters
    ----------
    series:

    remove:

    Returns
    -------
    """
    # Format (lower)
    series = series.str.lower()
    # Do str replacements
    for k, v in remove.items():
        series = series.str.replace(k, v)
    # Format (strip)
    series = series.str.strip()
    # Return
    return series



# ----------------------------------------------------
# Main cleaners
# ----------------------------------------------------
def clean_basic(data):
    """Performs the basic cleaning.

    1. Everything to lowercase
    2. Remove spaces begin/end (strip)
    3. Remove duplicate spaces (regexp)
    4. Remove duplicates

    Parameters
    ----------
    data: pd.DataFrame
        The data to clean.

    Returns
    -------
    pd.DataFrame
        The cleaned data
    """
    # Copy dataframe
    data = data.copy(deep=True)

    # Put everything to lowercase
    data = data.applymap(lambda x: x.lower()
        if isinstance(x, str) else x)

    # Drop all spaces
    data = data.applymap(lambda x: x.strip()
        if isinstance(x, str) else x)

    # Drop extra spaces
    #{'\s+': ' '}  # Remove duplicated spaces.

    # Basic formatting
    data = data.drop_duplicates()

    # Return
    return data


def clean_format(data):
    """Final formatting..."""

    aux = data.copy(deep=True)

    # Format title
    for c in ['patient_name',
              'patient_surname']:
        if c in aux:
            aux[c] = aux[c].str.title()

    # Format lower (not needed)
    for c in ['antimicrobial_name',
              'microorganism_name',
              'sensitivity_name',
              'method_name']:
        if c in aux:
            aux[c] = aux[c].str.lower()

    # Format upper
    for c in ['antimicrobial_code',
              'microorganism_code',
              'sensitivity_code',
              'method_code']:
        if c in aux:
            aux[c] = aux[c].str.upper()

    # Strip strings
    aux = aux.apply(lambda x: x.str.strip() \
        if x.dtype == "object" else x)

    # Format date-times
    for c in ['date_received', 'date_outcome']:
        if c in aux:
            aux[c] = pd.to_datetime(aux[c], errors='coerce')

    # Drop duplicates
    aux = aux.drop_duplicates()


def clean_clwsql008(data, clean_microorganism=True):
    """Performs cleaning for clwsql008 data

    1. rename columns
    2. clean basic
    3. correct issue with sensitivities
    4. correct issue with date_received

    Parameters
    ----------
    data: pd.DataFrame
        The data to clean.

    Returns
    -------
    pd.DataFrame
        The cleaned data
    """

    # ---------------------------------
    # Constants
    # ---------------------------------
    # Rename columns
    rename = {
        'DiagnosticTestID': 'uuid',
        'ReceiveDate': 'received_date',
        'ReceiveTime': 'received_time',
        'PtNumber': 'patient_hos_number',
        'AccNumber': 'laboratory_number',
        'BatTstCode': 'specimen_code',
        'OrderName': 'specimen_name',
        'SpecType': 'specimen_description',
        'OrgPieceCounter': 'microorganism_piece_counter',
        'OrgCode': 'microorganism_code',
        'Organism': 'microorganism_name',
        'DrugCode': 'antimicrobial_code',
        'AntiBiotic Name': 'antimicrobial_name',
        'SensMethod': 'method_code',
        'Sensitivity': 'sensitivity_name',
        'MIC': 'mic',
        'Reported': 'reported',
        'FinalDate': 'date_outcome'
    }

    # There are both code and names merged.
    sensitivity_code_map = {
        's': 'sensitive',
        'ss': 'sensitive',
        'r': 'resistant',
        'i': 'intermediate',
        'nd': 'not done',
        'hr': 'highly resistant',
        'hide': 'hide',
        'fix': 'validation fix entry'
    }

    sensitivity_name_map = {
        'sensitive': 's',
        'resistant': 'r',
        'intermediate': 'i',
        'not done': 'nd',
        'highly resistant': 'hr',
        'hide': 'hide',
        '<<do not report>>': 'hide',
        'validation fix entry': 'fix'
    }

    # --------------------------
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values
    data = data.rename(columns=rename)
    data = clean_basic(data)
    #data = data.convert_dtypes()

    # --------------------------
    # Correct sensitivities
    # --------------------------
    # Replace codes with the names
    data['sensitivity_name'] = \
        data.sensitivity_name.replace(sensitivity_code_map)
    # Map names to corresponding codes
    data['sensitivity_code'] = \
        data.sensitivity_name.map(sensitivity_name_map)

    # --------------------------
    # Add method name
    # --------------------------
    data['method_name'] = data.method_code

    # --------------------------
    # Clean microorganism
    # --------------------------
    if clean_microorganism:
        # Create registry
        from pyamr.datasets.registries import MicroorganismRegistry

        # Create registry
        rego = MicroorganismRegistry(keyword='microorganism').fit(data)

        # Format microorganism name
        data.microorganism_name = \
            rego.replace(data.microorganism_name,
                key='original', value='name')

    # --------------------------
    # Add date
    # --------------------------
    # Add new column date
    data['date_received'] = pd.to_datetime(
        data.received_date + ' ' + data.received_time, errors='coerce')

    # Format date-times
    for c in ['date_received', 'date_outcome']:
        if c in data:
            data[c] = pd.to_datetime(data[c], errors='coerce')

    # Return data
    return data


def clean_legacy(data, clean_microorganism=True, verbose=10):
    """This method cleans microbiology data from legacy.

    1. Rename columns
    2. clean basic
    3. Add sensitivity code
    4. Correct specimen issue

    Parameters
    ----------
    data: pd.DataFrame
        The data to clean

    Returns
    -------
    pd.DataFrame
        The cleaned data
    """
    # ---------------------------------
    # Constants
    # ---------------------------------
    # Rename columns
    rename = {
        'dateReceived': 'date_received',
        'age': 'age',
        'gender': 'gender',
        'patNumber': 'patient_hos_number',
        'labNumber': 'laboratory_number',
        'orderCode': 'specimen_code',
        'orderName': 'specimen_name',
        'specimenType': 'specimen_description',
        'OrgPieceCounter': 'microorganism_piece_counter',
        'organismCode': 'microorganism_code',
        'organismNameOrig': 'microorganism_name',
        'antibioticCode': 'antimicrobial_code',
        'antibioticName': 'antimicrobial_name',
        'sensitivity': 'sensitivity_name'
    }

    # Map sensitivity names with codes.
    sensitivity_name_map = {
        'sensitive': 's',
        'resistant': 'r',
        'intermediate': 'i',
        'not done': 'nd',
        'highly resistant': 'hr',
        '<<do not report>>': 'hide',
        'validation fix entry': 'fix'
    }


    # --------------------------
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values
    # Drop duplicates
    data = data.rename(columns=rename)
    data = clean_basic(data)
    #data = data.convert_dtypes() # issue with np.nan in replace

    # --------------------------
    # Correct sensitivities
    # --------------------------
    # Create column code
    data['sensitivity_code'] = \
        data.sensitivity_name.map(sensitivity_name_map)

    # --------------------------
    # Correct specimens
    # --------------------------
    # Get those with both name and code
    aux = data[['specimen_code', 'specimen_name']]
    aux = aux.dropna(how='any').drop_duplicates()
    tup1 = zip(aux.specimen_name, aux.specimen_code)
    tup2 = zip(aux.specimen_code, aux.specimen_name)

    # Replace names that appear in code
    data.specimen_code = data.specimen_code.replace(dict(tup1))

    # Fill missing (NaN) names
    data.specimen_name = data.specimen_name \
        .fillna(data.specimen_code.replace(dict(tup2)))

    # --------------------------
    # Add method code/name
    # --------------------------
    data['method_name'] = None
    data['method_code'] = None

    # --------------------------
    # Clean microorganism
    # --------------------------
    if clean_microorganism:
        # Create registry
        from pyamr.datasets.registries import MicroorganismRegistry

        # Create registry
        rego = MicroorganismRegistry(keyword='microorganism').fit(data)

        # Could I do it with fit_transform(data)

        # Format microorganism name
        data.microorganism_name = \
            rego.replace(data.microorganism_name,
                key='original', value='name')

    # Format date-times
    for c in ['date_received', 'date_outcome']:
        if c in data:
            data[c] = pd.to_datetime(data[c], errors='coerce')

    # Return
    return data







































def clean_microorganism(data):
    """This method...."""
    # Copy data
    aux = data.copy(deep=True)

    # Add backup columns
    microorganism_name_original = \
        aux.microorganism_name

    # Put everything to lowercase
    aux = aux.applymap(lambda x: x.lower()
        if isinstance(x, str) else x)

    # Save microorganism name origina
    aux['microorganism_name_original'] = \
        microorganism_name_original

    # Apply regexp mapping
    aux.microorganism_name = \
        aux.microorganism_name.replace(regex=REGEX_MAP_MICROORGANISM)

    # Correct hyphens
    for hp in ['haemolytic']:
        aux.microorganism_name = \
            aux.microorganism_name.str.lower() \
                .transform(hyphen_before, w=hp)

    # Correct order of genus
    for sp in ['enterococcus',
               'staphylococcus',
               'streptococcus',
               'coliform']:
        aux.microorganism_name = \
            aux.microorganism_name.str.lower() \
                .transform(word_to_start, w=sp, pos='start')

    # Correct order of tags
    for sp in ['methicillin resistant',
               'vancomycin resistant',
               'mixed']:
        aux.microorganism_name = \
            aux.microorganism_name.str.lower() \
                .transform(word_to_start, w=sp, pos='end')

    # Apply regexp mapping
    aux = aux.replace(regex=REGEX_MAP)

    # Strip
    aux.microorganism_name = \
        aux.microorganism_name.str.strip()


    keep = ['microorganism_name',
            'microorganism_code',
            'microorganism_name_original']

    # Sort
    aux = aux[keep]
    aux = aux.drop_duplicates(subset=['microorganism_name'])
    aux = aux.sort_values(by='microorganism_name')
    aux = aux.reset_index(drop=True)
    aux.insert(0, 'microorganism_id', aux.index)

    # Return
    return aux



def clean_common(data, verbose=10):
    """This method cleans the microbiology data.

    It assumes the following columns are imputed:
       date_received
       date_outcome
       microorganism_code
       microorganism_name (required = True)
       antimicrobial_code
       antimicrobial_name
       method_code
       method_name
       sensitivity_code
       sensitivity_name

    Parameters
    ----------
    data: pd.DataFrame
        The dataframe to clean

    Returns
    -------
    pd.DataFrame
        The cleaned dataframe
    """
    # ------------------------------
    # Constants
    # ------------------------------
    # Create required columns
    required = [
        'date_received',
        'date_outcome',
        'specimen_name',
        'microorganism_name',
        'antimicrobial_name',
        'method_name',
        'sensitivity_name']

    # Copy data
    aux = data.copy(deep=True)

    # Add required columns
    for c in required:
        if not c in aux.columns:
            aux[c] = None

    # ------------------------------
    # Missing columns and replace
    # ------------------------------
    # Add backup columns
    aux['microorganism_name_original'] = \
        aux.microorganism_name
    aux['antimicrobial_name_original'] = \
        aux.antimicrobial_name

    # Put everything to lowercase
    aux = aux.applymap(lambda x: x.lower()
        if isinstance(x, str) else x)

    for c in ['specimen', 'method', 'sensitivity']:
        c_name = '%s_name' % c
        c_code = '%s_code' % c
        if c_code not in aux:
            aux[c_code] = aux[c_name]
        aux[c_name].fillna(aux[c_code], inplace=True)

    # Verbose
    if verbose > 5:
        print("Formatting... specimen/method/sensitivity.")

    # .. note: It would be also possible to forget about the
    #          codes and create our own acronyms ensuring that
    #          they are unique.
    # Fix codes (ss -> s)
    if 'sensitivity_code' in aux:
        aux.sensitivity_code = \
            aux.sensitivity_code.replace(SENSITIVITY_CODE_REPLACE)
    if 'microorganism_code' in aux:
        aux.microorganism_code = \
            aux.microorganism_code.replace(MICROORGANISM_CODE_REPLACE)
    if 'antimicrobial_code' in aux:
        aux.antimicrobial_code = \
            aux.antimicrobial_code.replace(ANTIMICROBIAL_CODE_REPLACE)

    # Replace
    aux = aux.replace({
        'specimen_name': SPECIMEN_CODE_MAP,
        'specimen_code': invert(SPECIMEN_CODE_MAP),
        'method_name': METHOD_CODE_MAP,
        'method_code': invert(METHOD_CODE_MAP),
        'sensitivity_name': SENSITIVITY_CODE_MAP,
        'sensitivity_code': invert(SENSITIVITY_CODE_MAP)
    })

    # ------------------------------
    # Fixing orgs/abxs names
    # ------------------------------
    # Verbose
    if verbose > 5:
        print("Formatting... microorganism/antimicrobials.")

    # Apply regexp mapping
    aux = aux.replace(regex=REGEX_MAP)

    # Correct hyphens
    for hp in ['haemolytic']:
        aux.microorganism_name = \
            aux.microorganism_name.str.lower() \
                .transform(hyphen_before, w=hp)

    # Correct order of genus
    for sp in ['enterococcus',
               'staphylococcus',
               'streptococcus',
               'coliform']:
        aux.microorganism_name = \
            aux.microorganism_name.str.lower() \
                .transform(word_to_start, w=sp)

    # Apply regexp mapping
    aux = aux.replace(regex=REGEX_MAP)

    # ------------------------------
    # String formatting
    # ------------------------------
    # Verbose
    if verbose > 5:
        print("Formatting... lower/title/upper.")

    # Format title
    for c in ['patient_name',
              'patient_surname']:
        if c in aux:
            aux[c] = aux[c].str.title()

    # Format lower (not needed)
    for c in ['antimicrobial_name',
              'microorganism_name',
              'sensitivity_name',
              'method_name']:
        if c in aux:
            aux[c] = aux[c].str.lower()

    # Format upper
    for c in ['antimicrobial_code',
              'microorganism_code',
              'sensitivity_code',
              'method_code']:
        if c in aux:
            aux[c] = aux[c].str.upper()

    # Strip strings
    aux = aux.apply(lambda x: x.str.strip() \
        if x.dtype == "object" else x)

    # ------------------------------
    # Time formatting
    # ------------------------------
    # Verbose
    if verbose > 5:
        print("Formatting... date_received/date_outcome.")

    # Format date-times
    for c in ['date_received', 'date_outcome']:
        if c in aux:
            aux[c] = pd.to_datetime(aux[c], errors='coerce')

    # We could also use the convert_dtypes, however there is a big
    # issue with the pd.NA values. I think that issue is only if
    # we want to apply replace and there are pd.NA (only works with
    # np.nan) but it should be fine now that all that has been done.
    #aux = aux.convert_dtypes()

    # Remove empty (sensitivity, date_received, ...?)
    #aux = aux.dropna(how='any', subset=[])

    # Drop duplicates
    aux = aux.drop_duplicates()

    # Return
    return aux


def clean_clwsql008_old(data, verbose=10):
    """This method cleans microbiology data from clwsql008.

    .. notes: CLW-SQL-008
      - The sensitivity values found are
        { 'SS', 'R', 'ND', 'I', 'HIDE', 'HR' }

    .. note: Using UTC=True gives an error when using
             django-import-export to import the data in
             the databases (commented).

    Parameters
    ----------
    data: pd.DataFrame
        The dataframe with the data

    Returns
    -------
    pd.DataFrame
        The cleaned dataframe.
    """
    # ---------------------------------
    # Constants
    # ---------------------------------
    # Rename columns
    rename = {
        'DiagnosticTestID': 'uuid',
        'ReceiveDate': 'received_date',
        'ReceiveTime': 'received_time',
        'PtNumber': 'patient_hos_number',
        'AccNumber': 'laboratory_number',
        'BatTstCode': 'specimen_code',
        'OrderName': 'specimen_name',
        'SpecType': 'specimen_description',
        'OrgPieceCounter': 'microorganism_piece_counter',
        'OrgCode': 'microorganism_code',
        'Organism': 'microorganism_name',
        'DrugCode': 'antimicrobial_code',
        'AntiBiotic Name': 'antimicrobial_name',
        'SensMethod': 'method_code',
        'Sensitivity': 'sensitivity_code',
        'MIC': 'mic',
        'Reported': 'reported',
        'FinalDate': 'date_outcome'
    }

    # --------------------------
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values
    # Drop duplicates
    data = data.drop_duplicates()
    data = data.rename(columns=rename)
    #data = data.convert_dtypes()

    # Show
    if verbose > 5:
        print("\n")
        print(data.columns)

    # Add new columns
    data['date_received'] = pd.to_datetime(
        data.received_date + ' ' + data.received_time, errors='coerce')

    # Final formatting
    data = clean_common(data, verbose)

    # Return
    return data



def clean_legacy_old(data, verbose=10):
    """This method cleans microbiology data from legacy.

    .. notes: LEGACY
      - The sensitivities found are ...

    Parameters
    ----------
    data: pd.DataFrame
        The dataframe with the data

    Returns
    -------
    pd.DataFrame
        The cleaned dataframe.
    """
    # ---------------------------------
    # Constants
    # ---------------------------------
    # Rename columns
    rename = {
        'dateReceived': 'date_received',
        'age': 'age',
        'gender': 'gender',
        'patNumber': 'patient_hos_number',
        'labNumber': 'laboratory_number',
        'orderCode': 'specimen_code',
        'orderName': 'specimen_name',
        'specimenType': 'specimen_description',
        'OrgPieceCounter': 'microorganism_piece_counter',
        'organismCode': 'microorganism_code',
        'organismNameOrig': 'microorganism_name',
        'antibioticCode': 'antimicrobial_code',
        'antibioticName': 'antimicrobial_name',
        'sensitivity': 'sensitivity_name'
    }

    # --------------------------
    # Method
    # --------------------------
    # The method codes are given but the method names are not
    # included. We could use this opportunity to set their
    # values
    # Drop duplicates
    data = data.drop_duplicates()
    data = data.rename(columns=rename)
    #data = data.convert_dtypes() # issue with np.nan in replace

    # Show
    if verbose > 5:
        print("\n")
        print(data.columns)

    # Final formatting
    data = clean_common(data, verbose)

    # Return
    return data


def clean_mimic(data):
    """This method...

    .. note: Need to merge datetime for date and datetime for time
             as done in the datablend package if want full info.

    """
    # ---------------------------------
    # Constants
    # ---------------------------------
    # Rename columns
    rename = {
        'subject_id': 'patient_hos_number',
        'micro_specimen_id': 'laboratory_number',
        'spec_type_desc': 'specimen_description',
        'test_seq': 'microorganism_piece_counter',
        'org_name': 'microorganism_name',
        'ab_name': 'antimicrobial_name',
        'test_name' : 'method',
        'interpretation': 'sensitivity_name',
        'chartdate': 'date_received',
        'storedate': 'date_outcome'
    }

    # Replace values
    replace = {
        #'sensitivity': SENSITIVITY_MAP,
        'microorganism_code': MICROORGANISM_CODE_MAP,
        'microorganism_name': MICROORGANISM_NAME_MAP,
        'antimicrobial_code': ANTIMICROBIAL_CODE_MAP
    }

    # Rename
    data = data.rename(columns=rename)

    # Replace
    data = data.replace(replace)

    # Format
    data.microorganism_name = data.microorganism_name.str.capitalize()
    data.antimicrobial_name = data.antimicrobial_name.str.capitalize()
    data['microorganism_code'] = data.microorganism_name
    data['antimicrobial_code'] = data.antimicrobial_name
    data['specimen_code'] = data.specimen_description

    # Format date
    if 'date_received' in data:

        # Convert to datetime.
        data.date_received = \
            pd.to_datetime(data.date_received, errors='coerce')

        # Ignore those without result
        data = data[data.sensitivity.notna()]

    # Return
    return data