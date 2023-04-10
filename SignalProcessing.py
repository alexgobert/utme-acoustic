# -*- coding: utf-8 -*-
"""
@author: ishaa
"""

import numpy as np
from scipy.io import wavfile
from acoustics.standards.iec_61672_1_2013 import Weighting

# Define the weighting filter to use (e.g. A-weighting)
weighting_filter = Weighting('A')

# Define the path to the directory containing the WAV files
directory_path = 'C:\Users\ishaa\OneDrive\Documents\UTME Acoustic\Sample Results'

# Define the number of files and the angle increment between them
num_files = 18
angle_increment = 20

# Initialize the arrays to hold the SPL data and the max SPL values
spl_data = np.zeros((num_files,))  # One value per file
max_spl_values = np.zeros((num_files,))  # One value per file

# Loop over each WAV file and extract the SPL data
for i in range(num_files):
    # Construct the file name
    file_name = f'{i*angle_increment:03d}.wav'  # e.g. "000.wav", "020.wav", "040.wav", etc.

    # Read the WAV file and extract the data
    sample_rate, data = wavfile.read(f'{directory_path}/{file_name}')
    
    # Apply the weighting filter to the data
    weighted_data = weighting_filter(data, sample_rate)
    
    # Calculate the root-mean-squared (rms) value of the weighted data
    rms_value = np.sqrt(np.mean(weighted_data**2))
    
    # Store the rms value in the array
    spl_data[i] = rms_value
    
    # Find the maximum SPL value in the data and store it in the array
    max_spl_values[i] = np.max(weighted_data)

# Print the maximum SPL value from each file
print(max_spl_values)

# Print the highest overall SPL value
print(np.max(max_spl_values))
