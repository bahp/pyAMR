"""
Plotting a gaussian (tutorial)
==============================

Example ``matplotlib`` to plot a gaussian.

"""
#######################################
# Let's import numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt


#######################################
# -------------------------------------
# Methods
# -------------------------------------
# First, lets define the gaussian method
def gaussian(x, mu=0, sig=1):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


#############################
# ---------------------------
# Main
# ---------------------------
# Lets create the x and y values
x = np.linspace(-3, 3, 120)
y = gaussian(x)

#############################
# Lets plot using matplotlib
plt.plot(x, y)
plt.show()