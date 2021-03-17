"""
Plotting a gaussian (script)
============================

Example ``matplotlib`` to plot a gaussian.

"""
# Libraries
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------
# Methods
# ---------------------------
def gaussian(x, mu=0, sig=1):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


# ---------------------------
# Configuration
# ---------------------------


# ---------------------------
# Main
# ---------------------------
# Load data
x = np.linspace(-3, 3, 120)
y = gaussian(x)

# Plot
plt.plot(x, y)

# Show
plt.show()
