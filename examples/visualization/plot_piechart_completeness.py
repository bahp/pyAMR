"""
Piechart Profile Completeness
=============================

Example using your package
"""
#######################################################################
# Author: Bernard
# Date: 19/08/2016
# Description: This script creates PIECHARTS for the paper which 
#              describes the infection risk inference: "Evaluating
#              machine learning algorithms for infection risk inference
#              using routinely collected pathology labotartory data".
#
# Notes: The values can be changed to display other data.
#
# Useful links:
# @see: http://matplotlib.org/examples/color/named_colors.html
# @see: http://matplotlib.org/examples/color/colormaps_reference.html
# @see: http://matplotlib.org/api/patches_api.html#matplotlib.patches.Wedge
# @see: http://matplotlib.org/api/text_api.html#matplotlib.text.Text
#
#######################################################################

# Libraries.
import numpy as np
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
labels = ['P1','P2','P3','P4','P5','P6']    # labels
labels_empty = ['', '', '', '', '', '']     # labels empty
colors = transparency(sns.color_palette("Blues", n_colors=7), 0.75)
colors = colors[1:]       # First color is white...
explode = (0,0,0,0,0,0)   # proportion with which to offset each wedge
autopct = '%1.0f%%'       # print values inside the wedges  
pctdistance = 0.5         # ratio betwen center and text (default=0.6)
labeldistance = 0.7       # radial distance wich pie labels are drawn
shadow = False            # shadow.
startangle = 90           # rotate piechart (default=0)
radius = None             # size of piechart (default=1)
counterclock = False      # fractions direction.
center = (0,0)            # center position of the chart.
frame = False             # plot axes frame with the pie chart.

# map with arguments for the text objects.
textprops = {'fontsize':'x-large'}

# map with arguments for the wedge objects.           
wedgeprops = {}

# Color manually selected.
colors_manual = ['mediumpurple',      
                 'violet',                           
                 'mediumaquamarine',
                 'lightskyblue', 
                 'lightsalmon',
                 'indianred'] 

# ---------------------------------------------------------------------
#                              FIGURE 1
# ---------------------------------------------------------------------
# Number of complege profiles for each of the selected biochemical
# markers (ALP, ALT, BIL, CRE, CRP, WBC) for the non-infection category
# during the years 2014 and 2015.

# Portions.
sizes = [17, 7, 10, 8, 26, 32]               # proportions


# Plot.
plt.figure()
plt.pie(sizes,             
        explode=explode,     
        labels=labels,       # Use: labels / labels_empty  
        colors=colors,       # Use: colors / colors_manual 
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

# ---------------------------------------------------------------------
#                              FIGURE 2
# ---------------------------------------------------------------------
# Number of complete profiles for each of the selected biochemical
# markers (ALP, ALT, BIL, CRE, CRP, WBC) for the infection category
# during the years 2014 and 2015.

# Portions
sizes = [5, 5, 18, 6, 12, 54]                  # proportions

# Plot.
plt.figure()
plt.pie(sizes,             
        explode=explode,     
        labels=labels,      # Use: labels / labels_empty 
        colors=colors,      # Use: colors / colors_manual   
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
plt.title("", fontsize=title_font_size)  # Add title.
#plt.legend(labels=labels)               # Add legend.

# Show graphs.
plt.show()