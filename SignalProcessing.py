import numpy as np
from scipy.io import wavfile
from acoustics._signal import Signal
from data_processing import get_filenames_in_order

# Define the weighting filter to use (e.g. A-weighting)
# weighting_filter = Weighting('A')
# weighting_filter = WEIGHTING_FUNCTIONS['A']

# Define the path to the directory containing the WAV files
# directory_path = 'C:\Users\ishaa\OneDrive\Documents\UTME Acoustic\Sample Results'
directory_path = 'test_results'
files = get_filenames_in_order(directory_path)

# Define the number of files and the angle increment between them
# num_files = len(files)
# angle_increment = 20

# Initialize the arrays to hold the SPL data and the max SPL values
# spl_data = np.zeros((num_files,))  # One value per file
# max_spl_values = np.zeros((num_files,))  # One value per file
spl_data = []
max_spl_values = []

# Loop over each WAV file and extract the SPL data
# for i in range(num_files):
for file in files:
    # Construct the file name
    # file_name = f'{i*angle_increment:03d}.wav'  # e.g. "000.wav", "020.wav", "040.wav", etc.

    # Read the WAV file and extract the data
    # sample_rate, data = wavfile.read(f'{directory_path}/{file}')
    signal = Signal(*wavfile.read(f'{directory_path}/{file}')).weigh()
    
    # Apply the weighting filter to the data
    # weighted_data = weighting_filter(data, sample_rate)
    # weighted_data = weighting_filter(data)
    
    # Calculate the root-mean-squared (rms) value of the weighted data
    # rms_value = np.sqrt(np.mean(weighted_data**2))
    
    # Store the rms value in the array
    # spl_data[i] = rms_value
    # spl_data.append(rms_value)
    # max_spl_values.append(weighted_data)

    spl_data.append(signal.rms())
    max_spl_values.append(signal.max())
    
    # Find the maximum SPL value in the data and store it in the array
    # max_spl_values[i] = np.max(weighted_data)

# Print the maximum SPL value from each file
print(max_spl_values)

# Print the highest overall SPL value
print(np.max(max_spl_values))
