"""
Plotting greetings
============================

Example using your package
"""

# Libraries
from pkgname.utils.display import show
from pkgname.core.greetings import Hello
from pkgname.core.greetings import Morning

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