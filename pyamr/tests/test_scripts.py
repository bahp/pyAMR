# Libraries
import pytest
import pathlib
import runpy

from mock import patch

# Find the examples folder
examples = pathlib.Path(__file__, '../../../', 'examples').resolve()

# Find all the scripts
scripts_tutorial = (examples / 'tutorial').glob('**/*.py')
scripts_visualisation = (examples / 'visualisation').glob('**/*.py')

#@pytest.mark.parametrize('script', scripts_tutorial)
#def test_script_execution_widgets(script):
#    runpy.run_path(str(script))


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

# .. note: For some reason, I have not managed to combine
#          parametrize and mock together into one single
#          method.
@patch('matplotlib.pyplot.show')
def test_script_run_examples_tutorials_no_show(self):
    for f in (examples / 'tutorials').glob('**/*.py'):
        runpy.run_path(str(f))

"""
@patch('matplotlib.pyplot.show')
def test_script_run_examples_forecasting_no_show(self):
    for f in (examples / 'forecasting').glob('**/*.py'):
        runpy.run_path(str(f))
"""

"""
@patch('matplotlib.pyplot.show')
def test_script_run_examples_indexes_no_show(self):
    for f in (examples / 'indexes').glob('**/*.py'):
        runpy.run_path(str(f))
"""

"""
@patch('matplotlib.pyplot.show')
def test_script_run_examples_visualization_no_show(self):
    for f in (examples / 'visualization').glob('**/*.py'):
        runpy.run_path(str(f))
"""