# This script so far contains functions that will be useful in the data processing.

from os import listdir
from datetime import datetime

# This function creates a list of the filenames, in order, in a specified directory
def get_filenames_in_order(directory, limit=None):
    filenames = listdir(directory)
    timestamps = []
    for filename in filenames:
        timestamp_str = filename.split('-')[-1].split('.')[0]
        timestamp = datetime.fromtimestamp(int(timestamp_str))
        timestamps.append((timestamp, filename))
    timestamps.sort()
    
    files = [filename for _, filename in timestamps]
    return files[:limit] if limit else files

def parse_freq_input(input_string):
    freq_list = input_string.split(",")
    freq_list = [int(freq.strip()) for freq in freq_list]
    return freq_list

if __name__ == '__main__':
    directory = '../test_results'
    print(get_filenames_in_order(directory))