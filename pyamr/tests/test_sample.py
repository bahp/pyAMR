# Libraries
import pytest
import numpy as np
import pandas as pd

# Specific
from pyamr.core.sari import sari
from pyamr.core.sari import SARI

# ----------------------------------------------------
#
# ----------------------------------------------------


def func(x):
    return x + 1


@pytest.fixture
def fixture():
    data = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1]
    ]
    return pd.DataFrame(data=data,
        columns=['resistant', 'intermediate', 'sensitive'])

@pytest.fixture
def fixture3():
    return pd.read_csv('pyamr/fixtures/fixture_3.csv')

def test_answer():
    """
    PyTest sample test
    :return:
    """
    assert func(3) == 4


# ----------------------------------------------
#   Single Antibiotic Resistance Index (SARI)
# ----------------------------------------------
def test_sari_method_empty(fixture3):
    assert 4 == 4

def test_sari_strategy_hard(fixture):
    r = sari(fixture, strategy='hard')
    assert isinstance(r, pd.Series)
    assert np.isnan(r.get(0))

def test_sari_strategy_soft(fixture):
    r = sari(fixture, strategy='soft')
    assert isinstance(r, pd.Series)
    assert np.isnan(r.get(0))

def test_sari_strategy_medium(fixture):
    r = sari(fixture, strategy='medium')
    assert isinstance(r, pd.Series)
    assert np.isnan(r.get(0))

def test_sari_strategy_basic(fixture):
    r = sari(fixture, strategy='basic')
    assert isinstance(r, pd.Series)
    assert np.isnan(r.get(0))
    assert np.isnan(r.get(2))

def test_sari_class_overall(fixture3):
    r = SARI().compute(fixture3)
    assert isinstance(r, pd.DataFrame)
    assert r.shape[0] == 4

def test_sari_class_timeseries(fixture3):
    r = SARI().compute(fixture3, period='year', cdate='DATE')
    assert isinstance(r, pd.DataFrame)
    assert r.shape[0] == 5
    assert 'DATE' in r.index.names

# ----------------------------------------------
#   Single Antibiotic Resistance Trend (SART)
# ----------------------------------------------