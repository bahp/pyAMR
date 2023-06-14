"""
Plot function
=============

# Code source: Óscar Nájera
# License: BSD 3 clause
"""

import numpy as np
import matplotlib.pyplot as plt



def main():
    x = np.linspace(-1, 2, 100)
    y = np.exp(x)

    plt.figure()
    plt.plot(x, y)
    plt.xlabel('$x$')
    plt.ylabel(r'$\exp(x)$')
    plt.title('Exponential function')

    plt.figure()
    plt.plot(x, -np.exp(-x))
    plt.xlabel('$x$')
    plt.ylabel(r'$-\exp(-x)$')
    plt.title('Negative exponential\nfunction')
    # To avoid matplotlib text output
    plt.show()

if __name__ == '__main__':
    main()