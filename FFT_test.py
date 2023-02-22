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

# ========================== different functions go here ======================

# function to convert comma to dot in a file
def comma_to_dot(filename: str) -> None:
    # Open the input file in read mode
    with open(filename, 'r') as f:
        # Read all lines of the file and store them in the list 'lines'
        lines = f.readlines()

    # Open a new file in write mode to write the updated data
    with open('tmp_data.txt', 'w') as f:
        # Loop through the lines of the input file
        for i, line in enumerate(lines):
            # Skip the first line (header)
            if i > 0:
                # Split the line into a list of values
                data = line.strip().split(';')
                # Replace commas with dots in the first four values of the line
                data[0] = data[0].replace(',', '.')
                data[1] = data[1].replace(',', '.')
                data[2] = data[2].replace(',', '.')
                data[3] = data[3].replace(',', '.')
                # Join the updated values with semicolons and write them to the new file
                f.write(';'.join(data) + '\n')

# function to perform data smoothening on the current-time data
def data_smoothening(filename: str) -> List[float]:
    # Load the data from the file using np.loadtxt()
    data = np.loadtxt(filename, dtype=str, delimiter=';')

    # Extract the current from the data array and Convert from strings to floats
    current = data[:, 1]
    current_float = [float(x) for x in current]
    time = data[:, 0]
    time_float = [float(x) for x in time]

    # Perform data smoothing using Savitzky-Golay filter with window length of 30 and polynomial order of 3
    # Note: Higher window length -> more smoothing, less detail; higher polynomial order -> more detail, introduced noise
    current_float_smooth = savgol_filter(current_float, 30, 3)
    
    # Create a figure and axes objects for plotting
    fig, ax = plt.subplots()

    # Plot the original current-time data in blue
    ax.plot(current_float, color='blue', label='Original Data')

    # Plot the smoothed data in red
    ax.plot(current_float_smooth, color='red', label='Smoothed Data')

    # Set the title and axis labels
    ax.set_title('Current vs. Time')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Current (A)')

    # Add a legend to the plot
    ax.legend()

    # Show the plot
    #plt.show()
    # Create the subfolder if it does not exist yet
    if not os.path.exists(os.path.join(path,'Smooth')):
        os.makedirs(os.path.join(path,'Smooth'))
    plt.savefig(os.path.join(path, f'Smooth/{input_filename}_smooth.png'), dpi=300)
    with open(os.path.join(path, f'Smooth/{input_filename}_smooth.txt'), 'w') as f:
        for i in range(len(time_float)):
             f.write('{} {} {}\n'.format(time_float[i], np.abs(current_float[i]), np.abs(current_float_smooth[i])))
    # Return the smoothed current data as a list of floats
    return current_float_smooth

# function to perform FFT on the current data
def perform_fft(current_float_smooth: List[float]) -> List[complex]:
    window = np.hanning(len(current_float_smooth))
    current_float_windowed = current_float_smooth * window
    fft_current = np.fft.fft(current_float_windowed)
    return fft_current

# function to plot and save the FFT figure and txt file
def plot_fft(fft_current: List[complex], time_float: List[float], voltage: int, volume: int, length: int, path: str, input_filename: str) -> None:
    freq = np.fft.fftfreq(len(fft_current), time_float[1] - time_float[0])
    max_value = np.max(np.abs(fft_current[(freq >= 0.1)]))
    plt.plot(freq, np.abs(fft_current), linewidth=0.2, color='black')
    plt.xlabel('Frequency (Hz)', fontsize=16)
    plt.ylabel('Amplitude', fontsize=16)
    plt.xlim([-0.1, 60])
    plt.ylim([0, max_value * 1.1])
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.legend(['{}V, {} µL, {} cm'.format(voltage, volume, length)])
    
    # Create the subfolder if it does not exist yet
    if not os.path.exists(os.path.join(path, "FFT")):
        os.makedirs(os.path.join(path, "FFT"))
        
    # Save the FFT data and plot to a text file in a folder called "FFT"
    plt.savefig(os.path.join(path, f'FFT/{input_filename}.png'), dpi=300)
    with open(os.path.join(path, f'FFT/{input_filename}_FFT.txt'), 'w') as f:
        for i in range(len(freq)):
             f.write('{} {}\n'.format(freq[i], np.abs(fft_current[i])))
        #plt.figure() #shows all plots 1-by-1 instead of just last one
        
# ========================== functions end here ==============================

# ========================== user input =======================================

# Ask the user for the mass of the droplet and the voltage applied
volume = float(input("Enter the volume of the droplet in µL: "))
voltage = float(input("Enter the voltage applied: "))
length = float(input("Enter the distance between the electrodes in cm: "))

# Ask the user for the path to the directory
path = input("Enter the path to the directory: ")

smooth = input("Do you want to smoothen I-V data? (y/n)")
if smooth == 'n':
    # ============= Perform FFT and fit without smoothing =========================
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            input_filename = os.path.splitext(os.path.basename(filename))[0]
            comma_to_dot(os.path.join(path, filename))
            data = np.loadtxt('tmp_data.txt', dtype=str, delimiter=';')
            # Extract the current from the data array and Convert from strings to floats
            current = data[:, 1]
            current_float = [float(x) for x in current]
            
            fft_result = perform_fft(current_float) # pass the stored value as the input argument to perform_fft
            
            # Extract the time from the data array and Convert from strings to floats
            time = data[:, 2]
            time_float = [float(x) for x in time]
            plot_fft(fft_result, time_float, voltage, volume, length, path, input_filename)
elif smooth == 'y':    
    # ============= Perform FFT and fit with  smoothing ===========================
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            input_filename = os.path.splitext(os.path.basename(filename))[0]
            comma_to_dot(os.path.join(path, filename))
            current_float_smooth = data_smoothening('tmp_data.txt')  # pass input_filename to data_smoothening
            fft_result = perform_fft(current_float_smooth) # pass the stored value as the input argument to perform_fft
            
            data = np.loadtxt('tmp_data.txt', dtype=str, delimiter=';')
            # Extract the time from the data array and Convert from strings to floats
            time = data[:, 2]
            time_float = [float(x) for x in time]
            plot_fft(fft_result, time_float, voltage, volume, length, path, input_filename)
else:
    print("Wrong input, I asked y/n, start again :-P")