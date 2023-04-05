# This script so far contains functions that will be useful in the data processing.

from os import listdir
from datetime import datetime

# This function creates a list of the filenames, in order, in a specified directory
def get_filenames_in_order(directory):
    filenames = listdir(directory)
    timestamps = []
    for filename in filenames:
        timestamp_str = filename.split('-')[-1].split('.')[0]
        timestamp = datetime.fromtimestamp(int(timestamp_str))
        timestamps.append((timestamp, filename))
    timestamps.sort()
    
    return [filename for _, filename in timestamps]

if __name__ == '__main__':
    directory = '../test_results'
    print(get_filenames_in_order(directory))