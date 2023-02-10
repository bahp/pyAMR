# Libraries
import pytest
import numpy as np
import pandas as pd

# Specific
from pyamr.core.sari import sari
from pyamr.core.asai import asai
from pyamr.core.sari import SARI
from pyamr.core.asai import ASAI
from pyamr.core.mari import MARI

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

@pytest.fixture
def fixture4():
    return pd.read_csv('pyamr/fixtures/fixture_4.csv')

@pytest.fixture
def fixture5():
    return pd.read_csv('pyamr/fixtures/fixture_5.csv')

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
#   Multiple Antibiotic Resistance Index (MARI)
# ----------------------------------------------
def test_mari_class(fixture5):
    r, isolates = MARI().compute(fixture5,
        return_frequencies=True,
        retyrn_isolates=False)
    assert r.shape[0] == 3

def test_mari_class_temporal_iti(fixture5):
    r = MARI().compute(fixture5, shift='1D',
        period=1, cdate='DATE',
        return_isolates=False)
    assert r.shape[0] == 7

def test_mari_class_temporal_oti(fixture5):
    r = MARI().compute(fixture5, shift='1D',
        period='2D', cdate='DATE',
        return_isolates=False)
    assert r.shape[0] == 7


# ---------------------------------------------------
#   Antimicrobial Spectrum of Activity Index (ASAI)
# ---------------------------------------------------
def test_asai_error_missing_column_resistance(fixture4):
    with pytest.raises(ValueError):
        r = fixture4.drop(columns=['RESISTANCE']) \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai)

def test_asai_error_missing_column_genus(fixture4):
    with pytest.raises(ValueError):
        r = fixture4.drop(columns=['GENUS']) \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai)

def test_asai_error_missing_column_specie(fixture4):
    with pytest.raises(ValueError):
        r = fixture4.drop(columns=['SPECIE']) \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai)

def test_asai_error_missing_column_wgenus(fixture4):
    with pytest.raises(ValueError):
        r = fixture4.drop(columns=['W_GENUS']) \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai)

def test_asai_error_threshold_double_defined(fixture4):
    with pytest.warns():
        r = fixture4 \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai, threshold=0.6)

def test_asai_error_threshold_not_defined(fixture4):
    with pytest.warns():
        r = fixture4.drop(columns=['THRESHOLD']) \
            .groupby(['ANTIBIOTIC']) \
            .apply(asai)

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

