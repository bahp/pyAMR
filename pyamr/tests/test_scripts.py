# Libraries
import pytest
import pathlib
import runpy

from mock import patch

# Find the examples folder
examples = pathlib.Path(__file__, '../../../', 'examples').resolve()

# Find all the scripts
scripts_tutorial = (examples / 'tutorial').glob('**/*.py')

#@pytest.mark.parametrize('script', scripts_tutorial)
#def test_script_execution_widgets(script):
#    runpy.run_path(str(script))


# .. note: For some reason, I have not managed to combine
#          parametrize and mock together into one single
#          method.
@patch('matplotlib.pyplot.show')
def test_script_run_no_show(self):
    for f in scripts_tutorial:
        runpy.run_path(str(f))