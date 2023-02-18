# Libraries
import os
import pytest
import pathlib
import runpy

from mock import patch

# .. note: When using <runpy>, the patch works so that we avoid
#          running the pyplot.show method but the code run does
#          not count for coverage. When using <os> the opposite
#          happens.

# Find the examples folder
examples = pathlib.Path(__file__, '../../../', 'examples').resolve()
pyamr_core = pathlib.Path(__file__, '../../', 'core').resolve()
pyamr_stats = pathlib.Path(__file__, '../../', 'core/stats').resolve()

# Find all the scripts
scripts_tutorial = (examples / 'tutorial').glob('**/*.py')
scripts_visualisation = (examples / 'visualisation').glob('**/*.py')
scripts_stats = list((pyamr_core / 'stats').glob('**/*.py'))
scripts_core = (pyamr_core / 'stats').glob('*.py')
scripts_metrics = (pyamr_core / 'stats').glob('*.py')

pyamr = pathlib.Path(__file__, '../../').resolve()

# --------------------------------------
# Run scripts
# --------------------------------------
"""
@patch('matplotlib.pyplot.show')
def test_script_run_pyamr(self):
    for f in (pyamr).glob('**/*.py'):
        runpy.run_path(str(f))
"""


@patch('matplotlib.pyplot.show')
def test_script_run_pyamr_metrics(self):
    for f in (pyamr / 'metrics').glob('**/*.py'):
        os.system(str(f))
        runpy.run_path(str(f))

@patch('matplotlib.pyplot.show')
def test_script_run_pyamr_graphics(self):
    for f in (pyamr / 'graphics').glob('**/*.py'):
        os.system(str(f))
        runpy.run_path(str(f))

@patch('matplotlib.pyplot.show')
def test_script_run_pyamr_core(self):
    for f in (pyamr / 'core').glob('*.py'):
        os.system(str(f))
        #runpy.run_path(str(f))

@patch('matplotlib.pyplot.show')
def test_script_run_pyamr_core_regression(self):
    for f in (pyamr / 'core' / 'regression').glob('**/*.py'):
        os.system(str(f))
        #runpy.run_path(str(f))

@patch('matplotlib.pyplot.show')
def test_script_run_pyamr_core_stats(self):
    for f in (pyamr / 'core' / 'stats').glob('**/*.py'):
        os.system(str(f))
        #runpy.run_path(str(f))

@patch('matplotlib.pyplot.show')
def test_script_run_pyamr_core_table(self):
    for f in (pyamr / 'core' / 'table').glob('**/*.py'):
        os.system(str(f))
        #runpy.run_path(str(f))


"""
@patch('matplotlib.pyplot.show')
def test_script_run_core(self):
    for f in [pyamr_core / 'sari.py',
              pyamr_core / 'asai.py',
              pyamr_core / 'sart.py',
              pyamr_core / 'mari.py']:
        runpy.run_path(str(f))
"""
"""
def test_script_run_stats(self):
    #for f in [pyamr_stats / 'adfuller.py',
    #          pyamr_stats / 'correlation.py',
    #          pyamr_stats / 'kendall.py',
    #          pyamr_stats / 'kpss.py',
    #          pyamr_stats / 'stationarity.py']:
    #    print(f)
    #    #runpy.run_path(str(f))
    #    assert 4 == 5
    aux = pathlib.Path(__file__, '../../', 'core/stats').resolve()
    print(aux)
    assert 4==5
"""

"""
def test_script_execution_core_stats():
    f = pathlib.Path(__file__, '../../', 'core/stats').resolve()
    print(f / 'adfuller.py')
    runpy.run_path(str(f / 'adfuller.py'))
"""

"""
@pytest.mark.parametrize('script', scripts_stats)
def test_script_execution_core_stats(script):
    runpy.run_path(str(script))

@pytest.mark.parametrize('script', scripts_core)
def test_script_execution_core(script):
    runpy.run_path(str(script))
"""
"""
@pytest.mark.parametrize('script', scripts_tutorial)
def test_script_execution_widgets(script):
    runpy.run_path(str(script))
"""

"""
@patch('matplotlib.pyplot.show')
def test_script_run_visualisation_no_show(self):
    for f in scripts_visualisation:
        runpy.run_path(str(f))
"""

"""
@patch('matplotlib.pyplot.show')
def test_script_run_examples_no_show(self):
    for f in examples.glob('**/*.py'):
        runpy.run_path(str(f))
"""
"""
@patch('matplotlib.pyplot.show')
def test_script_run_examples_tutorials_no_show(self):
    for f in (examples / 'tutorials').glob('**/*.py'):
        runpy.run_path(str(f))
"""

"""
# .. note: For some reason, I have not managed to combine
#          parametrize and mock together into one single
#          method.
@patch('matplotlib.pyplot.show')
def test_script_run_examples_tutorials_no_show(self):
    for f in (examples / 'tutorials').glob('**/*.py'):
        runpy.run_path(str(f))
"""

"""
@patch('matplotlib.pyplot.show')
def test_script_run_examples_indexes_no_show(self):
    for f in (examples / 'indexes').glob('**/*.py'):
        runpy.run_path(str(f))

@patch('matplotlib.pyplot.show')
def test_script_run_examples_forecasting_no_show(self):
    for f in (examples / 'forecasting').glob('**/*.py'):
        runpy.run_path(str(f))

@patch('matplotlib.pyplot.show')
def test_script_run_examples_indexes_no_show(self):
    for f in (examples / 'indexes').glob('**/*.py'):
        runpy.run_path(str(f))

@patch('matplotlib.pyplot.show')
def test_script_run_examples_visualization_no_show(self):
    for f in (examples / 'visualization').glob('**/*.py'):
        runpy.run_path(str(f))
"""