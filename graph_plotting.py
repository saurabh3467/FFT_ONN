# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:58:05 2023

@author: SoniS
"""
import matplotlib.pyplot as plt
import numpy as np

# Define formatting parameters
line_width = 2
marker_size = 5
axis_width = 1
font_size = 12

# Load data from file
filename = input("Enter path to input file: ")
data = np.loadtxt(filename, delimiter=',', skiprows=1)

# Extract x and y data
x = data[:, 0]
y = data[:, 1]

# Create plot
fig, ax = plt.subplots()
ax.plot(x, y, '-o', linewidth=line_width, markersize=marker_size)

# Customize plot formatting
ax.spines['bottom'].set_linewidth(axis_width)
ax.spines['left'].set_linewidth(axis_width)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', direction='out', width=axis_width, labelsize=font_size)
ax.set_xlabel('X Axis Label', fontsize=font_size)
ax.set_ylabel('Y Axis Label', fontsize=font_size)
ax.set_xlim([min(x), max(x)])
ax.set_ylim([min(y), max(y)])
ax.set_title('Plot Title', fontsize=font_size)
ax.grid(True, linestyle='--', linewidth=axis_width)

# Add legend
ax.legend(['Data'], fontsize=font_size, loc='best')

# Show plot
plt.show()

