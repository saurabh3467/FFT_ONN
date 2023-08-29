# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 10:07:35 2023

@author: saura
"""

import os
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

def lorentzian(x, amplitude, center, width):  
    return amplitude / (1 + 4 * ((x - center) / width)**2)

def process_spectrum(filename):
    data = np.loadtxt(filename, dtype=str, delimiter='\t', skiprows=1)
    freq_str = data[:, 0]
    amp_str = data[:, 1]
    freqs = [float(x) for x in freq_str]
    amps = [float(x) for x in amp_str]
    positive_freq_indices = np.where(freqs > 0)[0]
    freqs1 = freqs[positive_freq_indices]
    amps1 = amps[positive_freq_indices]
    peaks, _ = find_peaks(amps, height=0, distance=750)
    result = []
    for peak in peaks:
        p0 = (amps1[peak], freqs1[peak], 2)
        try:
            popt, _ = curve_fit(lorentzian, freqs1, amps1, p0=p0)
            result.append(popt[1])
        except:
            pass
    return result
                            

def process_folder(folder):                     
    if not os.path.exists(os.path.join(folder,'Fits')):
        os.makedirs(os.path.join(folder,'Fits'))
    with open(os.path.join(folder, 'Fits/Frequencies.txt'), 'w') as fa:  
        for filename in os.listdir(folder):  
            if filename.endswith('.txt'):  
                try:
                    peaks = process_spectrum(os.path.join(folder, filename))  
                    fa.write(filename + '\t' + '\t'.join(str(p) for p in peaks) + '\n')  
                except:
                    pass  
            fa.close()

direc = input("Where are the FFT spectra?: ")
process_folder(direc)
