import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import os

# Ask the user for the mass of the droplet and the voltage applied
volume = float(input("Enter the volume of the droplet in µL: "))
voltage = float(input("Enter the voltage applied: "))
length = float(input("Enter the distance between the electrodes in cm: "))

# Ask the user for the path to the directory
path = input("Enter the path to the directory: ")

def perform_fft_analysis(filename, voltage, volume, length):
    # Load the data from the file using np.loadtxt()
    # Use delimiter=';' to specify that the columns are separated by semicolons
    # Use skiprows=1 to skip the header row
    # Use converters to replace commas with periods in both columns of the data
    with open(os.path.join(path, filename), 'r') as f:
        lines = f.readlines()

    with open(os.path.join(path, 'tmp_data.txt'), 'w') as f:
        for i, line in enumerate(lines):
            if i > 0:
                data = line.strip().split(';')
                data[0] = data[0].replace(',', '.')
                data[1] = data[1].replace(',', '.')
                data[2] = data[2].replace(',', '.')
                data[3] = data[3].replace(',', '.')
                f.write(';'.join(data) + '\n')

    data = np.loadtxt(os.path.join(path, 'tmp_data.txt'), dtype=str, delimiter=';')
    
    os.remove(os.path.join(path, 'tmp_data.txt'))

    # Extract the time and current data from the data array
    # Use array slicing to extract the first and second columns (0-indexed)
    time = data[:, 2]
    current = data[:, 1]

    current_float = [float(x) for x in current]
    time_float = [float(x) for x in time]

    # numbers are for window length and polynomial order of the Savitzky-Golay filter
    current_float_smooth = savgol_filter(current_float, 30, 3)  # higher window -> more smooth, less detail; higher poly order --> more detail, introduced noise

    # Define the Hanning window and apply it to the current data
    window = np.hanning(len(current_float_smooth))
    current_float_windowed = current_float_smooth * window

    # Compute the FFT of the current data
    fft_current = fft(current_float_windowed)

    # Compute the frequency values corresponding to the FFT
    # Use np.fft.fftfreq() to compute the frequency values
    # The first argument is the length of the data array
    # The second argument is the time difference between adjacent samples
    freq = np.fft.fftfreq(len(current_float_windowed), time_float[1] - time_float[0])
    max_value = np.max(np.abs(fft_current[(freq >= 0.1)]))

    plt.plot(freq, np.abs(fft_current), linewidth=0.2, color='black')  # Use plt.plot() to plot the FFT results
    # Use np.abs() to compute the magnitude of the FFT values
    plt.xlabel('Frequency (Hz)', fontsize=16)  # Use plt.xlabel() and plt.ylabel() to set the x and y axis labels
    plt.ylabel('Amplitude', fontsize=16)
    # Adjust the x and y range of the plot
    plt.xlim([-0.1, 60])
    plt.ylim([0, max_value * 1.1])
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.legend(['{}V, {} µL, {} cm'.format(voltage, volume, length)])  # Use plt.legend() to show the legend

    # Create the subfolder if it does not exist yet
    if not os.path.exists("FFT"):
        os.makedirs("FFT")
    
    # Save the FFT data and plot to a text file in a folder called "FFT"
    plt.savefig(f'FFT/{input_filename}.png')
    with open(f'FFT/{input_filename}_FFT.txt', 'w') as f:
        for i in range(len(freq)):
            f.write('{} {}\n'.format(freq[i], np.abs(fft_current[i])))

    plt.show()  # Use plt.show() to display the plot


for filename in os.listdir(path):
    if filename.endswith(".txt"):
        input_filename = os.path.splitext(filename)[0]
        
        perform_fft_analysis(filename, voltage, volume, length)


