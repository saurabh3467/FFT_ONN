import numpy as np
from scipy.fft import fft
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

    # Extract the time and current data from the data array
    time = data[:, 2]
    current = data[:, 1]

    # Convert current and time data from strings to floats
    current_float = [float(x) for x in current]
    time_float = [float(x) for x in time]

    # Perform data smoothing using Savitzky-Golay filter with window length of 30 and polynomial order of 3
    # Note: Higher window length -> more smoothing, less detail; higher polynomial order -> more detail, introduced noise
    current_float_smooth = savgol_filter(current_float, 30, 3)

    # Return the smoothed current data as a list of floats
    return current_float_smooth

# function to perform FFT on the current data
def perform_fft(current_float_smooth: List[float]) -> List[complex]:
    window = np.hanning(len(current_float_smooth))
    current_float_windowed = current_float_smooth * window
    fft_current = np.fft.fft(current_float_windowed)
    return fft_current

# function to plot and save the FFT figure and txt file
def plot_fft(fft_current: List[complex], time_float: List[float], voltage: int, volume: int, length: int) -> None:
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
    if not os.path.exists("FFT"):
        os.makedirs("FFT")
        
    # Save the FFT data and plot to a text file in a folder called "FFT"
    plt.savefig(f'FFT/{input_filename}.png')
    with open(f'FFT/{input_filename}_FFT.txt', 'w') as f:
        for i in range(len(freq)):
             f.write('{} {}\n'.format(freq[i], np.abs(fft_current[i])))
        plt.figure() #shows all plots 1-by-1 instead of just last one
    
# ========================== functions end here ==============================

# ========================== user input =======================================

# Ask the user for the mass of the droplet and the voltage applied
volume = float(input("Enter the volume of the droplet in µL: "))
voltage = float(input("Enter the voltage applied: "))
length = float(input("Enter the distance between the electrodes in cm: "))

# Ask the user for the path to the directory
path = input("Enter the path to the directory: ")

# ============= use above functions in code here ==============================

for filename in os.listdir(path):
    if filename.endswith(".txt"):
        input_filename = os.path.splitext(os.path.basename(filename))[0]
        comma_to_dot(os.path.join(path, filename))
        current_float_smooth = data_smoothening('tmp_data.txt')  # pass input_filename to data_smoothening
        fft_result = perform_fft(current_float_smooth) # pass the stored value as the input argument to perform_fft
        
        data = np.loadtxt('tmp_data.txt', dtype=str, delimiter=';')

        # Extract the time and current data from the data array
        time = data[:, 2]
        current = data[:, 1]

        # Convert current and time data from strings to floats
        current_float = [float(x) for x in current]
        time_float = [float(x) for x in time]
        plot_fft(fft_result, time_float, voltage, volume, length)