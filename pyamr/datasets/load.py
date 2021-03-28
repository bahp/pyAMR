# Division
from __future__ import division

# Generic libraries
import os
import sys
import warnings
import numpy as np
import pandas as pd
# import cPickle as pickle # no needed in python 3.x

# Import specific
from os.path import dirname

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
    path = './microbiology/sample/susceptibility-20210324-194524.csv'
    # Load
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
