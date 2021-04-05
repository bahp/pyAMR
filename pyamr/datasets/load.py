# Division
from __future__ import division

# Generic libraries
import os
import sys
import glob
import warnings
import numpy as np
import pandas as pd
# import cPickle as pickle # no needed in python 3.x

# Import specific
from os.path import dirname
from pathlib import Path

# Import own module
sys.path.append('../../')

# Import libraries
import pyamr.utils.io.read as pd_read

# --------------------------------------
# DEFINITION OF DATABASE PATHS
# --------------------------------------
# This paths should be relative to the folder datasets in which they
# are contained. Otherwise it will not work.

# Create dirname
dirname = dirname(__file__)

# ---------
# nhs
# ---------
# Antibiotics
epicimpoc_antibiotics = './nhs/antibiotics/antibiotics.csv'

# Organisms
epicimpoc_organisms = './nhs/organisms/organisms.csv'

# Profiles
epicimpoc_susceptibility_comp = './nhs/susceptibility/complete'
epicimpoc_susceptibility_year = './nhs/susceptibility/by_year'
epicimpoc_susceptibility_type = './nhs/susceptibility/by_cultures'

# Microbiology data


# Other
other_shampoo_sales = './other/shampoo_sales.csv'


# -----------------------------------------------------------------------------
#                              HELPER METHODS
# -----------------------------------------------------------------------------
def make_timeseries():
    """This method creates a hard-coded time series.

    Returns
    -------
    x, y, f:
      The x values, the y values and the frequencies.

    """
    # Create exogenous variable
    x = np.arange(100)
    # Create endogenous variable
    y = np.concatenate((np.arange(50) * 10 + np.random.randn(50) * 20 + 40,
                        np.arange(50) * 2 + np.random.randn(50) * 20 + 400))
    # Create frequency variable
    f = np.concatenate((np.random.rand(35) * 50 + 50,
                        np.random.rand(30) * 50 + 100,
                        np.random.rand(35) * 50 + 150))
    # Return
    return x, y, f


def make_susceptibility():
    """This method loads susceptibility.

    .. note: Default path
    """
    # Define path
    path = './microbiology/sample/nhs-susceptibility-2009.csv'
    # Return
    return pd.read_csv("{0}/{1}".format(dirname, path))


def load_registry_microorganisms():
    """This method returns the microorganisms registry"""
    # Define path
    path = './microbiology/registry/microorganisms/registry_microorganisms.csv'
    # Return
    return pd.read_csv("{0}/{1}".format(dirname, path))


def load_registry_antimicrobials():
    """This method returns the antimicrobials registry"""
    # Define path
    path = './microbiology/registry/antimicrobials/registry_antimicrobials.csv'
    # Return
    return pd.read_csv("{0}/{1}".format(dirname, path))


def load_microbiology_folder(path, folder,
        glob_pattern='susceptibility-*.csv', **kwargs):
    """This method loads the susceptibility data.

    .. note:: It assumes all the susceptibility data is stored in csv
              files whose files name starts with 'susceptibility'. In
              addition, it assumes that the additional iformation is
              is available in files named 'antimicrobials.csv' and
              'microorganisms.csv'

    Parameters
    ----------
    path: string
        The path where the folder is located.
    folder: string
        Name of the folder with the data.
    kwargs:
        Arguments to pass to pd.read_csv

    Returns
    -------
    susceptibility
        The susceptibility test data
    db_abxs
        The registries with the antimicrobials
    db_orgs
        The registry with the microorganisms
    """
    # Define paths
    path = Path("{0}/{1}".format(dirname, path))
    path_sus = path / folder
    path_abx = path / folder / 'antimicrobials.csv'
    path_org = path / folder / 'microorganisms.csv'

    # Load data
    data = pd.concat([ \
        pd.read_csv(f, parse_dates=['date_received'], **kwargs)
            for f in glob.glob(str(path_sus / glob_pattern))])

    # Load databases (registries)
    db_abxs = pd.read_csv(path_abx)
    db_orgs = pd.read_csv(path_org)

    # Return
    return data, db_abxs, db_orgs


def load_data_nhs(folder='susceptibility-v0.0.2', **kwargs):
    """This method loads the susceptibility data.

    """
    return load_microbiology_folder( \
        path='./microbiology/nhs/aggregated/',
        folder=folder, **kwargs)


def load_data_mimic(folder='susceptibility-v0.0.1', **kwargs):
    """This method loads the susceptibility data.

    """
    return load_microbiology_folder( \
        path='./microbiology/mimic/aggregated/',
        folder=folder, **kwargs)

# --------------------------------------
# METHODS TO LOAD DATABASES
# --------------------------------------
# -----------------
# epic impoc basic
# -----------------
def dataset_epicimpoc_antibiotics(**kwargs):
    return pd.read_csv('%s/%s' % (dirname, epicimpoc_antibiotics), *kwargs)

def dataset_epicimpoc_organisms(**kwargs):
    return pd.read_csv('%s/%s' % (dirname, epicimpoc_organisms), *kwargs)


# -----------------------------------
# epic impoc susceptibility test data
# -----------------------------------
def dataset_epicimpoc_susceptibility(**kwargs):
    """
    """
    return pd_read.read_csv('%s/%s' % \
      (dirname, epicimpoc_susceptibility_comp), **kwargs)

def dataset_epicimpoc_susceptibility_year(year='2014', **kwargs):
    """
    """
    return pd_read.read_csv('%s/%s/%s' % \
      (dirname, epicimpoc_susceptibility_year, str(year)), **kwargs)

def dataset_epicimpoc_susceptibility_culture(cultures=['bldcul']):
    """
    """
    pass



def dataset_shampoo_sales(**kwargs):
    return pd.read_csv('%s/%s' % (dirname, other_shampoo_sales), **kwargs)



if __name__ == '__main__':

    # Import
    import warnings

    # Suppress warnings
    warnings.simplefilter('ignore')

    # Set numpy options
    np.set_printoptions(threshold=np.nan)

    # -----------------------------------
    # Loading default datasets
    # -----------------------------------
    # Load antibiotics
    antibiotics = dataset_epicimpoc_antibiotics()

    # Load organisms
    organisms = dataset_epicimpoc_organisms()

    # Load profiles
    #microbiology = dataset_epicimpoc_susceptibility_year(year=2014)


    # Show information
    print(antibiotics.head(5))
    print(organisms.head(5))
    print(len(microbiology))

    print(dataset_shampoo_sales())
