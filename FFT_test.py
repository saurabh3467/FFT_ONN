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
    with open(filename, 'r') as f:# Open the input file in read mode
        lines = f.readlines()# Read all lines of the file and store them in the list 'lines'
    with open('tmp_data.txt', 'w') as f:# Open a new file in write mode to write the updated data
        for i, line in enumerate(lines):        # Loop through the lines of the input file
            #if i > 0:# Skip the first line (header)
            data = line.strip().split(';')# Split the line into a list of values
            for j, value in enumerate(data):# Replace commas with dots in the all values of the line
                data[j] = data[j].replace(',', '.')
            f.write('\t'.join(data) + '\n')# Join the updated values with semicolons and write them to the new file

# function to perform data smoothening on the current-time data
def data_smoothening(filename: str, input_filename) -> List[float]:
    data = np.loadtxt(filename, dtype=str, delimiter='\t')    # Load the data from the file using np.loadtxt()
    current = data[:, cc]    # Extract the current from the data array and Convert from strings to floats
    current_float = [float(x) for x in current]
    time = data[:, tc]
    time_float = [float(x) for x in time]
    voltage = float(input_filename.split("_")[-1].split(".")[0].replace("V", ""))
    volume = float(input_filename.split("_")[3].replace("uL", ""))
    length = float(input_filename.split("_")[2].replace("cm", ""))
    elec_field = float(100 * voltage / length)
    
    # Perform data smoothing using Savitzky-Golay filter with window length of 30 and polynomial order of 3
    # Note: Higher window length -> more smoothing, less detail; higher polynomial order -> more detail, introduced noise
    current_float_smooth = savgol_filter(current_float, 31, 3)
    
    fig, ax = plt.subplots()    # Create a figure and axes objects for plotting
    ax.plot(current_float, color='blue', label='Original Current')    # Plot the original current-time data in blue
    ax.plot(current_float_smooth, color='red', label='Smoothed Current')    # Plot the smoothed data in red
    ax.set_title(['Current vs. Time: {} V/m, {} uL'.format(elec_field, volume)])    # Set the title and axis labels
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Current (A)')
    ax.legend()    # Add a legend to the plot
    #plt.show()# Show the plot
    if not os.path.exists(os.path.join(path,'Smoothed_Data')):# Create the subfolder if it does not exist yet
        os.makedirs(os.path.join(path,'Smoothed_Data'))
    plt.savefig(os.path.join(path, f'Smoothed_Data/{input_filename}_smooth.png'), dpi=300)
    plt.close()
    with open(os.path.join(path, f'Smoothed_Data/{input_filename}_smooth.txt'), 'w') as f:
        f.write('Time(s) \t Original_Current(A) \t Smoothed_Current(A)\n')
        for i in range(len(time_float)):
             f.write('{} \t {} \t {}\n'.format(time_float[i], np.abs(current_float[i]), np.abs(current_float_smooth[i])))
    return current_float_smooth# Return the smoothed current data as a list of floats
    
# function to perform FFT on the current data
def perform_fft(current_float_smooth: List[float]) -> List[complex]:
    window = np.hanning(len(current_float_smooth))
    current_float_windowed = current_float_smooth * window
    fft_current = np.fft.fft(current_float_windowed)
    return fft_current

# function to plot and save the FFT figure and txt file
def plot_fft(fft_current: List[complex], time_float: List[float], path: str, input_filename: str) -> None:
    voltage = float(filename.split("_")[-1].split(".")[0].replace("V", ""))
    volume = float(filename.split("_")[3].replace("uL", ""))
    length = float(filename.split("_")[2].replace("cm", ""))
    elec_field = float(100 * voltage / length)
    freq = np.fft.fftfreq(len(fft_current), time_float[1] - time_float[0])
    max_value = np.max(np.abs(fft_current[(freq >= 0.1)]))
    plt.plot(freq, np.abs(fft_current), linewidth=0.2, color='red')
    plt.xlabel('Frequency (Hz)', fontsize=16)
    plt.ylabel('Amplitude', fontsize=16)
    plt.xlim([-0.1, 60])
    plt.title('Fast Fourier Transform')
    plt.ylim([0, max_value * 1.1])
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.legend(['{} V/m, {} $\mu$L'.format(elec_field, volume)])
    
    if smooth == 'n':
        if not os.path.exists(os.path.join(path, "FFT")):
            os.makedirs(os.path.join(path, "FFT"))
        plt.savefig(os.path.join(path, f'FFT/{input_filename}_FFT.png'), dpi=300)
        with open(os.path.join(path, f'FFT/{input_filename}_FFT.txt'), 'w') as f:
            f.write('Frequency (Hz) \t Amplitude\n')
            for i in range(len(freq)):
                 f.write('{} \t {}\n'.format(freq[i], np.abs(fft_current[i])))
    elif smooth == 'y':
        if not os.path.exists(os.path.join(path, "FFT_smoothed")):
            os.makedirs(os.path.join(path, "FFT_smoothed"))
        plt.savefig(os.path.join(path, f'FFT_smoothed/{input_filename}_FFT_smoothed.png'), dpi=300)
        with open(os.path.join(path, f'FFT_smoothed/{input_filename}_FFT_smoothed.txt'), 'w') as f:
            f.write('Frequency (Hz) \t Amplitude\n')
            for i in range(len(freq)):
                 f.write('{} \t {}\n'.format(freq[i], np.abs(fft_current[i]))) 
    else:
        None
        
def split_file(input_file, vol_range, vol_i):
    with open(input_file, 'r') as f:# Open the input file in read mode
        lines = f.readlines()# Read all lines of the file and store them in the list 'lines'
    with open('tmp_data.txt', 'w') as f:# Open a new file in write mode to write the updated data
        #f.write('Real time (s) \t Time (s) \t Current (A) \n')    
        for i, line in enumerate(lines[1:]):        # Loop through the lines of the input file, skipping first line
            data = line.replace(',', '.')
            f.write(data) # Join the updated values with semicolons and write them to the new file
    data = np.loadtxt('tmp_data.txt', delimiter='\t')
    # Split data into 10 separate arrays based on the voltage value
    #vol_range = float(input("How many number of voltage points were recorded: "))
    split_data = np.split(data, vol_range, axis=1)
    
    output_dir = os.path.join(direc, "Split_inputfile")
    os.makedirs(output_dir, exist_ok=True)
    # Save each split array to a separate file with the original file name appended by the voltage value
    #V_start = float(input("Specify the starting voltage: "))
    #vs = int(V_start)
    for i, data in enumerate(split_data, start=1):
        np.savetxt(os.path.join(output_dir, f"{input_filenames}_{i+vol_i-1}V.txt"), data, delimiter='\t')
        
# ========================== functions end here ===============================

# ======== Ask the user for the path & parameters to the directory ============
direc = input("Enter the path to the directory: ")
split = input("Do you need to split files for individual voltages? (y/n) ")
current_col = float(input("Which column has the current data? ")) - 1
time_col = float(input("Which column has the time data? ")) - 1
cc = int(current_col)
tc = int(time_col)
vol_range = int(input("How many number of voltage points were recorded: "))
vol_i = int(input("what was the first voltage value?: "))

if split == 'y':
    for filenames in os.listdir(direc):
        input_filenames = os.path.splitext(os.path.basename(filenames))[0]
        if filenames.endswith(".txt"):
            split_file(os.path.join(direc, filenames), vol_range, vol_i)
            output_dir = os.path.join(direc, "Split_inputfile")
    path = os.path.join(direc, "Split_inputfile")
elif split == 'n':
    path = direc

smooth = input("Do you want to smoothen I-V data? (y/n) ")
for filename in os.listdir(path):
    if filename.endswith('.txt'):
        input_filename = os.path.splitext(os.path.basename(filename))[0]
        comma_to_dot(os.path.join(path, filename))
        if smooth == 'y':
            current_float_smooth = data_smoothening('tmp_data.txt', input_filename)  # pass input_filename to data_smoothening
            fft_result = perform_fft(current_float_smooth) # pass the stored value as the input argument to perform_fft
        elif smooth == 'n':
            data = np.loadtxt('tmp_data.txt', dtype=str, delimiter='\t')
            current = data[:, cc]
            current_float = [float(x) for x in current]
            fft_result = perform_fft(current_float) # pass the stored value as the input argument to perform_fft
        else:
            print("What is wrong with you? Answer y/n!")
        data = np.loadtxt('tmp_data.txt', dtype=str, delimiter='\t')
        current = data[:, cc]
        current_float = [float(x) for x in current]
        time = data[:, tc]
        time_float = [float(x) for x in time]
        plt.close()
        plot_fft(fft_result, time_float, path, input_filename)
        plt.close()
