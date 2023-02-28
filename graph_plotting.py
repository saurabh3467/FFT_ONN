# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:58:05 2023

@author: SoniS
"""
import matplotlib.pyplot as plt
import numpy as np

# Define formatting parameters
line_width = 1
marker_size = 3
axis_width = 2
font_size = 12
x_label = "Frequency (Hz)"
y_label = "Amplitude"
plottitle = "Fast Fourier Transform"
legend = "0.5 V/m"
delimiter_in_file = '\t'

# Load data from file
filename = input("Enter path and name of the file: ")
data = np.loadtxt(filename, delimiter=delimiter_in_file, skiprows=1)

# Extract x and y data
x = data[:, 0]
y = data[:, 1]

y_min = -0.01
y_max = 150
x_min = -0.01
x_max = 20

# Create plot
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, '-o', linewidth=line_width, markersize=marker_size)

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
ax.grid(False)#, linestyle='--', linewidth=axis_width)

# Add legend
ax.legend([legend], fontsize=font_size, loc='best')

plt.savefig('{}.png'.format(filename), transparent=True, dpi=300)
# Show plot
plt.show()