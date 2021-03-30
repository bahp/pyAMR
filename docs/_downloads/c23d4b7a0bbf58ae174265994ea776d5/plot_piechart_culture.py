"""
Piechart Cultures
=================

Example using your package
"""

from __future__ import division

# Libraries.
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# Matplotlib font size configuration.
mpl.rcParams['font.size'] = 9.0

# ------------------------------------------------------------------------
#                            HELPER METHODS
# ------------------------------------------------------------------------
def transparency(cmap, alpha):
    """
    """
    for i,rgb in enumerate(cmap):
        cmap[i] = rgb + (alpha,)
    return cmap

# ------------------------------------------------------------------------
#                            CONFIGURATION
# ------------------------------------------------------------------------
# Common configuration.
title_font_size = 30
labels = ['BLD', 'SPT','WOU', 'URI', 'OTH'] # labels
labels_empty = ['', '', '', '', '']         # labels empty
colors = transparency(sns.color_palette("Set2", desat=0.75, n_colors=7), 0.4)
explode = (0,0,0,0,0)   # proportion with which to offset each wedge
autopct = '%1.0f%%'       # print values inside the wedges  
pctdistance = 0.4         # ratio betwen center and text (default=0.6)
labeldistance = 0.7       # radial distance wich pie labels are drawn
shadow = False            # shadow
startangle = 90           # rotate piechart (default=0)
radius = None             # size of piechart (default=1)
counterclock = False      # fractions direction.
center = (0,0)            # center position of the chart.
frame = False             # plot axes frame with the pie chart.

# map with arguments for the text objects.
textprops = {'fontsize':'x-large'}

# map with arguments for the wedge objects.           
wedgeprops = {}

# Color manually selected 
colors_manual = ['mediumpurple',  
                 'violet',                           
                 'mediumaquamarine',
                 'lightskyblue', 
                 'lightsalmon',
                 'indianred'] 




# -------------------------------------------------------------------------
#                              FIGURE 1
# -------------------------------------------------------------------------
# Number of pathology laboratory data for each of the selected biochemical
# markers (ALP, ALT, BIL, CRE, CRP, WBC) for the non-infection category
# during the years 2014 and 2015.

# Portions.
sizes = [6, 7, 26, 30, 31] # Add proportions

# reset feature
startangle = 90

# Plot
plt.figure()
plt.pie(sizes,             
        explode=explode,     
        labels=labels,   # Use: labels / labels_empty   
        colors=colors,   # Use: colors / colors_manual 
        autopct=autopct,   
        pctdistance=pctdistance,
        labeldistance=labeldistance,
        shadow=shadow,       
        startangle=startangle,
        radius=radius,
        counterclock=counterclock,
        center=center,
        frame=frame,
        textprops=textprops,
        wedgeprops={'linewidth':0.35,
                    'edgecolor':'k'})

# Format figure.
plt.axis('equal')
plt.tight_layout()
plt.title("", fontsize=title_font_size)          # Add title.
#plt.legend(labels=labels, fontsize='xx-large')  # Add legend.


# Show figures
plt.show()