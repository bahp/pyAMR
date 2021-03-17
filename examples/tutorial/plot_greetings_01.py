"""
Plotting greetings
============================

Example using your package
"""

# Libraries
from pyamr.utils.display import show
from pyamr.core.greetings import Hello
from pyamr.core.greetings import Morning

# -------------------------------------
# Constants
# -------------------------------------

# -------------------------------------
# Main
# -------------------------------------
# Execute show
show()

# Create instances
h = Hello()
m = Morning()

# Greet
h.greet(name='Maria')
m.greet(name='Damien')