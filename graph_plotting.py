# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:58:05 2023

@author: SoniS
"""
import matplotlib.pyplot as plt
import numpy as np

# Define formatting parameters
line_width = 0.5
marker_size = 3 #change size of data points
axis_width = 2
font_size = 12
x_label = "Frequency (Hz)"
y_label = "Amplitude"
plottitle = "Fast Fourier Transform"
legend = "0.5 V/m"
delimiter_in_file = '\t' # change this to ',' or ' ' or ';' if you have comma, space, or semicolor as delimiter in the input file

# Load data from file
filename = input("Enter path and name of the file: ")
data = np.loadtxt(filename, delimiter=delimiter_in_file, skiprows=1)

# Extract x and y data
x = data[:, 0]
y = data[:, 1]
y_filtered = y[x > 0.01]
# Set the maximum range of y to be 1.1 times the maximum value of y_filtered
ymax = np.max(y_filtered)
x_freq1 =  x[np.argmax(y_filtered)]

y_min = -0.01
y_max = 1.1*ymax
x_min = -0.01
x_max = 20

# Create plot
# See link for options: https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.plot.html
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, '-', linewidth=line_width, markersize=marker_size, color='red')

# Customize plot formatting
ax.spines['bottom'].set_linewidth(axis_width)
ax.spines['left'].set_linewidth(axis_width)
ax.spines['top'].set_linewidth(axis_width)
ax.spines['right'].set_linewidth(axis_width)
ax.tick_params(axis='both', direction='in', width=axis_width, labelsize=font_size)
ax.set_xlabel(x_label, fontsize=font_size)
ax.set_ylabel(y_label, fontsize=font_size)
ax.set_xlim([x_min, x_max])
ax.set_ylim([y_min, y_max])
ax.set_title(plottitle, fontsize=font_size)
ax.text(x_freq1, ymax*0.95, f"f1={x_freq1:.2f}", ha='left', va='center')
ax.grid(False)#, linestyle='--', linewidth=axis_width) # grid lines, replace True 

# Add legend
ax.legend([legend], fontsize=font_size, loc='best')

plt.savefig('{}.png'.format(filename), transparent=True, dpi=300)
# Show plot
plt.show()