# Libraries
import pytest
import numpy as np
import pandas as pd

from pathlib import Path

# Specific
from pyamr.core.sari import sari
from pyamr.core.asai import asai
from pyamr.core.sari import SARI
from pyamr.core.asai import ASAI
from pyamr.core.mari import MARI

# ----------------------------------------------------
# Fixtures
# ----------------------------------------------------
# Define path to fixtures folder
fixtures_path = Path(__file__).parent.parent.absolute() / 'fixtures'

def func(x):
    return x + 1

@pytest.fixture
def fixture():
    """This ..."""
    data = [
        [0, 0, 0, np.NaN, np.NaN, np.NaN, np.NaN],
        [0, 0, 1, 0/1, 0.0/1, 0/1, 0/1],
        [0, 1, 0, 1/1, 0.5/1, 0/1, np.NaN],
        [0, 1, 1, 1/2, 0.5/2, 0/2, 0/1],
        [1, 0, 0, 1/1, 1.0/1, 1/1, 1/1],
        [1, 0, 1, 1/2, 1.0/2, 1/2, 1/2],
        [1, 1, 0, 2/2, 1.5/2, 1/2, 1/1],
        [1, 1, 1, 2/3, 1.5/3, 1/3, 1/2]
    ]
    return pd.DataFrame(data=data,
        columns=['resistant', 'intermediate', 'sensitive',
                 'hard', 'medium', 'soft', 'basic'])

def fixtur1():
    """This ..."""


@pytest.fixture
def fixture3():
    return pd.read_csv(fixtures_path / 'fixture_3.csv')

@pytest.fixture
def fixture4():
    return pd.read_csv(fixtures_path / 'fixture_4.csv')

@pytest.fixture
def fixture5():
    return pd.read_csv(fixtures_path / 'fixture_5.csv')

@pytest.fixture
def fixture_index_mari():
    return pd.read_csv(fixtures_path / 'indexes' / 'fixture_mari.csv')


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

def test_sari_empty_dataframe():
    with pytest.raises(Exception) as e:
        sari(pd.DataFrame())

@pytest.mark.parametrize("strategy",
    ['hard', 'medium', 'soft', 'basic',
     pytest.param('other', marks=pytest.mark.xfail)])
def test_sari_strategy(fixture, strategy):
    r = sari(fixture, strategy=strategy)
    assert isinstance(r, pd.Series)
    assert r.equals(fixture[strategy])

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
#   Multiple Antibiotic Resistance Index (MARI)
# ----------------------------------------------
def test_mari_class(fixture5):
    r, isolates = MARI().compute(fixture5,
        return_frequencies=True,
        retyrn_isolates=False)
    assert r.shape[0] == 3

def test_mari_class_temporal_oti(fixture5):
    r = MARI().compute(fixture5, shift='1D',
        period='2D', cdate='DATE',
        return_isolates=False)
    assert r.shape[0] == 7

def test_mari_class_temporal_iti_period_is_integer_fails(fixture5):
    with pytest.raises(Exception) as e:
        r = MARI().compute(fixture5, shift='1D',
            period=1, cdate='DATE',
            return_isolates=False)

# ---------------------------------------------------
#   Antimicrobial Spectrum of Activity Index (ASAI)
# ---------------------------------------------------
@pytest.mark.parametrize("columns,kwargs",
    [('RESISTANCE', {}),
     ('GENUS', {}),
     ('SPECIE', {}),
     ('FREQUENCY', {'weights':'frequency'}),
     ('W_GENUS', {'weights':'specified'}),
     ('W_SPECIE', {'weights':'specified'})])
def test_asai_error_missing_column(fixture4, columns, kwargs):
    with pytest.raises(ValueError):
        r = fixture4.drop(columns=columns) \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai, **kwargs)

def test_asai_warn_threshold_double_defined(fixture4):
    with pytest.warns():
        r = fixture4 \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai, threshold=0.6)

def test_asai_warn_threshold_not_defined(fixture4):
    with pytest.warns():
        r = fixture4.drop(columns=['THRESHOLD']) \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai, threshold=None)

def test_asai_weights_from_column(fixture4):
    r = fixture4 \
        .groupby(['ANTIBIOTIC']) \
        .apply(asai, verbose=0)
    assert r.shape[0] == 2

def test_asai_weights_uniform(fixture4):
    r = fixture4 \
        .groupby(['ANTIBIOTIC', 'GRAM']) \
        .apply(asai, weights='uniform')
    assert r.shape[0] == 4

def test_asai_weights_frequency(fixture4):
    r = fixture4 \
        .groupby(['ANTIBIOTIC', 'GRAM']) \
        .apply(asai, weights='frequency')
    assert r.shape[0] == 4

def test_asai_class(fixture4):
    scores = ASAI().compute(fixture4,
        groupby=['ANTIBIOTIC', 'GRAM'],
        weights='uniform',
        threshold=None,
        min_freq=0)
    assert scores.shape[0]==4


# --------------------------------------
# Statistical tests (statstools)
# --------------------------------------
