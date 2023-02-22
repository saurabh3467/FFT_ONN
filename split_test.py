# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 14:36:51 2023

@author: SoniS
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import os
from typing import List

def split_file(input_file):
    with open(input_file, 'r') as f:# Open the input file in read mode
        lines = f.readlines()# Read all lines of the file and store them in the list 'lines'
    with open('tmp_data.txt', 'w') as f:# Open a new file in write mode to write the updated data
        for i, line in enumerate(lines[1:]):        # Loop through the lines of the input file, skipping first line
            data = line.replace(',', '.')
            f.write(data) # Join the updated values with semicolons and write them to the new file
    data = np.loadtxt('tmp_data.txt', delimiter='\t')
    # Split data into 10 separate arrays based on the voltage value
    split_data = np.split(data, 10, axis=1)
    
    output_dir = os.path.join(path, "Split_file")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each split array to a separate file with the original file name appended by the voltage value
    for i, data in enumerate(split_data, start=1):
        np.savetxt(os.path.join(output_dir, f"{input_filename}_{i}V.txt"), data, delimiter='\t')

# ============== Ask the user for the path to the directory ===================
path = input("Enter the path to the directory: ")

for filename in os.listdir(path):
    input_filename = os.path.splitext(os.path.basename(filename))[0]
    if filename.endswith(".txt"):
        split_file(os.path.join(path, filename))
    