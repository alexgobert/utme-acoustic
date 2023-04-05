# This script so far contains functions that will be useful in the data processing.

import os
from datetime import datetime

# This function creates a list of the filenames, in order, in a specified directory
def get_filenames_in_order(directory):
    filenames = os.listdir(directory)
    timestamps = []
    for filename in filenames:
        timestamp_str = filename.split('-')[-1].split('.')[0]
        timestamp = datetime.fromtimestamp(int(timestamp_str))
        timestamps.append((timestamp, filename))
    timestamps.sort()
    return [filename for _, filename in timestamps]

if __name__ == '__main__':
    directory = r"C:\Users\Calvin Pradian\Documents\GitHub\utme-acoustic\test_results"
    print(get_filenames_in_order(directory))