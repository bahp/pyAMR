"""
Piechart AMR review
===================

"""

#######################################################################
#
# Author: Bernard
# Date: 19/08/2016
# Description: This script creates PIECHARTS for the paper which
#              describes the infection risk inference: "Evaluating
#              machine learning algorithms for infection risk inference
#              using routinely collected pathology laboratory data".
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

from __future__ import division

# Libraries
import seaborn as sns
import matplotlib as mpl
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
#                              FIGURE 1
# ------------------------------------------------------------------------
# Common configuration.
title_font_size = 30
labels = ['Prescription', 'Surveillance','Diagnosis', 'Dosing', 'Others'] # labels
labels_empty = ['', '', '', '', '']         # labels empty
colors = transparency(sns.color_palette("Set2", desat=0.75, n_colors=7), 0.4)
explode = (0.00,0,0,0,0)     # proportion with which to offset each wedge
autopct = ''#'%1.0f%%'       # print values inside the wedges
pctdistance = 0.8         # ratio betwen center and text (default=0.6)
labeldistance = 0.5       # radial distance wich pie labels are drawn
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

# ---------------------------
#  plot
# ---------------------------
# Portions.
sizes = [69, 10, 5, 2, 14] # Add proportions

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


# ------------------------------------------------------------------------
#                            FIGURE 2
# ------------------------------------------------------------------------
# Common configuration.
title_font_size = 30
labels = ['Rule-based', 'Tree-based','Case-based', 'Other'] # labels
labels_empty = ['', '', '', '']         # labels empty
colors = transparency(sns.color_palette("Set2", desat=0.75, n_colors=7), 0.4)
explode = (0.00,0,0,0)     # proportion with which to offset each wedge
autopct = ''#'%1.0f%%'       # print values inside the wedges
pctdistance = 0.6         # ratio betwen center and text (default=0.6)
labeldistance = 0.4       # radial distance wich pie labels are drawn
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

# ---------------------------
#  plot
# ---------------------------
# Portions.
sizes = [64, 18, 10, 6] # Add proportions

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

# ------------------------------------------------------------------------
#                            FIGURE 3
# ------------------------------------------------------------------------
# Common configuration.
title_font_size = 30
labels = ['Bacteremia', 'SSI','UTI', 'RTI' ' C+', 'Gram'] # labels
labels_empty = ['', '', '', '', '', '']         # labels empty
colors = transparency(sns.color_palette("Set2", desat=0.75, n_colors=7), 0.4)
explode = (0.00,0,0,0,0,0) # proportion with which to offset each wedge
autopct = ''#'%1.0f%%'    # print values inside the wedges
pctdistance = 0.6         # ratio betwen center and text (default=0.6)
labeldistance = 0.4       # radial distance wich pie labels are drawn
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

# ---------------------------
#  plot
# ---------------------------
# Portions.
sizes = [49, 19, 14, 14, 2, 2] # Add proportions

# reset feature
startangle = 90

# Plot
plt.figure()
plt.pie(sizes,
        explode=explode,
        labels=labels_empty,   # Use: labels / labels_empty
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